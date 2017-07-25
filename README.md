# firesave
Python script for manipulation of Fire Pro Wrestling World save files.

Functionality:
1. Complete all Missions (-m)

  python FireSave.py -m savedata.dat

2. List all Promotions and Stables (-s)

  python FireSave.py -s savedata.dat
  
  The number value is the Stable ID that can be used for:

3. Move all Retired wrestlers to a specific stable (-r stableid)

  python FireSave.py -r 5 savedata.data
