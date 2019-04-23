"""Module with all the functions for the menu loop for taskmaster"""

import os
import sys
import termios
import signal
import curses

import term_setup
import output
import tools
import classes
import output
import errors
import execution


class Taskmaster:
	"""Class for the main program"""

	def __init__(self, rows, columns, termios):
		"""starts base settings"""
		self.name = "taskmaster"
		self.rows = rows
		self.columns = columns
		self.termios = termios
		self.menustate = "base"
		self.statusselected = 1
		self.startselected = 0
		self.restartselected = 0
		self.stopselected = 0
		self.reloadselected = 0
		self.exitselected = 0
		self.confirmselected = 1
		self.cancelselected = 0

	def enter_key(self, programList):
		"""switches elements on enter key press"""
		if self.menustate == "base":
			if self.statusselected == 1:
				output.display_status(programList)
			elif self.startselected == 1:
				programList[0].firsttime = 1
				self.menustate = "startselect"
			elif self.restartselected == 1:
				programList[0].firsttime = 1
				self.menustate = "restartselect"
			elif self.stopselected == 1:
				programList[0].firsttime = 1
				self.menustate = "stopselect"
			elif self.reloadselected == 1:
				self.menustate = "confirm"
				print("This will reload the config file, "
				+ "potentially killing previous jobs, are you sure?\n")
			elif self.exitselected == 1:
				self.menustate = "confirm"
				print("Exiting will close all programs, are you sure?")
		elif (self.menustate == "startselect"
		or self.menustate == "restartselect" or self.menustate == "stopselect"):
			count = len(programList)
			while count > -1:
				print('\r', end='')
				sys.stdout.write("\033[K")
				print('\r', end='')
				sys.stdout.write("\033[F")
				sys.stdout.write("\033[K")
				count -= 1
			self.menustate = "base"
		elif self.menustate == "confirm":
			if self.exitselected == 1:
				if self.confirmselected == 1:
					return programList, 1
				elif self.cancelselected == 1:
					self.menustate = "base"
					self.cancelselected = 0
					self.confirmselected = 1
			elif self.reloadselected == 1:
				if self.confirmselected == 1:
					self.menustate = "base"
					saveprogramList = programList
					configList = tools.parse_yaml_file()
					fail = tools.verify_config(1, configList)
					if fail == 1:
						errors.error_reload_config()
						return saveprogramList, 0
					else:
						programList = classes.init_classes(configList)
						execution.load_or_reload(programList, saveprogramList)
						print(output.bcolors.OKGREEN + "Config file reloaded",
						output.bcolors.ENDC)
						return programList, 0
				elif self.cancelselected == 1:
					print('\r', end='')
					sys.stdout.write("\033[K")
					print('\r', end='')
					sys.stdout.write("\033[F")
					sys.stdout.write("\033[K")
					print('\r', end='')
					sys.stdout.write("\033[K")
					print('\r', end='')
					sys.stdout.write("\033[F")
					sys.stdout.write("\033[K")
					self.menustate = "base"
					self.cancelselected = 0
					self.confirmselected = 1
		return programList, 0

	def left_key(self, programList):
		"""switches elements on left key press"""
		if self.menustate == "base":
			if self.statusselected == 1:
				self.statusselected = 0
				self.exitselected = 1
			elif self.startselected == 1:
				self.startselected = 0
				self.statusselected = 1
			elif self.restartselected == 1:
				self.restartselected = 0
				self.startselected = 1
			elif self.stopselected == 1:
				self.stopselected = 0
				self.restartselected = 1
			elif self.reloadselected == 1:
				self.reloadselected = 0
				self.stopselected = 1
			elif self.exitselected == 1:
				self.exitselected = 0
				self.reloadselected = 1
		elif (self.menustate == "startselect"
		or self.menustate == "restartselect" or self.menustate == "stopselect"):
			i = 0
			for program in programList:
				if program.selected == 1:
					program.selected = 0
					if i == len(programList) - 1:
						programList[0].selected = 1
					else:
						programList[i + 2].selected = 1
				i += 1
			return programList
		elif self.menustate == "confirm":
			if self.confirmselected == 1:
				self.confirmselected = 0
				self.cancelselected = 1
			elif self.cancelselected == 1:
				self.cancelselected = 0
				self.confirmselected = 1
		return programList

	def right_key(self, programList):
		"""switches elements on right key press"""
		if self.menustate == "base":
			if self.statusselected == 1:
				self.statusselected = 0
				self.startselected = 1
			elif self.startselected == 1:
				self.startselected = 0
				self.restartselected = 1
			elif self.restartselected == 1:
				self.restartselected = 0
				self.stopselected = 1
			elif self.stopselected == 1:
				self.stopselected = 0
				self.reloadselected = 1
			elif self.reloadselected == 1:
				self.reloadselected = 0
				self.exitselected = 1
			elif self.exitselected == 1:
				self.exitselected = 0
				self.statusselected = 1
		elif (self.menustate == "startselect"
		or self.menustate == "restartselect" or self.menustate == "stopselect"):
			i = 0
			for program in programList:
				if program.selected == 1:
					program.selected = 0
					if i == 0:
						programList[len(programList) - 1].selected = 1
					else:
						programList[i - 2].selected = 1
				i += 1
			return programList
		elif self.menustate == "confirm":
			if self.confirmselected == 1:
				self.confirmselected = 0
				self.cancelselected = 1
			elif self.cancelselected == 1:
				self.cancelselected = 0
				self.confirmselected = 1
		return programList

	def update_term(self):
		"""updates terminal rows and cols after a SIGWNCH"""
		self.rows, self.columns = os.popen('stty size', 'r').read().split()

	def get_rows(self):
		"""returns terminal rows"""
		return int(self.rows)

	def get_columns(self):
		"""returns terminal columns"""
		return int(self.columns)

def draw_menu(taskmaster, programList):
	if taskmaster.get_columns() >= 39 and taskmaster.get_rows() >= 8:
		if taskmaster.menustate == "base":
			output.display_basic_menu(taskmaster)
		elif (taskmaster.menustate == "startselect"
		or taskmaster.menustate == "restartselect"
		or taskmaster.menustate == "stopselect"):
			programList = output.display_programs_menu(taskmaster, programList)
		elif taskmaster.menustate == "confirm":
			output.display_confirm_menu(taskmaster)
		print('\r', end='')
	elif taskmaster.get_columns() >= 8 and taskmaster.get_rows() >= 8:
		print('\r', end='')
		i = taskmaster.get_columns()
		while i > 0:
			print(' ', end='')
			i -= 1
		print('\r', end='')
		print("No space", end='')
		print('\r', end='')
	return programList

def init_menu(key, programList, configList, taskmaster):
	"""This function updates the menu of the taskmaster"""
	if key == "enter":
		programList, exiting = taskmaster.enter_key(programList)
		if exiting == 1:
			return programList, 1
	elif key == "right":
		programList = taskmaster.right_key(programList)
	elif key == "left":
		programList = taskmaster.left_key(programList)
	programList = draw_menu(taskmaster, programList)
	return programList, 0


def initloop(programList, configList, taskmaster, stdin):
	"""This function initialises the loop"""

	def sigwinch_handler(sig, frame):
		"""This function is a signal handler to update the output"""
		taskmaster.update_term()

	signal.signal(signal.SIGWINCH, sigwinch_handler)
	key = None
	while True:
		programList, leave = init_menu(key, programList, configList, taskmaster)
		if leave == 1:
			break
		keychar = stdin.read(1)
		if keychar == '\n':
			key = "enter"
		elif keychar == '\x1b':
			keychar = stdin.read(1)
			if keychar == '[':
				keychar = stdin.read(1)
				if keychar == 'C':
					key = "right"
				elif keychar == 'D':
					key = "left"
		else:
			key = None
		execution.update_program_status(programList)
		curses.filter()
		stdscr = curses.initscr()
		stdscr.refresh()
		curses.endwin()

def setuploop(programList, configList):
	"""This function setups the menu loop"""
	rows, columns = os.popen('stty size', 'r').read().split()
	terminfo, fd = term_setup.init_term()
	taskmaster = Taskmaster(rows, columns, terminfo)
	initloop(programList, configList, taskmaster, sys.stdin)
	term_setup.restore_term(terminfo, fd)
	tools.kill_jobs(programList)
