# Algo Notes 📚

Сервис для хранения и управления алгоритмическими заметками.

## 🚀 Стек

* FastAPI
* PostgreSQL
* Docker
* SQLAlchemy

## ⚙️ Запуск проекта

```bash
git clone https://github.com/your-username/algo-notes.git
cd algo-notes
cp .env.example .env
docker compose up --build
```

## 🌐 Доступ

* API: http://localhost:8000
* Docs: http://localhost:8000/docs

## 📂 Структура проекта

```
backend/     — API (FastAPI)
frontend/    — клиент
```

## 🛠 Разработка

```bash
docker compose up
```

## 📁 Структура

```
backend/app — бизнес-логика
backend/app/api — роуты
backend/app/core — конфиги
backend/app/db — база данных
```

## 📌 GitFlow

* main — продакшен
* develop — разработка
* feature/* — фичи
* hotfix/* — сроные фиксы