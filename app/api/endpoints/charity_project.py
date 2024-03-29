from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_already_invested,
                                check_charity_project_closed,
                                check_charity_project_exists,
                                check_charity_project_invested_sum,
                                check_name_duplicate,
                                )
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.models import CharityProject, Donation
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.utils.investing import new_investing_process, get_not_full_invested_objects
from app.crud.base import CRUDBase


router = APIRouter()
charity_project_crud = CRUDBase(CharityProject)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров. Создает благотворительный проект."""

    await check_name_duplicate(charity_project.name, session)
    await charity_project_crud.get_project_id_by_name(
        CharityProject, charity_project.name, session)

    new_project = await charity_project_crud.create(
        charity_project, session)

    target_objects = await get_not_full_invested_objects(
        Donation, session)
    new_project = new_investing_process(
        new_project, target_objects)

    await session.commit()
    await session.refresh(new_project)

    return new_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Получает список всех проектов."""
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Закрытый проект нельзя редактировать,
    нельзя установить сумму меньше вложенной.
    """
    project = await check_charity_project_exists(
        project_id, session
    )

    check_charity_project_closed(project)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        check_charity_project_invested_sum(project, obj_in.full_amount)

    charity_project = await charity_project_crud.update(
        project, obj_in, session
    )
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Удаляет проект. Нельзя удалить проект,
    в который уже были инвестированы средства,
    его можно только закрыть.
    """
    project = await check_charity_project_exists(
        project_id, session
    )
    check_charity_project_already_invested(project)
    charity_project = await charity_project_crud.remove(
        project, session
    )
    return charity_project
