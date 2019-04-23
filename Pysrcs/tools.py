"""File for general tooling"""
import sys
import yaml
import os
import signal

import errors

def kill_jobs(programList):
	for program in programList:
		if program.state != "Finished" and program.state != "Not started":
			for pid in program.pidList:
				if pid[1] != "Finished":
					os.kill(pid[0].pid, signal.SIGKILL)

def verify_config(mode, configList):
	"""Verifies that the parsed yaml file doesn't contain any errors and has
	all required parameters
	"""
	for config in configList:
		if len(config) != 15:
			return errors.error_config_len(mode)
		elif config[2] < 1:
			return errors.error_ammount_cmds(mode, config[0])
		elif config[3] != True and config[3] != False:
			return errors.error_config(mode, config[0], "autostart")
		elif (config[4] != "never" and config[4] != "always"
		and config[4] != "unexpected"):
			return errors.error_config(mode, config[0], "autorestart")
		elif config[5] < 0 or config[6] < 0 or config[7] < 0:
			return errors.error_config(mode, config[0],
			"starttime/stoptime/startretries")
		elif (isinstance(config[8], str) != True or (config[8] != "TERM" and
		config[8] != "QUIT" and config[8] != "INT" and config[8] != "KILL")):
			return errors.error_config(mode, config[0], "quitsig")

def parse_yaml_file():
	"""parses the yaml config file and returns it to the main function"""
	with open(sys.argv[1], 'r') as stream:
		try:
			configload = yaml.safe_load(stream)
			for data in configload:
				configList = []
				for program in configload[data]:
					config = []
					config.append(program)
					for param in configload[data][program]:
						config.append(configload[data][program][param])
					configList.append(config)
		except yaml.YAMLError as exc:
			errors.error_yaml(exc)
	return configList
