import base64
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from Crypto.Cipher import AES

pw = os.urandom(32)
msg = "Very useless message"
iv = os.urandom(16)

backend = default_backend()
cipher = Cipher(algorithms.AES(pw), modes.CBC(iv), backend=backend)
encryptor = cipher.encryptor()
ciphertext = encryptor.update(msg) + encryptor.finalize()

aes = AES.new(pw, AES.MODE_CBC, iv)
plaintext2 = aes.decrypt(ciphertext)

aes = AES.new(pw, AES.MODE_CBC, iv)
ciphertext2 = aes.encrypt(msg)


backend = default_backend()
cipher = Cipher(algorithms.AES(pw), modes.CBC(iv), backend=backend)
decryptor = cipher.decryptor()
plaintext = decryptor.update(ciphertext2) + decryptor.finalize()

print(f"Plaintext: {str(base64.b64encode(msg), 'utf8')[:100]}...")
print(f"Ciphertext with cryptography: {str(base64.b64encode(ciphertext), 'utf8')[:100]}...")
print(f"Decrypted decrypted with pycrypto: {str(base64.b64encode(plaintext2), 'utf8')[:100]}...")
print(f"Compare 1= ? {plaintext2==msg}")

print(f"Ciphertext with pycrypto: {str(base64.b64encode(ciphertext2), 'utf8')[:100]}...")
print(f"Decrypted decrypted with cryptography: {str(base64.b64encode(plaintext), 'utf8')[:100]}...")
print(f"Compare 2= ? {plaintext==msg}")
