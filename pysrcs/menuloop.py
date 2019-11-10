"""Module with all the functions for the menu loop for taskmaster"""

import os
import sys
import termios
import signal
import curses
import cmd
import time

import output
import tools
import classes
import output
import errors
import execution
import processes
import userinput
import logging

globProgramList = []
globProgramconfigList = []

class TaskmasterShell(cmd.Cmd):
    global globProgramList
    global globConfigList
    intro = 'Welcome to the Taskmaster shell. Type help or ? to list commands. Also type help <command> for further information about a specific command\n'
    prompt = '($>) '
    file = None

    # ----- basic taskmaster commands -----
    def do_status(self, arg):
        'Displays status for all supervised programs, or invididual programs. Usage -> status or status <program name>'
        execution.update_program_status(globProgramList)
        logging.info(f'Displaying program status.')
        output.display_status(globProgramList, arg)
        execution.update_program_status(globProgramList)
	
    def complete_status(self, text, line, begidx, endidx):
        execution.update_program_status(globProgramList)
        newList = [i.name for i in globProgramList]
        execution.update_program_status(globProgramList)
        return [i for i in newList if i.startswith(text)]

    def do_start(self, arg):
        'Starts desired program(s). Usage -> start <program name(s)>'
        execution.update_program_status(globProgramList)
        logging.info(f'Starting programs.')
        args = arg.split(' ')
        checker = 0
        if len(args) == 1:
            for c in args:
                if c.isalpha():
                    checker = 1
                    break
        if len(args) == 1 and checker == 0:
            args = ""
        if len(args) < 1:		
            print(output.bcolors.FAIL + "Please select valid program(s) to start!" + output.bcolors.ENDC)
            print(output.bcolors.FAIL + "Possible programs: " + output.bcolors.ENDC)
            for program in globProgramList:
                print(output.bcolors.FAIL + program.name + output.bcolors.ENDC)
        else:
            counter = 0
            for a in args:
                for program in globProgramList:
                    if program.name == a:
                        program.selected = 1
                        counter += 1
            if counter == 0:
                print(output.bcolors.FAIL + "Please select valid program(s) to start!" + output.bcolors.ENDC)
                print(output.bcolors.FAIL + "Possible programs: " + output.bcolors.ENDC)
                for program in globProgramList:
                    print(output.bcolors.FAIL + program.name + output.bcolors.ENDC)
            else:
                processes.handle_program(globProgramList, 'startselect')            
        for program in globProgramList:
            program.selected = 0
        execution.update_program_status(globProgramList)


    def complete_start(self, text, line, begidx, endidx):
        execution.update_program_status(globProgramList)
        newList = [i.name for i in globProgramList if i.state == "Not started"]
        execution.update_program_status(globProgramList)
        return [i for i in newList if i.startswith(text)]
	
    def do_stop(self, arg):
        'Stops desired program(s). Usage -> stop <program name(s)>'
        execution.update_program_status(globProgramList)
        logging.info(f'Stopping programs.')
        args = arg.split(' ')
        checker = 0
        if len(args) == 1:
            for c in args:
                if c.isalpha():
                    checker = 1
                    break
        if len(args) == 1 and checker == 0:
            args = ""
        if len(args) < 1:		
            print(output.bcolors.FAIL + "Please select valid program(s) to stop!" + output.bcolors.ENDC)
            print(output.bcolors.FAIL + "Possible programs: " + output.bcolors.ENDC)
            for program in globProgramList:
                print(output.bcolors.FAIL + program.name + output.bcolors.ENDC)
        else:
            counter = 0
            for a in args:
                for program in globProgramList:
                    if program.name == a:
                        program.selected = 1
                        counter += 1
            if counter == 0:
                print(output.bcolors.FAIL + "Please select valid program(s) to stop!" + output.bcolors.ENDC)
                print(output.bcolors.FAIL + "Possible programs: " + output.bcolors.ENDC)
                for program in globProgramList:
                    print(output.bcolors.FAIL + program.name + output.bcolors.ENDC)
            else:
                processes.handle_program(globProgramList, 'stopselect')
        for program in globProgramList:
            program.selected = 0
        execution.update_program_status(globProgramList)

    def complete_stop(self, text, line, begidx, endidx):
        execution.update_program_status(globProgramList)
        newList = [i.name for i in globProgramList if i.state == "Running" or i.state == "Starting"]
        execution.update_program_status(globProgramList)
        return [i for i in newList if i.startswith(text)]
	
    def do_restart(self, arg):
        'Restarts desired program(s). Usage -> stop <program name(s)>'
        execution.update_program_status(globProgramList)
        logging.info(f'Restarting programs.')
        args = arg.split(' ')
        checker = 0
        if len(args) == 1:
            for c in args:
                if c.isalpha():
                    checker = 1
                    break
        if len(args) == 1 and checker == 0:
            args = ""
        if len(args) < 1:		
            print(output.bcolors.FAIL + "Please select valid program(s) to restart!" + output.bcolors.ENDC)
            print(output.bcolors.FAIL + "Possible programs: " + output.bcolors.ENDC)
            for program in globProgramList:
                print(output.bcolors.FAIL + program.name + output.bcolors.ENDC)
        else:
            counter = 0
            for a in args:
                for program in globProgramList:
                    if program.name == a:
                        program.selected = 1
                        counter += 1
            if counter == 0:
                print(output.bcolors.FAIL + "Please select valid program(s) to restart!" + output.bcolors.ENDC)
                print(output.bcolors.FAIL + "Possible programs: " + output.bcolors.ENDC)
                for program in globProgramList:
                    print(output.bcolors.FAIL + program.name + output.bcolors.ENDC)
            else:
                processes.handle_program(globProgramList, 'restartselect')
        for program in globProgramList:
            program.selected = 0
        execution.update_program_status(globProgramList)

    def complete_restart(self, text, line, begidx, endidx):
        execution.update_program_status(globProgramList)
        newList = [i.name for i in globProgramList if i.state != "Not started"]
        execution.update_program_status(globProgramList)
        return [i for i in newList if i.startswith(text)]
	
    def do_reload(self, arg):
        'Reloads the whole configuration. Usage -> reload'
        global globProgramList
        global globConfigList
        execution.update_program_status(globProgramList)
        logging.info(f'Reloading programs.')
        if userinput.ask_for_reload_confirmation():
            output.display_progress()
            start = time.time()
            configList = tools.parse_json_file()
            if configList == None:
                print(f"Couldn't load the new configuration, error while parsing the json config file")
                return
            verif = tools.verify_config(1, configList)
            if verif == 1:
                print(f"Couldn't load the new configuration, error while verifying the new configuration")
                return
            programList = classes.init_classes(configList)
            end = time.time()
            verif = userinput.ask_for_confirmation(programList, str(end - start), None, 1)
            if verif != 1:
                execution.load_or_reload(programList, globProgramList)
                globProgramList = programList
                globConfigList = configList
        execution.update_program_status(globProgramList)
	
    def do_exit(self, arg):
        'Close the Taskmaster shell, kill remaining jobs and exit. Usage -> exit'
        confirmation = userinput.ask_for_exit_kill_confirmation()
        global exit
        if confirmation == "yes" or confirmation == "y":
            print('\nAll programs are being terminated... Please wait. Thank you for using our Taskmaster.')
            exit = True
            self.close()
            return True
        elif confirmation == "no" or confirmation == "n":
            print('\nNo programs were terminated... Please wait. Thank you for using our Taskmaster.')
            logging.info(f'No programs were terminated on exit.')
            self.close()
            return True
        elif confirmation == "cancel" or confirmation == "c":
            logging.info(f'Exit was cancelled.')
            print('\nExit was cancelled.\n')

    def close(self):
        if self.file:
            self.file.close()
            self.file = None

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))

exit = False

def setuploop(programList, configList):
	"""This function setups the menu loop"""
	global globProgramList
	global globConfigList
	globProgramList = programList
	globConfigList = configList
	TaskmasterShell().cmdloop()
	logging.info(f'Taskmaster loop started.')
	if exit == True:
		tools.kill_jobs(programList)
