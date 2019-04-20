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

	def update_term(self):
		"""updates terminal rows and cols after a SIGWNCH"""
		self.rows, self.columns = os.popen('stty size', 'r').read().split()
	
	def get_rows(self):
		"""returns terminal rows"""
		return int(self.rows)
	
	def get_columns(self):
		"""returns terminal columns"""
		return int(self.columns)

def initloop(classList, configList, taskmaster, stdin):
	"""This function initialises the loop"""

	def sigwinch_handler(sig, frame):
		"""This function is a signal handler to update the output"""
		taskmaster.update_term()

	signal.signal(signal.SIGWINCH, sigwinch_handler)
	while True:
		option = None
		output.init_menu(option, classList, configList, taskmaster)
		char = stdin.read(1)
		if char == 'x':
			break
		elif char == '\x1b':
			char = stdin.read(1)
			if char == '[':
				char = stdin.read(1)
				if char == 'C':
					print("FLECHA DERECHA")
				elif char == 'D':
					print("FLECHA IZQ")

def setuploop(classList, configList):
	"""This function setups the menu loop"""
	rows, columns = os.popen('stty size', 'r').read().split()
	terminfo, fd = term_setup.init_term()
	taskmaster = Taskmaster(rows, columns, terminfo)
	initloop(classList, configList, taskmaster, sys.stdin)
	termios.tcsetattr(fd, termios.TCSAFLUSH, terminfo)
