#!/usr/bin/env python3

"""Main module for this taskmaster project"""
import sys
import termios
import tty
import yaml

import errors
import tools
import classes

def main():
	"""main function"""
	errors.error_check_params()
	configList = tools.parse_yaml_file()
	tools.verify_config(configList)
	classes.init_classes(configList)

	stdin = sys.stdin
	fd = stdin.fileno()
	new = old = termios.tcgetattr(fd)
	new[3] &= ~termios.ICANON
	termios.tcsetattr(fd, termios.TCSAFLUSH, new)
	tty.setraw(sys.stdin)
	char = stdin.read(1)
	termios.tcsetattr(fd, termios.TCSAFLUSH, old)

if __name__ == '__main__':
	main()
