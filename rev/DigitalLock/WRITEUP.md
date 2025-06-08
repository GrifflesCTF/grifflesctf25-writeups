## Understanding the code
The lock in the program works just like the one in the image. It is represented by the `lock` array, which stores 3 numbers. The numbers can be modified as we adjust the lock, and can go from 0-9.

### 1. `rotate_lock`
The `rotate_lock` function adjusts the lock. It takes in an action and rotates the given row either leftwards or rightwards by the given number of steps (row, direction and number of steps are specified by the action).

### 2. `init`
Inside the `init` function:
1. `lock` is set to 3 random digits
2. `password` is set to these same digits
3. every letter from A-Z is assigned to represent a random action
4. `lock` is scrambled using the action string "HGSAJDBEOWSUCYTBSPVFCJNBK"
    - i.e. applying the actions reprented by H, G, S, ... in sequence

### 3. `main`
You are allowed to adjust the lock by using the letters A-Z. You can also try to open the lock which, when successful, gives you the flag.

## Getting the flag
To get the flag, we need to adjust `lock` to match `password`. We do not know what `password` is, neither do we know what actions the letters A-Z represent.

### Observation 1
The password was set to be whatever `lock` was, before `lock` was scrambled. This means we just need to undo the action "HGSAJDBEOWSUCYTBSPVFCJNBK". But undoing isn't as simple as typing the string backwards, because each letter represents a specific action, and typing the string backwards does not make the opposite action happen.

### Observation 2
Notice that for such a lock, any action, when repeated 10 times, leaves the lock unchanged.
- For example, if we shift the top row to the right by 1 step, 10 times, we return to our original position. If we shift the top row to the right by k stpes, 10 times, we return to our original position.

Since the lock was scrambled by applying "HGSAJDBEOWSUCYTBSPVFCJNBK" once, if we apply this exact string another 9 times, we return to the original position - the same as the password.

**Further illustration on why this works**

Consider the string "HGSAJDBEOWSUCYTBSPVFCJNBK". Some actions might shift the top row, some shift the middle row, some shift the bottom row. Overall, each row will be displaced by a certain amount. Note that how much each row is shifted is independent of how much the other rows are shifted. Now, if doing "HGSAJDBEOWSUCYTBSPVFCJNBK" shifts the top row by k, doing "HGSAJDBEOWSUCYTBSPVFCJNBK" another 9 times shifts the top row by k another 9 times, back to the original. The same happens for the other 2 rows. Hence, `lock` will then match `password`.

### Solution
Select option 1 to mess with lock, and paste the string "HGSAJDBEOWSUCYTBSPVFCJNBK" 9 times. Select option 2 to open lock, and the program outputs "unlock successful!" with the flag, `grifflesCTF{v3ry_s3cure_d1gil0ck}`.