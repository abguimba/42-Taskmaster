"""Module for the execution of the commands"""

import subprocess
import os
import logging
import threading
import time
import sys

import processes
import errors
import term_setup
import signals
import execution
import tools

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
							if programList[i].env == "None" or programList[i].env == "default":
								envcopy = None
							else:
								envcopy = os.environ.copy()
								if programList[i].env != "default" and isinstance(programList[i].env, list):
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
								outpath = os.devnull
							if (isinstance(programList[i].stderr, str)
								and programList[i].stderr != "None" and programList[i].stderr != "discard"):
									if programList[i].workingdir != "None":
										errpath = programList[i].workingdir + programList[i].stderr
									else:
										errpath = programList[i].stderr
							else:
								errpath = os.devnull
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
							if programList[i].workingdir != "None" and isinstance(programList[i].workingdir, str):
								workingdir = os.chdir(programList[i].workingdir)
							else:
								workingdir = os.chdir(os.getcwd())
							if isinstance(programList[i].umask, int):
								umaskSave = os.umask(programList[i].umask)
							while retries > 0:
								try:
									with open(outpath, "wb", 0) as out, open(errpath, "wb", 0) as err:
										proc = subprocess.Popen(cmdList, stdout=out, stderr=err, cwd=workingdir, env=envcopy, start_new_session=True)
										break
								except:
									if retries > 0:
										print("Could not run the subprocess for", programList[i].name, end='')
										print(f". retries left: {retries}")
										retries -= 1
										if retries == 0:
											if isinstance(programList[i].umask, int):
												os.umask(umaskSave)
											alarm = 1
											print("Could not run the subprocess for", programList[i].name,
											"skipping this execution")
										continue
							if alarm == 1:
								continue
							if isinstance(programList[i].umask, int):
								os.umask(umaskSave)
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
						if programList[i].env == "None" or programList[i].env == "default":
								envcopy = None
						else:
							envcopy = os.environ.copy()
							if programList[i].env != "default" and isinstance(programList[i].env, list):
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
							outpath = os.devnull
						if (isinstance(programList[i].stderr, str)
							and programList[i].stderr != "None" and programList[i].stderr != "discard"):
								if programList[i].workingdir != "None":
									errpath = programList[i].workingdir + programList[i].stderr
								else:
									errpath = programList[i].stderr
						else:
							errpath = os.devnull
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
						if programList[i].workingdir != "None" and isinstance(programList[i].workingdir, str):
							workingdir = os.chdir(programList[i].workingdir)
						else:
							workingdir = os.chdir(os.getcwd())
						if isinstance(programList[i].umask, int):
							umaskSave = os.umask(programList[i].umask)
						while retries > 0:
							try:
								with open(outpath, "wb", 0) as out, open(errpath, "wb", 0) as err:
									proc = subprocess.Popen(cmdList, stdout=out, stderr=err, cwd=workingdir, env=envcopy, start_new_session=True)
									break
							except:
								if retries > 0:
									print("Could not run the subprocess for", programList[i].name, end='')
									print(f". retries left: {retries}")
									retries -= 1
									if retries == 0:
										if isinstance(programList[i].umask, int):
											os.umask(umaskSave)
										alarm = 1
										print("Could not run the subprocess for", programList[i].name,
										"skipping this execution")
									continue
						if alarm == 1:
							continue
						if isinstance(programList[i].umask, int):
							os.umask(umaskSave)
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

def load_or_reload(programList, prevProgramList):
	"""this function loads the first batch of programs, or reloads new ones"""

	if prevProgramList == None:
		logging.info(f'There is no previous program list.')
		for program in programList:
			logging.info(f'Configuring instance for \"{program.name}\"')
			logging.info(f'Creating environment.')
			if program.env == "None" or program.env == "default":
				envcopy = None
			else:
				envcopy = os.environ.copy()
				if program.env != "default" and isinstance(program.env, list):
					for envitem in program.env:
						l = envitem.split('=', 2)
						envcopy[l[0]] = l[1]
					logging.info(f'\t{l[0]} = {envcopy[l[0]]}')
				logging.info(f'Environment created succesfully.')
			logging.info('Selecting standard outputs.')	
			if (isinstance(program.stdout, str)
				and program.stdout != "None" and program.stdout != "discard"):
					if program.workingdir != "None":
						outpath = program.workingdir + program.stdout
					else:
						outpath = program.stdout
			else:
				outpath = os.devnull
			if (isinstance(program.stderr, str)
				and program.stderr != "None" and program.stderr != "discard"):
					if program.workingdir != "None":
						errpath = program.workingdir + program.stderr
					else:
						errpath = program.stderr
			else:
				errpath = os.devnull
			logging.info(f'Selected standard outputs in:\n\t\t\t\t\tSTDOUT: {outpath}\n\t\t\t\t\tSTDERR: {errpath}')	
			if program.autostart == True:
				program.started = True
				cmdList = program.cmd.split()
				instances = program.cmdammount
				logging.info(f'Starting {instances} instances')
				if program.workingdir != "None" and isinstance(program.workingdir, str):
					workingdir = os.chdir(program.workingdir)
				else:
					workingdir = os.chdir(os.getcwd())
				if isinstance(program.umask, int):
					umaskSave = os.umask(program.umask)
				while instances > 0:
					alarm = 0
					retries = program.restartretries
					while retries > 0:
						try:
							with open(outpath, "wb", 0) as out, open(errpath, "wb", 0) as err:
								proc = subprocess.Popen(cmdList, stdout=out, stderr=err, cwd=workingdir, env=envcopy, start_new_session=True)
								break
						except:
							if retries > 0:
								print("Could not run the subprocess for", program.name, end='')
								print(f". retries left: {retries}")
								retries -= 1
								if retries == 0:
									if isinstance(program.umask, int):
										os.umask(umaskSave)
									alarm = 1
									print("Could not run the subprocess for", program.name,
									"skipping this execution")
								continue
					if alarm == 1:
						break
					if isinstance(program.umask, int):
						os.umask(umaskSave)
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
	else:
		restartList = list()
		for prevProgram in prevProgramList:
			if prevProgram.name not in [newProgram.name for newProgram in programList]:
				tools.kill_job(prevProgram)
				prevProgramList.remove(prevProgram)
		for newProgram in programList:
			if newProgram.name in [prevProgram.name for prevProgram in prevProgramList]:
				for program in prevProgramList:
					if program.name == newProgram.name:
						if program.cmd != newProgram.cmd:
							restartList.append(1)
							break
						elif program.cmdammount != newProgram.cmdammount:
							restartList.append(2)
							newProgram.pidList = program.pidList
							newProgram.started = program.started
							newProgram.state = program.state
							newProgram.selected = program.selected
						else:
							restartList.append(3)
							newProgram.pidList = program.pidList
							newProgram.started = program.started
							newProgram.state = program.state
							newProgram.selected = program.selected
			else:
				restartList.append(0)
		i = 0
		print(restartList)
		while i < len(restartList):
			if restartList[i] == 0 or restartList[i] == 1:
				logging.info(f'Configuring instance for \"{programList[i].name}\"')
				logging.info(f'Creating environment.')
				if programList[i].env == "None" or programList[i].env == "default":
					envcopy = None
				else:
					envcopy = os.environ.copy()
					if programList[i].env != "default" and isinstance(programList[i].env, list):
						for envitem in programList[i].env:
							l = envitem.split('=', 2)
							envcopy[l[0]] = l[1]
						logging.info(f'\t{l[0]} = {envcopy[l[0]]}')
					logging.info(f'Environment created succesfully.')
				logging.info('Selecting standard outputs.')	
				if (isinstance(programList[i].stdout, str)
					and programList[i].stdout != "None" and programList[i].stdout != "discard"):
						if programList[i].workingdir != "None":
							outpath = programList[i].workingdir + programList[i].stdout
						else:
							outpath = programList[i].stdout
				else:
					outpath = os.devnull
				if (isinstance(programList[i].stderr, str)
					and programList[i].stderr != "None" and programList[i].stderr != "discard"):
						if programList[i].workingdir != "None":
							errpath = programList[i].workingdir + programList[i].stderr
						else:
							errpath = programList[i].stderr
				else:
					errpath = os.devnull
				logging.info(f'Selected standard outputs in:\n\t\t\t\t\tSTDOUT: {outpath}\n\t\t\t\t\tSTDERR: {errpath}')	
				if programList[i].autostart == True:
					programList[i].started = True
					cmdList = programList[i].cmd.split()
					instances = programList[i].cmdammount
					logging.info(f'Starting {instances} instances')
					if programList[i].workingdir != "None" and isinstance(programList[i].workingdir, str):
						workingdir = os.chdir(programList[i].workingdir)
					else:
						workingdir = os.chdir(os.getcwd())
					if isinstance(programList[i].umask, int):
						umaskSave = os.umask(programList[i].umask)
					while instances > 0:
						alarm = 0
						retries = programList[i].restartretries
						while retries > 0:
							try:
								with open(outpath, "wb", 0) as out, open(errpath, "wb", 0) as err:
									proc = subprocess.Popen(cmdList, stdout=out, stderr=err, cwd=workingdir, env=envcopy, start_new_session=True)
									break
							except:
								if retries > 0:
									print("Could not run the subprocess for", programList[i].name, end='')
									print(f". retries left: {retries}")
									retries -= 1
									if retries == 0:
										if isinstance(programList.umask, int):
											os.umask(umaskSave)
										alarm = 1
										print("Could not run the subprocess for", programList.name,
										"skipping this execution")
									continue
						if alarm == 1:
							break
						if isinstance(programList.umask, int):
							os.umask(umaskSave)
						if programList.starttime > 0:
							programList.pidList.append([proc, "Starting", None])
							timer = threading.Timer(programList.starttime, processes.start_time, [proc])
							timer.daemon = True
							timer.start()
						else:
							programList.pidList.append([proc, "Running", None])
						instances -= 1
					if programList.starttime > 0:
						programList.state = "Starting"
					else:
						programList.state = "Running"
			elif restartList[i] == 2:
				if programList.cmdammount < len(programList.pidList):
					tools.delete_instances(newProgram, len(programList.pidList) - programList.cmdammount)
				else:
					realinstances = newProgram.cmdammount - len(programList.pidList)
					logging.info(f'Configuring instance for \"{programList.name}\"')
					logging.info(f'Creating environment.')
					if programList.env == "None" or programList.env == "default":
						envcopy = None
					else:
						envcopy = os.environ.copy()
						if programList.env != "default" and isinstance(programList.env, list):
							for envitem in programList.env:
								l = envitem.split('=', 2)
								envcopy[l[0]] = l[1]
							logging.info(f'\t{l[0]} = {envcopy[l[0]]}')
						logging.info(f'Environment created succesfully.')
					logging.info('Selecting standard outputs.')	
					if (isinstance(programList.stdout, str)
						and programList.stdout != "None" and programList.stdout != "discard"):
							if programList.workingdir != "None":
								outpath = programList.workingdir + programList.stdout
							else:
								outpath = programList.stdout
					else:
						outpath = os.devnull
					if (isinstance(programList.stderr, str)
						and programList.stderr != "None" and programList.stderr != "discard"):
							if programList.workingdir != "None":
								errpath = programList.workingdir + programList.stderr
							else:
								errpath = programList.stderr
					else:
						errpath = os.devnull
					logging.info(f'Selected standard outputs in:\n\t\t\t\t\tSTDOUT: {outpath}\n\t\t\t\t\tSTDERR: {errpath}')	
					if programList.autostart == True:
						programList.started = True
						cmdList = programList.cmd.split()
						instances = realinstances
						logging.info(f'Starting {instances} instances')
						if programList.workingdir != "None" and isinstance(programList.workingdir, str):
							workingdir = os.chdir(programList.workingdir)
						else:
							workingdir = os.chdir(os.getcwd())
						if isinstance(programList.umask, int):
							umaskSave = os.umask(programList.umask)
						while instances > 0:
							alarm = 0
							retries = programList.restartretries
							while retries > 0:
								try:
									with open(outpath, "wb", 0) as out, open(errpath, "wb", 0) as err:
										proc = subprocess.Popen(cmdList, stdout=out, stderr=err, cwd=workingdir, env=envcopy, start_new_session=True)
										break
								except:
									if retries > 0:
										print("Could not run the subprocess for", programList.name, end='')
										print(f". retries left: {retries}")
										retries -= 1
										if retries == 0:
											if isinstance(programList.umask, int):
												os.umask(umaskSave)
											alarm = 1
											print("Could not run the subprocess for", programList.name,
											"skipping this execution")
										continue
							if alarm == 1:
								break
							if isinstance(programList.umask, int):
								os.umask(umaskSave)
							if programList.starttime > 0:
								programList.pidList.append([proc, "Starting", None])
								timer = threading.Timer(programList.starttime, processes.start_time, [proc])
								timer.daemon = True
								timer.start()
							else:
								programList.pidList.append([proc, "Running", None])
							instances -= 1
						if programList.starttime > 0:
							programList.state = "Starting"
						else:
							programList.state = "Running"
			i += 1
