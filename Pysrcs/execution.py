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
					status = pid[0].poll()
					if status != None:
						pid[1] = "Finished"
						status = str(status)
						if status[0] == '-':
							pid[1] = "Killed"
							status = status[1]
						pid[2] = status
		if program.state == "Started":
			runningCount = 0
			finishedCount = 0
			stoppedCount = 0
			killedCount = 0
			for pid in program.pidList:
				if pid[1] == "Finished":
					finishedCount += 1
				elif pid[1] == "Killed":
					killedCount += 1
				elif pid[1] == "Running":
					runningCount += 1
				elif pid[1] == "Stopped":
					stoppedCount += 1
			if runningCount == 0 and stoppedCount == 0:
				program.state = "Finished"
			elif stoppedCount == len(program.pidList):
				program.state = "Stopped"

def load_or_reload(programList, prevprogramList):
	"""this function loads the first batch of programs, or reloads new ones"""
	def initchildproc(program):
		"""this function modifies a popen process"""
		os.setpgrp()
		os.umask(program.umask)

	if prevprogramList == None:
		for program in programList:
			if program.autostart == True:
				program.started = True
				cmdList = program.cmd.split()
				instances = program.cmdammount
				while instances > 0:
					try:
						with open("/dev/null", "wb", 0) as out:
							proc = subprocess.Popen(cmdList, stdout=out, shell=False, preexec_fn=initchildproc(program))
					except OSError:
						print("Could not run the subprocess for", program.name,
						"skipping this execution")
						break
					program.pidList.append([proc, "Running", None])
					instances -= 1
				program.state = "Started"
	# ACABAR LA FUNCION CUANDO PREVPROGRAMLIST EXISTE
