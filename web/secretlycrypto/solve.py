import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad # Add this import
import base64
import binascii

BASE_URL = "http://146.190.194.252:9995" 

AUTH_ENDPOINT = f"{BASE_URL}/auth"
FLAG_ENDPOINT = f"{BASE_URL}/flag"

# Decrypt username
username_key = binascii.unhexlify("deadbeefdeadbeefdeadbeefdeadbeef")
username_iv = binascii.unhexlify("cafebabecafebabecafebabecafebabe")
username_ciphertext = base64.b64decode("YJDvU4qfKVpwFRc1rSNtmQ==")
cipher_username = AES.new(username_key, AES.MODE_CBC, username_iv)
decrypted_username_padded = cipher_username.decrypt(username_ciphertext)
EXPECTED_USERNAME = unpad(decrypted_username_padded, AES.block_size).decode('utf-8') # Modified line

# Decrypt password hash
password_key = binascii.unhexlify("cafebabecafebabecafebabecafebabe")
password_iv = binascii.unhexlify("deadbeefdeadbeefdeadbeefdeadbeef")
password_ciphertext = base64.b64decode("7rYaypE5sqI8qHTMecoLg6LtXBQQhPxncOmf4kWpvgtFytlvwpVMZSf0zHw/r/Fe")
cipher_password = AES.new(password_key, AES.MODE_CBC, password_iv)
decrypted_password_padded = cipher_password.decrypt(password_ciphertext)
EXPECTED_PASSWORD_HASH = unpad(decrypted_password_padded, AES.block_size).decode('utf-8') # Modified line

print(f"[*] Decrypted username: {EXPECTED_USERNAME}")
print(f"[*] Decrypted password hash: {EXPECTED_PASSWORD_HASH}")

print(f"[*] Attempting to authenticate to {AUTH_ENDPOINT}...")

auth_payload = {
    "username": EXPECTED_USERNAME,
    "password": EXPECTED_PASSWORD_HASH  # Sending the pre-calculated MD5 hash
}

try:
    # Step 1: Authenticate and get the secret
    # The client-side code sends username and the MD5 hash of the password
    response = requests.post(AUTH_ENDPOINT, json=auth_payload)
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
    
    secret = response.text
    print(f"[+] Successfully authenticated. Received secret: {secret}")
    
    # Step 2: Use the secret to get the flag
    print(f"[*] Attempting to get the flag from {FLAG_ENDPOINT}...")
    flag_response = requests.get(FLAG_ENDPOINT, params={"secret": secret})
    flag_response.raise_for_status()
    
    flag = flag_response.text
    print("\n[SUCCESS] Challenge Solved!")
    print(f"Flag: {flag}")
    
except requests.exceptions.RequestException as e:
    print(f"[ERROR] An error occurred: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"    Response status: {e.response.status_code}")
        print(f"    Response content: {e.response.text}")