"""Module with all the functions to handle (start/restart/stop)processes"""

import subprocess
import execution
import os
import signal
import time

def stop_program(programList):
	"""this function stops a program with the desired signal"""
	for program in programList:
		if program.selected == 1:
			if (program.state != "Stopped" and program.state != "Finished"
				and program.state != "Killed" and program.state != "Not started"):
				if program.quitsig == "TERM":
					s = signal.SIGTERM
				elif program.quitsig == "QUIT":
					s = signal.SIGQUIT
				elif program.quitsig == "INT":
					s = signal.SIGINT
				elif program.quitsig == "KILL":
					s = signal.SIGKILL
				elif program.quitsig == "TSTP":
					s = signal.SIGTSTP
				elif program.quitsig == "STOP":
					s = signal.SIGSTOP
				elif program.quitsig == "HUP":
					s = signal.SIGHUP
				for pid in program.pidList:
					os.kill(pid[0].pid, s)
				execution.update_program_status(programList)
				return 0
			else:
				return 2

def restart_program(programList):
	"""this function restarts a program"""
	for program in programList:
		if program.selected == 1:
			for pid in program.pidList:
				if pid[1] != "Finished":
					os.kill(pid[0].pid, signal.SIGKILL)
			program.state = "Not started"
			program.started = False
			program.pidList = []	
	return start_program(programList)

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
					outpath = program.stdout
				else:
					outpath = "/dev/null"
				if (isinstance(program.stderr, str)
					and program.stderr != "None" and program.stderr != "discard"):
					errpath = program.stderr
				else:
					errpath = "/dev/null"
				program.started = True
				cmdList = program.cmd.split()
				instances = program.cmdammount
				while instances > 0:
					try:
						with open(outpath, "wb", 0) as out, open(errpath, "wb", 0) as err:
							proc = subprocess.Popen(cmdList, stdout=out, stderr=err, env=envcopy, preexec_fn=execution.initchildproc(program))
					except:
						print("Could not run the subprocess for", program.name,
						"skipping this execution")
						break
					program.pidList.append([proc, "Running", None])
					instances -= 1
				program.state = "Started"
				return 0
			else:
				return 1

def	handle_program(programList, menustate):
	"""this function handles start/stop/restart of programs"""
	if menustate == "startselect":
		return start_program(programList)
	elif menustate == "restartselect":
		return restart_program(programList)
	elif menustate == "stopselect":
		return stop_program(programList)
