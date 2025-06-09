import pyzipper
'''
We cannot use zipfile, as it is an unsupported compression type "WinZip AES encryption"
---
unzip -lv 3.1.zip
Archive:  3.1.zip
 Length   Method    Size  Cmpr    Date    Time   CRC-32   Name
--------  ------  ------- ---- ---------- ----- --------  ----
       0  Stored        0   0% 2025-06-03 08:29 00000000  3.1/
    1646  Unk:099     237  86% 2025-06-03 08:29 00000000  3.1/devious.txt
--------          -------  ---                            -------
    1646              237  86%                            2 files
---
'''
passwords = []
FILENAME = '3.1.zip'

# These are just guesses
days = [str(num).zfill(2) for num in range(1, 32)]
months = [str(num).zfill(2) for num in range(1, 13)]
years = [str(num).zfill(4) for num in range(1800, 2025)]

# Trying DDMMYYYY first (this is a bit of foresight as a tester, but testing other formats first is fine)
for day in days:
    for month in months:
        for year in years:      
            passwordTest = f'{day}{month}{year}'
            f = pyzipper.AESZipFile(FILENAME, 'r')
            try:
                f.setpassword(passwordTest.encode())
                f.extractall()
                print(f"Password {passwordTest} success")
                break
            except RuntimeError:
                continue