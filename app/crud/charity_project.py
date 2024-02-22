from app.core.db import AsyncSessionLocal
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectCreate


async def create_charity(charity: CharityProjectCreate) -> CharityProject:
    charity_data = charity.dict()
    db_room = CharityProject(**charity_data)
    async with AsyncSessionLocal() as session:
        session.add(db_room)
        await session.commit()
        await session.refresh(db_room)
    return db_room
