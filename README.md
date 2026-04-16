![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135.1-green?style=flat-square)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.48-red?style=flat-square)
![Pydantic](https://img.shields.io/badge/Pydantic-2.12.5-0288D1?style=flat-square&logo=pydantic)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue?style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?style=flat-square)
![Uvicorn](https://img.shields.io/badge/Uvicorn-0.41.0-F8F8F9?style=flat-square&logo=uvicorn&logoColor=000000)
![Pytest](https://img.shields.io/badge/Pytest-9.0.3-0A9EDC?style=flat-square&logo=pytest)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&logo=github-actions)
![License](https://img.shields.io/github/license/Denisonya/algo-notes?style=flat-square)

# Algo Notes 📚

Algo Notes - сервис для хранения, структурирования и изучения алгоритмов.

---

## 📑 Основные разделы

* [🧠 Удобное обучение](#-удобное-обучение)
* [🚀 Возможности](#-возможности)
* [🛠 Технологический стек](#-технологический-стек)
* [📂 Актуальная структура проекта](#-актуальная-структура-проекта)
* [⚙️ Полная установка и запуск (Docker)](#-полная-установка-и-запуск-docker)
* [🐳 Полезные Docker команды](#-полезные-docker-команды)
* [📌 REST API](#-rest-api)
* [🧪 Тестирование](#-тестирование)
* [🧱 Архитектурный подход](#-архитектурный-подход)
* [🔐 Конфигурация](#-конфигурация)
* [🚀 Будущие улучшения](#-будущие-улучшения)
* [📌 GitFlow](#-gitflow)
* [✨ Полезные ссылки](#-полезные-ссылки)
* [📄 Лицензия](#-лицензия)
* [📬 Контакты](#-контакты)

---

# 🧠 Удобное обучение

Пользователь может:
* Писать конспекты по алгоритмам
* У каждого пользователя свои заметки
* Структурировать знания
* Быстро находить нужное

---

# 🚀 Возможности

* Создание категорий заметок
* Создание заметок с привязкой к категориям
* Получение списка заметок и категорий
* Получение заметки по ID
* Фильтрация заметок по категории
* Полное обновление
* Частичное обновление
* Удаление записей
* Автоматическая Swagger-документация
* Контейнеризация через Docker Compose

---

# 🛠 Технологический стек

## Backend

* FastAPI
* SQLAlchemy 2.0
* Pydantic v2
* PostgreSQL

## Infrastructure

* Docker
* Docker Compose

---

# 📂 Актуальная структура проекта

```text
algo-notes/
│
├── app/
│   ├── core/              # настройки, БД, исключения
│   │   ├── database.py
│   │   ├── settings.py
│   │   └── exceptions.py
│   │
│   ├── dependencies/      # зависимости FastAPI
│   │   └── db.py
│   │
│   ├── models/            # SQLAlchemy модели
│   │   ├── base.py
│   │   ├── category.py
│   │   └── note.py
│   │
│   ├── repositories/      # работа с БД
│   │   ├── category_repository.py
│   │   └── note_repository.py
│   │
│   ├── routers/           # API endpoints
│   │   ├── category_router.py
│   │   └── note_router.py
│   │
│   ├── schemas/           # Pydantic схемы
│   │   ├── category.py
│   │   └── note.py
│   │
│   ├── services/          # бизнес-логика
│   │   ├── category_service.py
│   │   └── note_service.py
│   │
│   ├── utils/             # вспомогательные функции
│   │   ├── common.py
│   │   └── markdown.py
│   │
│   └── main.py            # точка входа
│
├── tests/                 # тесты
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

# ⚙️ Полная установка и запуск (Docker)

## 1. Клонировать репозиторий

```bash
git clone https://github.com/Denisonya/algo-notes.git
cd algo-notes
```

---

## 2. Создать файл `.env`

Создай файл `.env` в корне проекта:

```env
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=algo_notes
POSTGRES_USER=algo_user
POSTGRES_PASSWORD=algo_password
```

> `db` - это имя контейнера PostgreSQL внутри Docker сети.

---

## 3. Собрать и запустить контейнеры

```bash
docker compose up --build
```

После запуска будут подняты сервисы:

* `backend` - FastAPI приложение
* `db` - PostgreSQL база данных

---

## 4. Проверить доступность

### API

http://localhost:8000

### Swagger UI

http://localhost:8000/docs

### ReDoc

http://localhost:8000/redoc

---

# 🐳 Полезные Docker команды

## Запуск в фоне

```bash
docker compose up -d
```

## Остановить контейнеры

```bash
docker compose down
```

## Пересобрать проект

```bash
docker compose up --build
```

## Удалить контейнеры + volumes

```bash
docker compose down -v
```

## Логи приложения

```bash
docker compose logs -f backend
```

## Подключиться к PostgreSQL контейнеру

```bash
docker compose exec db psql -U algo_user -d algo_notes
```

---

# 📌 REST API

## Categories

| Метод  | Endpoint           | Описание             |
|--------|--------------------|----------------------|
| GET    | `/categories/`     | Все категории        |
| GET    | `/categories/{id}` | Категория по ID      |
| POST   | `/categories/`     | Создать категорию    |
| PUT    | `/categories/{id}` | Полное обновление    |
| PATCH  | `/categories/{id}` | Частичное обновление |
| DELETE | `/categories/{id}` | Удалить категорию    |

---

## Notes

| Метод  | Endpoint               | Описание             |
|--------|------------------------|----------------------|
| GET    | `/notes/`              | Все заметки          |
| GET    | `/notes/{id}`          | Заметка по ID        |
| GET    | `/notes/category/{id}` | Заметки категории    |
| POST   | `/notes/`              | Создать заметку      |
| PUT    | `/notes/{id}`          | Полное обновление    |
| PATCH  | `/notes/{id}`          | Частичное обновление |
| DELETE | `/notes/{id}`          | Удалить заметку      |

---

# 🧪 Тестирование

Если тесты подключены:

```bash
pytest
```

Или внутри контейнера:

```bash
docker compose exec backend pytest
```

---

# 🧱 Архитектурный подход

## Router Layer

Обрабатывает HTTP запросы/ответы.

## Service Layer

Содержит бизнес-логику.

## Repository Layer

Работа напрямую с БД.

## Schema Layer

Валидация данных через Pydantic.

## Utils Layer

Переиспользуемые функции.

---

# 🔐 Конфигурация

Настройки проекта находятся в:

```text
app/core/settings.py
```

Используется `pydantic-settings`.

---

# 🚀 Будущие улучшения

* Alembic миграции
* JWT авторизация
* Пользователи
* Поиск по заметкам
* Markdown preview
* Frontend (Jinja)
* Асинхронный режим работы
* CI/CD pipeline
* Production deployment

---

# 📌 GitFlow

* `main` - стабильная версия
* `develop` - разработка
* `feature/*` - новые функции
* `hotfix/*` - срочные исправления
* `docs/*` - документация

---

# ✨ Полезные ссылки

* FastAPI - https://fastapi.tiangolo.com/
* SQLAlchemy - https://docs.sqlalchemy.org/
* PostgreSQL - https://www.postgresql.org/docs/
* Docker - https://docs.docker.com/

---

# 📄 Лицензия

Проект лицензирован под [MIT License](LICENSE)

---

## 📬 Контакты

Если у вас есть идеи, предложения или вопросы по проекту - буду рад обратной связи.

* GitHub: https://github.com/Denisonya
* Repository: https://github.com/Denisonya/algo-notes
* Issues: https://github.com/Denisonya/algo-notes/issues

⭐ Если проект оказался полезным - поставьте звезду репозиторию.

---