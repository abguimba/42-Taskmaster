"""Module for the execution of the commands"""

import subprocess
import os
import logging
import threading

import processes
import errors
import term_setup
import signals
import execution

def initchildproc(program):
		"""this function modifies a popen process"""
		os.setpgrp()
		if isinstance(program.umask, int):
			os.umask(program.umask)
		if program.workingdir != "None" and isinstance(program.workingdir, str):
			os.chdir(program.workingdir)
		else:
			os.chdir(os.getcwd())

def check_revive_process(programList):
	"""function to revive process on unexpected exit"""
	for program in programList:
		l = program.autorestart
		if l != "never":
			if l == "unexpected" and isinstance(program.exitcodes, list) == True:
				codes = program.exitcodes
				for pid in program.pidList:
					if pid[1] == "Finished" or pid[1] == "Stopped" or pid[1] == "Stopping":
						if int(pid[2]) not in codes:
							# program.pidList = []
							envcopy = os.environ.copy()
							if program.env != "None" and isinstance(program.env, list):
								for envitem in program.env:
									l = envitem.split('=', 2)
									envcopy[l[0]] = l[1]
							if (isinstance(program.stdout, str)
								and program.stdout != "None" and program.stdout != "discard"):
									if program.workingdir != "None":
										outpath = program.workingdir + program.stdout
									else:
										outpath = program.stdout
							else:
								outpath = "/dev/null"
							if (isinstance(program.stderr, str)
								and program.stderr != "None" and program.stderr != "discard"):
									if program.workingdir != "None":
										errpath = program.workingdir + program.stderr
									else:
										errpath = program.stderr
							else:
								errpath = "/dev/null"
							cmdList = program.cmd.split()
							program.started = True
							program.state = "Starting"
							# instances = program.cmdammount
							# while instances > 0:
							try:
								with open(outpath, "wb", 0) as out, open(errpath, "wb", 0) as err:
									proc = subprocess.Popen(cmdList, stdout=out, stderr=err, env=envcopy, preexec_fn=execution.initchildproc(program))
									timer = threading.Timer(program.starttime, processes.start_time, [proc])
									timer.start()
							except:
								print("Could not run the subprocess for", program.name,
								"skipping this execution")
								break
							pid = ([proc, "Starting", None])
							# instances -= 1
			elif l == "always":
				for pid in program.pidList:
					if pid[1] == "Finished" or pid[1] == "Stopped" or pid[1] == "Stopping":
						# program.pidList = []
						envcopy = os.environ.copy()
						if program.env != "None" and isinstance(program.env, list):
							for envitem in program.env:
								l = envitem.split('=', 2)
								envcopy[l[0]] = l[1]
						if (isinstance(program.stdout, str)
							and program.stdout != "None" and program.stdout != "discard"):
								if program.workingdir != "None":
									outpath = program.workingdir + program.stdout
								else:
									outpath = program.stdout
						else:
							outpath = "/dev/null"
						if (isinstance(program.stderr, str)
							and program.stderr != "None" and program.stderr != "discard"):
								if program.workingdir != "None":
									errpath = program.workingdir + program.stderr
								else:
									errpath = program.stderr
						else:
							errpath = "/dev/null"
						program.started = True
						program.state = "Starting"
						cmdList = program.cmd.split()
						# instances = program.cmdammount
						# while instances > 0:
						try:
							with open(outpath, "wb", 0) as out, open(errpath, "wb", 0) as err:
								proc = subprocess.Popen(cmdList, stdout=out, stderr=err, env=envcopy, preexec_fn=execution.initchildproc(program))
								timer = threading.Timer(program.starttime, processes.start_time, [proc])
								timer.start()
						except:
							print("Could not run the subprocess for", program.name,
							"skipping this execution")
							break
						pid = ([proc, "Starting", None])
						# instances -= 1
						# break

def update_program_status(programList):
	"""updates every instance's status"""
	for program in programList:
		if program.state != "Stopped" and program.state != "Finished" and program.state != "Stopping":
			for pid in program.pidList:
				if pid[1] == "Stopping":
					status = pid[0].poll()
					if status[0] == '-':
						# pid[1] = "Killed"
						status = status[1:]
					pid[2] = status
				else:
					status = pid[0].poll()
					if status != None:
						pid[1] = "Finished"
						status = str(status)
						if status[0] == '-':
							# pid[1] = "Killed"
							status = status[1:]
						pid[2] = status
		if program.state == "Running" or program.state == "Starting":
			runningCount = 0
			# finishedCount = 0
			stoppingCount = 0
			startingCount = 0
			stoppedCount = 0
			finishedCount = 0
			for pid in program.pidList:
				if pid[1] == "Stopped":
					stoppedCount += 1
				elif pid[1] == "Finished":
					finishedCount += 1
				elif pid[1] == "Running":
					runningCount += 1
				elif pid[1] == "Starting":
					startingCount += 1
				elif pid[1] == "Stopping":
					stoppingCount += 1
			if stoppedCount == len(program.pidList):
				program.state = "Stopped"
			if stoppingCount == len(program.pidList):
				program.state = "Stopping"
			if finishedCount == len(program.pidList):
				program.state = "Finished"
			if startingCount == len(program.pidList):
				program.state == "Starting"
			if runningCount > 0:
				program.state = "Running"
	check_revive_process(programList)

def load_or_reload(programList, prevprogramList):
	"""this function loads the first batch of programs, or reloads new ones"""

	if prevprogramList == None:
		for program in programList:
			envcopy = os.environ.copy()
			if program.env != "None" and isinstance(program.env, list):
				for envitem in program.env:
					l = envitem.split('=', 2)
					envcopy[l[0]] = l[1]
			if (isinstance(program.stdout, str)
				and program.stdout != "None" and program.stdout != "discard"):
					if program.workingdir != "None":
						outpath = program.workingdir + program.stdout
					else:
						outpath = program.stdout
			else:
				outpath = "/dev/null"
			if (isinstance(program.stderr, str)
				and program.stderr != "None" and program.stderr != "discard"):
					if program.workingdir != "None":
						errpath = program.workingdir + program.stderr
					else:
						errpath = program.stderr
			else:
				errpath = "/dev/null"
			if program.autostart == True:
				program.started = True
				cmdList = program.cmd.split()
				instances = program.cmdammount
				while instances > 0:
					try:
						with open(outpath, "wb", 0) as out, open(errpath, "wb", 0) as err:
							proc = subprocess.Popen(cmdList, stdout=out, stderr=err, env=envcopy, preexec_fn=initchildproc(program))
							timer = threading.Timer(program.starttime, processes.start_time, [proc])
							timer.start()
					except:
						print("Could not run the subprocess for", program.name,
						"skipping this execution")
						break
					program.pidList.append([proc, "Starting", None])
					instances -= 1
				program.state = "Starting"
	# ACABAR LA FUNCION CUANDO PREVPROGRAMLIST EXISTE
