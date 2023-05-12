from datetime import datetime as dt

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"
SHEETS_BODY = {
        'properties': {'title': '',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': 100,
                                                      'columnCount': 5}}}]
    }


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Функция создания документа с таблицами."""
    SHEETS_BODY['properties']['title'] = 'Отчет на {}'.format(dt.now().strftime(FORMAT))
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=SHEETS_BODY))
    return response['spreadsheetId']


async def set_user_permissions(spreadsheet_id: str,
                               wrapper_services: Aiogoogle) -> None:
    """Функция для предоставления прав доступа вашему личному аккаунту
    к созданному документу."""
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(fileId=spreadsheet_id,
                                   json=permissions_body,
                                   fields="id"))


async def spreadsheets_update_value(spreadsheet_id: str,
                                    projects: list,
                                    wrapper_services: Aiogoogle
                                    ) -> None:
    """Функция обновления данных в гугл-таблице."""
    now_date_time = dt.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']]
    for project in projects:
        new_row = [str(project['name']),
                   str(project['close_time']),
                   str(project['description'])]
        table_values.append(new_row)

    update_body = {'majorDimension': 'ROWS',
                   'values': table_values}
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:C30',
            valueInputOption='USER_ENTERED',
            json=update_body))
