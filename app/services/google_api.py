from datetime import datetime as dt
from typing import Dict

from aiogoogle import Aiogoogle
from app.core.config import settings


FORMAT = "%Y/%m/%d %H:%M:%S"


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Функция создания документа с таблицами."""
    now_date_time = dt.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {'title': f'Отчет от {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': 100,
                                                      'columnCount': 5}}}]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body))
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(spreadsheetid: str,
                               wrapper_services: Aiogoogle) -> None:
    """Функция для предоставления прав доступа вашему личному аккаунту
    к созданному документу."""
    permissions_body = {'type': 'user',
                                        'role': 'writer',
                                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(fileId=spreadsheetid,
                                   json=permissions_body,
                                   fields="id"))


async def spreadsheets_update_value(spreadsheetid: str,
                                    projects: list,
                                    wrapper_services: Aiogoogle
                                    ) -> None:
    """Функция для записи данных, полученных из базы, в гугл-таблицу."""
    now_date_time = dt.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание'] ]
    for project in projects:
        new_row = [str(project['name']),
                              str(project['close_time']),
                              str(project['description'])]
        table_values.append(new_row)

    update_body = {'majorDimension': 'ROWS',
                                   'values': table_values}
    response = await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body))
