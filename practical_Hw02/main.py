import base64
import os
from hashlib import pbkdf2_hmac

import pbkdf2
import binascii
import secrets
import pyaes

salt = os.urandom(16)
final_key = pbkdf2.PBKDF2("2022*ICTSec*A", salt).read(32)

random = secrets.randbelow(100)
counter = pyaes.Counter(random)
aes = pyaes.AESModeOfOperationCTR(final_key, counter)
aes2 = pyaes.AESModeOfOperationCTR(final_key, counter)

enter = input("choose E for encryption and D for decryption")
while (1):

    if enter == "E":
        print("here's the encrypted key: " + str(binascii.hexlify(final_key)))
        with open("stunum.txt", 'r') as filer:
            ciphertxt = filer.readline()
            ciphertxt = aes.encrypt(ciphertxt)
            filer.close()
        with open("result.txt", 'wb') as file:
            file.write(binascii.hexlify(ciphertxt))
            file.close()
    elif enter == 'D':
        with open("result.txt", "r+b")as file:
            cipher = file.readline()
            cipher = binascii.unhexlify(cipher)
            file.close()
        with open("decode.txt", 'wb') as file:
            file.write(aes2.decrypt(cipher))
            file.close()
    enter = input()
