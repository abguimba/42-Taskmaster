"""Module to handle terminal configuration"""

import termios
import sys
import tty
import os
import curses

def init_term():
	"""This function tries to initialise the terminal, or exits gracefully"""
	try:
		stdin = sys.stdin
		fd = stdin.fileno()
		new = old = termios.tcgetattr(fd)
		new[3] &= ~termios.ICANON
		new[3] &= ~termios.ECHO
		termios.tcsetattr(fd, termios.TCSAFLUSH, new)
		tty.setraw(fd)
		
		curses.filter()
		stdscr = curses.initscr()
		stdscr.addstr("normal-")
		stdscr.addstr("Hello world!", curses.A_REVERSE)
		stdscr.addstr("-normal")
		stdscr.refresh()
		curses.endwin()
		print
		# curses.filter()
		# curses.curs_set(0)
	except:
		termios.tcsetattr(fd, termios.TCSAFLUSH, old)
		print("There was an error setting the terminal settings"
		+ ", resetting base terminal settings")
		sys.exit(0)
	finally:
		return old, fd
