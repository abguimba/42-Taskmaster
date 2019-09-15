#!/usr/bin/env python3

"""Main module for this taskmaster project"""
import errors
import tools
import classes
import userinput
import output
import time
import signals
import menuloop
import execution
import logging

import subprocess


def main():
	"""main function"""
	try:
		logging.basicConfig(filename='taskmaster.log',
							level=logging.DEBUG,
							filemode='w',
							format='%(asctime)s %(levelname)s\t%(message)s')
	except Exception as error_log:
		userinput.ask_for_confirmation(None, None, error_log)
	errors.error_check_params()
	signals.set_signal_handlers_taskmaster()
	output.display_progress()
	start = time.time()
	configList = tools.parse_json_file()
	tools.verify_config(0, configList)
	programList = classes.init_classes(configList)
	end = time.time()
	userinput.ask_for_confirmation(programList,
									str(end - start),
									None)
	execution.load_or_reload(programList, None)
	menuloop.setuploop(programList, configList)


if __name__ == '__main__':
	main()
