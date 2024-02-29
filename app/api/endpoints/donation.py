from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.models import CharityProject, User, Donation
from app.schemas.donation import DonationBase, DonationCreate, DonationDB
from app.utils.investing import new_investing_process, get_not_full_invested_objects
from app.crud.base import CRUDBase

router = APIRouter()
donation_crud = CRUDBase(Donation)


@router.post(
    '/',
    response_model=DonationCreate,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationBase,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Сделать пожертвование."""
    new_donation = await donation_crud.create(donation, session, user)
    target_objects = await get_not_full_invested_objects(
        CharityProject, session)
    new_project = new_investing_process(
        new_donation, target_objects)

    await session.commit()
    await session.refresh(new_project)
    return new_donation


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Получает список всех пожертвований.
    """
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=List[DonationCreate],
    response_model_exclude={'user_id'},
)
async def get_my_reservations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Получить список моих пожертвований."""
    donations = await donation_crud.get_by_user(
        Donation, session=session, user=user
    )
    return donations
