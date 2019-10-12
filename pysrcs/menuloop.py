"""Module with all the functions for the menu loop for taskmaster"""

import os
import sys
import termios
import signal
import curses
import cmd
import time

import term_setup
import output
import tools
import classes
import output
import errors
import execution
import processes
import userinput

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
        execution.update_program_status(globProgramList)
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
                tools.kill_jobs(globProgramList)
                execution.load_or_reload(programList, None)
                globProgramList = programList
        execution.update_program_status(globProgramList)
	
    def do_exit(self, arg):
        'Stop recording, close the Taskmaster window, and exit. Usage -> exit'
        print('\nAll programs are being terminated... Please wait. Thank you for using our Taskmaster')
        self.close()
        return True

    def close(self):
        if self.file:
            self.file.close()
            self.file = None

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))

# class Taskmaster:
# 	"""Class for the main program"""

# 	def __init__(self, rows, columns, termios, configList):
# 		"""starts base settings"""
# 		self.name = "taskmaster"
# 		self.rows = rows
# 		self.columns = columns
# 		self.termios = termios
# 		self.config = configList
# 		self.menustate = "base"
# 		self.statusselected = 1
# 		self.startselected = 0
# 		self.restartselected = 0
# 		self.stopselected = 0
# 		self.reloadselected = 0
# 		self.exitselected = 0
# 		self.confirmselected = 1
# 		self.cancelselected = 0

# 	def enter_key(self, programList):
# 		"""switches elements on enter key press"""
# 		if self.menustate == "base":
# 			if self.statusselected == 1:
# 				output.display_status(programList)
# 			elif self.startselected == 1:
# 				programList[0].firsttime = 1
# 				self.menustate = "startselect"
# 			elif self.restartselected == 1:
# 				programList[0].firsttime = 1
# 				self.menustate = "restartselect"
# 			elif self.stopselected == 1:
# 				programList[0].firsttime = 1
# 				self.menustate = "stopselect"
# 			elif self.reloadselected == 1:
# 				self.menustate = "confirm"
# 				print("This will reload the config file, "
# 				+ "potentially killing previous jobs, are you sure?\n")
# 			elif self.exitselected == 1:
# 				self.menustate = "confirm"
# 				print("Exiting will close all programs, are you sure?")
# 		elif (self.menustate == "startselect"
# 		or self.menustate == "restartselect" or self.menustate == "stopselect"):
# 			error = processes.handle_program(programList, self.menustate)
# 			count = len(programList)
# 			while count > -1:
# 				print('\r', end='')
# 				sys.stdout.write("\033[K")
# 				print('\r', end='')
# 				sys.stdout.write("\033[F")
# 				sys.stdout.write("\033[K")
# 				count -= 1
# 			if error == 1:
# 				print(output.bcolors.FAIL + "Program already started/finished!" + output.bcolors.ENDC)
# 			elif error == 2:
# 				print(output.bcolors.FAIL + "Program is not running!" + output.bcolors.ENDC)
# 			self.menustate = "base"
# 		elif self.menustate == "confirm":
# 			if self.exitselected == 1:
# 				if self.confirmselected == 1:
# 					return programList, 1
# 				elif self.cancelselected == 1:
# 					self.menustate = "base"
# 					self.cancelselected = 0
# 					self.confirmselected = 1
# 			elif self.reloadselected == 1:
# 				if self.confirmselected == 1:
# 					self.menustate = "base"
# 					saveprogramList = programList
# 					configList = tools.parse_yaml_file()
# 					fail = tools.verify_config(1, configList)
# 					if fail == 1:
# 						errors.error_reload_config()
# 						return saveprogramList, 0
# 					else:
# 						programList = classes.init_classes(configList)
# 						execution.load_or_reload(programList, saveprogramList)
# 						print(output.bcolors.OKGREEN + "Config file reloaded",
# 						output.bcolors.ENDC)
# 						return programList, 0
# 				elif self.cancelselected == 1:
# 					print('\r', end='')
# 					sys.stdout.write("\033[K")
# 					print('\r', end='')
# 					sys.stdout.write("\033[F")
# 					sys.stdout.write("\033[K")
# 					print('\r', end='')
# 					sys.stdout.write("\033[K")
# 					print('\r', end='')
# 					sys.stdout.write("\033[F")
# 					sys.stdout.write("\033[K")
# 					self.menustate = "base"
# 					self.cancelselected = 0
# 					self.confirmselected = 1
# 		return programList, 0

# 	def left_key(self, programList):
# 		"""switches elements on left key press"""
# 		if self.menustate == "base":
# 			if self.statusselected == 1:
# 				self.statusselected = 0
# 				self.exitselected = 1
# 			elif self.startselected == 1:
# 				self.startselected = 0
# 				self.statusselected = 1
# 			elif self.restartselected == 1:
# 				self.restartselected = 0
# 				self.startselected = 1
# 			elif self.stopselected == 1:
# 				self.stopselected = 0
# 				self.restartselected = 1
# 			elif self.reloadselected == 1:
# 				self.reloadselected = 0
# 				self.stopselected = 1
# 			elif self.exitselected == 1:
# 				self.exitselected = 0
# 				self.reloadselected = 1
# 		elif (self.menustate == "startselect"
# 		or self.menustate == "restartselect" or self.menustate == "stopselect"):
# 			i = 0
# 			for program in programList:
# 				if program.selected == 1:
# 					program.selected = 0
# 					if i == 0:
# 						programList[len(programList) - 1].selected = 1
# 						return programList
# 					else:
# 						programList[i - 1].selected = 1
# 						return programList
# 				i += 1
# 			return programList
# 		elif self.menustate == "confirm":
# 			if self.confirmselected == 1:
# 				self.confirmselected = 0
# 				self.cancelselected = 1
# 			elif self.cancelselected == 1:
# 				self.cancelselected = 0
# 				self.confirmselected = 1
# 		return programList

# 	def right_key(self, programList):
# 		"""switches elements on right key press"""
# 		if self.menustate == "base":
# 			if self.statusselected == 1:
# 				self.statusselected = 0
# 				self.startselected = 1
# 			elif self.startselected == 1:
# 				self.startselected = 0
# 				self.restartselected = 1
# 			elif self.restartselected == 1:
# 				self.restartselected = 0
# 				self.stopselected = 1
# 			elif self.stopselected == 1:
# 				self.stopselected = 0
# 				self.reloadselected = 1
# 			elif self.reloadselected == 1:
# 				self.reloadselected = 0
# 				self.exitselected = 1
# 			elif self.exitselected == 1:
# 				self.exitselected = 0
# 				self.statusselected = 1
# 		elif (self.menustate == "startselect"
# 		or self.menustate == "restartselect" or self.menustate == "stopselect"):
# 			i = 0
# 			for program in programList:
# 				if program.selected == 1:
# 					program.selected = 0
# 					if i == len(programList) - 1:
# 						programList[0].selected = 1
# 						return programList
# 					else:
# 						programList[i + 1].selected = 1
# 						return programList
# 				i += 1
# 			return programList
# 		elif self.menustate == "confirm":
# 			if self.confirmselected == 1:
# 				self.confirmselected = 0
# 				self.cancelselected = 1
# 			elif self.cancelselected == 1:
# 				self.cancelselected = 0
# 				self.confirmselected = 1
# 		return programList

# 	def update_term(self):
# 		"""updates terminal rows and cols after a SIGWNCH"""
# 		self.rows, self.columns = os.popen('stty size', 'r').read().split()

# 	def get_rows(self):
# 		"""returns terminal rows"""
# 		return int(self.rows)

# 	def get_columns(self):
# 		"""returns terminal columns"""
# 		return int(self.columns)

# def draw_menu(taskmaster, programList):
# 	if taskmaster.get_columns() >= 39 and taskmaster.get_rows() >= 8:
# 		if taskmaster.menustate == "base":
# 			output.display_basic_menu(taskmaster)
# 		elif (taskmaster.menustate == "startselect"
# 		or taskmaster.menustate == "restartselect"
# 		or taskmaster.menustate == "stopselect"):
# 			programList = output.display_programs_menu(taskmaster, programList)
# 		elif taskmaster.menustate == "confirm":
# 			output.display_confirm_menu(taskmaster)
# 		print('\r', end='')
# 	elif taskmaster.get_columns() >= 8 and taskmaster.get_rows() >= 8:
# 		print('\r', end='')
# 		i = taskmaster.get_columns()
# 		while i > 0:
# 			print(' ', end='')
# 			i -= 1
# 		print('\r', end='')
# 		print("No space", end='')
# 		print('\r', end='')
# 	return programList

# def init_menu(key, programList, configList, taskmaster):
# 	"""This function updates the menu of the taskmaster"""
# 	if key == "enter":
# 		programList, exiting = taskmaster.enter_key(programList)
# 		if exiting == 1:
# 			return programList, 1
# 	elif key == "right":
# 		programList = taskmaster.right_key(programList)
# 	elif key == "left":
# 		programList = taskmaster.left_key(programList)
# 	programList = draw_menu(taskmaster, programList)
# 	return programList, 0


# def initloop(programList, configList, taskmaster, stdin):
# 	"""This function initialises the loop"""

# 	def sigwinch_handler(sig, frame):
# 		"""This function is a signal handler to update the output"""
# 		taskmaster.update_term()

# 	signal.signal(signal.SIGWINCH, sigwinch_handler)
# 	key = None
# 	while True:
# 		programList, leave = init_menu(key, programList, configList, taskmaster)
# 		if leave == 1:
# 			break
# 		keychar = stdin.read(1)
# 		if keychar == '\n':
# 			key = "enter"
# 		elif keychar == '\x1b':
# 			keychar = stdin.read(1)
# 			if keychar == '[':
# 				keychar = stdin.read(1)
# 				if keychar == 'C':
# 					key = "right"
# 				elif keychar == 'D':
# 					key = "left"
# 		else:
# 			key = None
# 		execution.update_program_status(programList)
# 		curses.filter()
# 		stdscr = curses.initscr()
# 		stdscr.refresh()
# 		curses.endwin()

def setuploop(programList, configList):
	"""This function setups the menu loop"""
	global globProgramList
	global globConfigList
	globProgramList = programList
	globConfigList = configList
	# rows, columns = os.popen('stty size', 'r').read().split()
	# terminfo, fd = term_setup.init_term()
	# taskmaster = Taskmaster(rows, columns, terminfo, configList)
	# initloop(programList, configList, taskmaster, sys.stdin)
	TaskmasterShell().cmdloop()
	# term_setup.restore_term(terminfo, fd)
	tools.kill_jobs(programList)
