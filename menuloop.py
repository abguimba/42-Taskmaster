"""Module with all the functions for the menu loop for taskmaster"""

import os
import sys
import termios
import signal

import term_setup

class Taskmaster:
	"""Class for the main program"""

	def __init__(self, rows, columns, termios):
		"""starts base settings"""
		self.name = "taskmaster"
		self.rows = rows
		self.columns = columns
		self.termios = termios

	def update_term(self):
		self.rows, self.columns = os.popen('stty size', 'r').read().split()

def initloop(classList, configList, taskmaster, stdin):
	"""This function initialises the loop"""

	def sigwinch_handler():
		"""This function is a signal handler to update the output"""
		taskmaster.update_term()

	signal.signal(signal.SIGWINCH, sigwinch_handler)
	while True:
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
