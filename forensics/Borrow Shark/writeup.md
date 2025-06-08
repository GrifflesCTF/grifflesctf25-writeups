# Challenge Solution

1. We observe a simulated mitm. After supposed arp poissoning, when the user requests “house_standings.pdf” from a website “fakegrifflesctfwebsite.com”, the attacker instead sends a pyc file disguised as the house_standings.pdf file. 
2. Downloading the file, we notice that taking the ‘flag’ found from strings is not the flag.
3. Instead, we must decompyle the pyc. To do so:
    1. `pip install uncompyle6`
    2. `uncompyle6 cat.pyc > decompiled.py`
4. Either 
    1. Observe that the flag is given by reversing the password (below), or
        
        ```
                print("Here's your flag! grifflesCTF{" + os.getenv("SECRET_PASSWORD")[None[None:-1]] + "}")
        ```
        
    2. Simply set the environment variable as required using `$env:SECRET_PASSWORD = "d3c0mp1l3_m3_n0w"`in powershell and run the file.

# The Flag

Flag: `grifflesCTF{w0n_3m_3l1pm0c3d}`