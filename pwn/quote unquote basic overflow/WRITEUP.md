# quote unquote very basic overflow

First thing you want to check out whenever you get any sort of pwn
challenge is the protections set on the binary: pwn checksec chall

    [*] './chall'
        Arch:       amd64-64-little
        RELRO:      Partial RELRO
        Stack:      No canary found
        NX:         NX enabled
        PIE:        PIE enabled
        Stripped:   No

Notice that there is no stack canary. So we already know this is some
sort of stack overflow vulnerability. If we look at the code, there are
two places where input is taken, on lines 16 and 41.

The overflow on scanf("%100s", s); is pretty obvious, you get 85 bytes
of overflow which looks like it's more than enough for a return address
overwrite to win. But you can't really do that because you don't know
any addresses due to PIE. So we need to leak some address somehow.

Let's look at the first scanf on line 16: scanf("%010s", buf);. This
reads 10 chars into buf, which is 8 bytes on the stack (010 is octal
due to the leading zero). This gives a more subtle three-byte overflow,
including the terminating null. What can you do with three bytes?
Checking the assembly with objdump,

    1206:       48 8d 45 f8             lea    -0x8(%rbp),%rax
    120a:       48 89 c6                mov    %rax,%rsi
    120d:       48 8d 05 07 0e 00 00    lea    0xe07(%rip),%rax        # 201b <_IO_stdin_used+0x1b>
    1214:       48 89 c7                mov    %rax,%rdi
    1217:       b8 00 00 00 00          mov    $0x0,%eax
    121c:       e8 5f fe ff ff          call   1080 <__isoc99_scanf@plt>

So the buffer is indeed 8 bytes from the stack base. Recall the stack
layout: variables, then saved stack base, then saved return address.
So your three bytes are three bytes into the saved stack base. Since
addresses are little-endian, you basically control the three least
significant bytes of the saved bp, i.e. you can move it around a little.

Remember that your goal is to get a pointer leak. getname is called
at line 37, so you can control the base pointer after that. Notice how
a function pointer is stored in the buffer f, which is 16 bytes away
from s on the stack. There is also a puts(s). Unless compiled with
-fomit-frame-pointer stack variables are addressed relative to rbp; so
obviously your goal is to manipulate rbp such that you get a puts(f)
which will have the address of getname. Checking the disassembly,
s and f are 16 and is 32 bytes away from the base as expected.
So obviously you want to shift the base pointer backward by 16. so
puts(rbp-16) is instead puts(f). Now, clearly the base pointer is
randomised each run of the program, so if you run it a bunch of times,
there will be instances where the LSB is 0x10. If you overwrite just
that with 0x00 you get the correct offset. So in fact you only need one
byte of overflow with the null terminator.

Once you have the address of getname the rest of the challenge is trivial