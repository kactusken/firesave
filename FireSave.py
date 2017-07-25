#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''
file: FireSave.py
version: .01
description: Python script for manipulation of Fire Pro Wrestling World save files.
author: Kactus Ken (burningsave@gmail.com)
'''
import argparse
import os
import StringIO
import struct
import subprocess
import sys
from binascii import hexlify
from zipfile import ZipFile

# Constants
VER_STRING = ".01"
OFFSET_MISSIONS = 0xf8
OFFSET_PROMOTIONS = 0x88
OFFSET_STABLES = 0x98

# CLI Parser setup
parser = argparse.ArgumentParser()
parser.add_argument("-m", help="Unlock all missions with Rank S", action="store_true")
parser.add_argument("-s", help="Print all Promotions and Stables", action="store_true")

parser.add_argument("basevalue", help="Save file path for parsing")

# Assign arguments to variables
globals().update(vars(parser.parse_args()))

# Dumb Ascii Art Banner
def banner_print():
	print ""
	print "███████╗██╗██████╗ ███████╗███████╗ █████╗ ██╗   ██╗███████╗".decode('utf-8')
	print "██╔════╝██║██╔══██╗██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝".decode('utf-8')
	print "█████╗  ██║██████╔╝█████╗  ███████╗███████║██║   ██║█████╗  ".decode('utf-8')
	print "██╔══╝  ██║██╔══██╗██╔══╝  ╚════██║██╔══██║╚██╗ ██╔╝██╔══╝  ".decode('utf-8')
	print "██║     ██║██║  ██║███████╗███████║██║  ██║ ╚████╔╝ ███████╗".decode('utf-8')
	print "╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝".decode('utf-8')
	print "                 burningsave@gmail.com                 v %s " % (VER_STRING)
	print ""

# Print the banner
banner_print()

# Open the savedata.dat file, extract to memory the savedata with the hardcoded password
try:
	z = ZipFile(basevalue)
	x = z.extract('savedata', os.getcwd(), 'w#qjH_xaZ~Fm')
	f = open(x, 'r+b')
except:
	print "ERROR: Unable to open savedata.dat"
	quit()

# Update Mission table to pass with S Rank
def mission_update():
	# Updating Mission Progress
	print "+ Updating mission progress..."

	# Seek to the mission header and get offset for mission data
	f.seek(OFFSET_MISSIONS, 0)
	offset_missiondata = struct.unpack('i', f.read(4))[0]

	# Seek to the mission data structure
	f.seek(offset_missiondata, 0)

	# Write the S rank to each mission
	for x in range(0, 56):
		f.write(bytearray(int(i,16) for i in ['0x04','0x00','0x00','0x00']))

	# Complete
	print "+ Update Complete!"


# Print list of stables
def stable_print():
	# Create array of Promotions
	promotions = []

	# Updating Mission Progress
	print "+ Reading promotions"

	# Seek to the promotions header and get offset for promotion data
	f.seek(OFFSET_PROMOTIONS, 0)
	offset_promotiondata = struct.unpack('i', f.read(4))[0]

	# Seek to the mission data structure
	f.seek(offset_promotiondata, 0)

	# Get number of promotions
	promotions_count = struct.unpack('i', f.read(4))[0]

	# Loop through all promotions
	for x in range(0, promotions_count):
		# Get long name
		promotion_long_len = int(hexlify(f.read(1)),16)
		promotion_long = f.read(promotion_long_len)

		# Get short name
		promotion_short_len = int(hexlify(f.read(1)),16)
		promotion_short = f.read(promotion_short_len)

		# Get Logo ID
		promotion_logoid = struct.unpack('i', f.read(4))

		# Append Promotions to array
		if x == 0:
			promotions.append("Retire")
		else:
			promotions.append("%s - %s" % (promotion_short, promotion_long))

	# Updating Mission Progress
	print "+ Reading stables\n"

	# Seek to the stables header and get offset for stable data
	f.seek(OFFSET_STABLES, 0)
	offset_stabledata = struct.unpack('i', f.read(4))[0]

	# Seek to the mission data structure
	f.seek(offset_stabledata, 0)

	# Get number of promotions
	stables_count = struct.unpack('i', f.read(4))[0]

	# Loop through all promotions
	for x in range(0, stables_count):
		# Get long name
		stable_long_len = int(hexlify(f.read(1)),16)
		stable_long = f.read(stable_long_len)

		# Get short name
		stable_short_len = int(hexlify(f.read(1)),16)
		stable_short = f.read(stable_short_len)

		# Get Promotion ID
		stable_promotionid = struct.unpack('i', f.read(4))[0]

		# Get Alignment
		stable_alignment = struct.unpack('i', f.read(4))[0]

		if x == 0:
			print "\t%s. %s - %s (%s)" % (x, "Retire", "", promotions[stable_promotionid])
		else:
			print "\t%s. %s - %s (%s)" % (x, stable_short, stable_long, promotions[stable_promotionid])

def write_zip():
	try:
		cmd = ['7za.exe','a','-tzip','savedataedit.dat','savedata','-pw#qjH_xaZ~Fm']
		sp = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
		out, err = sp.communicate()
		print "+ Save file completed"
	except:
		print "Unable to create zip file"

# Check CLI Arguments
if m == True:
	mission_update()
	f.close()
	write_zip()

if s == True:
	stable_print()
