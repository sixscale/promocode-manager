# 🚀 Jet Land PromoCode Manager

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

**Управление промокодами для системы Jet Land**

[Установка](#-установка) • [Использование](#-использование) • [API](#-api) 

</div>

---

## 📋 Описание

**Jet Land PromoCode Manager** — это тестовое задание для компании Jet Land.

### ✨ Основные возможности

| Функция | Описание |
|---------|----------|
| 🎫 **Генерация** | Создание уникальных промокодов с кастомными параметрами |
| ✅ **Валидация** | Проверка срока действия, статуса и условий использования |
| 🎯 **Применение** | Интеграция с системой заказов Jet Land |
| 🐳 **Docker** | Полная контейнеризация для быстрого развертывания |
| 🧪 **Тестирование** | Покрытие pytest для надежности |

---

---

## 🚀 Быстрый старт

### Требования

- **Python** 3.10+
- **Docker** & Docker Compose
- **uv** (рекомендуется) или pip

### Установка

#### 1. Клонирование репозитория

```bash
git clone https://github.com/sixscale/test-jet-land-promocode.git
cd test-jet-land-promocode
```
#### 2. Настройка окружения
```bash
Copy
cp .env.example .env
```
# Отредактируйте .env при необходимости
#### 3. Установка зависимостей
```bash
С использованием uv (рекомендуется ⚡):
bash
Copy
uv sync
```
Или с pip:
```bash
Copy
pip install -e .
```
#### 4. Запуск с Docker 🐳
```bash
Copy
docker compose up --build
```
## 💻 Использование
#### Локальный запуск сервера
```bash
Copy
python manage.py runserver
```
### Сервер будет доступен по адресу: http://127.0.0.1:8000
#### Запуск тестов
```bash
Copy
pytest -v
```
#### CLI-интерфейс
```bash
Copy
python main.py --help
```
## 🔧 Переменные окружения
## Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `DEBUG` | Режим отладки | `False` |
| `SECRET_KEY` | Секретный ключ Django | — |
| `DATABASE_URL` | URL подключения к БД | `sqlite:///db.sqlite3` |

Распространяется под лицензией MIT. См. LICENSE для подробностей.
<div align="center">
⭐ Star this repo if you find it helpful!
Made with ❤️ for Jet Land
</div>
```
