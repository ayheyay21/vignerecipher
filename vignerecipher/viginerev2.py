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
    rowlist = tablemaker()
    original_string = plaintext
    string_without_spaces, space_positions = remove_spaces(original_string)
    plaintext = string_without_spaces
    word_length = len(key.split()[0])
    repetitions = (len(plaintext) // word_length) + 1
    extended_string = key * repetitions
    extended_string = extended_string[:len(plaintext)]
    keystring = extended_string
    return keystring , string_without_spaces, space_positions, plaintext


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

def tableprinter(rowlist):
    for l in range(0, len(rowlist)):
        print(rowlist[l])

def encoutput(key):
    keystring, x, y, z = generatingkeystring(key, 'x'*5000)
    keystringcounter1 = 0
    string2a = ''
    string2b = ''
    def on_key_event(event):
        nonlocal keystringcounter1
        nonlocal string2a
        nonlocal string2b
        letter = event.name
        def encscreen(string2a, string2b):
            os.system('cls')
            print("press 'esc' to confirm")
            print("_____________________________________")
            print(f'Plaintext  > {string2a}')
            print("")
            print(f'Ciphertext > {string2b}')
            print("_____________________________________")

        if letter.upper() in alphabetlist():
            cipher = encrypting(keystring[keystringcounter1], letter)
            keystringcounter1 += 1
            string2a = string2a + letter
            string2b = string2b + cipher
            encscreen(string2a, string2b)

        elif letter == 'space':
            string2a = string2a + ' '
            string2b = string2b + ' '
            encscreen(string2a, string2b)

        elif letter == 'backspace' and string2a != '' and string2b != '':
            if string2a[-1] != ' ' and string2b[-1] != ' ':
                keystringcounter1 -= 1
            string2a = string2a[:-1]
            string2b = string2b[:-1]
            encscreen(string2a, string2b)

    keyboard.on_press(on_key_event)
    keyboard.wait("esc")
    keyboard.unhook_all()
    input("Press Enter to Exit")

def main():
    os.system('cls')
    while True:
        os.system('cls')
        password = input("Enter Password: ")
        if password == "hello_world":
            os.system('cls')
            print("Correct Password")
            while True:
                print("_____________________________________")
                print("Enter 1 for Encryption")
                print("Enter 2 for Decryption")
                print("Enter 3 to quit program")
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
                    message = input(">Enter the message to be encrypted below: \n\n")
                    print("_____________________________________")
                    keyenc = input("Enter the key to be used for encryption: ")
                    print("_____________________________________")
                    complete = encrypting(keyenc, message)
                    os.system('cls')
                    print("\n")
                    print(">Encrypted text below:")
                    print("_____________________________________")
                    print(f"{complete}")
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
                                complete = decrypting(keydec, cipher)
                                print("\n")
                                print(">Decrypted text below:")
                                print("_____________________________________")
                                print(f"{complete}")
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

encoutput('cinnamon')


