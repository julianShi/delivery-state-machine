# Development Guide

This document provides instructions for setting up and developing the Delivery State Machine service.

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Redis 6+
- RabbitMQ 3.8+
- Docker and Docker Compose (optional)

## Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd delivery-state-machine
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   POSTGRES_SERVER=localhost
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=delivery_state_machine
   REDIS_HOST=localhost
   REDIS_PORT=6379
   RABBITMQ_HOST=localhost
   RABBITMQ_PORT=5672
   RABBITMQ_USER=guest
   RABBITMQ_PASSWORD=guest
   SECRET_KEY=your-secret-key
   ```

5. **Set up the database**
   ```bash
   # Create database
   createdb delivery_state_machine

   # Run migrations
   alembic upgrade head
   ```

6. **Start the services**
   ```bash
   # Start Redis
   redis-server

   # Start RabbitMQ
   rabbitmq-server

   # Start Celery worker
   celery -A app.worker worker --loglevel=info

   # Start the API server
   uvicorn app.main:app --reload
   ```

## Using Docker

Alternatively, you can use Docker Compose to start all services:

```bash
docker-compose up -d
```

## Running Tests

1. **Set up test database**
   ```bash
   createdb delivery_state_machine_test
   ```

2. **Run tests**
   ```bash
   pytest
   ```

   For coverage report:
   ```bash
   pytest --cov=app tests/
   ```

## Debugging

### API Server

1. **Enable debug logging**
   Set `LOG_LEVEL=DEBUG` in your `.env` file

2. **Access API documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Monitor logs**
   ```bash
   tail -f logs/app.log
   ```

### Database

1. **Connect to database**
   ```bash
   psql -U postgres -d delivery_state_machine
   ```

2. **View recent delivery events**
   ```sql
   SELECT * FROM delivery_state_events 
   ORDER BY created_at DESC 
   LIMIT 10;
   ```

### Message Queue

1. **Monitor RabbitMQ**
   - Management UI: http://localhost:15672
   - Default credentials: guest/guest

2. **View Celery tasks**
   ```bash
   celery -A app.worker flower
   ```

## Common Issues

1. **Database Connection Issues**
   - Check PostgreSQL is running
   - Verify database credentials in `.env`
   - Ensure database exists

2. **Message Queue Issues**
   - Check RabbitMQ is running
   - Verify connection settings
   - Check Celery worker logs

3. **WebSocket Connection Issues**
   - Check client connection URL
   - Verify WebSocket endpoint is accessible
   - Check server logs for connection errors

## Development Workflow

1. **Code Style**
   ```bash
   # Format code
   black .
   isort .

   # Check code style
   flake8
   mypy .
   ```

2. **Database Migrations**
   ```bash
   # Create new migration
   alembic revision --autogenerate -m "description"

   # Apply migrations
   alembic upgrade head
   ```

3. **API Testing**
   ```bash
   # Run specific test file
   pytest tests/api/test_delivery.py -v

   # Run with specific marker
   pytest -m "integration" -v
   ```

## Monitoring

1. **Prometheus Metrics**
   - Available at: http://localhost:8000/metrics

2. **Grafana Dashboards**
   - Access Grafana: http://localhost:3000
   - Default credentials: admin/admin

## Contributing

1. Create a new branch for your feature
2. Write tests for new functionality
3. Ensure all tests pass
4. Submit a pull request

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
