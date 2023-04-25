cat_charity_fund

# Сервис Благотворительного фонда поддержки котиков QRKot

Фонд собирает пожертвования на любые цели, связанные с поддержкой кошачьей популяции.

В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.

## Технологии
- Python
- FastAPI
- SQLAlchemy
- Alembic
- Uvicorn

### Документация и функционал Swagger доступны на локальном сервере

```sh
http://127.0.0.1:8000/docs
```

## Использование

#### Клонируйте реппозиторий

```sh
git clone https://github.com/margoloko/cat_charity_fund
```

#### Перейдите в папку cat_charity_fund, установите и запустите виртуальное окружение.

```sh
cd cat_charity_fund
```

```
python -m venv venv
```

* Если у вас Linux/MacOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/Scripts/activate
    ```
#### Установите зависимости:

```sh
pip install -r requirements.txt
```

#### Запустите приложение на локальном сервере

```sh
uvicorn app.main:app --reload
```

### Автор
[Балахонова Марина](https://github.com/margoloko)
