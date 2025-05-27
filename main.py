from flask import Flask

from flask_session import Session
from routes import cities_bp, index_bp
from weather.settings import settings
from weather.utils import get_city_statistics, init_db


app = Flask(__name__)

# Настройка Flask-Session
# Сохранять сессии на диске
app.config["SESSION_TYPE"] = settings.session_type
app.config["SECRET_KEY"] = settings.secret_key
Session(app)

# Регистрация маршрута для статистики городов
app.register_blueprint(cities_bp)
app.register_blueprint(index_bp)


@app.route("/settings", methods=["GET"])
def get_settings():
    """Возвращает настройки приложения."""
    return settings.secret_key


if __name__ == "__main__":
    init_db()  # Инициализация базы данных при запуске приложения
    print(get_city_statistics())
    print(settings.secret_key)
    app.run(debug=settings.debug)
