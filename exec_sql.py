#!/bin/python
import sys, tty, termios
import mysql.connector as sql
from os import listdir, system
from os.path import isfile, join

# Some colors for the output 
BLUE = '\033[94m'
NC = '\033[0m'

# Load options with the names of all the files in the sql/ directory
options = [f for f in listdir('./sql') if isfile(join('./sql', f))]

def run():
	sel = 0
	while True:
		display(sel)
		sel = get_key(sel)

def display(sel):
	system('clear')
	print('Select a SQL file to execute:\n')
	
	# Print all the options, highlighting the currently selected one
	i = 0
	while i < len(options):
		if i == sel:
			print('  [' + BLUE + options[i] + NC + ']')
		else:
			print('   ' + options[i])
		i += 1

def get_key(sel):
	
	# Get the last pressed key's ansi escape sequence
	key = get_ch()

	# Check the escape sequences
	# Up or right arrow: add one, down or left arrow: subtract 1
	if key == '\x1b[A' or key == '\x1b[D':
		sel -= 1
	elif key == '\x1b[B' or key == '\x1b[C':
		sel += 1
	else:
		execute(sel)
	
	# If the selection leaves the bounds of the array, wrap it around to the other end
	if sel == -1:
		sel = len(options) - 1
	elif sel == len(options):
		sel = 0

	return sel


# A helper class to get the last pressed key's ansi escape sequence
def get_ch():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch1 = sys.stdin.read(1)
		if ord(ch1) != 27: return ''
		ch2 = sys.stdin.read(1)
		if ord(ch2) != 91: return ''
		ch3 = sys.stdin.read(1)
		ch = ch1 + ch2 + ch3
		
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

def execute(sel):
	system('clear')
	print('Executing ' + options[sel] + '...')
	db = sql.connect(user='CS353_ChatApp',
				password='Jpjb!2020',
				host='52.87.177.126',
				database='ChatApp',
				raise_on_warnings=True)
	cursor = db.cursor()
	query = ""

	# Iterate through the file and separate queries by semicolon
	# Smash them into one line by removing line feeds and execute the queries one at a time
	with open(join('./sql', options[sel])) as f:
		for c in f.read():
			if ord(c) > 31:
				query += c
			elif ord(c) == 10 and len(query) > 0:
				query += ' '
			if c == ';':
				cursor.execute(query)
				query = ""
	db.commit()
	db.close()

	print(options[sel] + ' has been executed')
	sys.exit(0)

run()
