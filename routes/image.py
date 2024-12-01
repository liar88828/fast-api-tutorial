import shutil
from pathlib import Path
from typing import Annotated

from fastapi import File, UploadFile, HTTPException, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse

router = APIRouter(prefix="/images", tags=["image"])


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


# Define the folder where files will be saved
UPLOAD_FOLDER = Path("public")
UPLOAD_FOLDER.mkdir(exist_ok=True)  # Create the folder if it doesn't exist
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


@router.post("/save-image/")
async def save_image(file: UploadFile):
	if not file:
		raise HTTPException(status_code=400, detail="No file sent")

	# Check file extension
	file_extension = Path(file.filename).suffix.lower()
	if file_extension not in ALLOWED_EXTENSIONS:
		raise HTTPException(status_code=400, detail=f"Invalid file extension. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")

	# Check file size
	file_size = await file.read()  # Read file content to check size
	if len(file_size) > MAX_FILE_SIZE:
		raise HTTPException(status_code=400, detail=f"File size exceeds {MAX_FILE_SIZE // (1024 * 1024)} MB limit")

	# Reset file pointer after size check
	file.file.seek(0)

	# Define the file path to save the uploaded file
	file_path = UPLOAD_FOLDER / file.filename

	try:
		with file_path.open("wb") as buffer:
			shutil.copyfileobj(file.file, buffer)
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"File could not be saved: {str(e)}")

	return JSONResponse(content={"message": "File saved successfully", "file_path": str(file_path)})


@router.get("/index")
async def main():
	content = """
<body>

    <h1>Upload File as Bytes</h1>
    <form action="/images/files/" method="post" enctype="multipart/form-data">
        <label for="file_bytes">Choose a file:</label>
        <input type="file" id="file_bytes" name="file">
        <button type="submit">Upload</button>
    </form>

   <h1>Upload File with Metadata</h1>
    <form action="/images/uploadfile/" method="post" enctype="multipart/form-data">
        <label for="file_metadata">Choose a file:</label>
        <input type="file" id="file_metadata" name="file">
        <button type="submit">Upload</button>
    </form>


     <h1>Upload and Save Image</h1>
    <form id="uploadForm" action="/images/save-image/" method="post" enctype="multipart/form-data">
        <label for="file">Choose an image:</label>
        <input type="file" id="file" name="file" accept=".jpg,.jpeg,.png,.gif" required>
        <small>Allowed extensions: .jpg, .jpeg, .png, .gif (Max size: 5MB)</small>
        <br>
        <button type="submit">Upload</button>
    </form>

    <script>
        const form = document.getElementById('uploadForm');
        const fileInput = document.getElementById('file');
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
                }
            }
        });
    </script>
  
</body>
    """
	return HTMLResponse(content=content)
