import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, hmac, padding
import bcrypt


##### Encryption #####


# This function returns the IV and the encrypted data (ciphertext). The IV should be stored alongside the ciphertext in the database.
# This function uses AES-CBC encryption with the client password as the encryption key.
def encrypt_data(plaintext, password):

    plaintext_encoded = plaintext.encode("utf-8")
    IV = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded_plaintext = padder.update(plaintext_encoded) + padder.finalize()
    encryptor = Cipher(algorithms.AES(password), modes.CBC(IV)).encryptor()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    return IV, ciphertext


def decrypt_data(iv, ciphertext, password):

    dencryptor = Cipher(algorithms.AES(password), modes.CBC(iv)).decryptor()
    unpad = padding.PKCS7(128).unpadder()
    plaintext_with_padding = dencryptor.update(ciphertext) + dencryptor.finalize()
    plaintext = unpad.update(plaintext_with_padding) + unpad.finalize()
    plaintext = plaintext.decode("utf-8")

    return plaintext

##### Hashing #####

# Hashes plaintext password, returns hash of password as string
def hash_plaintext(password):

    password_to_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(password_to_bytes, salt)

    return hashedPassword.decode("utf-8")

    # Checks stored encoded password with given password (plaintext)
def check_password(enteredPassword, storedPassword):
    return bcrypt.checkpw(enteredPassword.encode("utf-8"), storedPassword.encode("utf-8"))