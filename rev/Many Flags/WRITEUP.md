## Understanding the code
### 1. `gimme_more_flags`
A function that take in an argument x, and adds x number of "flag"s to `fake_flag`.

### 2. `init`
We have an array `arr` consisting of 20 digits — 10 `0`s and 10 `1`s. `arr` is randomly shuffled.

In lines 24-33:
- `password` is set to whatever is represented by `arr`
    - e.g. if `arr` = `[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]` then `password` = `"10101010101010101010"`
- If `arr[i]` is 0, call `gimme_more_flags(count)`, where `count` = 2<sup>i</sup>.
    - essentially add 2<sup>i</sup> "flag"s to `fake_flag` if `arr[i]` = 0.

## Getting the flag
To get the flag, we need to enter the correct password. We are given `fake_flag`. So, what information does it give?

Well, the number of "flag"s (let's call this number x) printed tells us exactly which positions are `0`s. This is because we know x is a sum of unique powers of 2, and we can find exactly what these powers of 2 are by looking at the binary representation of x. A `1` in the (reverse-order) binary representation of x means a `0` in `arr[i]`.

To illustrate, suppose `arr` = `[0,0,1,0]`. 2<sup>0</sup> + 2<sup>1</sup> + 2<sup>3</sup> = 11 "flag"s will be printed. Binary representation of 11 = 1011. We then know that postitions i = 0,1,3 are `0`s. Hence we can deduce `arr` = `[0,0,1,0]`.

We can interact with the server using something like pwntools, to read the outputed `fake_flag`, determine the password and send it back to the server. For coding, I personally find it most convenient to decompose number of "flag"s manually into powers of 2 and construct password from there.
## Solve code
```python
from pwn import *

io = remote('209.38.56.153', 9996)

fake_flag = io.recvline().decode()
k = int(len(fake_flag)/4)

ans = ""
for i in range(19,-1,-1):
    j = 2**i
    if(k-j >= 0):
        ans += "0"
        k -= j
    else:
        ans += "1"

ans1 = ans[::-1]
log.info(ans1)
io.sendline(ans1.encode())

io.interactive()
```
