
import os
import keyboard
import time

#makes the table array
def tablemaker():
    alphabetstring = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphabetstring2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[::-1]
    rowlist1 = [''] * 26
    rowlist2 = [''] * 26
    rowlist = [''] * 26
    flag = True
    z = 0
    while flag == True:
        temparr = [] * 26
        for y in range(z, len(alphabetstring)):
            temparr.append(alphabetstring[y])
        rowlist1[z] = temparr
        if z >= 25:
            flag = False
        z += 1
    flag = True
    z = 0
    while flag == True:
        temparr = [] * 26
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

#forms an array of all aplhabets in order
def alphabetlist():
    alphabetarray = []
    alphabetstring = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for item in alphabetstring:
        alphabetarray.append(item)
    return alphabetarray

#returns the positions of the spaces in the original text along with the text w/o spaces
def remove_spaces(input_string):
    space_positions = [i for i, char in enumerate(input_string) if char == ' ']
    modified_string = input_string.replace(' ', '')
    return modified_string, space_positions

#this takes the original string without spaces and the space position, returning the text with spaces
def add_spaces(input_string, space_positions):
    original_string_list = list(input_string)
    for pos in space_positions:
        original_string_list.insert(pos, ' ')
    original_string = ''.join(original_string_list)
    return original_string

#takes a key and plaintext to return the keystring(key repeated to fit plaintext length)
#removes spaces from the plaintext by sending it to the remove spaces function
#returns the keystring along with some other stuff
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
    return keystring , string_without_spaces, space_positions, plaintext

#imports the table array from the tablemaker function
#imports keystring and other neccesary data from the generatingkeystring array by using the key letter and single plaintext element
#uses the rowlist vignere table contained in 'rowlist' to encrypt the letter
#returns the encrypted letter
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

#uses the table array from tablemaker to decrypt simply
#uses the add_spaces function to return the original text including the spaces
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

#for each text letter and key letter, it forms a table with dots along the key column and row
#prints said table using the tableprinter function for each iteration
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

#adds spaces and prints the table contained in the rowlist array
def tableprinter(rowlist):
    print("_____________________________________")
    for row in rowlist:
        string2n = ''
        for element in row:
            string2n = string2n+' '+element
        print(string2n)
    print("_____________________________________")

#this function manages all encryptions
#imports a keystring by inserting the single word key and a plaintext placeholder X which is 2000 character long
def encoutput(key):
    keystring, x, y, z = generatingkeystring(key, 'x'*2000)
    keystringcounter1 = 0
    string2a = ''
    string2b = ''
    string2c = ''
    #takes and registers keyboard inputs and categorizes keypresses to their corresponding outputs
    def on_key_event(event):
        nonlocal keystringcounter1
        nonlocal string2a
        nonlocal string2b
        nonlocal string2c
        letter = event.name
        #Outputs the entire table and cipher/plain texts for each key pressed
        def encscreen(string2a, string2b, letter, string2c):
            nonlocal keystringcounter1
            nonlocal keystring
            os.system('cls')
            print("press 'esc' to confirm")
            enctablecreator(letter, keystring[keystringcounter1-1])
            print("_____________________________________")
            print(f'Plaintext  > {string2a}')
            print("")
            print(f'Keystring  > {string2c}')
            print("")
            print(f'Ciphertext > {string2b}')
            print("_____________________________________")

        if letter.upper() in alphabetlist():
            cipher = encrypting(keystring[keystringcounter1], letter)
            keystringcounter1 += 1
            string2a = string2a + letter
            string2b = string2b + cipher
            string2c = string2c + keystring[keystringcounter1-1]
            encscreen(string2a, string2b, letter, string2c)

        elif letter == 'space':
            string2a = string2a + ' '
            string2b = string2b + ' '
            string2c = string2c + ' '
            encscreen(string2a, string2b, letter, string2c)

        elif letter == 'backspace' and string2a != '' and string2b != '' and string2c != '':
            if string2a[-1] != ' ' and string2b[-1] != ' ' and string2c[-1] != ' ':
                keystringcounter1 -= 1
            string2a = string2a[:-1]
            string2b = string2b[:-1]
            string2c = string2c[:-1]
            encscreen(string2a, string2b, letter, string2c)

    os.system('cls')
    print("press 'esc' to confirm")
    print("_____________________________________")
    print(f'Plaintext  > {string2a}')
    print("")
    print(f'Keystring  > {string2c}')
    print("")
    print(f'Ciphertext > {string2b}')
    print("_____________________________________")

    keyboard.on_press(on_key_event)
    keyboard.wait("esc")
    keyboard.unhook_all()
    input("Press Enter to Exit")
    return -2

#this function manages all decryptions
#used to automatically decrypt a previously inputted cipher
def decoutput(key, cipher):
    keystring, x, y, z = generatingkeystring(key, 'x'*2000)
    keystringcounter1 = 0
    string2a = ''
    string2b = ''
    string2c = ''
    #takes and registers keyboard inputs and categorizes keypresses to their corresponding outputs
    def eachletter(event):
        nonlocal keystringcounter1
        nonlocal string2a
        nonlocal string2b
        nonlocal string2c
        letter = event
        #Outputs the entire table and cipher/plain texts for each key pressed
        def encscreen(string2a, string2b, letter, cipher, string2c):
            nonlocal keystringcounter1
            nonlocal keystring
            os.system('cls')
            print("press 'esc' to confirm")
            enctablecreator(keystring[keystringcounter1-1], cipher)
            print("_____________________________________")
            print(f'Ciphertext > {string2a}')
            print("")
            print(f'Keystring  > {string2c}')
            print("")
            print(f'Plaintext  > {string2b}')
            print("_____________________________________")
            time.sleep(0.25)

        if letter.upper() in alphabetlist():
            cipher = decrypting(keystring[keystringcounter1], letter)
            keystringcounter1 += 1
            string2a = string2a + letter
            string2b = string2b + cipher
            string2c = string2c + keystring[keystringcounter1-1]
            encscreen(string2a, string2b, letter, cipher, string2c)

        elif letter == ' ':
            string2a = string2a + ' '
            string2b = string2b + ' '
            string2c = string2c + ' '
            encscreen(string2a, string2b, letter, letter, string2c)

    os.system('cls')
    print("press 'esc' to confirm")
    print("_____________________________________")
    print(f'Ciphertext > {string2a}')
    print("")
    print(f'Keystring  > {string2c}')
    print("")
    print(f'Plaintext  > {string2b}')
    print("_____________________________________")
    for letter in cipher:
        eachletter(letter)
    
    input("Press Enter to Exit")
    return -2



def main():
    os.system('cls')
    while True:
        os.system('cls')
        password = input("Enter Password: ")
        if password == "hello_world":
            os.system('cls')
            print("Correct Password")
            print("Maximize the program to avoid cutting")
            while True:
                print("_____________________________________")
                print("Enter 1 for Encryption")
                print("Enter 2 for Decryption")
                print("Enter 3 for Exiting")
                print("")
                print("Then press enter")
                print("_____________________________________")
                while True:
                    try:
                        encchoice = int(input(">"))
                        os.system('cls')
                        break
                    except:
                        print("invalid input, try again: ")
                if encchoice == 1:
                    keyenc = input("Enter the key to be used for encryption: ")
                    print("_____________________________________")
                    response = encoutput(keyenc)
                    os.system('cls')
                    print("\n")
                    if response == -2:
                        print("_____________________________________")
                        print(f"Encrypted using the key [{keyenc}]")
                        print("_____________________________________")
                    input("Press Enter to Continue")
                elif encchoice == 2:
                    while True:
                        try:
                            cipher = input(">Enter encrypted text below or type 'x' to return: \n\n")
                            print("_____________________________________")
                            keydec = input("Enter the key that was used to encrypt the message: ")
                            if cipher == 'x' or cipher == 'X':
                                break
                            else:
                                os.system('cls')
                                complete = decoutput(keydec, cipher)
                                print("\n")
                                print("_____________________________________")
                                print(f"Decrypted using the key [{keydec}]")
                                print("_____________________________________")
                                input("Press Enter to Continue")
                                break

                        except:
                            print("Invalid cipher, try again or type 'x' to return:")
                elif encchoice == 3:
                    return -1
                else:
                    print("INVALID INPUT")
                    input("Press Enter to Retry")
                os.system('cls')
        else:
            os.system('cls')
            print("Incorrect Password, try again or contact ayaan for password details.")

try:
    main()
    keyboard.unhook_all()
except Exception as e:
    keyboard.unhook_all()
    print(e)
    print("Press Enter To Exit")

#issues to note
#1- limit of 2000 characters for encrypting
#2- crashes if the encryption key has a space in it
#3- unable to copy and paste into the encryption bar
