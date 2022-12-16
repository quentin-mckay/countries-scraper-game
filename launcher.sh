#!/bin/bash



# check if system has python
if ! [[ -x "$(command -v python)" ]]
then
	echo 'Error
		This program runs on Python, but it looks like Python is not installed.
    To install Python, check out https://installpython3.com/' >&2
	exit 1
fi

# check for different operating systems
if [[ $OSTYPE == 'darwin'* ]]
then
	# echo 'macOS'
	python3 app.py $1
fi

if [[ $OSTYPE == 'linux'* ]]
then
	# echo 'linux'
	python app.py $1
fi

if [[ $OSTYPE == 'msys'* ]]
then
	# echo 'windows'
	py app.py $1
fi


