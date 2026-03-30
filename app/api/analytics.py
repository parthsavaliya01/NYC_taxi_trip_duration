from fastapi import APIRouter
from app.db import get_stats

router = APIRouter()

@router.get("/analytics")
def analytics():
    return get_stats()