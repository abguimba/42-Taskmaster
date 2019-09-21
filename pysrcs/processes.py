"""Module with all the functions to handle (start/restart/stop)processes"""

import subprocess
import execution
import os
import signal
import time
import threading
import sys

import output
import menuloop

def stop_time(saved_pid):
	for program in menuloop.globProgramList:
		for pid in program.pidList:
			if saved_pid == pid[0]:
				if pid[1] == "Stopping":
						pid[1] = "Stopped"

def start_time(saved_pid):
	for program in menuloop.globProgramList:
		for pid in program.pidList:
			if saved_pid == pid[0]:
				if pid[1] == "Starting":
						pid[1] = "Running"

def stop_program(programList):
	"""this function stops a program with the desired signal"""
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
							if program.stoptime > 0:
								pid[1] = "Stopping"
								timer = threading.Timer(program.stoptime, stop_time, [pid[0]])
								timer.daemon = True
								timer.start()
							else:
								pid[1] = "Stopped"
				if program.stoptime > 0:
					program.state = "Stopping"
				else:
					program.state = "Stopped"
			else:
				print(output.bcolors.FAIL + "Program " + program.name + " was already stopped/finished/killed or hadn't started!" + output.bcolors.ENDC)
	return 0

def restart_program(programList):
	"""this function restarts a program"""
	for program in programList:
		if program.selected == 1:
			if program.state != "Not started":
				for pid in program.pidList:
					if pid[1] != "Stopped" and pid[1] != "Finished" and pid[1] != "Stopping":
						os.kill(pid[0].pid, signal.SIGKILL)
				program.pidList = []
				program.started = True
				if program.starttime > 0:
					program.state = "Starting"
				else:
					program.state = "Running"
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
				instances = program.cmdammount
				while instances > 0:
					alarm = 0
					retries = program.restartretries
					while retries > 0:
						try:
							with open(outpath, "wb", 0) as out, open(errpath, "wb", 0) as err:
								proc = subprocess.Popen(cmdList, stdout=out, stderr=err, env=envcopy, preexec_fn=execution.initchildproc(program))
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
						timer = threading.Timer(program.starttime, start_time, [proc])
						timer.daemon = True
						timer.start()
					else:
						program.pidList.append([proc, "Running", None])
					instances -= 1
			else:
				print(f"The program: {program.name} had never been started, so restarting is not possible!", file=sys.stderr)
	return programList

def start_program(programList):
	"""this function starts programs that hadn't been started previously"""
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
					alarm = 0
					retries = program.restartretries
					while retries:
						try:
							with open(outpath, "wb", 0) as out, open(errpath, "wb", 0) as err:
								proc = subprocess.Popen(cmdList, stdout=out, 
														stderr=err, 
														env=envcopy,
														preexec_fn=execution.initchildproc(program))
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
						timer = threading.Timer(program.starttime, start_time, [proc])
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
