import secrets
import string

from urllib.parse import urlparse

from app import db
from app.models import URL


# Символы, которые будем использовать
# для генерации короткого кода.
#
# Получаем:
#
# abcdefghijklmnopqrstuvwxyz
# ABCDEFGHIJKLMNOPQRSTUVWXYZ
# 0123456789
#
# Например из этих символов может получиться:
#
# aB7xK2
#
CHARACTERS = string.ascii_letters + string.digits


def generate_short_code(length=6):
    """
    Генерирует случайный короткий код.

    Параметр length определяет длину кода.

    По умолчанию:
        length = 6

    Например функция может вернуть:

        "aB72xK"

    Используем secrets.choice(), потому что secrets
    предназначен для генерации качественных случайных значений.
    """

    return "".join(
        secrets.choice(CHARACTERS)
        for _ in range(length)
    )


def generate_unique_short_code():
    """
    Генерирует уникальный короткий код.

    Проблема:
    случайно может сгенерироваться код,
    который уже существует в базе.

    Например:

        В базе уже есть:
        ABC123

        Генератор снова создал:
        ABC123

    Поэтому проверяем базу.

    Если код уже существует —
    генерируем новый.

    Если свободен —
    возвращаем его.
    """

    while True:

        # Генерируем случайный код.
        code = generate_short_code()

        # Ищем такой код в базе данных.
        existing_url = URL.query.filter_by(
            short_code=code
        ).first()

        # Если запись не найдена,
        # значит код свободен.
        if existing_url is None:
            return code


def is_valid_url(url):
    """
    Проверяет, является ли строка корректным URL.

    Например:

        https://google.com
        -----------------
        True

        http://example.com
        ------------------
        True

        google.com
        ----------
        False

        hello
        -----
        False

    """

    try:

        # Разбираем URL на отдельные части.

        # Например:

        # https://google.com/test

        # scheme:
        # https

        # netloc:
        # google.com

        parsed = urlparse(url)

        # Разрешаем только HTTP и HTTPS.
        valid_scheme = parsed.scheme in (
            "http",
            "https"
        )

        # Проверяем наличие домена.
        has_domain = bool(parsed.netloc)

        # URL считается правильным,
        # если есть подходящий протокол
        # И есть домен.
        return valid_scheme and has_domain

    except ValueError:

        # Если urlparse() обнаружил
        # некорректный URL,
        # возвращаем False.
        return False


def create_short_url(original_url):
    """
    Создаёт новую сокращённую ссылку.

    Эта функция выполняет несколько действий:

    1. Генерирует уникальный short_code.
    2. Создаёт объект URL.
    3. Добавляет его в SQLAlchemy session.
    4. Сохраняет данные в базе.
    5. Возвращает созданный объект.
    """

    # Получаем уникальный короткий код.

    # Например:
    #
    # "aB7xK2"
    #
    short_code = generate_unique_short_code()

    # Создаём объект модели URL.

    # Пока он существует только
    # в памяти Python.
    url = URL(
        original_url=original_url,
        short_code=short_code
    )

    # Добавляем объект в текущую транзакцию.
    db.session.add(url)

    # COMMIT фактически сохраняет
    # изменения в базе данных.
    db.session.commit()

    # Возвращаем созданный объект.
    return url


def get_url_by_code(short_code):
    """
    Ищет URL по короткому коду.
    """

    return URL.query.filter_by(
        short_code=short_code
    ).first()