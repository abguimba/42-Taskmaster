"""General error output and handling file"""
import sys

def error_ammount_cmds(str):
	"""error for when a command has less than 1 instance in config file"""
	print('\n' + "taskmaster : ", end='')
	print("command -> " + str + " has less than one desired instance"
	+ "in the config file")
	exit(1)

def error_config(command, param):
	"""Base error function for config file errors"""
	print('\n' + "taskmaster : ", end='')
	print("command -> ", end='')
	print(command, end=' ')
	print("has ", end='')
	print(param, end=' ')
	print("not set correctly in the config file")
	exit(1)

def error_yaml(exc):
	"""error function for when yaml file doesn't load"""
	print('\n' + "taskmaster : ", end='')
	print(exc)
	print("bad formatting or error loading yaml file")
	exit(1)

def error_config_len():
	"""error function for when the yaml file doesn't contain all the fields"""
	print('\n' + "taskmaster : ", end='')
	print("Not all parameters are present in the config file!")
	exit(1)

def error_check_params():
	"""Initial error checking"""
	if len(sys.argv) != 2:
		print("taskmaster : ", end='')
		print("usage: main.py config_file")
		exit(1)
