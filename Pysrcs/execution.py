"""Module for the executioon of the commands"""

import subprocess
import os

import errors
import term_setup
import signals

def update_program_status(programList):
	"""updates every instance's status"""
	for program in programList:
		if program.state != "Finished":
			for pid in program.pidList:
				if pid[1] != "Finished":
					status = os.waitpid(pid[0], os.WNOHANG | os.WCONTINUED | os.WUNTRACED)
					if status != (0, 0):
						if os.WIFEXITED(status[1]) == True:
							pid[1] = "Finished"
							pid[2] = os.WEXITSTATUS(status[1])
		if program.state == "Started":
			runningCount = 0
			finishedCount = 0
			stoppedCount = 0
			for pid in program.pidList:
				if pid[1] == "Finished":
					finishedCount += 1
				elif pid[1] == "Running":
					runningCount += 1
				elif pid[1] == "Stopped":
					stoppedCount += 1
			if finishedCount == len(program.pidList):
				program.state = "Finished"
			elif stoppedCount == len(program.pidList):
				program.state = "Stopped"

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
					program.pidList.append([proc.pid, "Running", None])
					instances -= 1
				program.state = "Started"
