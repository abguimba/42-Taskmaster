#!/usr/bin/env python3

"""Main module for this taskmaster project"""
import sys
import termios
import tty
import yaml

import errors
import tools
import classes
import userinput
import output
import time

def main():
	"""main function"""
	errors.error_check_params()
	output.display_progress()
	start = time.time()
	configList = tools.parse_yaml_file()
	tools.verify_config(configList)
	classList = classes.init_classes(configList)
	end = time.time()
	userinput.ask_for_confirmation(classList, str(end - start))

	try:
		stdin = sys.stdin
		fd = stdin.fileno()
		new = old = termios.tcgetattr(fd)
		new[3] &= ~termios.ICANON
		termios.tcsetattr(fd, termios.TCSAFLUSH, new)
		tty.setraw(sys.stdin)
		char = 'a'
		# while char != '\x1b':
		char = stdin.read(3)
		print("JAA")
		print("XDDDDDDD")
	except:
		termios.tcsetattr(fd, termios.TCSAFLUSH, old)
		exit(0)
	finally:
		termios.tcsetattr(fd, termios.TCSAFLUSH, old)
	# print(str(int(char)))
	# if char == '\x1b':
	print(int(char))

if __name__ == '__main__':
	main()
