import shutil
from os import urandom
from pathlib import Path

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from fastapi import UploadFile, HTTPException

# Define the folder where files will be saved
UPLOAD_FOLDER = Path("public")
UPLOAD_FOLDER.mkdir(exist_ok=True)  # Create the folder if it doesn't exist
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
ENCRYPTION_PASSWORD = b"securepassword"  # Use a secure and secret password
SALT = b"static_salt_value"  # Salt for KDF, ideally unique per file


class ImageController():
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

    def encrypt_image(self, data: bytes, password: bytes) -> bytes:
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

    def decrypt_image(self, encrypted_data: bytes, password: bytes) -> bytes:
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
