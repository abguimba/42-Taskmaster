"""Module with all the functions for the menu loop for taskmaster"""

import os
import sys
import termios
import signal

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
		self.startselected = False
		self.restartselected = False
		self.stopselected = False
		self.statusselected = True
		self.reloadselected = False
		self.exitselected = False
		self.yesselected = False
		self.cancelselected = False

	def update_term(self):
		"""updates terminal rows and cols after a SIGWNCH"""
		self.rows, self.columns = os.popen('stty size', 'r').read().split()

	def get_rows(self):
		"""returns terminal rows"""
		return int(self.rows)

	def get_columns(self):
		"""returns terminal columns"""
		return int(self.columns)

def init_menu(option, classList, configList, taskmaster):
	"""This function updates and initialises the menu of the taskmaster"""
	if option == "base":
		if taskmaster.get_columns() >= 37:
			pass
		elif taskmaster.get_columns() >= 8:
			print("No space")


def initloop(classList, configList, taskmaster, stdin):
	"""This function initialises the loop"""

	def sigwinch_handler(sig, frame):
		"""This function is a signal handler to update the output"""
		taskmaster.update_term()

	signal.signal(signal.SIGWINCH, sigwinch_handler)
	option = "base"
	while True:
		init_menu(option, classList, configList, taskmaster)
		keychar = stdin.read(1)
		if keychar == 'x':
			break
		elif keychar == '\n':
			option = "enter"
		elif keychar == '\x1b':
			keychar = stdin.read(1)
			if keychar == '[':
				keychar = stdin.read(1)
				if keychar == 'C':
					option = "right"
				elif keychar == 'D':
					option = "left"
		else:
			option = "base"

def setuploop(classList, configList):
	"""This function setups the menu loop"""
	rows, columns = os.popen('stty size', 'r').read().split()
	terminfo, fd = term_setup.init_term()
	taskmaster = Taskmaster(rows, columns, terminfo)
	initloop(classList, configList, taskmaster, sys.stdin)
	termios.tcsetattr(fd, termios.TCSAFLUSH, terminfo)
