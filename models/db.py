import asyncpg
import os

class Database:
    async def create(self):
        self.pool = await asyncpg.create_pool(
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        async with self.pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute('''
                        CREATE TABLE IF NOT EXISTS users (
                            id BIGINT PRIMARY KEY,
                            age INTEGER,
                            gender VARCHAR
                        );
                    ''')
    async def create_user(self,id,age,gender):
        async with self.pool.acquire() as connection:
            await connection.execute(f"INSERT INTO users (id, age, gender) VALUES ('{id}', '{age}', '{gender}')")
    async def check_user(self,id) -> bool:
         async with self.pool.acquire() as con:
            result = await con.fetchval(f"SELECT * FROM users WHERE id = {id} LIMIT 1")
            if result:
                 return True
            else:
                 return False

DB = Database()