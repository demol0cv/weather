# Сохранение запроса в базу данных
import sqlite3
from datetime import datetime, timezone
from http import HTTPStatus
from pathlib import Path
from typing import Any

import requests
from cachetools import TTLCache, cached
from geopy.geocoders import Nominatim

from weather.settings import settings


DB_NAME = "weather.db"
DB_PATH = Path(settings.database_path) / DB_NAME
# Создание директории для базы данных, если она не существует
Path(settings.database_path).mkdir(parents=True, exist_ok=True)

autocomplete_cache = TTLCache(
    maxsize=settings.cache.autocomplete_cache_maxsize,
    ttl=settings.cache.autocomplete_cache_ttl,
)
weather_cache = TTLCache(
    maxsize=settings.cache.weather_cache_maxsize,
    ttl=settings.cache.weather_cache_ttl,
)

# Инициализация геокодера
geolocator = Nominatim(user_agent=settings.geolocator_user_agent, timeout=10)


# Инициализация базы данных SQLite
def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS weather_requests (
                user_id TEXT,
                city TEXT,
                latitude REAL,
                longitude REAL,
                request_time TEXT,
                views_count INTEGER DEFAULT 1,
                PRIMARY KEY (user_id, city)
            
            )
        """,
        )
        conn.commit()


def save_request(user_id: str, city: str, latitude: float, longitude: float) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Проверяем, существует ли запись с данной комбинацией user_id и city
        cursor.execute(
            """
            SELECT 1 FROM weather_requests WHERE user_id = ? AND city = ?
        """,
            (user_id, city),
        )
        exists = cursor.fetchone()

        if exists:
            # Обновляем существующую запись
            requests_count = cursor.execute(
                """
                SELECT views_count FROM weather_requests WHERE user_id = ? AND city = ?
            """,
                (user_id, city),
            ).fetchone()[0]
            requests_count += 1
            cursor.execute(
                """
                UPDATE weather_requests
                SET latitude = ?, longitude = ?, request_time = ?, views_count = ?
                WHERE user_id = ? AND city = ?
                """,
                (
                    latitude,
                    longitude,
                    datetime.now().isoformat(),
                    requests_count,
                    user_id,
                    city,
                ),
            )
        else:
            # Создаем новую запись
            cursor.execute(
                """
                INSERT INTO weather_requests (user_id, city, latitude, longitude, request_time)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    user_id,
                    city,
                    latitude,
                    longitude,
                    datetime.now().isoformat(),
                ),
            )
        conn.commit()


# Получение истории запросов пользователя
def get_user_history(user_id: str) -> list[tuple[str, str, float, float, str]]:
    """Получает историю запросов пользователя из базы данных."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT city, latitude, longitude, request_time
            FROM weather_requests
            WHERE user_id = ?
            ORDER BY request_time DESC
        """,
            (user_id,),
        )
        return cursor.fetchall()


def get_city_statistics() -> list[dict[str, Any]]:
    """Получает статистику по городам из базы данных."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT sum(views_count) , city
            FROM weather_requests
            group by city
        """,
        )

        return [
            {"count_views": count, "city_name": city_name}
            for count, city_name in cursor.fetchall()
        ]


# Функция для сохранения города в базе данных
def save_city(city: str) -> None:
    """Сохраняет город и текущую метку времени в базу данных."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now(tz=timezone.UTC)  # .strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO cities (city, timestamp) VALUES (?, ?)",
        (city, timestamp),
    )
    conn.commit()
    conn.close()


# Функция для геокодирования с кэшированием
@cached(autocomplete_cache)
def geocode_city(query: str, **kwargs) -> list[dict[str, Any]] | list:
    """Геокодирует город с использованием Nominatim и кэширует результаты."""
    try:
        locations = geolocator.geocode(query, exactly_one=False, limit=10, **kwargs)
        if locations:
            res = [
                {
                    "label": location.address,
                    "value": location.address,
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                }
                for location in locations
            ]
            return res
        return []
    except Exception as e:
        print(f"Geocode error: {e}")
        return []


# Функция для получения прогноза погоды с кэшированием
@cached(weather_cache, key=lambda lat, lon: f"{lat}:{lon}")
def get_weather(lat: float | str, lon: float | str):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,precipitation"
        response = requests.get(url, timeout=10)
        if response.status_code == HTTPStatus.OK:
            return response.json()
        return None
    except Exception as e:
        print(f"Weather API error: {e}")
        return None
