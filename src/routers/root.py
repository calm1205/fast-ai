from typing import Dict
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def read_root() -> Dict[str, str]:
    return {"message": "Hello World"}


@router.get("/health_check")
def health_check() -> Dict[str, str]:
    return {"success": "ok"}
