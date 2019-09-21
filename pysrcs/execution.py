"""Module for the execution of the commands"""

import subprocess
import os
import logging
import threading
import time

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
	i = 0
	while i < len(programList):
		l = programList[i].autorestart
		if l != "never":
			if l == "unexpected" and isinstance(programList[i].exitcodes, list) == True:
				codes = programList[i].exitcodes
				j = 0
				while j < len(programList[i].pidList):
					if programList[i].pidList[j][1] == "Finished" or programList[i].pidList[j][1] == "Stopped" or programList[i].pidList[j][1] == "Stopping":
						if int(programList[i].pidList[j][2]) not in codes:
							# program.pidList = []
							envcopy = os.environ.copy()
							if programList[i].env != "None" and isinstance(programList[i].env, list):
								for envitem in programList[i].env:
									l = envitem.split('=', 2)
									envcopy[l[0]] = l[1]
							if (isinstance(programList[i].stdout, str)
								and programList[i].stdout != "None" and programList[i].stdout != "discard"):
									if programList[i].workingdir != "None":
										outpath = programList[i].workingdir + programList[i].stdout
									else:
										outpath = programList[i].stdout
							else:
								outpath = "/dev/null"
							if (isinstance(programList[i].stderr, str)
								and programList[i].stderr != "None" and programList[i].stderr != "discard"):
									if programList[i].workingdir != "None":
										errpath = programList[i].workingdir + programList[i].stderr
									else:
										errpath = programList[i].stderr
							else:
								errpath = "/dev/null"
							cmdList = programList[i].cmd.split()
							programList[i].started = True
							if programList[i].starttime > 0:
								programList[i].state = "Starting"
							else:
								programList[i].state = "Running"
							# instances = program.cmdammount
							# while instances > 0:
							alarm = 0
							retries = programList[i].restartretries
							while retries > 0:
								try:
									with open(outpath, "wb", 0) as out, open(errpath, "wb", 0) as err:
										proc = subprocess.Popen(cmdList, stdout=out, stderr=err, env=envcopy, preexec_fn=execution.initchildproc(programList[i]))
										break
								except:
									if retries > 0:
										print("Could not run the subprocess for", programList[i].name, end='')
										print(f". retries left: {retries}")
										retries -= 1
										if retries == 0:
											alarm = 1
											print("Could not run the subprocess for", programList[i].name,
											"skipping this execution")
										continue
							if alarm == 1:
								continue
							if programList[i].starttime > 0:
								programList[i].pidList[j] = ([proc, "Starting", None])
								timer = threading.Timer(programList[i].starttime, processes.start_time, [proc])
								timer.daemon = True
								timer.start()
							else:
								programList[i].pidList[j] = ([proc, "Running", None])
					j += 1		# instances -= 1
			elif l == "always":
				j = 0
				while j < len(programList[i].pidList):
					if programList[i].pidList[j][1] == "Finished" or programList[i].pidList[j][1] == "Stopped" or programList[i].pidList[j][1] == "Stopping":
						# program.pidList = []
						envcopy = os.environ.copy()
						if programList[i].env != "None" and isinstance(programList[i].env, list):
							for envitem in programList[i].env:
								l = envitem.split('=', 2)
								envcopy[l[0]] = l[1]
						if (isinstance(programList[i].stdout, str)
							and programList[i].stdout != "None" and programList[i].stdout != "discard"):
								if programList[i].workingdir != "None":
									outpath = programList[i].workingdir + programList[i].stdout
								else:
									outpath = programList[i].stdout
						else:
							outpath = "/dev/null"
						if (isinstance(programList[i].stderr, str)
							and programList[i].stderr != "None" and programList[i].stderr != "discard"):
								if programList[i].workingdir != "None":
									errpath = programList[i].workingdir + programList[i].stderr
								else:
									errpath = programList[i].stderr
						else:
							errpath = "/dev/null"
						programList[i].started = True
						if programList[i].starttime > 0:
							programList[i].state = "Starting"
						else:
							programList[i].state = "Running"
						cmdList = programList[i].cmd.split()
						# instances = program.cmdammount
						# while instances > 0:
						alarm = 0
						retries = programList[i].restartretries
						while retries > 0:
							try:
								with open(outpath, "wb", 0) as out, open(errpath, "wb", 0) as err:
									proc = subprocess.Popen(cmdList, stdout=out, stderr=err, env=envcopy, preexec_fn=execution.initchildproc(programList[i]))
									break
							except:
								if retries > 0:
									print("Could not run the subprocess for", programList[i].name, end='')
									print(f". retries left: {retries}")
									retries -= 1
									if retries == 0:
										alarm = 1
										print("Could not run the subprocess for", programList[i].name,
										"skipping this execution")
									continue
						if alarm == 1:
							continue
						if programList[i].starttime > 0:
							programList[i].pidList[j] = ([proc, "Starting", None])
							timer = threading.Timer(programList[i].starttime, processes.start_time, [proc])
							timer.daemon = True
							timer.start()
						else:
							programList[i].pidList[j] = ([proc, "Running", None])

						# instances -= 1
						# break
					j += 1
		i += 1

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
				# print("1")
				program.state = "Stopped"
			if stoppingCount == len(program.pidList):
				# print("2")
				program.state = "Stopping"
			if finishedCount == len(program.pidList):
				# print("3")
				program.state = "Finished"
			if startingCount == len(program.pidList):
				# print("4")
				program.state == "Starting"
			if runningCount > 0:
				# print("5")
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
					alarm = 0
					retries = program.restartretries
					while retries > 0:
						try:
							with open(outpath, "wb", 0) as out, open(errpath, "wb", 0) as err:
								proc = subprocess.Popen(cmdList, stdout=out, stderr=err, env=envcopy, preexec_fn=initchildproc(program))
								break
						except:
							if retries > 0:
								print("Could not run the subprocess for", program.name, end='')
								print(f". retries left: {retries}")
								retries -= 1
								if retries == 0:
									alarm = 1
									print("Could not run the subprocess for", program.name,
									"skipping this execution")
								continue
					if alarm == 1:
						break
					if program.starttime > 0:
						program.pidList.append([proc, "Starting", None])
						timer = threading.Timer(program.starttime, processes.start_time, [proc])
						timer.daemon = True
						timer.start()
					else:
						program.pidList.append([proc, "Running", None])
					instances -= 1
				if program.starttime > 0:
					program.state = "Starting"
				else:
					program.state = "Running"
