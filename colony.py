#!/usr/local/bin/python3

import * from utils.py

def col_eprint(err):
	eprint("error: " + err)

class colony:
	def __init__(self):
		self.antn = 0
		self.size = 0 #number of rooms
		self.rooms = {}
		self.links = []
		self.start = ""
		self.end = ""
		self.turns = []

	#TODO: obviously finish this
	def add_room(self, name, x, y):
		if name in self.rooms:
			eprint("error: room \"" + spl[0]  + "\" already defined.")

class room:
	def __init__(self):
		# graphical coordinates if any
		self.x = -1
		self.y = -1
		# links to other rooms
		self.links = []
		# command attributes ("start", "end", etc...)
		self.attrs = []
