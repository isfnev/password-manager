from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

class PasswordManager:
    def __init__(self):
        self.backend = default_backend()
        self.salt = os.urandom(16)  # Generate a random salt for key derivation

    def generate_key(self, password):
        """Derive a secure encryption key from a password using PBKDF2."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,  # Adjust this iteration count as per your security needs
            backend=self.backend
        )
        return kdf.derive(password.encode())

    def encrypt_password(self, password, key):
        """Encrypt a password using AES encryption."""
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        password_bytes = password.encode()
        padded_data = padder.update(password_bytes) + padder.finalize()

        iv = os.urandom(16)  # Generate a random IV
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        encrypted_password = encryptor.update(padded_data) + encryptor.finalize()

        return iv + encrypted_password

    def decrypt_password(self, encrypted_data, key):
        """Decrypt an encrypted password using AES decryption."""
        iv = encrypted_data[:16]
        encrypted_password = encrypted_data[16:]

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(encrypted_password) + decryptor.finalize()

        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

        return decrypted_data.decode()

# Main function to run the program
if __name__ == "__main__":
    password_manager = PasswordManager()

    # Get password input from user
    password = input("Enter the password to encrypt: ")

    # Generate encryption key
    key = password_manager.generate_key(password)

    # Encrypt the password
    encrypted_data = password_manager.encrypt_password(password, key)

    # Print the encrypted data (in hexadecimal format for better display)
    print("Encrypted password (in hexadecimal):")
    encrypted_hex = encrypted_data.hex()
    print(encrypted_hex)
