# MegaProz-Consult

> Hello I need you to help me generate a set of code. But I can use to deploy. A web application. That can be used to deliver geological services such as. Borehole drilling, Soak away drilling, Soil testing. Industrial cleaning. Cons Con Geological Consultations. Erosion control, etcetera. Give me a stack of codes, very simple ones that I can use to just deploy the application and ensure that. This set of codes are validated and error proof. Make sure that the codes that you give me are enough for me to readily deploy my application. The name of the site will be MegaProz Consult. ank you.

## Tech Stack
- FastAPI

## Quick Start

```bash
cp .env.example .env
docker compose up --build
```

- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

## Authentication

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"secret123","full_name":"Jane Smith"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -d "username=user@example.com&password=secret123"

# Use token
curl http://localhost:8000/api/v1/surveys/ \
  -H "Authorization: Bearer <token>"
```

## Running Tests
```bash
docker compose exec api pytest --cov=app -v
```

## Deployment
```bash
cd infra && terraform init && terraform apply
```