#!/usr/bin/env python2

"""
There is nothing much to say, this challenge is pretty straighfowards
I used pil to remove the color on the captcha and then gocr gives a pretty high success rate
"""


from pwn import *
import qrtools
import urllib
import cairosvg
import Image
import requests
import base64
import urllib
import sys
import re
import json

cookie = dict(session="cookie")
nonce = "nonce"
req = requests.get("https://challenge-ecw.fr/chals/divers200", cookies=cookie)
data = req.text
cookie['session'] = req.cookies['session']
qrcode = re.findall("QRCode\" src=\"data:image/png;base64,([^\"]+)", data)[0]
with open("qrcode.png", "wb") as f:
    f.write(base64.b64decode(qrcode))
qr = qrtools.QR()
qr.decode("qrcode.png")
captcha = re.findall("Captcha\" src=\"data:image/png;base64,([^\"]+)", data)[0]
with open("captcha.png", "wb") as f:
    f.write(base64.b64decode(captcha))
picture = Image.open("captcha.png")
pic = picture.convert('RGB')
width, height = pic.size
for x in range(0, width):
    for y in range(0, height):
        r,g,b = pic.getpixel( (x,y) )
        if r != 255:
            pic.putpixel((x,y), (255, 255, 255))
pic.save("captcha_solved.png")
r = process(["/usr/bin/gocr", "-i", "captcha_solved.png"]).recvall()
cap = r.strip()
qrcode = qr.data.rstrip()

print "Got qr: %s - cap: %s" % (qrcode, cap)

ret = requests.post("https://challenge-ecw.fr/chals/divers200", data={'nonce':nonce, 'captcha':cap, 'qrcode':qrcode}, cookies=req.cookies)
#print ret.text
if "Captcha Win" not in ret.text:
    print "Failed step 1"
    exit()

win = re.findall("Captcha Win\" src=\"data:image/png;base64,([^\"]+)", ret.text)[0]
with open("captcha_win.png", "wb") as f:
    f.write(base64.b64decode(win))

bbb = Image.open("captcha_win.png")
aaa = bbb.convert('RGB')
width, height = aaa.size
for x in range(0, width):
    for y in range(0, height):
        r,g,b = aaa.getpixel( (x,y) )
        if r != 255:
            aaa.putpixel((x,y), (255, 255, 255))
aaa.save("captcha_win_solved.png")
r = process(["/usr/bin/gocr", "-i", "captcha_win_solved.png"]).recvall()


win = re.findall("QRCode Win\" src=\"data:image/png;base64,([^\"]+)", ret.text)[0]
with open("QRCode_win.png", "wb") as f:
    f.write(base64.b64decode(win))
qr.decode("QRCode_win.png")
print r.rstrip() + qr.data

# flag is: ECW(20cbf8e17eb7e62936e3602b498776e6}
