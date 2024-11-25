from cryptography.fernet import Fernet
from decouple import config

key = config('CRYPTOGRAPHY_KEY')
cipher = Fernet(key)


def encrypt_password(password):  # для шифрования пароля
    return cipher.encrypt(password.encode()).decode()


def decrypt_password(encrypted_password):  # для расшифрования пароля
    return cipher.decrypt(encrypted_password.encode()).decode()
