# Веб-приложение Погода

## Установка

1. Клонируем репозиторий:

```bash
git clone repo
```

2. Конфигурация

   > Конфигурация происходит при помощи переменных окружения, которые устанавливаются при помощи файла **.env** (и/или **.env.prod**) или при помощи [параметров запуска docker-compose](https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/) или комбинируя оба метода. Параметры заданные при помощи переменных окружения имеют наивысший приоритет, затем идёт **.env** и последний **.env.prod**.

- Устанавливаем secret_key при помощи переменной окружения WEATHER\_\_SECRET_KEY [Обязательно]
- Указываем расположение логов при помощи переменной WEATHER\_\_LOGS_DIR, если изменили точку монтирования. По умолчанию **logs**

Остальные переменные описаны ниже и в файле **.env.example**:

```toml
WEATHER__SECRET_KEY="your-secret-key-1234567890"
WEATHER__SESSION_TYPE=filesystem
WEATHER__GEOLOCATOR_USER_AGENT=weather_app
WEATHER__CACHE__AUTOCOMPLETE_CACHE_MAXSIZE=1000
WEATHER__CACHE__AUTOCOMPLETE_CACHE_TTL=86400 # 24 часа в секундах
WEATHER__CACHE__WEATHER_CACHE_MAXSIZE=100
WEATHER__CACHE__WEATHER_CACHE_TTL=600  # 10 минут в секундах
WEATHER__DATABASE_PATH=weather.db
WEATHER__LOGS_DIR=logs
WEATHER__DEBUG=True
```

## Запуск

```bash
docker-compose up --build
```
