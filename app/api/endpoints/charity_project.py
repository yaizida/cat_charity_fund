from fastapi import APIRouter

from app.crud.charity_project import create_charity
from app.schemas.charity_project import CharityProjectCreate

router = APIRouter()


@router.post('/charity/')
async def create_new_charity(
    charity: CharityProjectCreate
):
    new_charity = await create_charity(charity)
    return new_charity