#!/usr/bin/python3

import sys
import argparse
import os

def getargs():
    parser = argparse.ArgumentParser(description='Generate pwn exploit script template')
    parser.add_argument('--binary', '-b', required=True, type=str, default=None, help='Name of the binary to be run')
    parser.add_argument('--remote', '-ip', type=str, default=None, help='Remote IP')
    parser.add_argument('-port', '-p', type=int, default=None, help='Remote port')
    parser.add_argument('--libc', '-l', type=str, default=None, help='Name of libc')
    parser.add_argument('--arch', '-a', type=str, default='amd64', help='Architecture of binary')
    return parser.parse_args()

def getscript(ip, port, binary, libc, arch):
    return f"""#!/usr/bin/python

from pwn import *
import sys

remote_ip, port = '{ip if ip else ""}', {port if port else ""}
binary = '{f"./{binary}" if binary else ""}'
brkpts = '''
'''

elf = ELF("{binary}")
libc = ELF("{libc if libc else '/lib/x86_64-linux-gnu/libc.so.6'}")

context.terminal = ['tmux', 'splitw', '-h']
context.arch = "{arch}"
context.log_level = "debug"
context.aslr = False

re = lambda a: io.recv(a)
reu = lambda a: io.recvuntil(a)
rl = lambda: io.recvline()
s = lambda a: io.send(a)
sl = lambda a: io.sendline(a)
sla = lambda a,b: io.sendlineafter(a,b)
sa = lambda a,b: io.sendafter(a,b)

if len(sys.argv) > 1:
    io = remote(remote_ip, port)

else:
    io = process(binary{", env = {'LD_PRELOAD' : './" + libc + "'})" if libc else ")"}

if __name__ == "__main__":
    #Write exploit here
    io.interactive()
"""

if __name__ == "__main__":
    args = getargs()
    script = getscript(args.remote, args.port, args.binary, args.libc, args.arch)
    if os.path.exists("exp.py"):
        f = open("newexp.py", "w+")
    else:
        f = open("exp.py", "w+")
    f.write(script)
