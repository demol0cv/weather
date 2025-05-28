from flask import Flask

from flask_session import Session
from routes import cities_bp, index_bp
from weather.settings import settings
from weather.utils import init_db


init_db()
app = Flask(__name__)


# Настройка Flask-Session
# Сохранять сессии на диске
app.config["SESSION_TYPE"] = settings.session_type
app.config["SECRET_KEY"] = settings.secret_key
Session(app)

# Регистрация маршрута для статистики городов
app.register_blueprint(cities_bp)
app.register_blueprint(index_bp)


if __name__ == "__main__":
    app.run(debug=settings.debug)
