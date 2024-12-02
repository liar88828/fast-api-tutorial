from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from routes import auth, item, product, secure, user, image
from service.image import UPLOAD_FOLDER

app = FastAPI()
# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/public", StaticFiles(directory="public"), name="public")

# Set up the public directory


app.include_router(secure.router)
app.include_router(auth.router)
app.include_router(image.router)
app.include_router(user.router)
app.include_router(product.router)
app.include_router(item.router)


@app.get("/")
async def index_test():
    return {'msg': 'hello world'}


# @app.get("/public-image/")
# async def list_files():
#     """Custom endpoint to list files in the /public/ directory."""
#     files = [f.name for f in UPLOAD_FOLDER.iterdir() if f.is_file()]
#     return files
#     # file_links = [f'<a href="/public/{file}">{file}</a>' for file in files]
#     # return HTMLResponse(content="<br>".join(file_links))
#

@app.get("/public-image/")
async def list_encrypted_images():
    """Return a list of encrypted image filenames in the public folder."""
    files = [file.name for file in UPLOAD_FOLDER.glob("*.enc")]
    return JSONResponse(content=files)


@app.get("/test-db")
async def read_root():
    return {"message": "Database session is ready"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
