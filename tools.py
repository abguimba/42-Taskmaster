"""File for general tooling"""

import sys
import yaml

import errors

def verify_config(configList):
	"""Verifies if the parsed yaml file doesn't contain any errors and has all required parameters"""
	for config in configList:
		if len(config) != 15:
			errors.config_len()
		//to finish

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