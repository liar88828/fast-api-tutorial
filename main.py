from fastapi import FastAPI

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    for_sell: Union[bool, None] = None


@app.get("/")
async def root():
    return {"message": "Hello World"}


