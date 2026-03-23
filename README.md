# WebSocket Chat

Real-time чат-приложение на базе WebSocket с использованием Clean Architecture, DDD и CQRS.

## Архитектура

Проект построен на принципах Clean Architecture с разделением на слои:

- **Domain Layer** - бизнес-логика, сущности, value objects, доменные события
- **Application Layer** - CQRS: команды, обработчики, медиатор
- **Infrastructure Layer** - база данных, Redis, репозитории
- **Presentation Layer** - API endpoints, WebSocket, схемы

### Используемые паттерны

- **DDD (Domain-Driven Design)** - сущности с уникальным идентификатором `oid`, Value Objects, доменные события
- **CQRS** - разделение команд и запросов через паттерн Mediator
- **Repository** - абстракция доступа к данным
- **Mediator** - централизованная диспетчеризация команд и событий

## Технологический стек

### Backend
- **FastAPI** - асинхронный веб-фреймворк
- **SQLAlchemy 2.0** - async ORM
- **PostgreSQL** - основная база данных
- **Redis** - pub/sub для распределенных событий
- **WebSocket** - real-time коммуникация
- **Alembic** - миграции базы данных
- **Pydantic v2** - валидация данных
- **Poetry** - управление зависимостями

### Frontend
- **HTML5, CSS3, JavaScript** - чистый фронтенд без фреймворков
- **Bootstrap 5** - стилизация и адаптивность
- **Bootstrap Icons** - иконки
- **WebSocket API** - real-time обмен сообщениями

## Структура проекта

```
app/
├── application/           # Слой приложения (CQRS)
│   ├── commands/          # Команды и их обработчики
│   ├── handlers/          # Обработчики событий
│   ├── exceptions/        # Исключения приложения
│   ├── dependencies.py    # FastAPI зависимости
│   └── mediator.py        # Реализация медиатора
├── domain/                # Доменный слой (DDD)
│   ├── entities/          # Доменные сущности
│   ├── events/            # Доменные события
│   ├── values/            # Value Objects
│   └── exceptions/        # Доменные исключения
├── infrastructure/        # Инфраструктурный слой
│   ├── database/
│   │   ├── models/        # SQLAlchemy ORM модели
│   │   ├── session.py     # Фабрика async сессий
│   │   └── migrations/    # Alembic миграции
│   ├── redis/             # Redis pub/sub
│   └── repositories/      # Реализации репозиториев
├── manager/               # WebSocket connection manager
├── presentation/          # Слой представления
│   └── api/
│       ├── endpoints/     # API endpoints
│       ├── schemas/       # Pydantic схемы
│       ├── static/        # Статические файлы (HTML, CSS, JS)
│       │   ├── index.html # Главная страница чата
│       │   ├── css/       # Стили
│       │   └── js/        # JavaScript
│       └── main.py        # FastAPI app factory
└── settings/              # Конфигурация
```

## Веб-интерфейс

Проект включает готовый веб-интерфейс для чата, доступный по адресу `http://localhost:8000/`

### Возможности:
- Авторизация по имени и email
- Создание чатов
- Real-time обмен сообщениями
- Список всех чатов
- Адаптивный дизайн (Bootstrap 5)
- Уведомления о новых сообщениях

### Как использовать:
1. Откройте `http://localhost:8000/` в браузере
2. Введите имя и email, нажмите "Войти"
3. Создайте чат или выберите существующий
4. Отправляйте сообщения в реальном времени

### Тестирование с несколькими пользователями:
1. Откройте две вкладки (или два разных браузера)
2. В каждой вкладке авторизуйтесь под разными пользователями
3. Создайте чат (или используйте общий)
4. Отправляйте сообщения - они появятся у всех участников

## Установка и запуск

### Предварительные требования

- Docker Desktop с включенным WSL2
- Make (опционально, для удобства)

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd websocket_chat
```

### 2. Настройка окружения

Скопируйте `.env.template` в `.env` и заполните параметры:

```bash
cp .env.template .env
```

Пример `.env`:

```env
API_PORT=8000
PYTHONPATH=app

DB_HOST=db
DB_PORT=5432
DB_USER=user
DB_PASSWORD=your_password
DB_NAME=websocket

DATABASE_URL=postgresql+asyncpg://user:your_password@db:5432/websocket

REDIS_HOST=redis
REDIS_PORT=6379
```

### 3. Первый запуск

```bash
# Остановить все контейнеры (если были запущены)
make down

# Запустить все сервисы
make all
```

### 4. Применение миграций

```bash
# Войти в контейнер приложения
make app-shell

# Применить миграции
alembic upgrade head

# Выйти из контейнера
exit
```

### 5. Проверка работы

Откройте в браузере: http://localhost:8000

**Веб-интерфейс чата:** http://localhost:8000/ (главная страница)

**Документация API:** http://localhost:8000/docs

**Health check:** http://localhost:8000/health

### 6. Быстрый тест чата

После запуска сервера:

1. Откройте http://localhost:8000/ в браузере
2. Введите имя и email, нажмите "Войти"
3. Нажмите "Новый чат", введите название
4. Откройте вторую вкладку в режиме инкогнито
5. Авторизуйтесь под другим пользователем
6. Обменивайтесь сообщениями в реальном времени!

### 7. Перезапуск после изменений кода

```bash
# Полный перезапуск с пересборкой
make down && make all

# Применить миграции если нужно
make app-shell
alembic upgrade head
```

## Команды Makefile

| Команда | Описание |
|---------|----------|
| `make all` | Запуск всех контейнеров |
| `make down` | Остановка всех контейнеров |
| `make storages` | Запуск PostgreSQL и Redis |
| `make app` | Запуск приложения |
| `make app-logs` | Просмотр логов приложения |
| `make app-shell` | Вход в контейнер приложения |
| `make test` | Запуск тестов |
| `make storages-down` | Остановка storages |

## API Endpoints

### REST API

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/users/` | Создание пользователя |
| GET | `/users/` | Получение всех пользователей |
| GET | `/users/{user_id}` | Получение пользователя по ID |
| POST | `/chats/` | Создание чата |
| GET | `/chats/` | Получение всех чатов |
| GET | `/chats/{chat_id}` | Получение чата по ID |
| GET | `/messages/chat/{chat_id}` | Получение сообщений чата |
| GET | `/health` | Health check |

### WebSocket

```
ws://localhost:8000/ws/{user_id}
```

Формат сообщений:

```json
// Отправка сообщения в чат
{
  "type": "message",
  "chat_id": "uuid",
  "text": "Привет!"
}

// Создание чата
{
  "type": "create_chat",
  "title": "Название чата",
  "participants": ["uuid1", "uuid2"]
}

// Присоединиться к конкретному чату
{
  "type": "join_chat",
  "chat_id": "uuid"
}
```

**Важно:** `sender_id` автоматически берется из URL WebSocket-соединения.

## Пример использования

### Пошаговое тестирование

#### 1. Создание пользователя

```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "username": "testuser", "password": "secret"}'
```

Ответ:
```json
{"id": "uuid-пользователя", "email": "user@example.com", "username": "testuser"}
```

#### 2. Создание чата

Используйте `id` пользователя из предыдущего шага:

```bash
curl -X POST http://localhost:8000/chats/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Мой чат", "type": "group", "creator_id": "ВАШ_USER_ID", "participants": ["ВАШ_USER_ID"]}'
```

Ответ:
```json
{"id": "uuid-чата", "title": "Мой чат", "type": "group", "participants": ["ВАШ_USER_ID"]}
```

#### 3. Получение пользователей

```bash
# Все пользователи
curl http://localhost:8000/users/

# Пользователь по ID
curl http://localhost:8000/users/ВАШ_USER_ID
```

#### 4. Получение чатов

```bash
# Все чаты
curl http://localhost:8000/chats/

# Чат по ID
curl http://localhost:8000/chats/ВАШ_CHAT_ID
```

### Проверка WebSocket

#### Вариант 1: Браузер (JavaScript)

Откройте консоль браузера (F12) и выполните:

```javascript
// Замените USER_ID на ID созданного пользователя
const ws = new WebSocket('ws://localhost:8000/ws/ВАШ_USER_ID');

ws.onopen = () => console.log('WebSocket подключен!');

ws.onmessage = (event) => console.log('Получено:', JSON.parse(event.data));

ws.onerror = (error) => console.error('Ошибка:', error);

// Отправка сообщения (замените chat_id)
ws.send(JSON.stringify({
  type: 'message',
  chat_id: 'ВАШ_CHAT_ID',
  text: 'Привет, мир!'
}));

// Присоединиться к чату
ws.send(JSON.stringify({
  type: 'join_chat',
  chat_id: 'ВАШ_CHAT_ID'
}));
```

#### Вариант 2: Postman

1. Откройте Postman
2. Создайте новый WebSocket запрос
3. URL: `ws://localhost:8000/ws/ВАШ_USER_ID`
4. Нажмите Connect
5. Отправьте JSON сообщение:
```json
{
  "type": "message",
  "chat_id": "ВАШ_CHAT_ID",
  "text": "Привет из Postman!"
}
```

#### Вариант 3: wscat (CLI)

Установка:
```bash
npm install -g wscat
```

Использование:
```bash
# Подключение
wscat -c ws://localhost:8000/ws/ВАШ_USER_ID

# Отправка сообщения (в интерактивном режиме)
>{"type":"message","chat_id":"ВАШ_CHAT_ID","text":"Привет!"}
```

#### Вариант 4: Python скрипт

Создайте файл `test_ws.py`:

```python
import asyncio
import websockets
import json

async def test_websocket():
    user_id = "ВАШ_USER_ID"
    chat_id = "ВАШ_CHAT_ID"
    
    uri = f"ws://localhost:8000/ws/{user_id}"
    
    async with websockets.connect(uri) as ws:
        print("Подключено!")
        
        # Сначала присоединяемся к чату
        await ws.send(json.dumps({
            "type": "join_chat",
            "chat_id": chat_id
        }))
        
        # Отправка сообщения
        message = {
            "type": "message",
            "chat_id": chat_id,
            "text": "Привет из Python!"
        }
        await ws.send(json.dumps(message))
        print(f"Отправлено: {message}")
        
        # Получение сообщений
        response = await ws.recv()
        print(f"Получено: {response}")

asyncio.run(test_websocket())
```

Запуск:
```bash
pip install websockets
python test_ws.py
```

## Полный сценарий тестирования

### Шаг 1: Создание пользователей

```bash
# Создать первого пользователя
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user1@test.ru", "username": "user1", "password": "pass1"}'

# Создать второго пользователя
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user2@test.ru", "username": "user2", "password": "pass2"}'

# Запомните ID обоих пользователей!
```

### Шаг 2: Создание чата

```bash
# Замените USER1_ID на ID первого пользователя
curl -X POST http://localhost:8000/chats/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Общий чат", "type": "group", "creator_id": "USER1_ID", "participants": ["USER1_ID", "USER2_ID"]}'

# Запомните ID чата!
```

### Шаг 3: Проверка данных

```bash
# Проверить пользователей
curl http://localhost:8000/users/

# Проверить чаты
curl http://localhost:8000/chats/

# Проверить сообщения чата
curl http://localhost:8000/messages/chat/CHAT_ID
```

### Шаг 4: Тестирование WebSocket

Откройте две вкладки браузера (F12 → Console):

**Таб 1 (User 1):**
```javascript
const ws1 = new WebSocket('ws://localhost:8000/ws/USER1_ID');
ws1.onmessage = (e) => console.log('User1:', JSON.parse(e.data));
ws1.onopen = () => ws1.send(JSON.stringify({type: 'join_chat', chat_id: 'CHAT_ID'}));
```

**Таб 2 (User 2):**
```javascript
const ws2 = new WebSocket('ws://localhost:8000/ws/USER2_ID');
ws2.onmessage = (e) => console.log('User2:', JSON.parse(e.data));
ws2.onopen = () => ws2.send(JSON.stringify({type: 'join_chat', chat_id: 'CHAT_ID'}));
```

**Отправить сообщение (из любой вкладки):**
```javascript
ws1.send(JSON.stringify({type: 'message', chat_id: 'CHAT_ID', text: 'Привет!'}));
```

Оба пользователя должны получить сообщение!

## Устранение проблем

### Ошибка "column does not exist"

Если возникает ошибка `column "is_active" of relation "users" does not exist`:

```bash
# Войти в контейнер
make app-shell

# Проверить статус миграций
alembic current

# Применить все миграции
alembic upgrade head

# Если не помогло - пересоздать базу
exit
make down
make all
make app-shell
alembic upgrade head
```

### Ошибка "relation does not exist"

```bash
# Полный перезапуск с очисткой
make down
docker volume rm websocket_chat_websocked_data 2>/dev/null || true
docker volume rm websocket_chat_redis_data 2>/dev/null || true
make all
make app-shell
alembic upgrade head
```

### Контейнер не запускается

```bash
# Посмотреть логи
make app-logs

# Проверить статус
docker ps -a

# Пересобрать
make down
make all
```

### WebSocket не подключается

1. Проверьте, что сервер запущен: http://localhost:8000/health
2. Проверьте логи: `make app-logs`
3. Убедитесь, что используете правильный `user_id`

## Разработка

### Установка зависимостей локально

```bash
poetry install
```

### Создание новой миграции

```bash
alembic revision --autogenerate -m "описание изменений"
```

### Запуск тестов

```bash
pytest
# или в контейнере:
make test
```

## Особенности реализации

### Value Objects

```python
@dataclass(frozen=True)
class Text(BaseValueObject[str]):
    def validate(self):
        if not self.value:
            raise EmptyTextException()
```

### Сущности с доменными событиями

```python
@dataclass(eq=False)
class Message(BaseEntity):
    chat_id: str
    sender_id: str
    text: Text
```

### CQRS через Mediator

```python
# Отправка команды
await mediator.send(SendMessageCommand(...))

# Подписка на события
mediator.subscribe(NewMessageReceivedEvent, handler)
```

## Лицензия

MIT