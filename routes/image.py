from io import BytesIO
from typing import Annotated

from fastapi import File, UploadFile, HTTPException, APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse

from service.image import ImageController, UPLOAD_FOLDER, ENCRYPTION_PASSWORD

router = APIRouter(prefix="/images", tags=["image"])
image_controller = ImageController()


@router.post("/files/")
async def create_file(file: Annotated[bytes | None, File()] = None):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}


@router.post("/save-image/")
async def save_image(file: UploadFile, request: Request):
    if not file:
        raise HTTPException(status_code=400, detail="No file sent")

    # Check file extension
    image_controller.extension_file(file=file)

    # Check file size
    file_content = await  image_controller.size_file(file=file)
    # print(file_content)
    # Encrypt the file content
    encrypted_data = image_controller.encrypt_image(data=file_content, password=ENCRYPTION_PASSWORD)

    # Define the file path to save the encrypted file
    encrypted_file_path = UPLOAD_FOLDER / (file.filename + ".enc")

    try:
        with encrypted_file_path.open("wb") as buffer:
            buffer.write(encrypted_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File could not be saved: {str(e)}")

    return JSONResponse(content={"message": "File saved successfully",
                                 "file_path": str(encrypted_file_path),
                                 'full_path': f"{str(request.base_url)}images/get-image/{str(file.filename)}"
                                 })


@router.get("/get-image/{filename}")
async def get_image(filename: str):
    """Decrypt and return the requested encrypted image."""
    encrypted_file_path = UPLOAD_FOLDER / (filename + ".enc")

    if not encrypted_file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        # Read the encrypted file
        encrypted_data = encrypted_file_path.read_bytes()

        # Decrypt the file content
        decrypted_data = image_controller.decrypt_image(
            encrypted_data=encrypted_data,
            password=ENCRYPTION_PASSWORD
        )

        # ---------
        # # Save the decrypted file temporarily (optional, for serving)
        # temp_file_path = UPLOAD_FOLDER / filename
        # temp_file_path.write_bytes(decrypted_data)
        #
        # # Return the decrypted file as a response
        # return FileResponse(temp_file_path, media_type="image/*", filename=filename)
        # -------

        # Create a BytesIO object to simulate a file-like object
        decrypted_image_stream = BytesIO(decrypted_data)

        # Return the decrypted image directly using StreamingResponse
        return StreamingResponse(
            decrypted_image_stream,
            media_type="image/*",
            headers={"Content-Disposition": f"inline; filename={filename}"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not decrypt file: {str(e)}")


@router.get("/show/")
async def list_files():
    """Custom endpoint to list files in the /public/ directory."""
    # files = [f.name for f in UPLOAD_FOLDER.iterdir() if f.is_file()]
    files = [file.name for file in UPLOAD_FOLDER.glob("*.enc")]
    return JSONResponse(content=files)
    # file_links = [f'<a href="/public/{file}">{file}</a>' for file in files]
    # return HTMLResponse(content="<br>".join(file_links))


# Serve static files for uploaded images
@router.get("/")
async def main():
    content = """
<body>
 

     <h1>Upload and Save Image</h1>
    <form id="uploadForm" action="/images/save-image/" method="post" enctype="multipart/form-data">
        <label for="file">Choose an image:</label>
        <input type="file" id="file" name="file" accept=".jpg,.jpeg,.png,.gif" required>
        <small>Allowed extensions: .jpg, .jpeg, .png, .gif (Max size: 5MB)</small>
        <br>
        <button type="submit">Upload</button>        
    </form>

    <h2>Uploaded Images</h2>
    <div id="imageGallery">
        <p>No images yet. Upload an image to see it here!</p>
    </div>


    <script>
        const form = document.getElementById('uploadForm');
        const fileInput = document.getElementById('file');
        const gallery = document.getElementById('imageGallery');
        const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB

        form.addEventListener('submit', function (event) {
            const file = fileInput.files[0];
        console.log(file)
            
            if (file) {
                // Validate file size
                if (file.size > MAX_FILE_SIZE) {
                    alert('File size exceeds 5MB limit.');
                    event.preventDefault();
                    return;
                }

                // Validate file extension
                const allowedExtensions = ['jpg', 'jpeg', 'png', 'gif'];
                const fileExtension = file.name.split('.').pop().toLowerCase();
                console.log(fileExtension);
                if (!allowedExtensions.includes(fileExtension)) {
                    alert(`Invalid file type. Allowed: ${allowedExtensions.join(', ')}`);
                    event.preventDefault();
                    return;
                }else{
                
                    alert('Image uploaded successfully!');
                
                }
            }
        });
        
         async function fetchImages() {
            try {
                const response = await fetch('/public-image/');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
        
                // Parse JSON response
                const fileList = await response.json(); // Assuming the response is a JSON array
                console.log(fileList); // Example: ["asrama.jpg.enc","IMG_16569.jpeg.enc","team.jpg.enc"]
        
                if (fileList.length === 0) {
                    gallery.innerHTML = '<p>No images yet. Upload an image to see it here!</p>';
                    return;
                }
        
                gallery.innerHTML = ''; // Clear gallery
        
                // Add each image to the gallery
                fileList.forEach(file => {
                    const filename = file.replace('.enc', ''); // Remove ".enc" extension
                    const imageUrl = `/images/get-image/${filename}`;// is request api
                    const img = document.createElement('img');
                    img.src = imageUrl;
                    img.alt = filename;
                    img.style = 'max-width: 200px; margin: 10px;';
                    gallery.appendChild(img);
                });
            } catch (error) {
                console.error('Error fetching images:', error);
                gallery.innerHTML = '<p>Failed to load images.</p>';
            }
        }
           // Fetch images on page load
         window.onload = fetchImages;
       
    </script>
  
</body>
    """
    return HTMLResponse(content=content)
