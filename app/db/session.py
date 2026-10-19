from sqlalchemy import create_engine
from app.core.config import settings

Database_URL = settings.database_url.get_secret_value()

engine = create_engine(Database_URL, echo=False, pool_pre_ping=True)
