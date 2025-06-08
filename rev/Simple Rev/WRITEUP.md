## Understanding the code
We have a dictionary `d` that maps characters to numbers: `a` -> 1, `b` -> 2 and so on until `_` -> 65.

In lines 13-17:
- each character in the flag is converted to its corresponding number, `x`
- a random number `y` is generated and printed
- `x+y` is appended to the array `g`

Finally, the difference between every 2 consecutive numbers in `g` is printed.

In summary, g = flag + random numbers, and we are given the list of random numbers as well as the difference array of g.
## Getting the flag
### 1. Reconstruct g
Note that we just need the value of one number in `g`, and we can reconstruct everything else using the differences.
- We make use of the fact that the flag format is "grifflesCTF{...}". We know that the first letter, "g", is converted to 7, and then 34 is added to it. Hence, the first number of `g` is 7 + 34 = **41**.
- Alternatively, you can bruteforce every character to be the first character if you are unsure...

Now that you know g[0] = 41, just keep adding back the differences to get the remaining numbers in `g`.

### 2. Subtract y 
After you have reconstructed `g`, subtract the corresponding `y` from each value in `g` and you get the original flag in number form.

### 3. Convert back to characters
Convert the numbers back to characters and you get the flag!

## Solve code
```python
with open("output.txt", "r") as file:
    line1 = file.readline()
    y = [int(num) for num in line1.split()]
    
    line2 = file.readline()
    diff = [int(num) for num in line2.split()]

# Reconstruct g
g = []
g.append(41)
for i in range(len(diff)):
    g.append(g[i]+diff[i])

# Subtract y and convert back to characters
characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_"
flag = ""
for i in range(len(y)):
    flag += characters[g[i]-y[i] - 1]

print(flag)
```