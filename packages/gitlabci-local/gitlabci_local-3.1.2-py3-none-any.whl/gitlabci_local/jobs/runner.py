#!/usr/bin/env python3

# Standard libraries
from os import chmod, environ, stat, system
from os.path import expandvars
from pathlib import Path, PurePosixPath
from signal import getsignal, SIGINT, signal, SIGTERM
from stat import S_IRGRP, S_IROTH, S_IXGRP, S_IXOTH, S_IXUSR
from sys import stdout
from time import sleep, time

# Components
from ..engines.engine import Engine
from ..package.bundle import Bundle
from ..system.platform import Platform
from ..types.paths import Paths
from ..types.volumes import Volumes
from .outputs import Outputs
from .scripts import Scripts

# Jobs class
class Jobs:

    # Constants
    __MARKER_DEBUG = '__GITLAB_CI_LOCAL_DEBUG__'
    __MARKER_RESULT = '__GITLAB_CI_LOCAL_RESULT__'

    # Members
    __engine = None
    __options = None

    # Constructor
    def __init__(self, options):

        # Prepare options
        self.__options = options

    # Run container
    def __run_container(self, variables, path_parent, target_parent, image, job_data,
                        script_file, entrypoint, network, target_workdir, last_result,
                        result):

        # Configure engine variables
        variables[Bundle.ENV_ENGINE_NAME] = self.__engine.name()

        # Prepare volumes mounts
        volumes = Volumes()

        # Mount repository folder
        volumes.add(path_parent, target_parent, 'rw', True)

        # Extend mounts
        if self.__options.volume:
            for volume in self.__options.volume:
                cwd = Path('.')
                volume_local = False
                volume_nodes = volume.split(':')

                # Handle .local volumes
                if volume_nodes[0] == '.local':
                    cwd = self.__options.path
                    volume_local = True
                    volume_nodes.pop(0)

                # Parse HOST:TARGET:MODE
                if len(volume_nodes) == 3:
                    volume_host = Paths.resolve(cwd / expandvars(volume_nodes[0]))
                    volume_target = expandvars(volume_nodes[1])
                    volume_mode = volume_nodes[2]

                # Parse HOST:TARGET
                elif len(volume_nodes) == 2:
                    volume_host = Paths.resolve(cwd / expandvars(volume_nodes[0]))
                    volume_target = expandvars(volume_nodes[1])
                    volume_mode = 'rw'

                # Parse VOLUME
                else:
                    volume_host = Paths.resolve(cwd / expandvars(volume))
                    volume_target = Paths.resolve(cwd / expandvars(volume))
                    volume_mode = 'rw'

                # Append volume mounts
                volumes.add(volume_host, volume_target, volume_mode, not volume_local)

        # Append sockets mounts
        if self.__options.sockets:
            self.__engine.sockets(volumes)

        # Image validation
        if not image: # pragma: no cover
            raise ValueError(
                'Missing image for "%s / %s"' % (job_data['stage'], job_data['name']))
        self.__engine.get(image)

        # Launch container
        container = self.__engine.run(image, script_file.target(), entrypoint, variables,
                                      network, volumes, target_workdir)

        # Create interruption handler
        def interrupt_handler(unused_signalnum, unused_handler):
            Outputs.interruption()
            self.__engine.stop(container, 0)

        # Register interruption handler
        handler_int_original = getsignal(SIGINT)
        handler_term_original = getsignal(SIGTERM)
        signal(SIGINT, interrupt_handler)
        signal(SIGTERM, interrupt_handler)

        # Execution wrapper
        success = False

        # Show container logs
        for line in self.__engine.logs(container):
            if isinstance(line, bytes):
                line_decoded = line.decode()
                if self.__MARKER_DEBUG in line_decoded:
                    break
                if self.__MARKER_RESULT in line_decoded:
                    break
                stdout.buffer.write(line)
                Platform.flush()

        # Runner bash or debug mode
        if self.__options.bash or self.__options.debug:

            # Select shell
            shell = 'sh'
            if self.__engine.supports(container, 'bash'):
                shell = 'bash'

            # Acquire container informations
            container_exec = self.__engine.cmd_exec()
            container_name = self.__engine.name(container)

            # Debugging informations
            Outputs.debugging(container_exec, container_name, shell)

        # Check container status
        success = self.__engine.wait(container)

        # Stop container
        self.__engine.stop(container, 0)
        sleep(0.1)

        # Remove container
        self.__engine.remove(container)

        # Unregister interruption handler
        signal(SIGINT, handler_int_original)
        signal(SIGTERM, handler_term_original)

        # Result evaluation
        if job_data['when'] in ['on_failure', 'always']:
            result = last_result
        elif success:
            result = True
        return result

    # Run native
    def __run_native(self, variables, entrypoint, script_file, job_data, last_result,
                     result):

        # Prepare environment
        _environ = dict(environ)
        environ.update(variables)

        # Native execution
        scripts = []
        if entrypoint:
            scripts += entrypoint
        if not scripts:
            scripts = ['sh']
        scripts += ['"%s"' % script_file.name()]
        success = (system(' '.join(scripts)) == 0)

        # Result evaluation
        if job_data['when'] in ['on_failure', 'always']:
            result = last_result
        elif success:
            result = True

        # Restore environment
        environ.clear()
        environ.update(_environ)

        # Result
        return result

    # Run
    def run(self, job_data, last_result, jobs_status):

        # Variables
        host = False
        quiet = self.__options.quiet
        real_paths = self.__options.real_paths and (Platform.IS_LINUX
                                                    or Platform.IS_MAC_OS)
        result = False
        script_file = None
        time_start = time()

        # Filter when
        if last_result and job_data['when'] not in ['on_success', 'manual', 'always']:
            return last_result
        if not last_result and job_data['when'] not in ['on_failure']:
            return last_result

        # Prepare image
        image = job_data['image']

        # Prepare local runner
        if self.__options.host or job_data['options']['host']:
            image = 'local'
            host = True

        # Prepare quiet runner
        if job_data['options']['quiet']:
            quiet = True
        elif jobs_status['quiet']:
            jobs_status['quiet'] = False

        # Prepare network
        network = 'bridge'
        if self.__options.network:
            network = self.__options.network

        # Prepare engine execution
        if not host:
            if self.__engine is None:
                self.__engine = Engine(self.__options)
            engine_type = self.__engine.name()

        # Prepare native execution
        else:
            engine_type = 'native'

        # Header
        if not quiet:
            Outputs.header(jobs_status, job_data, image, engine_type)

        # Acquire project paths
        path_project = Paths.resolve(self.__options.path)
        path_parent = Paths.resolve(Path(self.__options.path).parent)

        # Acquire project targets
        if host or real_paths:
            target_project = path_project
            target_parent = path_parent
        else:
            target_project = Paths.get(Platform.BUILDS_DIR / Path(path_project).name)
            target_parent = Paths.get(Platform.BUILDS_DIR)

        # Prepare working directory
        if self.__options.workdir:
            if self.__options.workdir.startswith('.local:'):
                workdir = self.__options.workdir[len('.local:'):]
                if host or real_paths:
                    target_workdir = Paths.get((self.__options.path / workdir).resolve())
                else:
                    target_workdir = Paths.get(PurePosixPath(target_project) / workdir)
            else:
                if host or real_paths:
                    target_workdir = Paths.get(
                        (Path('.') / self.__options.workdir).resolve())
                else:
                    target_workdir = Paths.get(
                        PurePosixPath(target_project) / self.__options.workdir)
        elif host or real_paths:
            target_workdir = Paths.get(self.__options.path)
        else:
            target_workdir = target_project

        # Prepare entrypoint and scripts
        entrypoint = job_data['entrypoint']
        scripts_after = []
        scripts_before = []
        scripts_commands = []
        scripts_debug = []

        # Prepare before_scripts
        if self.__options.before:
            scripts_before += job_data['before_script']

        # Prepare scripts
        scripts_commands += job_data['script']
        if not host:
            if self.__options.bash:
                scripts_commands = []
            if self.__options.bash or self.__options.debug:
                scripts_debug += [
                    'echo "' + self.__MARKER_DEBUG + '"', 'tail -f /dev/null'
                ]

        # Prepare after_scripts
        if self.__options.after:
            scripts_after += job_data['after_script']

        # Prepare script file
        script_file = Scripts(
            paths={
                path_parent: target_parent,
                path_project: target_project
            }, prefix='.tmp.entrypoint.')

        # Prepare execution context
        script_file.shebang()
        script_file.write('result=1')

        # Prepare host working directory
        if host:
            script_file.write('cd "%s"' % target_workdir)

        # Prepare before_script/script context
        script_file.subshell_start()
        script_file.configure(errors=True, verbose=not job_data['options']['silent'])

        # Prepare before_script commands
        if len(scripts_before) > 0:
            script_file.subgroup_start()
            script_file.writelines(scripts_before)
            script_file.subgroup_stop()

        # Prepare script commands
        if len(scripts_commands) > 0:
            script_file.subgroup_start()
            script_file.writelines(scripts_commands)
            script_file.subgroup_stop()
        else:
            script_file.write('false')

        # Finish before_script/script context
        script_file.subshell_stop()
        script_file.write('result=${?}')

        # Prepare debug script commands
        if len(scripts_debug) > 0:
            script_file.subshell_start()
            if not job_data['options']['silent']:
                script_file.configure(errors=False, verbose=True)
            script_file.writelines(scripts_debug)
            script_file.subshell_stop()

        # Prepare after_script commands
        if len(scripts_after) > 0:
            script_file.subshell_start()
            if job_data['options']['silent']:
                script_file.configure(errors=True, verbose=False)
            else:
                script_file.configure(errors=True, verbose=True)
            script_file.subgroup_start()
            script_file.writelines(scripts_after)
            script_file.subgroup_stop()
            script_file.subshell_stop()

        # Prepare container result
        if not host:
            script_file.write('echo "%s:${result}"' % (self.__MARKER_RESULT))

        # Prepare execution result
        script_file.write('exit "${result}"')

        # Prepare script execution
        script_stat = stat(script_file.name())
        chmod(script_file.name(), script_stat.st_mode | S_IXUSR | S_IXGRP
              | S_IRGRP | S_IROTH | S_IXOTH)
        script_file.close()

        # Acquire CI environment
        env_job_name = job_data['options']['env_job_name']
        env_job_path = job_data['options']['env_job_path']

        # Configure CI environment
        environ[env_job_name] = job_data['name']
        environ[env_job_path] = target_project

        # Configure local environment
        environ[Bundle.ENV_LOCAL] = 'true'

        # Prepare variables
        variables = dict()

        # Prepare environment
        _environ = dict(environ)
        environ.update(job_data['variables'])

        # Prepare job variables
        for variable in job_data['variables']:
            variables[variable] = expandvars(str(job_data['variables'][variable]))

        # Restore environment
        environ.clear()
        environ.update(_environ)

        # Prepare CI variables
        variables[env_job_name] = environ[env_job_name]
        variables[env_job_path] = environ[env_job_path]
        variables[Bundle.ENV_LOCAL] = environ[Bundle.ENV_LOCAL]

        # Container execution
        if not host:
            result = self.__run_container(variables, path_parent, target_parent, image,
                                          job_data, script_file, entrypoint, network,
                                          target_workdir, last_result, result)

        # Native execution
        else:
            result = self.__run_native(variables, entrypoint, script_file, job_data,
                                       last_result, result)

        # Initial job details
        job_details = ''
        job_details_list = []

        # Prepare when details
        if job_data['when'] not in ['on_success']:
            job_details_list += ['when: %s' % (job_data['when'])]

        # Prepare allow_failure details
        if job_data['allow_failure']:
            job_details_list += ['failure allowed']

        # Prepare job details
        if job_details_list:
            job_details = ' (' + ', '.join(job_details_list) + ')'

        # Evaluate duration time
        time_duration = time() - time_start
        time_seconds = '%.0f second%s' % (time_duration % 60,
                                          's' if time_duration % 60 > 1 else '')
        time_minutes = ''
        if time_duration >= 60:
            time_minutes = '%.0f minute%s ' % (time_duration / 60,
                                               's' if time_duration / 60 > 1 else '')
        time_string = time_minutes + time_seconds

        # Footer
        print(' ')
        Platform.flush()
        if not quiet:
            Outputs.footer(result, time_string, job_data, job_details)

        # Allowed failure result
        if job_data['when'] not in ['on_failure', 'always'
                                    ] and not result and job_data['allow_failure']:
            result = True

        # Result
        return result
