import uvicorn
from fastapi import FastAPI

from routes import ext_enpoints, cards_enpoints

app = FastAPI()
app.include_router(ext_enpoints.router)
app.include_router(cards_enpoints.router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
