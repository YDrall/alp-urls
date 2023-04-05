import aiopg

class PostgresDB:

    def __init__(self, dbname: str, user: str, password: str, host: str, port: int) -> None:
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self._pool = None
    
    async def init(self, poolMinsize=1, poolMaxsize=10, enableQueryLogs = False):
        if self._pool is None:
            self._pool = await aiopg.create_pool(dbname=self.dbname, user=self.user, password=self.password, host=self.host, port=self.port,
            minsize=poolMinsize, maxsize=poolMaxsize, echo=enableQueryLogs)
    
    async def close(self):
        self._pool.close()
        await self._pool.wait_closed()

    
    async def execute(self, query, paramters):
        async with self._pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, paramters)
                ret = []
                async for row in cur:
                    ret.append(row)
                return ret
