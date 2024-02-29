from datetime import datetime
from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def get_not_full_invested_objects(
    source: Union[CharityProject, Donation],
    session: AsyncSession
) -> List[Union[CharityProject, Donation]]:
    objects = await session.execute(
        select(source).where(source.fully_invested == 0
                             ).order_by(source.create_date)
    )
    return objects.scalars().all()


def close_donation_for_obj(source: Union[CharityProject, Donation]):
    source.invested_amount = source.full_amount
    source.fully_invested = True
    source.close_date = datetime.now()
    return source


def invest_money(
    source: Union[CharityProject, Donation],
    obj_model: Union[CharityProject, Donation],
) -> Union[CharityProject, Donation]:
    free_amount_in = source.full_amount - source.invested_amount
    free_amount_in_model = obj_model.full_amount - obj_model.invested_amount

    if free_amount_in > free_amount_in_model:
        source.invested_amount += free_amount_in_model
        close_donation_for_obj(obj_model)

    elif free_amount_in == free_amount_in_model:
        close_donation_for_obj(source)
        close_donation_for_obj(obj_model)

    else:
        obj_model.invested_amount += free_amount_in
        close_donation_for_obj(source)

    return source, obj_model


async def investing_process(
    source: Union[CharityProject, Donation],
    target: Union[CharityProject, Donation],
    session: AsyncSession,
) -> Union[CharityProject, Donation]:
    # Сессией я не её обделить т.к здесь она требуеться(
    # Мне кажеться я всё равно что то не понял
    # Не совсем понятно как быть с добовлением\обновлением\фиксированием в бд
    objects_model = await get_not_full_invested_objects(target, session)
    for model in objects_model:
        source, model = invest_money(source, model)
        session.add(source)
        session.add(model)

    # Вот в данном моменте не сосвес понятно как без сессии,
    # Как мне тогда обойтись без неё ?
    await session.commit()
    await session.refresh(source)
    return source


def new_investing_process(
    source: Union[CharityProject, Donation],
    target: Union[CharityProject, Donation],
):
    for model in target:
        source, model = invest_money(source, model)

    return source