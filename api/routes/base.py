from fastapi import APIRouter, Depends
from sqlmodel import Session

from api.conf.config import get_db

router = APIRouter()

@router.get("/api/py/helloFastApi")
def hello_fast_api():
    return {"message": "Hello from FastAPI1102"}

@router.get("/")
def read_root():
    return {"message": "root path"}

@router.get("/health/liveness")
def liveness():
    return {"status": "successful"}

@router.get("/health/readiness")
def readiness(db: Session = Depends(get_db)):
    try:
        if not db.is_active:
            return {"status": "not ready", "error": "Database is not active"}
    except Exception as e:
        return {"status": "not ready", "error": str(e)}
    return {"status": "successful"}
