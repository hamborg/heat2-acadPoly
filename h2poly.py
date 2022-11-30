import os
import pathlib as pl
import keyboard
from copy import copy
import re
import time
import pyperclip


def printline(x,y):
    if x: start = '\n'
    else: start = ''
    if y: end = '\n'
    else: end = ''
    print(start+'- - - - - - - - - - - - - - - - - - - - -'+end)

def extCoords(text):
    if text.strip().startswith('at point'):
        coordsRaw = re.findall('-?\d+\.?\d*',text)
        x = str(round(float(coordsRaw[0])/scale,3))
        y = str(round(float(coordsRaw[1])/scale,3))
        return x + ' ' + y + ' \t'
    else: return ''

def testrec(lines, i, mline):
    if lines[i-1].strip().lower().startswith('at point') and lines[i-2].strip().lower().startswith('at point') and lines[i-3].strip().lower().startswith('at point') and lines[i-4].strip().lower().startswith('at point'):
        reclines = lines[i-4:i]
        x = []; y = []

        for text in reclines:
            coords = re.findall('-?\d+\.?\d*',text)
            x.append(coords[0])
            y.append(coords[1])

        # Kontrol: to sæt ens koordinater
        if not len([*set(x)]) == len([*set(y)]) == 2: return mline
        
        # Kontrol: skiftende koordinater, som er ens
        x.insert(0, x.pop()) # Forskyd liste x for at matche liste y
        if (x[0] == x[-1] and y[0] == y[-1] and x[1] == x[2] and y[1] == y[2]) \
        or (x[0] == x[1] and y[0] == y[1] and x[2] == x[3] and y[2] == y[3]):
            # Der er nu en rektangel
            mpos = mline.rfind('m \t')
            keepline = mline[:mpos]
            sCoords = mline[mpos:].split()[1:]
            
            sbox = [sCoords[0], sCoords[1], str(round(float(sCoords[4]) - float(sCoords[0]),3)), str(round(float(sCoords[5]) - float(sCoords[1]),3))]
            instext = ['s \t',' \t',' \t',' \t']

            sline = ""
            for (s,t) in zip(sbox,instext):
                sline += t+s

            return keepline + sline + ' \t'
        else: return mline # Ikke et rekt

    else: return mline # Ikke 'at point' i alle 4 linjer

def finish():
    if input('- Run again? (Enter \'x\' to exit.) \n- ').lower() not in ['exit','x','n','no']:
        return True

errorfile =  'If you see this message and Notepad does not close automatically, an error occured...\n'
errorfile += 'The objects are still copied, but if you paste them to HEAT2 now, the objects might not show in individuel lines. (Try it for yourself?)\n\n'
errorfile += '- - SOULUTION: - -\nMark all text in here, paste the code, mark it again and copy it. Now the code is ready for HEAT2.\n'
errorfile += 'Press and hold the CTRL key and press the following combination:\n\n'
errorfile += '(Ctrl) + A\n'
errorfile += '(Ctrl) + V\n'
errorfile += '(Ctrl) + A\n'
errorfile += '(Ctrl) + C\n\n'
errorfile += 'Then close Notepad. (No need to save the file.)\n'
errorfile += 'Sorry for inconvenience!'

### SCRIPT START ###
printline(1,0)
print('| - Script by Lasse Hamborg - 27.10.2022 -')
print('| ')
print('| This programme translates AutoCAD polylines to HEAT2-script lines.')
print('| ')
print('| - - - - -')
print('| ')
print('| First:\tRun the \'LIST\' command in AutoCAD on the polylines you want to translate.')
print('| ')
print('| Second:\tCopy the lines containing the polyline coordinates.')
print('| \t\tThis programme here takes the coordinates of the lines with \'at point...\' coordinates.')
print('| ')
print('| Third:\tIf multiple polylines are entered, the programme will make an object for each.')
print('| ')
print('| Lastly:\tThe new HEAT2 objects are copied to the clipboard via this programme.')
print('| \t\tNow simply, paste these directly into your HEAT2 script and assign materials.')
print('| \t\tVoila!...')
print('| \t\t(Psst: check the hint at the end of this programme for easier overview.)')
printline(0,1)
time.sleep(0.5)

### SCALE
scale = 1000
print('Scale factor is 1000 (i.e.: mm --> m).')
valg = input('If you want to change this, write a new scalefactor (number). Else, press ENTER:\n- ')
if len(valg) > 0 :
    try:
        scale = float(valg)
        print('Scale factor changed to',scale)
    except: print('Invalid number! Scale remains at', scale)
    finally: time.sleep(0.5)
else: print('(Scale remains: ' + str(scale) + ')')

### LOOP IGENNEM 'LIST'
scriptOn = True
while scriptOn:
    i = 0
    lines = []

    startline = 'm \t'
    copyline = startline
    matr = 'INSET_MATR_HERE'
    morepolys = False

    time.sleep(0.5)
    print('\n- Paste polyline coordinates from AutoCAD (\'LIST\'): (Press ENTER (twice) when done)')
    while True:
        inputText = input('')
        if inputText.strip().lower().startswith('press enter'): continue

        copyline += extCoords(inputText)
        lines.append(inputText)

        if len(lines) > 2:
            # Tests for multiple polygons:
            if lines[i-2].strip().lower().startswith('at point') and lines[i].strip().lower().startswith('lwpoly'):
                # print('hej')
                copyline += matr + '\n' + startline
                morepolys = True

            # Script ends with two empty lines:
            if len(lines[i-1]) < 1 and len(lines[i]) < 1:
                break

        # Tests for rectangle object:
        if len(lines) > 5:
            if len(lines[i]) < 1 and len(lines[i-5]) < 1:
                copyline = testrec(lines, i, copyline)

        i += 1
    
    copyline += matr

    # Tests for empty 'matr.-line' at the end:
    delIdx = copyline.rfind(startline)
    if copyline[delIdx:].startswith(startline+matr):
        copyline = copyline[:delIdx-1]


# # # # # # PUT OBJECTS IN CLIPBOARD # # # # # #
    if copyline == startline + matr:
        print('- - - - - No coordinates found! - - - - -')
        print('Use \'LIST\' in AutoCAD and copy all the coordinates (\"at point X=... Y=...\") into the script.')
        time.sleep(1)
        print('\nPlease, try again.')
        printline(0,1)
        time.sleep(1)
        scriptOn = finish()

    else:
        pyperclip.copy(copyline)

        print('- - - - DONE! - - - - -\n')
        time.sleep(0.5)
        print('This code for the object(s) is now copied to the clipboard:')
        print(copyline)

        ### Tests for multiple objects:
        if morepolys:
            time.sleep(0.5)
            print('\nWAIT! Pasting more polygons to HEAT2 is not perfect. Hence Notepad will now open to copy/paste into this.')
            print('Please wait a few seconds.')
            try:
                time.sleep(0.5)
                fw = open('dummy.txt',"w")
                fw.write(errorfile)
                fw.close()

                ### Use Notepad as pasting board:
                os.startfile(pl.Path(str('dummy.txt')))
                time.sleep(0.2) # If the errorfile message shows, and Notepad does not close again, increase this number (seconds).
                keyboard.press_and_release('ctrl+a')
                keyboard.press_and_release('ctrl+v')
                keyboard.press_and_release('ctrl+a')
                keyboard.press_and_release('ctrl+x')
                keyboard.press_and_release('ctrl+w')
                keyboard.press_and_release('alt+n')
                
                print('\n- - Success! Now, paste it into your HEAT2 script! - -\n')
                
                time.sleep(0.2)
                os.remove('dummy.txt')
            except:
                time.sleep(5)
                printline(1,0)
                print('OBS! Notepad could not be opened!\n')
                time.sleep(5)
                print('Please, OPEN NOTEPAD manually, paste it and copy everything again from there (Ctrl + V -- Ctrl + A -- Ctrl + C).')
                print('Now paste into your HEAT2 script!')
                print('You can then just close Notepad again.\n')
                printline(0,1)
                time.sleep(30)
        else:
            time.sleep(0.5)
            print('\n- - Paste it into your HEAT2 script! - -\n')

        
        ### END OF SCRIPT
        time.sleep(1)
        
        printline(0,0)
        print('| - HINT! -')
        print('| ')
        print('| In HEAT, the material of an object is either entered at the end of the line or from the line above.')
        print('| Thus, make a line above the object with the material in an \'empty\' object:')
        print('| \'s 0 0 0 0 MATERIAL\'')
        print('| (your object goes here)')
        print('| ')
        print('| In this way, you can more easily see the materials of complex objects.')
        printline(0,1)

        time.sleep(10)
        scriptOn = finish()

print('\nGoodbye!\n')
try: os.remove('dummy.txt'); print('fil blev slettet')
except: 1+1
finally:
    time.sleep(2)
quit()
