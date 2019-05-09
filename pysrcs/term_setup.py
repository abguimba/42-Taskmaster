"""Module to handle terminal configuration"""

import termios
import sys
import tty
import os

def restore_term(terminfo, fd):
	"""restores original termios structure and shows cursor back again"""
	termios.tcsetattr(fd, termios.TCSAFLUSH, terminfo)
	sys.stdout.write("\033[?25h")
	sys.stdout.flush()
	print("Default terminal configuration restored, bye")

def init_term():
	"""This function tries to initialise the terminal, or exits gracefully"""
	try:
		stdin = sys.stdin
		fd = stdin.fileno()
		new = old = termios.tcgetattr(fd)
		new[3] &= ~termios.ICANON
		new[3] &= ~termios.ECHO
		new[6][termios.VTIME] = 1
		new[6][termios.VMIN] = 0
		termios.tcsetattr(fd, termios.TCSAFLUSH, new)
		sys.stdout.write("\033[?25l")
		sys.stdout.flush()
	except:
		termios.tcsetattr(fd, termios.TCSAFLUSH, old)
		print("There was an error setting the terminal settings"
		+ ", resetting base terminal settings")
		sys.exit(0)
	finally:
		return old, fd
