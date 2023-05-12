from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.services import investing
from app.api.validators import (check_investing, check_name_duplicate,
                                check_update)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)

router = APIRouter()


@router.post('/',
             response_model=CharityProjectDB,
             response_model_exclude_none=True,
             dependencies=[Depends(current_superuser)])
async def create_charity_project(project: CharityProjectCreate,
                                 session: AsyncSession = Depends(get_async_session),
                                 ):
    """
    Только для суперюзеров.

    Создаёт благотворительный проект."""
    await check_name_duplicate(project.name, session)
    project = await project_crud.create(project, session)
    await investing(session)
    await session.commit()
    await session.refresh(project)
    return project


@router.get('/',
            response_model=List[CharityProjectDB],
            response_model_exclude_none=True, )
async def get_all_charity_projects(session: AsyncSession = Depends(get_async_session)
                                   ) -> List[CharityProjectDB]:
    """Возвращает список всех проектов."""
    all_projects = await project_crud.get_multi(session)
    return all_projects


@router.patch('/{project_id}',
              response_model=CharityProjectDB,
              dependencies=[Depends(current_superuser)], )
async def update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)):
    """
    Только для суперюзеров.

    Закрытый проект нельзя редактировать;
    нельзя установить требуемую сумму меньше уже вложенной.
    """
    if obj_in.full_amount is not None:
        project = await check_update(project_id,
                                     session,
                                     obj_in.full_amount)
    else:
        project = await check_update(project_id,
                                     session)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    project = await project_crud.update(project, obj_in, session)
    await investing(session)
    await session.refresh(project)
    return project


@router.delete('/{project_id}',
               response_model=CharityProjectDB,
               dependencies=[Depends(current_superuser)], )
async def delete_charity_project(project_id: int,
                                 session: AsyncSession = Depends(get_async_session),
                                 ) -> CharityProjectDB:
    """
    Только для суперюзеров.

    Удаляет проект. Нельзя удалить проект, в который
    уже были инвестированы средства, его можно только закрыть.
    """
    project = await check_investing(project_id, session)
    return await project_crud.remove(project, session)
