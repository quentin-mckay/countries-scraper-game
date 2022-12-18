#!/bin/bash

# check if system has python
if ! [[ -x "$(command -v python)" ]]
then
	echo 'Error
		This program runs on Python, but it looks like Python is not installed.
    To install Python, check out https://installpython3.com/' >&2
	exit 1
fi

# start virtual environment

# install dependencies

# check for different operating systems
if [[ $OSTYPE == 'darwin'* ]]
then
	# echo 'macOS'
	python3 -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt
	python3 app.py $1 $2
fi

if [[ $OSTYPE == 'linux'* ]]
then
	# echo 'linux'
	python -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt
	python app.py $1 $2
fi

if [[ $OSTYPE == 'msys'* ]]
then
	# echo 'windows'
	python -m venv venv
	source venv/Scripts/activate
	pip install -r requirements.txt
	py app.py $1 $2
fi