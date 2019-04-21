"""File dedicated to user input handling"""

import output
import sys
import termios

import curses

def ask_for_confirmation(classList, time):
	"""Asks for confirmation of current setup"""
	output.display_summary(classList, time)
	confirmation = input()
	while confirmation != 'y' and confirmation != "yes":
		if confirmation == 'n' or confirmation == "no":
			print(output.bcolors.FAIL, "\n/!\\Aborting execution /!\\",
			output.bcolors.ENDC)
			sys.exit(0)
		print("Please answer with yes/y or no/n")
		confirmation = input()
	print('\n', end='')
