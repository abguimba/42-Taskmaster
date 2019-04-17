#!/usr/bin/env python3

"""Main module for this taskmaster project"""
import sys
import termios
import tty
import yaml

def main():
	"""main function"""
	if len(sys.argv) != 2:
		print("usage: main.py config_file")
		exit(1)
	with open(sys.argv[1], 'r') as stream:
		try:
			config = yaml.safe_load(stream)
			for i in config:
				print(config[i])
		except yaml.YAMLError as exc:
			print(exc)
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
