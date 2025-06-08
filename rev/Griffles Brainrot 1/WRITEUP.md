First, we need to determine the programming language used. Searching for the `.gyat` file extension reveals that it is a **PyGyat** file.  

To proceed, install **PyGyat** and use the `gyat2py` feature to convert the `.gyat` file into Python code.  

By analyzing and reverse-engineering the script, you will notice that the encryption process consists of two main steps:  
1. **XOR encryption** is applied to the plaintext.  
2. A **Caesar cipher** is then used to further obfuscate the data.  
   
(Note: The base64 function in the script does not actually contribute to the encryption.)  

To decrypt the flag, you can either:  
- Write a script to reverse the encryption process.  
- Use **CyberChef** to quickly decode the encrypted text.  

Once decrypted, you will find multiple flag-like strings. A simple script can help filter out any **"grifflesCTF{fake_flag}"** entries, leaving you with the correct flag.  
