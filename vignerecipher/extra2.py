import curses
import os
import keyboard

def tablemaker():
    alphabetstring = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphabetstring2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[::-1]
    rowlist1 = [''] * 26
    rowlist2 = [''] * 26
    rowlist = [''] * 26
    flag = True
    z = 0
    while flag:
        temparr = []
        for y in range(z, len(alphabetstring)):
            temparr.append(alphabetstring[y])
        rowlist1[z] = temparr
        if z >= 25:
            flag = False
        z += 1
    flag = True
    z = 0
    while flag:
        temparr = []
        for y in range(z, len(alphabetstring)):
            temparr.append(alphabetstring2[y])
        rowlist2[z] = temparr
        if z >= 25:
            flag = False
        z += 1
    rowlist3 = rowlist2[::-1]
    for f in range(0, 26):
        rowlist[f] = rowlist1[f] + rowlist3[f][::-1]
    for g in range(len(rowlist)):
        rowlist[g].pop()
    return rowlist

def alphabetlist():
    alphabetarray = []
    alphabetstring = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for item in alphabetstring:
        alphabetarray.append(item)
    return alphabetarray

def remove_spaces(input_string):
    space_positions = [i for i, char in enumerate(input_string) if char == ' ']
    modified_string = input_string.replace(' ', '')
    return modified_string, space_positions

def add_spaces(input_string, space_positions):
    original_string_list = list(input_string)
    for pos in space_positions:
        original_string_list.insert(pos, ' ')
    original_string = ''.join(original_string_list)
    return original_string

def generatingkeystring(key, plaintext):
    plaintext = plaintext.upper()
    key = key.upper()
    original_string = plaintext
    string_without_spaces, space_positions = remove_spaces(original_string)
    plaintext = string_without_spaces
    word_length = len(key.split()[0])
    repetitions = (len(plaintext) // word_length) + 1
    extended_string = key * repetitions
    extended_string = extended_string[:len(plaintext)]
    keystring = extended_string
    return keystring, string_without_spaces, space_positions, plaintext

def encrypting(key, plaintext1):
    rowlist = tablemaker()
    keystring, string_without_spaces, space_positions, plaintext = generatingkeystring(key, plaintext1)
    string1 = ''
    for p in range(0, len(plaintext)):
        for u in range(0, 26):
            if rowlist[u][0] == keystring[p]:
                for k in range(0, len(rowlist[0])):
                    if rowlist[0][k] == plaintext[p]:
                        string1 = string1 + rowlist[u][k]
                        break
                break
    original_string_back = add_spaces(string1, space_positions)
    ciphertext = original_string_back
    return ciphertext

def decrypting(key, ciphertext1):
    rowlist = tablemaker()
    keystring, string_without_spaces, space_positions, ciphertext = generatingkeystring(key, ciphertext1)
    string1 = ''
    for p in range(0, len(ciphertext)):
        for u in range(0, 26):
            if rowlist[u][0] == keystring[p]:
                for k in range(0, len(rowlist[u])):
                    if rowlist[u][k] == ciphertext[p]:
                        string1 = string1 + rowlist[0][k]
                        break
                break
    original_string_back = add_spaces(string1, space_positions)
    plaintext = original_string_back
    return plaintext

def enctablecreator(letter, key):
    letter = letter.upper()
    rowlist = tablemaker()
    alphabetarray = alphabetlist()
    if letter in alphabetarray and key in alphabetarray:
        rowindex = 0
        columnindex = 0
        for row in range(0, len(rowlist)):
            if rowlist[row][0] == letter:
                rowindex += row
                break
        for col in range(0, len(rowlist[0])):
            if rowlist[0][col] == key:
                columnindex += col
                break
        for y in range(0, len(rowlist[rowindex])):
            if rowlist[rowindex][y] != rowlist[rowindex][columnindex]:
                rowlist[rowindex][y] = '·'#■
        for x in range(0, len(rowlist)):
            if rowlist[x][columnindex] != rowlist[rowindex][columnindex]:
                rowlist[x][columnindex] = '·'#■
    tableprinter(rowlist)

def tableprinter(rowlist):
    print("_____________________________________")
    for row in rowlist:
        string2n = ''
        for element in row:
            string2n = string2n+' '+element
        print(string2n)
    print("_____________________________________")

def encoutput(key):
    keystring, x, y, z = generatingkeystring(key, 'x'*2000)
    keystringcounter1 = 0
    string2a = ''
    string2b = ''
    
    def on_key_event(event):
        nonlocal keystringcounter1, string2a, string2b, stdscr
        letter = event.name

        def encscreen(string2a, string2b, letter):
            nonlocal keystringcounter1, keystring, stdscr
            stdscr.clear()
            stdscr.addstr(0, 0, "press 'esc' to confirm\n")
            enctablecreator(letter, keystring[keystringcounter1-1])
            stdscr.addstr(1, 0, "_____________________________________\n")
            stdscr.addstr(2, 0, f'Plaintext  > {string2a}\n')
            stdscr.addstr(3, 0, f'Ciphertext > {string2b}\n')
            stdscr.addstr(4, 0, "_____________________________________\n")
            stdscr.refresh()

        if letter.upper() in alphabetlist():
            cipher = encrypting(keystring[keystringcounter1], letter)
            keystringcounter1 += 1
            string2a = string2a + letter
            string2b = string2b + cipher
            encscreen(string2a, string2b, letter)

        elif letter == 'space':
            string2a = string2a + ' '
            string2b = string2b + ' '
            encscreen(string2a, string2b, letter)

        elif letter == 'backspace' and string2a != '' and string2b != '':
            if string2a[-1] != ' ' and string2b[-1] != ' ':
                keystringcounter1 -= 1
            string2a = string2a[:-1]
            string2b = string2b[:-1]
            encscreen(string2a, string2b, letter)

    stdscr.clear()
    stdscr.addstr(0, 0, "press 'esc' to confirm\n")
    stdscr.addstr(1, 0, "_____________________________________\n")
    stdscr.addstr(2, 0, f'Plaintext  > {string2a}\n')
    stdscr.addstr(3, 0, f'Ciphertext > {string2b}\n')
    stdscr.addstr(4, 0, "_____________________________________\n")
    stdscr.refresh()

    keyboard.on_press(on_key_event)
    keyboard.wait("esc")
    keyboard.unhook_all()
    stdscr.addstr(5, 0, "Press Enter to Exit\n")
    stdscr.refresh()
    stdscr.getkey()

def main():
    curses.wrapper(_main)

def _main(stdscr):
    stdscr.clear()
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Enter Password: ")
        stdscr.refresh()
        password = stdscr.getstr().decode('utf-8')
        if password == "hello_world":
            stdscr.clear()
            stdscr.addstr(0, 0, "Correct Password\nMaximize the program to avoid cutting\n")
            stdscr.refresh()
            while True:
                stdscr.addstr(1, 0, "_____________________________________\n")
                stdscr.addstr(2, 0, "Enter 1 for Encryption\n")
                stdscr.addstr(3, 0, "Enter 2 for Decryption\n")
                stdscr.addstr(4, 0, "Enter 3 for Exiting\n")
                stdscr.addstr(5, 0, "Then press enter\n")
                stdscr.addstr(6, 0, "_____________________________________\n")
                stdscr.refresh()
                while True:
                    try:
                        stdscr.addstr(7, 0, ">")
                        stdscr.refresh()
                        encchoice = int(stdscr.getstr().decode('utf-8'))
                        stdscr.clear()
                        break
                    except:
                        stdscr.addstr(7, 0, "Invalid input, try again: ")
                        stdscr.refresh()
                if encchoice == 1:
                    stdscr.addstr(0, 0, "Enter the key to be used for encryption: ")
                    stdscr.refresh()
                    keyenc = stdscr.getstr().decode('utf-8')
                    stdscr.addstr(1, 0, "_____________________________________\n")
                    stdscr.refresh()
                    response = encoutput(keyenc)
                    stdscr.clear()
                    if response == -2:
                        stdscr.addstr(0, 0, "_____________________________________\n")
                        stdscr.addstr(1, 0, f"Encrypted using the key [{keyenc}]\n")
                        stdscr.addstr(2, 0, "_____________________________________\n")
                        stdscr.refresh()
                    stdscr.addstr(3, 0, "Press Enter to Continue\n")
                    stdscr.refresh()
                    stdscr.getkey()
                elif encchoice == 2:
                    while True:
                        stdscr.addstr(0, 0, ">Enter encrypted text below or type 'x' to return:\n\n")
                        stdscr.addstr(2, 0, "_____________________________________\n")
                        stdscr.refresh()
                        cipher = stdscr.getstr().decode('utf-8')
                        if cipher.lower() == 'x':
                            break
                        stdscr.addstr(3, 0, "Enter the key that was used to encrypt the message: ")
                        stdscr.refresh()
                        keydec = stdscr.getstr().decode('utf-8')
                        stdscr.clear()
                        complete = decrypting(keydec, cipher)
                        stdscr.addstr(0, 0, "\n>Decrypted text below:\n")
                        stdscr.addstr(2, 0, "_____________________________________\n")
                        stdscr.addstr(3, 0, f"{complete}\n")
                        stdscr.addstr(4, 0, "_____________________________________\n")
                        stdscr.addstr(5, 0, f"Decrypted using the key [{keydec}]\n")
                        stdscr.addstr(6, 0, "_____________________________________\n")
                        stdscr.addstr(7, 0, "Press Enter to Continue\n")
                        stdscr.refresh()
                        stdscr.getkey()
                        break
                elif encchoice == 3:
                    return -1
                else:
                    stdscr.addstr(0, 0, "INVALID INPUT\nPress Enter to Retry\n")
                    stdscr.refresh()
                    stdscr.getkey()
                stdscr.clear()
        else:
            stdscr.clear()
            stdscr.addstr(0, 0, "Incorrect Password, try again or contact ayaan for password details.\n")
            stdscr.refresh()

try:
    curses.wrapper(main)
    keyboard.unhook_all()
except Exception as e:
    keyboard.unhook_all()
    print(e)
    print("Press Enter To Exit")
