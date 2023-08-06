#!/usr/bin/env python3

# Components
from ..prints.colors import Colors
from ..system.platform import Platform

# Outputs class
class Outputs:

    # Header
    @staticmethod
    def header(jobs_status, job_data, image, engine_type):

        # Header output
        if jobs_status['jobs_count'] > 1:
            print(' ')
        print(' %s===[ %s%s: %s%s %s(%s, %s) %s]===%s' %
              (Colors.GREEN, Colors.YELLOW, job_data['stage'], Colors.YELLOW,
               job_data['name'], Colors.CYAN, image, engine_type, Colors.GREEN,
               Colors.RESET))
        print(' ')
        Platform.flush()

    # Footer
    @staticmethod
    def footer(result, time_string, job_data, job_details):

        # Footer output
        print(' %s> %s: %s in %s%s%s' %
              (Colors.YELLOW, job_data['name'],
               Colors.GREEN + 'Success' if result else Colors.RED + 'Failure',
               time_string, Colors.CYAN + job_details, Colors.RESET))
        print(' ')
        Platform.flush()

    # Debugging
    @staticmethod
    def debugging(container_exec, container_name, shell):

        # Debugging informations
        print(' ')
        print(
            ' %s> INFORMATION: %sUse \'%s%s %s %s%s\' commands for debugging. Interrupt with Ctrl+C...%s'
            % (Colors.YELLOW, Colors.BOLD, Colors.CYAN, container_exec, container_name,
               shell, Colors.BOLD, Colors.RESET))
        print(' ')
        Platform.flush()

    # Interruption
    @staticmethod
    def interruption():

        # Interruption output
        print(' ')
        print(' ')
        print(' %s> WARNING: %sUser interruption detected, stopping the container...%s' %
              (Colors.YELLOW, Colors.BOLD, Colors.RESET))
        print(' ')
        Platform.flush()
