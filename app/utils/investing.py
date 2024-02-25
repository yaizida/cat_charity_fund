from datetime import datetime
from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def get_not_full_invested_objects(
    obj_in: Union[CharityProject, Donation],
    session: AsyncSession
) -> List[Union[CharityProject, Donation]]:
    objects = await session.execute(
        select(obj_in).where(obj_in.fully_invested == 0
                             ).order_by(obj_in.create_date)
    )
    return objects.scalars().all()


async def close_donation_for_obj(obj_in: Union[CharityProject, Donation]):
    obj_in.invested_amount = obj_in.full_amount
    obj_in.fully_invested = True
    obj_in.close_date = datetime.now()
    return obj_in


async def invest_money(
    obj_in: Union[CharityProject, Donation],
    obj_model: Union[CharityProject, Donation],
) -> Union[CharityProject, Donation]:
    free_amount_in = obj_in.full_amount - obj_in.invested_amount
    free_amount_in_model = obj_model.full_amount - obj_model.invested_amount

    if free_amount_in > free_amount_in_model:
        obj_in.invested_amount += free_amount_in_model
        await close_donation_for_obj(obj_model)

    elif free_amount_in == free_amount_in_model:
        await close_donation_for_obj(obj_in)
        await close_donation_for_obj(obj_model)

    else:
        obj_model.invested_amount += free_amount_in
        await close_donation_for_obj(obj_in)

    return obj_in, obj_model


def investing_process(
    target: CharityProject,
    sources: List[CharityProject],
) -> List[CharityProject]:
    updated = []

    for source in sources:
        available_amount = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount)

        for investment in [target, source]:
            investment.invested_amount += available_amount
            investment.fully_invested = (investment.invested_amount == investment.full_amount)

            if investment.fully_invested:
                investment.close_date = datetime.now()

        updated.append(source)

        if target.fully_invested:
            break

    return updated