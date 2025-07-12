from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat, products

app = FastAPI()

app.include_router(chat.router, prefix="/api")
app.include_router(products.router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Server running!"}