#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''
file: FireSave.py
version: .03
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
VER_STRING = ".03"
OFFSET_MISSIONS = 0xf8
OFFSET_PROMOTIONS = 0x88
OFFSET_SORT = 0xb8
OFFSET_STABLES = 0x98
OFFSET_WRESTLERS = 0x58

# Global Variables
promotions = []
stables = []

# CLI Parser setup
parser = argparse.ArgumentParser()
parser.add_argument("-a", help="Sort Alphabetical", action="store_true")
parser.add_argument("-m", help="Unlock all missions with Rank S", action="store_true")
parser.add_argument("-r", help="Move all wrestlers from retire to specific Stable", default=0, type=int)
parser.add_argument("-s", help="Print all Promotions and Stables", action="store_true")
parser.add_argument("-w", help="Print wrestlers who are assigned to Retire", action="store_true")
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
	print "                 burningsave@gmail.com                  v%s " % (VER_STRING)
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

# Parses through all costumes
def costume_parse():
	# There are four costumes per wrestlers
	for costume in range(0, 4):
		# Is the costume used by the wrestler
		costume_valid = f.read(1)

		# Get all the layers for the costume
		for layertext in range(0, 9):
			for layertextdata in range(0,16):
				layertext_len = int(hexlify(f.read(1)),16)
				layertext_string = f.read(layertext_len)

		# Get all the colors for the layers
		for layercolor in range(0, 9):
			for colors in range(0, 16):
				colorA = f.read(4)
				colorB = f.read(4)
				colorG = f.read(4)
				colorR = f.read(4)

		# Get the scale of the costume parts
		costume_partsScale = f.read(4 * 5)

		# Get the highlights
		for highlights in range(0, 9):
			highlight = f.read(4 * 16)

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

def sort_alpha():
	# Create a list of wrestlers
	list_wrestlers = []

	# Read all of the wrestlers to get their names
	print "\n+ Reading Wrestlers"

	# Seek to the wrestler header and get offset for wrestler data
	f.seek(OFFSET_WRESTLERS, 0)
	offset_wrestlerdata = struct.unpack('i', f.read(4))[0]

	# Seek to the wrestler data structure
	f.seek(offset_wrestlerdata, 0)

	# Get number of wrestlers
	wrestlers_count = struct.unpack('i', f.read(4))[0]

	# Loop through all wrestlers
	for wrestler in range(0, wrestlers_count):
		wrestler_name = wrestler_parse(wrestler).lstrip()
		list_wrestlers.append((wrestler_name, wrestler))

	# Sort the list of wrestlers by their name
	list_wrestlers.sort(key=lambda x: x[0])

	# Seek to the display order
	f.seek(OFFSET_SORT, 0)
	offset_sortdata = struct.unpack('i', f.read(4))[0]

	# Seek to the wrestler data structure
	f.seek(offset_sortdata, 0)
	preset_count = struct.unpack('i', f.read(4))[0]
	order_count = struct.unpack('i', f.read(4))[0]
	pos = f.tell()
	f.seek(pos, 0)
	print "%s %s" % (preset_count, order_count)

	for order in range(0, wrestlers_count):
		hex_value = [hex(10000+list_wrestlers[order][1] >> i & 0xff) for i in (0,8,16,24)]
		f.write(bytearray(int(i, 16) for i in hex_value))

	for preset in range(0, preset_count):
		f.write(bytearray(int(i, 16) for i in [hex(preset),'0x00', '0x00', '0x00']))

# Print list of stables
def stable_print():
	# Updating Mission Progress
	print "+ Reading promotions\n"

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
			print "\t%s. %s" % (x, "Retire")
		else:
			promotions.append("%s - %s" % (promotion_short, promotion_long))
			print "\t%s. %s" % (x, promotion_long)

	# Updating Mission Progress
	print "\n+ Reading stables\n"

	# Seek to the stables header and get offset for stable data
	f.seek(OFFSET_STABLES, 0)
	offset_stabledata = struct.unpack('i', f.read(4))[0]

	# Seek to the mission data structure
	f.seek(offset_stabledata, 0)

	# Get number of promotions
	stables_count = struct.unpack('i', f.read(4))[0]

	# Loop through all promotions
	for stable in range(0, stables_count):
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

		# Check if selected stable
		if stable == r:
			choice = "** SELECTED STABLE **"
		else:
			choice = ""

		# Print the list of stables
		if stable == 0:
			print "\t%s. %s - %s (%s)" % (stable, "Retire", "", promotions[stable_promotionid])
		else:
			print "\t%s. %s - %s (%s) %s" % (stable, stable_short, stable_long, promotions[stable_promotionid], choice)

# Parse the wrestler data structure
def wrestler_parse(x):
	wrestler_ver = f.read(4)
	wrestler_sortingOrder = f.read(4)
	wrestler_weightClass = f.read(4)
	wrestler_isReverseNameDispOrder = f.read(1)
	wrestler_name1_len = int(hexlify(f.read(1)),16)
	wrestler_name1 = f.read(wrestler_name1_len)
	wrestler_name2_len = int(hexlify(f.read(1)),16)
	wrestler_name2 = f.read(wrestler_name2_len)
	wrestler_nickName_len = int(hexlify(f.read(1)),16)
	wrestler_nickName = f.read(wrestler_nickName_len)
	wrestler_delimiter_len = int(hexlify(f.read(1)),16)
	wrestler_delimiter = f.read(wrestler_delimiter_len)
	wrestler_country = f.read(4)
	wrestler_height = f.read(4)
	wrestler_weight = f.read(4)
	wrestler_birthYear = f.read(4)
	wrestler_birthMonth = f.read(4)
	wrestler_birthDay = f.read(4)

	# Record offset before stable
	offset_previous = f.tell()

	# Check if stable should be replaced
	wrestler_groupID = struct.unpack('i', f.read(4))[0]

	# Record offset after stable
	offset_next = f.tell()

	# Check if werstler is in Retire, if so, update with the specified stable
	if wrestler_groupID == 0:
		choice = "** UPDATED WRESTLER Stable **"
		f.seek(offset_previous, 0)
		f.write(bytearray(int(i,16) for i in [hex(r),'0x00','0x00','0x00']))
		f.seek(offset_next, 0)
	else:
		choice = ""

	# Continue parsing wrestler structure
	wrestler_fightStyle = f.read(4)
	wrestler_reversalType = f.read(4)
	wrestler_sex = f.read(4)
	wrestler_wrestlerRank = f.read(4)
	wrestler_charismaRank = f.read(4)
	wrestler_weaponLotTbl = f.read(4)
	wrestler_hpRecovery = f.read(4)
	wrestler_hpRecovery_Bleeding = f.read(4)
	wrestler_bpRecovery = f.read(4)
	wrestler_bpRecovery_Bleeding = f.read(4)
	wrestler_spRecovery = f.read(4)
	wrestler_spRecovery_Bleeding = f.read(4)
	wrestler_defNeck = f.read(4)
	wrestler_defArm = f.read(4)
	wrestler_defWaist = f.read(4)
	wrestler_defLeg = f.read(4)
	wrestler_walkSpeed = f.read(4)
	wrestler_upDownSpeed = f.read(4)
	wrestler_cornerPostActType = f.read(4)
	wrestler_criticalType = f.read(4)
	wrestler_exchangeOfStriking = f.read(1)
	wrestler_themeMusic = f.read(4)
	wrestler_voiceType_0 = f.read(4)
	wrestler_voiceType_1 = f.read(4)
	wrestler_voiceID_0 = f.read(4)
	wrestler_voiceID_1 = f.read(4)
	wrestler_specialSkill = f.read(4)
	wrestler_atkParam = f.read(4 * 12)
	wrestler_defParam = f.read(4 * 12)
	wrestler_skillSlot = f.read(4 * 91)
	wrestler_skillAttr = f.read(4 * 91)
	wrestler_skillVoice = f.read(4 * 91)
	wrestler_ai_Ver = f.read(4)
	wrestler_ai_Far_Ldmg = f.read(4 * 8)
	wrestler_ai_Far_Hdmg = f.read(4 * 8)
	wrestler_ai_Grapple_LDmg = f.read(4 * 15)
	wrestler_ai_Grapple_MDmg = f.read(4 * 15)
	wrestler_ai_Grapple_HDmg = f.read(4 * 15)
	wrestler_ai_holdBack_LDmg = f.read(4 * 7)
	wrestler_ai_holdBack_HDmg = f.read(4 * 7)
	wrestler_ai_throwToRope_LDmg = f.read(4 * 7)
	wrestler_ai_throwToRope_HDmg = f.read(4 * 7)
	wrestler_ai_leanOnCorner_LDmg = f.read(4 * 4)
	wrestler_ai_leanOnCorner_HDmg = f.read(4 * 4)
	wrestler_ai_downNearCorner_LDmg = f.read(4 * 6)
	wrestler_ai_downNearCorner_HDmg = f.read(4 * 6)
	wrestler_ai_downCenter_LDmg = f.read(4 * 3)
	wrestler_ai_downCenter_HDmg = f.read(4 * 3)
	wrestler_ai_downOnBack_LDmg = f.read(4 * 8)
	wrestler_ai_downOnBack_HDmg = f.read(4 * 8)
	wrestler_ai_downOnBack_FDmg = f.read(4 * 8)
	wrestler_ai_downOnFace_LDmg = f.read(4 * 8)
	wrestler_ai_downOnFace_HDmg = f.read(4 * 8)
	wrestler_ai_downOnFace_FDmg = f.read(4 * 8)
	wrestler_ai_stunNearCorner_LDmg = f.read(4 * 7)
	wrestler_ai_stunNearCorner_HDmg = f.read(4 * 7)
	wrestler_ai_stunCenter_LDmg = f.read(4 * 4)
	wrestler_ai_stunCenter_HDmg = f.read(4 * 4)
	wrestler_ai_stun_LDmg = f.read(4 * 5)
	wrestler_ai_stun_HDmg = f.read(4 * 5)
	wrestler_ai_stun_FDmg = f.read(4 * 5)
	wrestler_ai_guardPosision_LDmg = f.read(4 * 3)
	wrestler_ai_guardPosision_HDmg = f.read(4 * 3)
	wrestler_ai_faceLock_LDmg = f.read(4 * 3)
	wrestler_ai_faceLock_HDmg = f.read(4 * 3)
	wrestler_ai_backMount_LDmg = f.read(4 * 3)
	wrestler_ai_backMount_HDmg = f.read(4 * 3)
	wrestler_ai_breakFall_LDmg = f.read(4)
	wrestler_ai_breakFall_MDmg = f.read(4)
	wrestler_ai_breakFall_HDmg = f.read(4)
	wrestler_ai_backReversal = f.read(4 * 2)
	wrestler_ai_opponentOutOfRing = f.read(4 * 8)
	wrestler_ai_performance_Stun = f.read(4 * 5)
	wrestler_ai_performance_Down = f.read(4 * 5)
	wrestler_ai_performance_OutOfRing = f.read(4 * 5)
	wrestler_ai_performance_CornerPost = f.read(4 * 5)
	wrestler_ai_priorityAct_LDmg = f.read(4 * 3)
	wrestler_ai_priorityAct_HDmg = f.read(4 * 3)
	wrestler_ai_priorityAct = f.read(8 * 3)
	wrestler_ai_personalTraits = f.read(4)
	wrestler_ai_discreation = f.read(4)
	wrestler_ai_flexibility = f.read(4)
	wrestler_ai_cooperation = f.read(4)
	wrestler_ai_returnFromOutOfRingCount = f.read(4)
	wrestler_ai_touchCond = f.read(4)
	wrestler_ai_takeWeapon = f.read(4)
	wrestler_ai_secondAggressiveness = f.read(4)
	wrestler_flags = f.read(4)
	wrestler_editPoint= f.read(4)
	wrestler_criticalMoveName_len = int(hexlify(f.read(1)),16)
	wrestler_criticalMoveName = f.read(wrestler_criticalMoveName_len)
	wrestler_costumeVer = f.read(4)
	wrestler_costumeStance = f.read(4)
	wrestler_costumeFormSize= f.read(4)
	# Parse out the costuem data structure
	costume_parse()
	print "\t%s. %s %s %s" % (x, wrestler_name1, wrestler_name2, choice)
	return "%s %s" % (wrestler_name1, wrestler_name2)

# Update the stable for retired wrestlers
def stable_update():
	# Get list of Stables
	stable_print()

	# Updating Mission Progress
	print "\n+ Reading Wrestlers"

	# Seek to the promotions header and get offset for promotion data
	f.seek(OFFSET_WRESTLERS, 0)
	offset_wrestlerdata = struct.unpack('i', f.read(4))[0]

	# Seek to the mission data structure
	f.seek(offset_wrestlerdata, 0)

	# Get number of promotions
	wrestlers_count = struct.unpack('i', f.read(4))[0]

	# Loop through all promotions
	for wrestler in range(0, wrestlers_count):
		wrestler_parse(wrestler)

# Write the edited file back to disk
def write_zip():
	try:
		cmd = ['7za.exe','a','-tzip','savedataedit.dat','savedata','-pw#qjH_xaZ~Fm']
		sp = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
		out, err = sp.communicate()
		print "\n+ Save file completed"
	except:
		print "Unable to create zip file"

# Check CLI Arguments
if a == True:
	sort_alpha()

if m == True:
	mission_update()

if r > 0:
	stable_update()

if s == True:
	stable_print()


f.close()

if (m == True) or (r > 0) or (a == True):
	write_zip()
