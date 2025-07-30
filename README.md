# AutonomousTech Backend Engineering Task

This is a Django-based backend project designed for the Backend Engineer assessment at Autonomous Technologies.

## Features

- Django REST API
- Shopify Order Webhook Integration
- Celery for background task processing
- Redis as the task broker
- PostgreSQL as the database
- Dockerized setup
- AI features: Semantic Search and Insights API

## Tech Stack

- Django
- DRF
- Celery + Redis
- PostgreSQL
- Docker & Docker Compose
- OpenAI (Embeddings)

## Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/yasherali/test-sample
cd test-sample
```

2. **Run Docker**
```bash
docker-compose up --build
```

3. **Apply Migrations**
```bash
docker-compose exec web python manage.py migrate
```

4. **Create Superuser**
```bash
docker-compose exec web python manage.py createsuperuser
```
