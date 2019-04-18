"""File for general tooling"""
import sys
import yaml

import errors

def verify_config(configList):
	"""Verifies that the parsed yaml file doesn't contain any errors and has all required parameters"""
	for config in configList:
		if len(config) != 15:
			errors.error_config_len()
		if config[2] < 1:
			errors.error_ammount_cmds(config[0])
		if config[3] != True and config[3] != False:
			errors.error_config(config[0], "autostart")
		if config[4] != "never" and config[4] != "always" and config[4] != "unexpected":
			errors.error_config(config[0], autorestart)
		if config[5] < 0 or config[6] < 0 or config[7] < 0:
			errors.error_config(config[0], "starttime/stoptime/startretries")
		if config[8] != "TERM" and config[8] != "QUIT" and config[8] != "INT" and config[8] != "KILL":
			errors.error_config(config[0], "quitsig")

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