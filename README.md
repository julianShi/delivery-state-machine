# Delivery State Machine Service

This is the state machine microservice for the delivery order domain of the online book store business. It manages the lifecycle of delivery orders, handling state transitions and coordinating with other microservices in the ecosystem.

## Overview

The Delivery State Machine Service is responsible for:
- Managing delivery order state transitions
- Coordinating with third-party delivery partners
- Handling delivery exceptions and operator interventions
- Ensuring reliable delivery tracking and status updates

## Features

- State machine implementation for delivery order lifecycle
- Event-driven architecture using CQRS pattern
- Integration with payment and order management services
- Real-time delivery status updates
- Operator dashboard for exception handling
- Comprehensive monitoring and logging

## Tech Stack

- **Backend**: Python 3.9+
- **Framework**: FastAPI
- **Async Processing**: Celery
- **Message Queue**: RabbitMQ
- **Database**: PostgreSQL
- **Cache**: Redis
- **Monitoring**: Prometheus & Grafana
- **Logging**: ELK Stack
- **Infrastructure**: AWS, Kubernetes

## Prerequisites

- Python 3.9 or higher
- Docker and Docker Compose
- AWS CLI configured
- Kubernetes cluster (for production deployment)

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/your-org/delivery-state-machine.git
cd delivery-state-machine
```

2. Set up the development environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Start the development services:
```bash
docker-compose up -d
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

## Project Structure

```
delivery-state-machine/
├── app/
│   ├── api/            # API endpoints
│   ├── core/           # Core business logic
│   ├── models/         # Database models
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Business services
│   └── utils/          # Utility functions
├── tests/              # Test suite
├── resources/          # Configuration files
├── scripts/            # Utility scripts
└── docker/            # Docker configuration
```

## API Documentation

Once the service is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app tests/
```

## Deployment

### Development
```bash
docker-compose up -d
```

### Production
```bash
kubectl apply -f k8s/
```

## Monitoring

- Metrics: `http://localhost:9090` (Prometheus)
- Dashboards: `http://localhost:3000` (Grafana)
- Logs: `http://localhost:5601` (Kibana)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please:
1. Check the [documentation](docs/)
2. Open an issue in the repository
3. Contact the development team

## Related Projects

- [Order Management Service](https://github.com/your-org/order-management)
- [Payment Service](https://github.com/your-org/payment-service)
- [Customer Service](https://github.com/your-org/customer-service)

