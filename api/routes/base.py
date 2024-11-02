from fastapi import APIRouter

router = APIRouter()

@router.get("/api/py/helloFastApi")
def hello_fast_api():
    return {"message": "Hello from FastAPI1102"}

@router.get("/")
def read_root():
    return {"message": "root path"}