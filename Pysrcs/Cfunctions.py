"""This file is to be used to manage C functionality"""

from ctypes import cdll
from ctypes import CDLL

def refresh_screenC():
	cdll.LoadLibrary("Pysrcs/libCtaskmaster.so")
	libCtaskmaster = CDLL("Pysrcs/libCtaskmaster.so")
	print(libCtaskmaster.refresh_screen(5))
