from db import PostgresDB
from pydantic import BaseModel
from fastapi import Query


class AlpCreateRequest(BaseModel):
    url: str = Query(regex="^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$")


class AlpURL:
    url: str
    __TABLE_NAME__ = 'url'
    COLS = ('id', 'url', 'user_id', 'created_at', 'expires_at')
    COLS_STR = ", ".join(COLS)

    def __init__(self, id, url, user, created_at, expires_at) -> None:
        self._id, self._url, self._created_at, self._expires_at, self._user = id, url, created_at, expires_at, user
    
    @staticmethod
    async def get(db: PostgresDB, id: int):
        data = await db.execute(f"SELECT {AlpURL.COLS_STR} from {AlpURL.__TABLE_NAME__} where id = %s", (id, ))
        return AlpURL.create_instance_by_sql_retrun_data(data)
    
    @staticmethod
    async def create(db: PostgresDB, url: str):
        data = await db.execute(f"INSERT INTO {AlpURL.__TABLE_NAME__} (url, user_id, expires_at) values (%s, %s, %s) RETURNING {AlpURL.COLS_STR}", (url, 1, None))
        return AlpURL.create_instance_by_sql_retrun_data(data)
        
    @staticmethod
    def create_instance_by_sql_retrun_data(data):
        if not data or len(data) == 0:
            data = [()]
        data = data[0]
        if isinstance(data, str):
            data = data.split(",")
        return AlpURL(*data)
    
    @property
    def url(self):
        return self._url or ""
    
    @property
    def id(self):
        return self._id or None