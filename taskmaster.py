#!/usr/bin/env python3

"""Main module for this taskmaster project"""
import sys
import termios
import tty
import yaml

import errors
import tools

class Program():
	"""base class for all programs to be executed"""

	def __init__(self, config):
		"""assigns config for a program to his object"""
		self.config = config
		# self.name = 
		# self.cmd = 
		# self.cmdammount = 
		# self.autostart = 
		# self.autorestart = 
		# self.starttime = 
		# self. stoptime = 
		# self.restartretries = 
		# self.quisig = 
		# self.exitcodes = 
		# self.workingdir = 
		# self.umask = 
		# self.stdout = 
		# self.stdin = 
		# self.env = 

def main():
	"""main function"""
	errors.error_check_params()

	with open(sys.argv[1], 'r') as stream:
		try:
			configload = yaml.safe_load(stream)
			for data in configload:
				configList = []
				for program in configload[data]:
					config = []
					for param in configload[data][program]:
						config.append(configload[data][program][param])
					configList.append(config)
		except yaml.YAMLError as exc:
			errors.error_yaml(exc)
	
	
	classList = []
	
	for config in configList:
		newClass = Program(config)
		classList.append(newClass)
	

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
