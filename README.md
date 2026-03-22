![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135.1-green?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-✅-blue?style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?style=flat-square)

# Algo Notes 📚

Сервис для хранения и управления алгоритмическими заметками.

---

## 🚀 Стек технологий

* **Backend:** FastAPI
* **База данных:** PostgreSQL
* **Контейнеризация:** Docker + Docker Compose
* **ORM:** SQLAlchemy

---

## ⚙️ Установка и запуск проекта

1. Клонируем репозиторий:

```bash
git clone https://github.com/Denisonya/algo-notes.git
cd algo-notes
````

2. Создаём `.env` на основе примера:

```bash
cp .env.example .env
```

3. Сборка и запуск Docker-контейнеров:

```bash
docker compose up --build
```

> Контейнеры:
>
> * backend (FastAPI)
> * PostgreSQL
> * (в будущем фронтенд)

4. Доступ:

* API: [http://localhost:8000](http://localhost:8000)
* Документация: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📂 Структура проекта

```
backend/     — API (FastAPI)
frontend/    — клиент (React/Vue или другой)
```

### Backend

```
backend/app           — бизнес-логика
backend/app/api       — маршруты (routes)
backend/app/core      — конфигурации, настройки
backend/app/db        — база данных и модели
backend/app/schemas   — Pydantic схемы
backend/app/services  — сервисный слой
backend/app/tests     — тесты
```

---

## 🛠 Разработка

* Запуск разработки:

```bash
docker compose up
```

* Локальные изменения можно тестировать на [http://localhost:8000/docs](http://localhost:8000/docs)

* Для миграций базы данных (если используешь Alembic):

```bash
docker compose exec backend alembic upgrade head
```

---

## 📌 GitFlow

* **main** — продакшен
* **develop** — разработка
* **feature/*** — новые фичи
* **hotfix/*** — срочные исправления

> Каждый новый функционал делается в отдельной ветке `feature/название`, потом сливается в `develop`.
> После стабильного тестирования — merge в `main`.

---

## 📁 Лицензия

Проект лицензирован под [MIT License](LICENSE)

---

## ✨ Полезные ссылки

* [FastAPI Documentation](https://fastapi.tiangolo.com/)
* [Docker Documentation](https://docs.docker.com/)
* [PostgreSQL Documentation](https://www.postgresql.org/docs/)
* [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

---