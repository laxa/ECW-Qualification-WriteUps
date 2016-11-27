#!/usr/bin/env python2

import binascii
import string
import sys

"""
I know from start that the key is going to be 16 bytes long since the flag format is ECW{md5}
from there, I try every byte value for each character of the key and take the one with the highest value according to
the percentage of those letter in the english language.
I end up with a text that isn't correct yet, but I can modify each letter by guessing the words that are in the text then
"""


freq = {"a": 8.167, "b": 1.492, "c":2.782, "d":4.253, "e":12.702, "f":2.228, "g":2.015, "h":6.094, "i":6.966, "j":0.153, "k":0.772, "l":4.025, "m":2.406, "n":6.749, " ":13, "o":7.507, "p":1.929, "q":0.095, "r":5.987, "s":6.327, "t":9.056, "u":2.758, "v":0.978, "w":2.360, "x":0.150, "y":1.974, "z":0.074}

data = ["7e:00:67:1f:a6:46:16:eb:57:8b:3b:63:e1:d2:ac:3f:55:49:70:12:e3:0c:12:ec:0e:dc:74:44:a4:d7:a8:24", "52:0c:76:5a:f2:44:18:fd:57:87:27:7f:af:dd:ed:3d:47:00:67:1f:a6:58:11:ec:57:81:35:7b:a4:9a:b5:26", "42:49:6f:1f:ff:0c:10:fa:57:80:31:77:ad:d6:b4:69:5e:06:70:5a:e7:0c:1e:e6:18:96:74:7f:a5:df:ac:67"]

tab = []
for x in data:
    res = ""
    for a in x.split(":"):
        res += chr(int(a, 16))
        if len(res) == 16:
            tab.append(res)
            res = ""

key = ""
if len(sys.argv) > 1:
    key = sys.argv[1]
    tmp = ""
    for x in [key[i:i+2] for i in range(0, len(key), 2)]:
        tmp += chr(int(x, 16))
    key = tmp
charset = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ"
possibKey = []
if len(key) == 0:
    for key_idx in range(0, 16):
        possibKey.append([])
        m = 0
        s = "A"
        for i in range(0, 256):
            value = 0
            for idx in range(0, len(tab)):
                tmpChar = chr(ord(tab[idx][key_idx]) ^ i)
                if tmpChar not in charset:
                    break
                value += freq[tmpChar.lower()]
                if idx == len(tab) - 1: # if last elem in the tab
                    #print "[%d] %d" % (key_idx, i)
                    #if len(key) == key_idx:
                        #key += chr(i)
                    #possibKey[key_idx].append(i)
                    if value > m:
                        m = value
                        s = chr(i)
        #if len(key) == key_idx:
            #key += chr(i)
        #if len(key) == key_idx:
        key += s

print "Key is: " + binascii.hexlify(key)

count = 0
buf = ""
charset += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for x in tab:
    for i in range(0, len(key)):
        buf += chr(ord(key[i]) ^ ord(x[i]))
    count += 1
    if count % 2 == 0:
        for z in buf:
            if z in charset:
                sys.stdout.write(z)
            else:
                #sys.stdout.write("\\x%02x" % ord(z))
                sys.stdout.write(".")
        buf = ""
        print ""

# flag is: ECW{3069047a862c798977f25416c1bacd49}
