"""Module with all the functions for the menu loop for taskmaster"""

import os
import sys
import termios

import term_setup

class Taskmaster:
	"""Class for the main program"""

	def __init__(self, rows, columns, termios):
		"""starts base settings"""
		self.name = "taskmaster"
		self.rows = rows
		self.columns = columns
		self.termios = termios

def initloop(classList, configList, taskmaster):
	pass

def setuploop(classList, configList):
	"""This function setups the menu loop"""
	rows, columns = os.popen('stty size', 'r').read().split()
	terminfo, fd = term_setup.init_term()
	taskmaster = Taskmaster(rows, columns, terminfo)
	# char = None
	# while True:
	# 	char = stdin.read(1)
	# 	if char == '\x1b':
	# 		break
	# 	elif char == '\x1b':
	# 		char = stdin.read(1)
	# 		if char == '[':
	# 			char = stdin.read(1)
	# 			if char == 'C':
	# 				print("FLECHA DERECHA")
	# 			elif char == 'D':
	# 				print("FLECHA IZQ")
	initloop(classList, configList, taskmaster)
	termios.tcsetattr(fd, termios.TCSAFLUSH, terminfo)
