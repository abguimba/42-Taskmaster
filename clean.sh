#! /bin/sh

if [ "$1" == "all" ]
then
        rm -f setup.py
		rm -rf build
		rm -f *.so
		rm -f *.c
		echo "All items cleaned!"
else
	    rm -rf build
		rm -f *.so
		rm -f *.c
		echo "C Objects cleaned"
fi
