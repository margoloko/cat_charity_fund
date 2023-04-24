from typing import Optional

from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.crud.charity_project import project_crud
from app.schemas.charity_project import CharityProjectDB


async def check_name_duplicate(name: str,
                               session: AsyncSession,
                               ) -> None:
    project_id = await project_crud.get_project_by_name(name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!', )


async def check_project_exists(project_id: int,
                               session: AsyncSession
                               ) -> Optional[CharityProjectDB]:
    project = await project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='Этого проекта не существует!')
    return project


async def check_update(project_id: int,
                       session: AsyncSession,
                       full_amount: Optional[int] = None,
                       ) -> CharityProject:
    project = await check_project_exists(project_id, session)
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!')
    if full_amount:
        if full_amount < project.invested_amount:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail='Нельзя установить требуемую сумму'
                'меньше уже вложенной!')
    return project


async def check_investing(project_id: int,
                          session: AsyncSession,
                          ) -> CharityProject:
    project = await check_project_exists(project_id, session)
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!')
    return project
