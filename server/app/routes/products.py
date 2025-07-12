from fastapi import APIRouter
import json
import os

router = APIRouter()

@router.get("/products")
def get_products():
    with open(os.path.join("data", "products.json")) as f:
        return json.load(f)
