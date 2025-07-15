# Financial Data Streaming Backend

A modern, event-driven backend for real-time financial data polling, analytics, and streaming, built with FastAPI, async SQLAlchemy, Kafka, Redis, and PostgreSQL. Designed for speed, scalability, and developer happiness.

---

## 🚀 Overview

Financial Data Streaming Backend is a cloud-ready, microservice-inspired platform for:

- Polling and aggregating financial market data from multiple providers (Yahoo Finance, Alpha Vantage, etc.)
- Real-time price event streaming and analytics via Kafka
- Caching and fast retrieval with Redis
- Storing raw and processed data in PostgreSQL
- Async, background processing for high throughput
- Extensible API for integration and automation

---

## ✨ Features

- **Async FastAPI API**: Blazing-fast endpoints for price queries, polling jobs, and analytics
- **Polling Service**: Background polling of symbols/providers at custom intervals
- **Price Service**: Fetches, caches, and persists prices; supports multiple providers
- **Kafka Integration**: Publishes price events and consumes them for moving average analytics
- **Moving Average Consumer**: Background task computes and stores moving averages
- **Redis Caching**: Lightning-fast cache for price lookups and reduced API calls
- **PostgreSQL Storage**: Persists raw prices, price points, polling jobs, and analytics
- **Docker Compose**: One-command local dev with Postgres, Redis, Kafka, Zookeeper
- **Environment Variable Support**: All secrets/configs via `.env` for security and flexibility
- **Unit & API Tests**: Example tests for services and endpoints
- **Structured Logging**: Loguru + standard logging for beautiful, colorized logs
- **Extensible Architecture**: Add new providers, analytics, or event consumers easily
- **Adminer UI**: Visual database management out of the box
- **Makefile & Scripts**: Streamlined dev workflow

---

## 🏗️ Architecture

```
FastAPI
  ├── PollingService (async background task)
  │     └── Calls own API endpoints to fetch/store prices
  ├── PriceService
  │     ├── Fetches from providers (Yahoo, Alpha Vantage)
  │     ├── Caches in Redis
  │     └── Stores in PostgreSQL
  ├── Kafka Producer
  │     └── Publishes price events
  ├── Kafka Consumer (async background task)
  │     └── Computes moving averages, stores in DB
  ├── RedisService
  └── PostgreSQL (async SQLAlchemy)
```

---

## 🛠️ Setup & Local Development

### 1. Clone the repository

```sh
git clone https://github.com/ShreyansJa1n/financial-data-streaming-backend
cd financial-data-streaming-backend
```

### 2. Create a `.env` file

```env
DATABASE_URL=postgresql+asyncpg://backend_db:backend_db@postgres:5432/backend_db_db
REDIS_URL=redis://redis:6379/0
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
POSTGRES_USER=backend_db
POSTGRES_PASSWORD=backend_db
POSTGRES_DB=backend_db
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
```

### 3. Start services with Docker Compose

```sh
docker compose -f docker-compose-dev.yaml up --build
# OR
make -C ./scripts run_development
```

This will start:

- FastAPI app
- PostgreSQL
- Redis
- Kafka & Zookeeper
- Adminer (DB UI)

### 4. Install dependencies

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements/requirements.txt
```

Or use the helper script:

```sh
./scripts/install_dependency.sh [dependency]
```

---

## 📚 API Documentation

Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### Example Endpoints

- `GET /prices/latest/?symbol=AAPL&provider=yahoo_finance`  
  Get the latest price for a symbol from a provider.
- `POST /polling-jobs/`  
  Create a new polling job (symbols, provider, interval).
- `GET /polling-jobs/`  
  List all polling jobs.

---

## 🧪 Testing & Quality

- **Run tests:**

  ```sh
  PYTHONPATH=. pytest
  ```

- **Linting:**
  Use `flake8` or `black` for code style.
- **Type checking:**
  Use `mypy` for static type checks.

---

## 🧩 Extending & Integrating

- Add new price providers by implementing the provider interface
- Add new analytics/event consumers by subscribing to Kafka topics
- Use the API for automation, dashboards, or integration with other systems

---

## 🐞 Troubleshooting

- **ModuleNotFoundError: No module named 'app'**
    - Run pytest from the project root and/or set PYTHONPATH=.
- **Can't load plugin: sqlalchemy.dialects:ostgresql**
    - Typo in your DATABASE_URL. Use postgresql+asyncpg://..., not ostgresql.
- **Kafka/Redis/Postgres connection errors**
    - Ensure Docker containers are running and ports are not blocked.
- **Async SQLAlchemy errors**
    - Always `await` async DB calls like `fetchall()`.
- **Background tasks block server**
    - Use `asyncio.create_task(...)` for background services, never `await` infinite loops directly.

---

## 🧠 Architecture Decisions

- **Async everywhere:** For scalability and performance
- **Kafka for event-driven processing:** Decouples price ingestion and analytics
- **Background tasks via FastAPI lifespan:** Clean startup/shutdown of polling and consumer services
- **Environment variables for config:** Secure and flexible deployments
- **Docker Compose for local dev:** Easy onboarding and consistent environments

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch
3. Write tests for your feature/fix
4. Submit a PR

---

## 📄 License

MIT

---

*Built for speed, reliability, and fun. Happy coding!*

