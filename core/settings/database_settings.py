from config import DB_URL
from pydantic import BaseModel


class DatabaseSettings(BaseModel):
    url: str = DB_URL
    pool_size: int = 1
    max_overflow: int = 5
    pool_timeout: int = 30
    pool_recycle: int = -1
    pool_pre_ping: bool = False


class AsyncSessionmakerSettings(BaseModel):
    autocommit: bool = False
    autoflush: bool = False
    expire_on_commit: bool = False
