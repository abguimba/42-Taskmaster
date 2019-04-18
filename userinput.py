import output
import sys

def ask_for_confirmation(classList, time):
	output.display_summary(classList, time)
	confirmation = sys.stdin.read(1)
	if confirmation == 'n':
		print(output.bcolors.FAIL, "\n/!\\Aborting execution /!\\", output.bcolors.ENDC)
		exit(0)
