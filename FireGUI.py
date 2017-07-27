#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
file: FireGui.py
version: .06
description: GUI version of FireSave.py
author: Kactus Ken (burningsave@gmail.com)
'''
import csv
import os
import struct
import subprocess
import time
import tkFileDialog
import tkMessageBox
from binascii import hexlify
from Tkinter import *
from zipfile import ZipFile

# Constants
VER_STRING = ".06"
OFFSET_MISSIONS = 0xf8
OFFSET_PROMOTIONS = 0x88
OFFSET_SORT = 0xb8
OFFSET_STABLES = 0x98
OFFSET_WRESTLERS = 0x58

# Global Variables
promotions = []
stables = []
wrestlers = []
f = None

# Function to add list of default wrestlers
def DefaultWrestlers():
    # Clear wrestler list
    global wrestlers
    wrestlers = []

    DebugPrint(" + Adding list of default wrestlers")
    wrestlers.append(("Blan Fleming", 0))
    wrestlers.append(("Karts Rowdy", 1))
    wrestlers.append(("Sam Blocks", 2))
    wrestlers.append(("Red Dragon", 3))
    wrestlers.append(("Dag Boomer", 4))
    wrestlers.append(("Takaya Hinomiya", 5))
    wrestlers.append(("Blood Angel", 6))
    wrestlers.append(("Oliver Espadas", 7))
    wrestlers.append(("Max Bertrand", 8))
    wrestlers.append(("Trevor Darius", 9))
    wrestlers.append(("Mr.Cobra", 10))
    wrestlers.append(("Fuji Akatsuki", 11))
    wrestlers.append(("Steel Johnson", 12))
    wrestlers.append(("Bobby Bobby", 13))
    wrestlers.append(("Edward Joseph", 14))
    wrestlers.append(("Leonardo Pascual", 15))
    wrestlers.append(("Allen Hawkins", 16))
    wrestlers.append(("Dai Fugo", 17))
    wrestlers.append(("Laurence Holland", 18))
    wrestlers.append(("Soji Kanda", 19))
    wrestlers.append(("John Smith", 20))
    wrestlers.append(("Keiichiro Asakawa", 21))
    wrestlers.append(("Alex Thompson", 22))
    wrestlers.append(("Jose Santos", 23))
    wrestlers.append(("Damon Smith", 24))
    wrestlers.append(("Ernest Miller", 25))
    wrestlers.append(("Abbie Jones", 26))
    wrestlers.append(("Sophia Rodrigues", 27))
    wrestlers.append(("Caroline Collins", 28))
    wrestlers.append(("Jamie Wilson", 29))
    wrestlers.append(("Lindsey Stewart", 30))

# Function for button to ask for Save file
def GetSaveFilePath():
    filename_SaveFile = tkFileDialog.askopenfilename(initialdir="C:\\", title="Select FPPW Save File",
                                                     filetypes=(("dat files", "*dat"), ("all files", "*.*")))
    ent_SaveFile.delete(0, END)
    ent_SaveFile.insert(0, filename_SaveFile)
    ent_OutputFile.delete(0, END)
    ent_OutputFile.insert(0, filename_SaveFile.replace(".dat", "_edited.dat"))
    lst_Stables.delete(0, END)


# Function for button to ask for Output file
def GetOutputPath():
    filename_SaveFile = tkFileDialog.asksaveasfilename(initialdir="C:\\", title="Select Output File Path",
                                                       filetypes=(("dat files", "*dat"), ("all files", "*.*")))
    ent_OutputFile.insert(0, filename_SaveFile)


# Function to print status updates to the text area
def DebugPrint(dbg_message):
    # Insert the message
    txt_Output.insert(END, dbg_message + "\n")

    # Scroll to the bottom
    txt_Output.see(END)


# Function to open the save file
def OpenSave():
    global f

    # Attempt to Extract the
    try:
        z = ZipFile(ent_SaveFile.get())
        DebugPrint(" + Successfully opened save file archive")
        x = z.extract('savedata', os.getcwd(), 'w#qjH_xaZ~Fm')
        DebugPrint(" + Successfully extracted save contents")
        f = open(x, 'r+b')
        DebugPrint(" + Successfully opened save file data")
        return 1

    except:
        f = None
        DebugPrint(" + Unable to open save file data")
        tkMessageBox.showerror("FireGUI Error", "Unable to open savedata.dat file")
        return 0


# Function to close the save file
def CloseSave():
    global f

    # Close the file and set to none
    f.close()
    f = None


# Function to save the edit savedata as the password protected zip file
def SaveZip():
    try:
        cmd = ['7za.exe', 'a', '-tzip', ent_OutputFile.get(), 'savedata', '-pw#qjH_xaZ~Fm']
        sp = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        out, err = sp.communicate()
        DebugPrint(" + Save file generated")
        return 1
    except:
        DebugPrint(" + Unable to generate save file zip")
        return 0


# Function to retrieve the list of stables in the save file
def GetStableList():
    global f

    DebugPrint(" + Loading list of Stables")
    valid = OpenSave()
    if valid == 1:
        DebugPrint(" + Reading Promotions")

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
            promotion_long_len = int(hexlify(f.read(1)), 16)
            promotion_long = f.read(promotion_long_len)

            # Get short name
            promotion_short_len = int(hexlify(f.read(1)), 16)
            promotion_short = f.read(promotion_short_len)

            # Get Logo ID
            promotion_logoid = struct.unpack('i', f.read(4))

            # Append Promotions to array
            if x == 0:
                promotions.append("Retire")
                DebugPrint("\t%s. %s" % (x, "Retire"))
            else:
                promotions.append("%s - %s" % (promotion_short, promotion_long))
                DebugPrint("\t%s. %s" % (x, promotion_long))

        # Updating Mission Progress
        DebugPrint("+ Reading stables")

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
            stable_long_len = int(hexlify(f.read(1)), 16)
            stable_long = f.read(stable_long_len)

            # Get short name
            stable_short_len = int(hexlify(f.read(1)), 16)
            stable_short = f.read(stable_short_len)

            # Get Promotion ID
            stable_promotionid = struct.unpack('i', f.read(4))[0]

            # Get Alignment
            stable_alignment = struct.unpack('i', f.read(4))[0]

            # Print the list of stables
            if stable == 0:
                DebugPrint("\t%s. %s - %s (%s)" % (stable, "Retire", "", promotions[stable_promotionid]))
                lst_Stables.insert(END,
                                   "%s. %s - %s (%s)" % (stable, "Retire", "", promotions[stable_promotionid]))
            else:
                DebugPrint("\t%s. %s - %s (%s)" % (stable, stable_short, stable_long, promotions[stable_promotionid]))
                lst_Stables.insert(END,
                                   "%s. %s - %s (%s)" % (
                                   stable, stable_short, stable_long, promotions[stable_promotionid]))

        # CLose the file and set to none
        CloseSave()
        DebugPrint(" + Completed listing of stables")


# Function to validate the configuration file
def ValidateConfig():
    global val_Stable
    err_message = ""

    if ent_SaveFile.get() == "":
        err_message = "\nSaveData.dat location is empty"

    if ent_OutputFile.get() == "":
        err_message = err_message + "\nOutput file location is empty"

    if val_Stable.get() == 1:
        if lst_Stables.index(ACTIVE) == 0:
            err_message = err_message + "\nStable not selected"

    if err_message != "":
        tkMessageBox.showerror("FireGUI Error", "Unable to process: \n%s" % err_message)
        return 0
    else:
        return 1


# Function to update all the missions to rank S
def MissionUpdate():
    try:
        # Updating Mission Progress
        DebugPrint(" + Updating mission progress...")

        # Seek to the mission header and get offset for mission data
        f.seek(OFFSET_MISSIONS, 0)
        offset_missiondata = struct.unpack('i', f.read(4))[0]

        # Seek to the mission data structure
        f.seek(offset_missiondata, 0)

        # Write the S rank to each mission
        for x in range(0, 56):
            f.write(bytearray(int(i, 16) for i in ['0x04', '0x00', '0x00', '0x00']))
        f.seek(offset_missiondata, 0)

        # Complete
        DebugPrint(" + Mission Update Complete!")
        return 1
    except:
        DebugPrint(" + Mission Update Failed!")
        return 0

# Parses through all costumes
def CostumeParse():
    # There are four costumes per wrestlers
    for costume in range(0, 4):
        # Is the costume used by the wrestler
        costume_valid = f.read(1)

        # Get all the layers for the costume
        for layertext in range(0, 9):
            for layertextdata in range(0, 16):
                layertext_len = int(hexlify(f.read(1)), 16)
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

# Function to parse a wrestler data object and update stable if required
def WrestlerParse(x):
    wrestler_ver = f.read(4)
    wrestler_sortingOrder = f.read(4)
    wrestler_weightClass = f.read(4)
    wrestler_isReverseNameDispOrder = f.read(1)
    wrestler_name1_len = int(hexlify(f.read(1)), 16)
    wrestler_name1 = f.read(wrestler_name1_len)
    wrestler_name2_len = int(hexlify(f.read(1)), 16)
    wrestler_name2 = f.read(wrestler_name2_len)
    wrestler_nickName_len = int(hexlify(f.read(1)), 16)
    wrestler_nickName = f.read(wrestler_nickName_len)
    wrestler_delimiter_len = int(hexlify(f.read(1)), 16)
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

    # Check if wrestler is in Retire, if so, update with the specified stable
    choice = ""
    if val_Stable.get() == 1:
        if wrestler_groupID == 0:
            choice = "** UPDATED Wrestler Stable **"
            f.seek(offset_previous, 0)
            f.write(bytearray(int(i, 16) for i in [hex(lst_Stables.index(ACTIVE)), '0x00', '0x00', '0x00']))
            f.seek(offset_next, 0)

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
    wrestler_editPoint = f.read(4)
    wrestler_criticalMoveName_len = int(hexlify(f.read(1)), 16)
    wrestler_criticalMoveName = f.read(wrestler_criticalMoveName_len)
    wrestler_costumeVer = f.read(4)
    wrestler_costumeStance = f.read(4)
    wrestler_costumeFormSize = f.read(4)
    # Parse out the costuem data structure
    CostumeParse()
    DebugPrint("\t%s. %s %s %s" % (x, wrestler_name1, wrestler_name2, choice))
    return "%s %s" % (wrestler_name1, wrestler_name2)

# Function to replace stable of retired wrestlers
def StableUpdate():
    try:
        # Reading wrestlers
        DebugPrint(" + Reading Wrestlers")

        # Seek to the wrestler header and get offset for wrestler data
        f.seek(OFFSET_WRESTLERS, 0)
        offset_wrestlerdata = struct.unpack('i', f.read(4))[0]

        # Seek to the wrestler data structure
        f.seek(offset_wrestlerdata, 0)

        # Get number of wrestlers
        wrestlers_count = struct.unpack('i', f.read(4))[0]

        # Loop through all wrestlers
        for wrestler in range(0, wrestlers_count):
            WrestlerParse(wrestler)

        DebugPrint(" + Stable Update Complete!")
        f.seek(OFFSET_WRESTLERS, 0)
        return 1

    except:
        DebugPrint(" + Stable Update Failed!")
        return 0

# Function to replace the old savefile with the new savefile
def AskReplace():
    if tkMessageBox.askyesno("Replace save file?",
                             "Do you want to replace your existing save file?\nBackup of original will be created.") == True:
        replace_path = "%s_%d" % (ent_SaveFile.get(), int(time.time()))

        os.rename(ent_SaveFile.get(), replace_path)
        DebugPrint(" + Backed up save file to %s" % (replace_path))

        os.rename(ent_OutputFile.get(), ent_SaveFile.get())
        DebugPrint(" + Replace old save file with new save file")

# Function to alphabetize wrestler list
def Alphabetize():
    global wrestlers
    global f
    try:
        DefaultWrestlers()
        # Read all of the wrestlers to get their names
        DebugPrint(" + Reading Edit Wrestlers")

        # Seek to the wrestler header and get offset for wrestler data
        f.seek(OFFSET_WRESTLERS, 0)
        offset_wrestlerdata = struct.unpack('i', f.read(4))[0]

        # Seek to the wrestler data structure
        f.seek(offset_wrestlerdata, 0)

        # Get number of wrestlers
        wrestlers_count = struct.unpack('i', f.read(4))[0]
        # Loop through all wrestlers
        for wrestler in range(0, wrestlers_count):
            wrestler_name = WrestlerParse(wrestler).lstrip()
            wrestlers.append((wrestler_name, 10000 + wrestler))

        # Sort the list of wrestlers by their name
        DebugPrint(" + Sorting Wrestlers")
        wrestlers.sort(key=lambda x: x[0])

        # Seek to the display order
        f.seek(OFFSET_SORT, 0)
        offset_sortdata = struct.unpack('i', f.read(4))[0]

        # Seek to the wrestler data structure
        f.seek(offset_sortdata, 0)
        preset_count = struct.unpack('i', f.read(4))[0]
        order_count = struct.unpack('i', f.read(4))[0]
        pos = f.tell()
        f.seek(pos, 0)

        DebugPrint(" + Writing new sort order")
        for order in range(0, wrestlers_count):
            hex_value = [hex(wrestlers[order][1] >> i & 0xff) for i in (0, 8, 16, 24)]
            f.write(bytearray(int(i, 16) for i in hex_value))

        f.seek(OFFSET_SORT, 0)
        DebugPrint(" + Completed alphabetizing wrestlers")
        return 1

    except:
        DebugPrint(" + Alphabetize Update Failed!")
        return 0

# Main FireSave function
def FireSave():
    success = 0
    # Validate the configuration settings
    if ValidateConfig() == 1:
        # Try to open the save file
        if OpenSave() == 1:
            # Check for mission complete check
            if val_Alpha.get() == 1:
                success = Alphabetize()

            if val_Mission.get() == 1:
                success = MissionUpdate()

            if val_Stable.get() == 1:
                success = StableUpdate()

        # Close the Save File
        CloseSave()

        # Check if Everything went well
        if success == 1:
            DebugPrint(" + All modifications completed")
            if SaveZip() == 1:
                AskReplace()


# Create root window
top = Tk()
top.geometry("539x645+1328+563")
top.title("FireGUI v.06")
top.configure(background="#d9d9d9")

# Create Cherkbox variables
val_Alpha = IntVar()
val_Mission = IntVar()
val_Stable = IntVar()

# Create the Interface
lf_Configuration = LabelFrame(top)
lf_Configuration.place(relx=0.02, rely=0.01, relheight=0.49
                       , relwidth=0.96)
lf_Configuration.configure(relief=GROOVE)
lf_Configuration.configure(foreground="black")
lf_Configuration.configure(text='''Configuration''')
lf_Configuration.configure(background="#d9d9d9")
lf_Configuration.configure(width=520)

lbl_SaveFile = Label(lf_Configuration)
lbl_SaveFile.place(relx=0.02, rely=0.0, height=21, width=88)
lbl_SaveFile.configure(background="#d9d9d9")
lbl_SaveFile.configure(disabledforeground="#a3a3a3")
lbl_SaveFile.configure(foreground="#000000")
lbl_SaveFile.configure(justify=RIGHT)
lbl_SaveFile.configure(text='''FPPW Save File:''')
lbl_SaveFile.configure(width=88)

ent_SaveFile = Entry(lf_Configuration)
ent_SaveFile.place(relx=0.19, rely=0.0, relheight=0.06
                   , relwidth=0.68)
ent_SaveFile.configure(background="white")
ent_SaveFile.configure(disabledforeground="#a3a3a3")
ent_SaveFile.configure(font="TkFixedFont")
ent_SaveFile.configure(foreground="#000000")
ent_SaveFile.configure(insertbackground="black")
ent_SaveFile.configure(width=354)

btn_SaveFile = Button(lf_Configuration)
btn_SaveFile.place(relx=0.88, rely=0.0, height=24, width=49)
btn_SaveFile.configure(activebackground="#d9d9d9")
btn_SaveFile.configure(activeforeground="#000000")
btn_SaveFile.configure(background="#d9d9d9")
btn_SaveFile.configure(disabledforeground="#a3a3a3")
btn_SaveFile.configure(foreground="#000000")
btn_SaveFile.configure(highlightbackground="#d9d9d9")
btn_SaveFile.configure(highlightcolor="black")
btn_SaveFile.configure(pady="0")
btn_SaveFile.configure(text='''Browse''')
btn_SaveFile.configure(command=GetSaveFilePath)

lbl_OutputFile = Label(lf_Configuration)
lbl_OutputFile.place(relx=0.04, rely=0.09, height=21, width=88)
lbl_OutputFile.configure(background="#d9d9d9")
lbl_OutputFile.configure(disabledforeground="#a3a3a3")
lbl_OutputFile.configure(foreground="#000000")
lbl_OutputFile.configure(justify=RIGHT)
lbl_OutputFile.configure(text='''Output File:''')
lbl_OutputFile.configure(width=88)

ent_OutputFile = Entry(lf_Configuration)
ent_OutputFile.place(relx=0.19, rely=0.09, relheight=0.06
                     , relwidth=0.68)
ent_OutputFile.configure(background="white")
ent_OutputFile.configure(disabledforeground="#a3a3a3")
ent_OutputFile.configure(font="TkFixedFont")
ent_OutputFile.configure(foreground="#000000")
ent_OutputFile.configure(insertbackground="black")
ent_OutputFile.configure(width=354)

btn_OutputFile = Button(lf_Configuration)
btn_OutputFile.place(relx=0.88, rely=0.09, height=24, width=49)
btn_OutputFile.configure(activebackground="#d9d9d9")
btn_OutputFile.configure(activeforeground="#000000")
btn_OutputFile.configure(background="#d9d9d9")
btn_OutputFile.configure(disabledforeground="#a3a3a3")
btn_OutputFile.configure(foreground="#000000")
btn_OutputFile.configure(highlightbackground="#d9d9d9")
btn_OutputFile.configure(highlightcolor="black")
btn_OutputFile.configure(pady="0")
btn_OutputFile.configure(text='''Browse''')
btn_OutputFile.configure(command=GetOutputPath)

lst_Stables = Listbox(lf_Configuration)
lst_Stables.place(relx=0.19, rely=0.19, relheight=0.58
                  , relwidth=0.68)
lst_Stables.configure(background="white")
lst_Stables.configure(disabledforeground="#a3a3a3")
lst_Stables.configure(font="TkFixedFont")
lst_Stables.configure(foreground="#000000")
lst_Stables.configure(relief=GROOVE)
lst_Stables.configure(selectmode=SINGLE)
lst_Stables.configure(width=354)

btn_List = Button(lf_Configuration)
btn_List.place(relx=0.88, rely=0.19, height=24, width=49)
btn_List.configure(activebackground="#d9d9d9")
btn_List.configure(activeforeground="#000000")
btn_List.configure(background="#d9d9d9")
btn_List.configure(disabledforeground="#a3a3a3")
btn_List.configure(foreground="#000000")
btn_List.configure(highlightbackground="#d9d9d9")
btn_List.configure(highlightcolor="black")
btn_List.configure(pady="0")
btn_List.configure(text='''List''')
btn_List.configure(width=49)
btn_List.configure(command=GetStableList)

lbl_Stables = Label(lf_Configuration)
lbl_Stables.place(relx=0.1, rely=0.19, height=21, width=46)
lbl_Stables.configure(background="#d9d9d9")
lbl_Stables.configure(disabledforeground="#a3a3a3")
lbl_Stables.configure(foreground="#000000")
lbl_Stables.configure(justify=RIGHT)
lbl_Stables.configure(text='''Stables:''')

chk_Mission = Checkbutton(lf_Configuration)
chk_Mission.place(relx=0.19, rely=0.79, relheight=0.08
                  , relwidth=0.25)
chk_Mission.configure(activebackground="#d9d9d9")
chk_Mission.configure(activeforeground="#000000")
chk_Mission.configure(background="#d9d9d9")
chk_Mission.configure(disabledforeground="#a3a3a3")
chk_Mission.configure(foreground="#000000")
chk_Mission.configure(highlightbackground="#d9d9d9")
chk_Mission.configure(highlightcolor="black")
chk_Mission.configure(justify=LEFT)
chk_Mission.configure(text='''Complete Missions''')
chk_Mission.configure(onvalue=1)
chk_Mission.configure(offvalue=0)
chk_Mission.configure(variable=val_Mission)

chk_Alpha = Checkbutton(lf_Configuration)
chk_Alpha.place(relx=0.44, rely=0.79, relheight=0.08, relwidth=0.17)

chk_Alpha.configure(activebackground="#d9d9d9")
chk_Alpha.configure(activeforeground="#000000")
chk_Alpha.configure(background="#d9d9d9")
chk_Alpha.configure(disabledforeground="#a3a3a3")
chk_Alpha.configure(foreground="#000000")
chk_Alpha.configure(highlightbackground="#d9d9d9")
chk_Alpha.configure(highlightcolor="black")
chk_Alpha.configure(justify=LEFT)
chk_Alpha.configure(text='''Alphabetize''')
chk_Alpha.configure(onvalue=1)
chk_Alpha.configure(offvalue=0)
chk_Alpha.configure(variable=val_Alpha)

chk_Stable = Checkbutton(lf_Configuration)
chk_Stable.place(relx=0.62, rely=0.79, relheight=0.08
                 , relwidth=0.18)
chk_Stable.configure(activebackground="#d9d9d9")
chk_Stable.configure(activeforeground="#000000")
chk_Stable.configure(background="#d9d9d9")
chk_Stable.configure(disabledforeground="#a3a3a3")
chk_Stable.configure(foreground="#000000")
chk_Stable.configure(highlightbackground="#d9d9d9")
chk_Stable.configure(highlightcolor="black")
chk_Stable.configure(justify=LEFT)
chk_Stable.configure(text='''Stable Move''')
chk_Stable.configure(onvalue=1)
chk_Stable.configure(offvalue=0)
chk_Stable.configure(variable=val_Stable)

lbl_Actions = Label(lf_Configuration)
lbl_Actions.place(relx=0.1, rely=0.79, height=21, width=49)
lbl_Actions.configure(background="#d9d9d9")
lbl_Actions.configure(disabledforeground="#a3a3a3")
lbl_Actions.configure(foreground="#000000")
lbl_Actions.configure(text='''Actions:''')

btn_Save = Button(top)
btn_Save.place(relx=0.02, rely=0.52, height=24, width=514)
btn_Save.configure(activebackground="#d9d9d9")
btn_Save.configure(activeforeground="#000000")
btn_Save.configure(background="#d9d9d9")
btn_Save.configure(disabledforeground="#a3a3a3")
btn_Save.configure(foreground="#000000")
btn_Save.configure(highlightbackground="#d9d9d9")
btn_Save.configure(highlightcolor="black")
btn_Save.configure(pady="0")
btn_Save.configure(text='''FireSave''')
btn_Save.configure(width=514)
btn_Save.configure(command=FireSave)

lf_Output = LabelFrame(top)
lf_Output.place(relx=0.02, rely=0.56, relheight=0.43, relwidth=0.96)

lf_Output.configure(relief=GROOVE)
lf_Output.configure(foreground="black")
lf_Output.configure(text='''Output''')
lf_Output.configure(background="#d9d9d9")
lf_Output.configure(width=520)

txt_Output = Text(lf_Output)
txt_Output.place(relx=0.02, rely=0.01, relheight=0.95
                 , relwidth=0.95)
txt_Output.configure(background="white")
txt_Output.configure(font="TkTextFont")
txt_Output.configure(foreground="black")
txt_Output.configure(highlightbackground="#d9d9d9")
txt_Output.configure(highlightcolor="black")
txt_Output.configure(insertbackground="black")
txt_Output.configure(relief=GROOVE)
txt_Output.configure(selectbackground="#c4c4c4")
txt_Output.configure(selectforeground="black")
txt_Output.configure(width=504)
txt_Output.configure(wrap=NONE)

# Display Window
top.mainloop()
