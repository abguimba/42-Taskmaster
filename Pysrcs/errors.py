"""General error output and handling file"""
import sys
import output

def error_execution(str):
	print(output.bcolors.FAIL + "There was an error starting command:", str,
	", not executing any instance of this command", output.bcolors.ENDC)

def error_reload_config():
	print(output.bcolors.FAIL + "There was an error reloading the config file" +
	", staying on old config", output.bcolors.ENDC)

def error_ammount_cmds(mode, str):
	"""error for when a command has less than 1 instance in config file"""
	print('\n' + "taskmaster : ", end='')
	print("command -> " + str + " has less than one desired instance"
	+ "in the config file")
	if mode == 0:
		exit(1)
	return 1

def error_config(mode, command, param):
	"""Base error function for config file errors"""
	print('\n' + "taskmaster : ", end='')
	print("command -> ", end='')
	print(command, end=' ')
	print("has ", end='')
	print(param, end=' ')
	print("not set correctly in the config file")
	if mode == 0:
		exit(1)
	return (1)

def error_yaml(exc):
	"""error function for when yaml file doesn't load"""
	print('\n' + "taskmaster : ", end='')
	print(exc)
	print("bad formatting or error loading yaml file")
	exit(1)

def error_repeated_names(mode):
	"""error function for when there's repeated program names"""
	print('\n' + "taskmaster : ", end='')
	print("Repeated command names!")
	if mode == 0:
		exit(1)
	return (1)

def error_instances(mode):
	"""error function for when the yaml file contains too many instances"""
	print('\n' + "taskmaster : ", end='')
	print("Too many instances of some program in config file (fork bomb)")
	if mode == 0:
		exit(1)
	return (1)

def error_config_len(mode):
	"""error function for when the yaml file doesn't contain all the fields"""
	print('\n' + "taskmaster : ", end='')
	print("Not all parameters are present in the config file!")
	if mode == 0:
		exit(1)
	return (1)

def error_check_params():
	"""Initial error checking"""
	if len(sys.argv) != 2:
		print("taskmaster : ", end='')
		print("usage: main.py config_file")
		exit(1)
