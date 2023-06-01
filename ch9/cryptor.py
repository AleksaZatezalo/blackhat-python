"""
Descriptor: A cryptography script to use RSA keys.
Author: Aleksa Zatezalo
"""

from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes

import base64
import zlib

def generate():
    new_key = RSA.generate(2048)
    private_key = new_key.export_key()
    public_key = new_key.public_key()

    with open('key.pri', 'wb') as f:
        f.write(private_key)
    
    with open('key.pub', 'wb') as f:
        f.write(public_key)
    
def get_rsa_cipher(keytype):
    with open(f'key.{keytype}') as f:
        key = f.read()
    rsakey = RSA.import_key(key)
    return (PKCS1_OAEP.new(rsakey), rsakey.size_in_bytes())

# def encrypt(plaintext):
#     compressed_text = zlib.compress(plaintext)

#     session_key = get_random_bytes(16)
#     cipher_aes = AES.new(session_key, AES.MODE_EAX)
#     ciphertext, tag = cipher_aes.encrypt_and_digest(compressed_text)
#     encrypted_session_key = cipher_rsa.ene