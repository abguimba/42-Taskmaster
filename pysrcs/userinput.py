"""File dedicated to user input handling"""

import output
import sys
import termios
import logging

import curses

def ask_for_confirmation(programList, time):
	"""Asks for confirmation of current setup"""
	logging.info(f'Asking the user, if he wants to launch the loaded configuration.')
	output.display_summary(programList, time)
	confirmation = input().lower()
	while confirmation != 'y' and confirmation != "yes":
		if confirmation == 'n' or confirmation == "no":
			print(output.bcolors.FAIL, "\n/!\\Aborting execution /!\\",
			output.bcolors.ENDC)
			logging.info(f'User input {confirmation}, exit Taskmaster with RC=0.')
			sys.exit(0)
		logging.info(f'User input invlid:"{confirmation}". Re-asking')
		print("Please answer with yes/y or no/n")
		confirmation = input().lower()
	logging.info(f'User input "{confirmation}".')
