"""Module for the execution of the commands"""

import subprocess
import os

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
				for code in codes:
					for pid in program.pidList:
						if pid[1] == "Killed" or pid[1] == "Finished":
							if int(pid[2]) == code:
								program.pidList = []
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
								break
			elif l == "always":
				for pid in program.pidList:
					if pid[1] == "Killed" or pid[1] == "Finished":
						program.pidList = []
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
						break
				

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
							status = status[1:]
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
				outpath = program.stdout
			else:
				outpath = "/dev/null"
			if (isinstance(program.stderr, str)
				and program.stderr != "None" and program.stderr != "discard"):
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
					program.pidList.append([proc, "Running", None])
					instances -= 1
				program.state = "Started"
	# ACABAR LA FUNCION CUANDO PREVPROGRAMLIST EXISTE
