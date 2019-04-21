"""File for general output purposes"""

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	REV	= '\033[7m'
	UNDERLINED = '\033[4m'

def display_special_str(str, mode):
	"""Displays strings normally, underlined, or underlined + reversed"""
	if mode == 0:
		print(str, end=' ')
	elif mode == 1:
		print(bcolors.REV, str, bcolors.ENDC, end='')

def display_basic_menu(taskmaster):
	"""Displays the basic instance of the taskmaster's menu"""
	display_special_str("STATUS", taskmaster.statusselected)
	display_special_str("START", taskmaster.startselected)
	display_special_str("RESTART", taskmaster.restartselected)
	display_special_str("STOP", taskmaster.stopselected)
	display_special_str("RELOAD", taskmaster.reloadselected)
	display_special_str("EXIT", taskmaster.exitselected)

def display_summary(classList, time):
	"""Displays a summary of the config file and the programs that are about
	to be loaded
	"""
	print("took -> " + time[:-14] + " seconds")
	print("config file summary: \n")
	for instance in classList:
		print("Name:", bcolors.BOLD, instance.name, bcolors.ENDC)
		print("Cmd:", bcolors.BOLD, instance.cmd, bcolors.ENDC)
		print("Cmd ammount:", bcolors.BOLD, instance.cmdammount, bcolors.ENDC)
		print("Autostart:", bcolors.BOLD, instance.autostart, bcolors.ENDC)
		print("Autorestart:", bcolors.BOLD, instance.autorestart, bcolors.ENDC)
		print("Starttime:", bcolors.BOLD, instance.starttime, bcolors.ENDC)
		print("Stoptime:", bcolors.BOLD, instance.stoptime, bcolors.ENDC)
		print("Restartretries:", bcolors.BOLD, instance.restartretries,
		bcolors.ENDC)
		print("Quitsig:", bcolors.BOLD, instance.quitsig, bcolors.ENDC)
		print("Exitcodes:", bcolors.BOLD, instance.exitcodes, bcolors.ENDC)
		print("Workingdir:", bcolors.BOLD, instance.workingdir, bcolors.ENDC)
		print("Umask:", bcolors.BOLD, instance.umask, bcolors.ENDC)
		print("Stdout:", bcolors.BOLD, instance.stdout, bcolors.ENDC)
		print("Stderr:", bcolors.BOLD, instance.stderr, bcolors.ENDC)
		print("env:", bcolors.BOLD, instance.env, bcolors.ENDC)
		print('\n')
	print("#####################################################")
	print(bcolors.HEADER + "Would you really like to load this configuration"
	+ "? y/n" + bcolors.ENDC)
	print("#####################################################")

def display_progress():
	"""Displays a little progress message"""
	print(bcolors.OKGREEN + "Processing config..." + bcolors.ENDC, end=' ')
