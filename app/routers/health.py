from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import engine
import logging

router = APIRouter(prefix="/health", tags=["health"])
logger = logging.getLogger(__name__)


@router.get("/")
def health_check() -> dict[str, str]:
    try:
        with engine.connect()as conn:
            conn.execute(text("SELECT 1"))
            return {"Statur": "ok", "Database": "UP"}
    except SQLAlchemyError:
        logger.exception("log message:")
        raise HTTPException(status_code=503, detail="Database unavailable")
