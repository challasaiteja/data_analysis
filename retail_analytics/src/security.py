from Crypto.Cipher import AES
import base64
import os

BLOCK_SIZE = 16
SECRET_KEY = os.environ.get("SECRET_KEY", "default_key_32_chars_needed!")

def pad(data):
    return data + (BLOCK_SIZE - len(data) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(data) % BLOCK_SIZE)

def encrypt_data(plaintext):
    cipher = AES.new(SECRET_KEY.encode('utf-8'), AES.MODE_ECB)
    raw = pad(plaintext)
    encrypted_bytes = cipher.encrypt(raw.encode('utf-8'))
    return base64.b64encode(encrypted_bytes).decode('utf-8')

def decrypt_data(encrypted_text):
    cipher = AES.new(SECRET_KEY.encode('utf-8'), AES.MODE_ECB)
    decoded = base64.b64decode(encrypted_text.encode('utf-8'))
    decrypted = cipher.decrypt(decoded).decode('utf-8')
    # remove padding
    padding_length = ord(decrypted[-1])
    return decrypted[:-padding_length]

# Placeholder for RBAC checks
def check_user_role(role_required, user_role):
    return user_role == role_required

# Additional function for token-based authentication, etc.
