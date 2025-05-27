import time
import uuid
from datetime import datetime

import requests
from flask import Blueprint, render_template, request, session

from weather.utils import geocode_city, get_user_history, save_request


index_bp = Blueprint("index", __name__)


@index_bp.route("/", methods=["GET", "POST"])
def index():
    # Устанавливаем user_id, если он отсутствует
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())
    user_id = session["user_id"]

    history = get_user_history(user_id)

    weather_data = None
    daily_data: dict[str, list] = {}
    location = None
    if request.method == "POST":
        city = request.form.get("city")
        time_start = time.time()
        # Получение координат города
        locations = geocode_city(city, namedetails=True)
        location = locations[0] if city else None
        time_end = time.time()
        print(f"Geocoding took {time_end - time_start:.2f} seconds for city: {city}")
        if location:
            lat, lon = location.get("latitude"), location.get("longitude")
            # Запрос к Open-Meteo
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,precipitation"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                weather_data = response.json()
                hourly_data: list[dict] = []
                save_request(user_id, location.get("value"), lat, lon)
                for i, _ in enumerate(weather_data["hourly"]["time"]):
                    if weather_data["hourly"]["time"][i] >= datetime.now().isoformat():
                        t = datetime.strptime(
                            weather_data["hourly"]["time"][i], "%Y-%m-%dT%H:%M"
                        )
                        t2 = weather_data["hourly"]["temperature_2m"][i]
                        pcp = weather_data["hourly"]["precipitation"][i]
                        hourly_data.append(
                            {
                                "time": t,
                                "temperature_2m": t2,
                                "precipitation": pcp,
                            }
                        )
                for data in hourly_data:
                    str_date: str = datetime.strftime(data["time"], "%Y-%m-%d")
                    if daily_data.get(str_date, None) is None:
                        daily_data[str_date] = []
                    daily_data[str_date].append(
                        {
                            "time": datetime.strftime(data["time"], "%H:%M"),
                            "temperature_2m": data["temperature_2m"],
                            "precipitation": data["precipitation"],
                        }
                    )

                weather_data["hourly"] = hourly_data
    return render_template(
        "index2carousel.html",
        weather_data=daily_data,
        city=location.get("value") if location is not None else "",
        history=history,
    )
