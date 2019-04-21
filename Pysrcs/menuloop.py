"""Module with all the functions for the menu loop for taskmaster"""

import os
import sys
import termios
import signal
import curses

import term_setup
import output

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

	def right_key(self):
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
			pass
		elif self.menustate == "confirm":
			pass

	def update_term(self):
		"""updates terminal rows and cols after a SIGWNCH"""
		self.rows, self.columns = os.popen('stty size', 'r').read().split()

	def get_rows(self):
		"""returns terminal rows"""
		return int(self.rows)

	def get_columns(self):
		"""returns terminal columns"""
		return int(self.columns)

def init_menu(key, classList, configList, taskmaster):
	"""This function updates and initialises the menu of the taskmaster"""
	if key == "enter":
		pass
	elif key == "right":
		taskmaster.right_key()
	elif key == "left":
		pass
	if taskmaster.get_columns() >= 39:
		if taskmaster.menustate == "base":
			output.display_basic_menu(taskmaster)
		elif (taskmaster.menustate == "startselect"
		or taskmaster.menustate == "restartselect" or taskmaster.menustate == "stopselect"):
			pass
		elif taskmaster.menustate == "confirm":
			pass
		print('\r', end='')
	elif taskmaster.get_columns() >= 8:
		print('\r', end='')
		i = taskmaster.get_columns()
		while i > 0:
			print(' ', end='')
			i -= 1
		print('\r', end='')
		print("No space", end='')
		print('\r', end='')


def initloop(classList, configList, taskmaster, stdin):
	"""This function initialises the loop"""

	def sigwinch_handler(sig, frame):
		"""This function is a signal handler to update the output"""
		taskmaster.update_term()

	signal.signal(signal.SIGWINCH, sigwinch_handler)
	key = None
	while True:
		init_menu(key, classList, configList, taskmaster)
		keychar = stdin.read(1)
		if keychar == 'x':
			break
		elif keychar == '\n':
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
		curses.filter()
		stdscr = curses.initscr()
		stdscr.refresh()
		curses.endwin()

def setuploop(classList, configList):
	"""This function setups the menu loop"""
	rows, columns = os.popen('stty size', 'r').read().split()
	terminfo, fd = term_setup.init_term()
	taskmaster = Taskmaster(rows, columns, terminfo)
	initloop(classList, configList, taskmaster, sys.stdin)
	term_setup.restore_term(terminfo, fd)
