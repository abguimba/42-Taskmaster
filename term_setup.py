"""Module to handle terminal configuration"""

import termios
import sys

def init_term():
	try:
		stdin = sys.stdin
		fd = stdin.fileno()
		new = old = termios.tcgetattr(fd)
		new[3] &= ~termios.ICANON
		new[3] &= ~termios.ECHO
		termios.tcsetattr(fd, termios.TCSAFLUSH, new)
	except:
		termios.tcsetattr(fd, termios.TCSAFLUSH, old)
		print("There was an error setting the terminal settings"
		+ ", resetting base terminal settings")
		exit(0)
	finally:
		return old, fd
