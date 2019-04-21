"""Module for the executioon of the commands"""

import subprocess
import os

import errors
import term_setup

def load_or_reload(programList, prevprogramList):
	"""this function loads the first batch of programs, or reloads new ones"""
	if prevprogramList == None:
		for program in programList:
			cmdList = program.cmd.split()
			instances = program.cmdammount
			while instances > 0:
				try:
					pid = os.fork()
				except OSError:
					print("Could not fork, exiting")
					exit(1)
				if pid == 0:
					try:
						status = subprocess.run(cmdList)
					except OSError:
						print("Could not run the subprocess for", program.name,
						"skipping this execution")
						exit(1)
					exit(status.returncode)
				else:
					program.pidList.append(pid)
				instances -= 1