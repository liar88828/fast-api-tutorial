import shutil
from os import urandom
from pathlib import Path

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from fastapi import UploadFile, HTTPException

from key import settings
from service.aes_enc import encrypt_image_lib, decrypt_image_lib

# Define the folder where files will be saved
UPLOAD_FOLDER = Path("public")
UPLOAD_FOLDER.mkdir(exist_ok=True)  # Create the folder if it doesn't exist
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

# ENCRYPTION_PASSWORD = b"securepassword"  # Use a secure and secret password
# SALT = b"static_salt_value"  # Salt for KDF, ideally unique per file
ENCRYPTION_PASSWORD = settings.ENCRYPTION_PASSWORD.encode()
SALT = settings.SALT.encode()


# File paths
# input_image_path = 'lenna.png'  # Replace with your image file path
# encrypted_file_path = "encrypted_image.bin"
# decrypted_image_path = "decrypted_image.jpg"

# Generate a random key and IV
# _iv = b'\xa5\xa4\xa5)\xabh\xcdZ\xb9\x81\x17\x1d+\x92\xde\x80'  # 16 bytes
# _key = b'\x12\x34\x56\x78\x90\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10'  # 16 bytes (128-bit key)


# Run the encryption and decryption


class ImageController:
    def __init__(self):
        pass

    def extension_file(self, file: UploadFile):
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400,
                                detail=f"Invalid file extension. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")

    async def size_file(self, file: UploadFile):
        file_size = await file.read()  # Read file content to check size
        if len(file_size) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=f"File size exceeds {MAX_FILE_SIZE // (1024 * 1024)} MB limit")

        return file_size

    def save_file(self, file_path: Path, file: UploadFile):
        try:
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File could not be saved: {str(e)}")

    def password_image(self, password: bytes):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=SALT,
            iterations=100_000,
            backend=default_backend(),
        )

        return kdf.derive(password)

    async def encrypt_image(self, data: bytes, password: bytes) -> bytes:
        """Encrypt the image data using AES encryption."""
        # Derive key using PBKDF2
        key = self.password_image(password)

        # Generate a random initialization vector (IV)
        iv = urandom(16)
        # cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        # encryptor = cipher.encryptor()

        # Return IV concatenated with encrypted data (needed for decryption)
        return iv + encrypt_image_lib(data, key, iv)

    def decrypt_image(self,
                      password: bytes,
                      decrypted_image_path: str) -> bytes:
        """Decrypt the encrypted image data using AES encryption."""
        # Derive key using PBKDF2
        key = self.password_image(password)

        # Decrypt and return the original image data
        return decrypt_image_lib(decrypted_image_path, key)

    def _encrypt_image(self, data: bytes, password: bytes) -> bytes:
        """Encrypt the image data using AES encryption."""
        # Derive key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=SALT,
            iterations=100_000,
            backend=default_backend(),
        )
        key = kdf.derive(password)

        # Generate a random initialization vector (IV)
        iv = urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Return IV concatenated with encrypted data (needed for decryption)
        return iv + encryptor.update(data) + encryptor.finalize()

    def _decrypt_image(self, encrypted_data: bytes, password: bytes) -> bytes:
        """Decrypt the encrypted image data using AES encryption."""
        # Derive key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=SALT,
            iterations=100_000,
            backend=default_backend(),
        )
        key = kdf.derive(password)

        # Extract IV from the beginning of the encrypted data
        iv = encrypted_data[:16]
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt and return the original image data
        return decryptor.update(encrypted_data[16:]) + decryptor.finalize()
