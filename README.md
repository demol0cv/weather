# Веб-приложение Погода

- Всё запускается в контейнере при помощи docker-compose
- Сделаны автодоплнения при вводе города
- Пишется история просмотра погоды по городам. Авторизации нет, только cookies. Т.е. для каждого браузера/устройства своя история.
- При посещении страницы, если ранее в этом браузере смотрели погоду, будет показана история просмотра с возможностью повторить запрос
- Есть эндпоинт /city_statistics выводящий в json статистику по городам

## Установка

1. Клонируем репозиторий:

```bash
git clone git@github.com:demol0cv/weather.git
```

2. Конфигурация

   > Конфигурация происходит при помощи переменных окружения, которые устанавливаются при помощи файла **.env**.

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
