Solution requires one to access the debug console by generating a PIN code through LFI, then performing RCE to read the flag.

1. Looking at the images: `/retrieve?image=image7.jpg` suggests we have a path traversal vulnerability. We can **read the contents of any file** by changing `image7.jpg` to anything.
2. Trying to get `flag.txt` using `/retrieve?image=flag.txt`, we realize the file does not exist. Then, trying `http://localhost:9999/retrieve?image=../flag.txt`, we realize the **file does exist, but this method is blocked.**

3. **Crucially however,** when we did `/retrieve?image=flag.txt`, we got a `FileNotFoundError` and a flask traceback. Furthermore, at tthe bottom of the traceback, we see:

   > The debugger caught an exception in your WSGI application. You can now look at the traceback which led to the error. To switch between the interactive traceback and the plaintext one, you can click on the "Traceback" headline. From the text traceback you can also create a paste of it. For code execution mouse-over the frame you want to debug and click on the console icon on the right side.

4. This suggests that the **flask debug mode is enabled**, and we can try to access the debug console by clicking on the console icon at the right side of the any block of code in the traceback. However, we need a PIN code to access the console.

5. https://blog.gregscharf.com/2023/04/09/lfi-to-rce-in-flask-werkzeug-application/ -- this writeup tells you that the debug pin is actually generated from **machine parameters,** which can be obtained by **reading a few files.** Follow the instructions in the writeup.

6. After gaining access to the console, you now have **Remote Code Execution (RCE) privileges!** You can read `flag.txt` with `__import__("os").popen("cat flag.txt").read()`

7. The flag is `grifflesCTF{sh0u1d_h8v3_turn3d_0ff_d3bug_m0d3}`

8. Sample script is provided in solve.py
