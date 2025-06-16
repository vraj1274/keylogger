from cryptography.fernet import Fernet
import os

KEY_FILE = "secret.key"

# Generate and save the key if it doesn't exist
def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)

# Load the saved key
def load_key():
    with open(KEY_FILE, 'rb') as f:
        return f.read()

# Encrypt the log file
def encrypt_log_file(file_path):
    generate_key()
    key = load_key()
    fernet = Fernet(key)

    with open(file_path, 'rb') as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
