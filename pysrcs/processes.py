"""Module with all the functions to handle (start/restart/stop)processes"""

import subprocess
import execution
import os
import signal
import time
import threading

import output
import menuloop

startingList = []
stoppingList = []

def stop_time():
	global stoppingList
	name = stoppingList[0]
	for program in menuloop.globProgramList:
		if name == program.name and program.state == "Stopping":
			for pid in program.pidList:
				if pid[1] == "Stopping":
					pid[1] = "Stopped"
			program.state = "Stopped"
	stoppingList.pop(0)

def start_time():
	global startingList
	name = startingList[0]
	for program in menuloop.globProgramList:
		if name == program.name and program.state == "Starting":
			for pid in program.pidList:
				if pid[1] == "Starting":
					pid[1] = "Running"
			program.state = "Running"
	startingList.pop(0)

def stop_program(programList):
	"""this function stops a program with the desired signal"""
	global stoppingList
	for program in programList:
		if program.selected == 1:
			if (program.state == "Running" or program.state == "Starting"):
				if program.quitsig == "TERM":
					s = signal.SIGTERM
				elif program.quitsig == "QUIT":
					s = signal.SIGQUIT
				elif program.quitsig == "INT":
					s = signal.SIGINT
				elif program.quitsig == "KILL":
					s = signal.SIGKILL
				# elif program.quitsig == "TSTP":
				# 	s = signal.SIGTSTP
				# elif program.quitsig == "STOP":
				# 	s = signal.SIGSTOP
				for pid in program.pidList:
					if pid[1] != "Stopped" and pid[1] != "Finished" and pid[1] != "Stopping":
							os.kill(pid[0].pid, s)
							pid[1] = "Stopping"
				program.state = "Stopping"
				timer = threading.Timer(program.stoptime, stop_time)
				stoppingList.append(program.name)
				timer.start()
			else:
				print(output.bcolors.FAIL + "Program " + program.name + " was already stopped/finished/killed or hadn't started!" + output.bcolors.ENDC)
	return 0

def restart_program(programList):
	"""this function restarts a program"""
	global startingList
	for program in programList:
		if program.selected == 1:
			for pid in program.pidList:
				if pid[1] != "Stopped" and pid[1] != "Finished" and pid[1] != "Stopping":
					os.kill(pid[0].pid, signal.SIGKILL)
			program.state = "Not started"
			program.started = False
			program.pidList = []
			if program.autostart == 1:
				program.state = "Starting"
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
						except:
							print("Could not run the subprocess for", program.name,
							"skipping this execution")
							break
						program.pidList.append([proc, "Starting", None])
						instances -= 1
					program.state = "Starting"
					timer = threading.Timer(program.starttime, start_time)
					startingList.append(program.name)
					timer.start()
	return programList

def start_program(programList):
	"""this function starts programs that hadn't been started previously"""
	global startingList
	for program in programList:
		if program.selected == 1:
			if program.state == "Not started":
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
				cmdList = program.cmd.split()
				instances = program.cmdammount
				while instances > 0:
					try:
						with open(outpath, "wb", 0) as out, open(errpath, "wb", 0) as err:
							proc = subprocess.Popen(cmdList, stdout=out, 
													stderr=err, 
													env=envcopy,
													preexec_fn=execution.initchildproc(program))	
					except:
						print("Could not run the subprocess for", program.name,
						"skipping this execution")
						break
					program.pidList.append([proc, "Starting", None])
					instances -= 1
				program.state = "Starting"
				timer = threading.Timer(program.starttime, start_time)
				startingList.append(program.name)
				timer.start()
			else:
				print(output.bcolors.FAIL + "Program " + program.name + " was already started/stopped!" + output.bcolors.ENDC)
	return 0

def	handle_program(programList, menustate):
	"""this function handles start/stop/restart of programs"""
	if menustate == "startselect":
		return start_program(programList)
	elif menustate == "restartselect":
		return restart_program(programList)
	elif menustate == "stopselect":
		return stop_program(programList)
