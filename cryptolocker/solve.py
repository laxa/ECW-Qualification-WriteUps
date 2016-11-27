#!/usr/bin/env python2

"""
This is a padding oracle attack, using https://github.com/mwielgoszewski/python-paddingoracle, I can have the flag nicely :)
"""

from paddingoracle import BadPaddingException, PaddingOracle
from base64 import b64encode, b64decode
from urllib import quote, unquote
import requests.packages.urllib3
import requests
import socket
import time

class PadBuster(PaddingOracle):
    def __init__(self, **kwargs):
        super(PadBuster, self).__init__(**kwargs)
        self.session = requests.Session()
        #self.wait = kwargs.get('wait', 2.0)

    def oracle(self, data, **kwargs):
        somecookie = quote(b64encode(data))
        self.session.cookies['session'] = "cookie"
        nonce = "nonce"

        while 1:
            try:
                response = self.session.post('https://challenge-ecw.fr/chals/crypto300',
                        stream=False, timeout=5, verify=False, data= {'nonce':nonce, 'ciphertext':b64encode(data)})
                break
            except (socket.error, requests.exceptions.RequestException):
                logging.exception('Retrying request in %.2f seconds...',
                                  self.wait)
                time.sleep(self.wait)
                continue

        self.history.append(response)

        if "est valide" in response.text:
            logging.debug('No padding exception raised on %r', somecookie)
            return

        # An HTTP 500 error was returned, likely due to incorrect padding
        raise BadPaddingException

if __name__ == '__main__':
    import logging
    import sys

    requests.packages.urllib3.disable_warnings()
    logging.basicConfig(level=logging.INFO)

    encrypted_cookie = b64decode(sys.argv[1])
    padbuster = PadBuster()
    cookie = padbuster.decrypt(encrypted_cookie, block_size=16, iv=None)
    print('Decrypted input: %s => %r' % (sys.argv[1], cookie))

# flag is: ECW{b4ee274543dc15a0cdf825d846e6fb3f}
