# FireSave v.12
FireSave is a set of Python scripts that allows for the manipulation of Fire Pro Wrestling World save files. The tool has the following functionality:

**1. Complete all Missions with S Rank -** The script will modify the completion status for all missions to S rank, this will unlock all of the moves and edit points. 

**2. Move all Retired wrestlers to a specific Stable -** The script allows you choose a stable and assign all of the wrestlers in the Retire section to that stable. This allows you to quickly move all of the wrestlers downloaded from the Steam Workshop to a usable Stable so they can be accessed in the match modes.

**3. Alphabetize all wrestlers -** This functionality will allow you sort all of the wrestlers, regardless of their Promotion and Stable in alphabetical order. This includes the built in default wrestlers.

**4. Automatic assign wrestlers -** This function relys on the stables.csv and wrestlerlist.csv file to automatically assign the wrestlers to the specific stables. You can choose between All Wrestlers (ignores current stable) or Retire Only (moves wrestlers just in the Retire list).

I've gone through and have 1300+ setups already. I could use the communities help in adding to the list and having them sort out in to the proper stables.

Format of stables.csv and current stables:
"Promotion Short","Promotion Long","Stable Short","Stable Long","Alignment (0=Face,1=Neutral,2=Heel)"

**NJPW**
-   Bullet Club
-   Chaos
-   GBH
-   Hunter Club
-   Los Ingobernable
-   Main Unit
-   Suzuki-gun
-   Taguchi Japan

**WWE**
-   205 Live
-   Legacy
-   NXT
-   NXT F
-   Other
-   Modern
-   Modern F
-   UK

**ECW**
-   Roster

**WCW**
-   Roster

**AJPW**
-   Roster

**Lucha Underground**
-   Roster

**Indy**
-   Roster

**TNA**
-   Roster
  
Format of wrestlerlist.csv:
"Name 1","Name 2","Nickname","Promotion","Stable"

## Requirements

1. This script requires Python 2.7 ([https://www.python.org/download/releases/2.7/](https://www.python.org/download/releases/2.7/ "https://www.python.org/download/releases/2.7/"))

2. Download both the Python scripts as well as the 7-Zip command line tool 7za.exe that is included in this repo. The files need to be in the same directory.

3. Fire Pro Wrestling World must not be running as it locks the save file and prevents any editing.

4. Your save file is located in: C:\Users\YOUR WINDOWS USERNAME HERE\AppData\LocalLow\spikechunsoft\FireProWrestlingWorld\savedata.dat

5. To execute, just double click FireGUI.py and the user interface should become visible.

## Screenshot
![FireGUI](https://raw.githubusercontent.com/kactusken/firesave/master/FireGUI_v10.png "FireGUI")

## Special Thanks
Mike DG
Freem
Carlzilla
Madhat
FirePro community! 
