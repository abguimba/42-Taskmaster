"""Module for the executioon of the commands"""

import subprocess
import os

import errors
import term_setup
import signals

def load_or_reload(programList, prevprogramList):
	"""this function loads the first batch of programs, or reloads new ones"""
	if prevprogramList == None:
		for program in programList:
			if program.autostart == 1:
				cmdList = program.cmd.split()
				instances = program.cmdammount
				while instances > 0:
					try:
						with open("/dev/null", "wb", 0) as out:
							proc = subprocess.Popen(cmdList, stdout=out)
					except OSError:
						print("Could not run the subprocess for", program.name,
						"skipping this execution")
						break
					program.pidList.append((proc.pid, "Running"))
					instances -= 1
				program.state = "Started"
