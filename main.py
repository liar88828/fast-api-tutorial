from fastapi import FastAPI
from routes import product, item, user, secure, auth

app = FastAPI()
app.include_router(secure.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(product.router)
app.include_router(item.router)


@app.get("/")
async def index_test():
    return 'hello world'


@app.get("/test-db")
async def read_root():
    return {"message": "Database session is ready"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
