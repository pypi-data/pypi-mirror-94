#!/usr/bin/env python3

# Standard libraries
from time import time

# Components
from ..jobs.runner import Jobs
from ..prints.colors import Colors
from ..system.platform import Platform
from ..types.lists import Lists

# PipelinesFeature class
class PipelinesFeature:

    # Members
    __jobs = None
    __options = None

    # Constructor
    def __init__(self, jobs, options):

        # Prepare jobs
        self.__jobs = jobs

        # Prepare options
        self.__options = options

    # Launch
    def launch(self):

        # Variables
        jobs_status = {'jobs_count': 0, 'quiet': True, 'time_launcher': time()}
        result = None

        # Run selected jobs
        for job in self.__jobs:

            # Filter jobs list
            if not self.__options.pipeline and not Lists.match(
                    self.__options.names, job, ignore_case=self.__options.ignore_case,
                    no_regex=self.__options.no_regex):
                continue

            # Filter stages list
            if self.__options.pipeline and self.__options.names and not Lists.match(
                    self.__options.names, self.__jobs[job]['stage'],
                    ignore_case=self.__options.ignore_case,
                    no_regex=self.__options.no_regex):
                continue

            # Filter manual jobs
            job_manual = (self.__jobs[job]['when'] == 'manual')
            if job_manual and not self.__options.manual and not Lists.match(
                    self.__options.names, job, ignore_case=self.__options.ignore_case,
                    no_regex=self.__options.no_regex):
                continue

            # Filter disabled jobs
            if self.__jobs[job]['options']['disabled']:
                continue

            # Raise initial result
            if result is None:
                result = True

            # Run job
            attempt = 0
            expected = result
            jobs_status['jobs_count'] += 1
            result = Jobs(options=self.__options).run(self.__jobs[job], result,
                                                      jobs_status)

            # Retry job if allowed
            if expected and not result and self.__jobs[job]['retry'] > 0:
                while not result and attempt < self.__jobs[job]['retry']:
                    attempt += 1
                    result = Jobs(options=self.__options).run(self.__jobs[job], expected,
                                                              jobs_status)

        # Non quiet jobs
        if not jobs_status['quiet']:

            # Pipeline jobs footer
            if jobs_status['jobs_count'] > 1:

                # Evaluate duration total time
                time_total_duration = time() - jobs_status['time_launcher']
                time_total_seconds = '%.0f second%s' % (
                    time_total_duration % 60, 's' if time_total_duration % 60 > 1 else '')
                time_total_minutes = ''
                if time_total_duration >= 60:
                    time_total_minutes = '%.0f minute%s ' % (
                        time_total_duration / 60,
                        's' if time_total_duration / 60 > 1 else '')
                time_total_string = time_total_minutes + time_total_seconds

                # Final footer
                print(' %s> Pipeline: %s in %s total%s' %
                      (Colors.YELLOW, Colors.BOLD + 'Success' if result else Colors.RED +
                       'Failure', time_total_string, Colors.RESET))
                print(' ')
                print(' ')
                Platform.flush()

            # Simple job footer
            else:
                print(' ')
                Platform.flush()

        # Result
        return bool(result)
