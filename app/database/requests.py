import app.must_parser as mp

from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select, text



async def set_user(tg_id, must_id_value):
    async with async_session() as session:
        
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            new_user = User(tg_id = tg_id, must_id = must_id_value)
            session.add(new_user)
        else:
            user.must_id = must_id_value
        
        await session.commit()

async def check_user(tg_id):
    async with async_session() as session:
        
        user = await session.scalar(select(User).where(User.tg_id == tg_id))   
        
        mp.must_nickname = user.must_id
           
        await session.commit()
