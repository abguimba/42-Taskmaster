import sys

def error_yaml(exc):
	"""error function for when yaml file doesn't load"""
	print(exc)
	print("Error loading yaml file")
	exit(1)

def error_check_params():
	"""Initial error checking"""
	if len(sys.argv) != 2:
		print("usage: main.py config_file")
		exit(1)