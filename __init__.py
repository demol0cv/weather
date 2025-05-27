import logging
from pathlib import Path

from pythonjsonlogger import jsonlogger

from weather.settings import settings


# Получение пути к каталогу логов из переменной окружения
logs_dir = settings.logs_dir
Path(logs_dir).mkdir(
    parents=True, exist_ok=True
)  # Создаем каталог, если он не существует
log_file = Path(logs_dir) / "app.log"

# Настройка логгера
logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)

# Форматтер
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Обработчик для консоли
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Обработчик для файла
file_handler = logging.FileHandler(log_file, mode="a")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Обработчик для JSON-формата
json_handler = logging.FileHandler(log_file.with_suffix(".json"), mode="a")
json_handler.setLevel(logging.DEBUG)
json_formatter = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
)
json_handler.setFormatter(json_formatter)
logger.addHandler(json_handler)
