# Sari-Sari Store Sample

This repository contains a minimal Sari-Sari store application with a Django REST
backend and a Vite + React frontend. It is intended as a starting point for
experiments and tutorials.

## Environment Variables

Copy the provided examples and adjust values for your environment:

```bash
cp .env.example .env
cp frontend/.env.example frontend/.env
```

Key variables:

- `FRONTEND_API_URL` – URL where the React app will reach the backend.
- `BACKEND_API_URL` – URL where the Django API will be served.
- `DB_*` – MySQL connection details used by Django.
- `VITE_API_URL` – same as `BACKEND_API_URL` but consumed by Vite during the
  frontend build.

## Backend

The Django project lives in `backend/`.

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Running the tests requires the same dependencies and database access:

```bash
pytest -q
```

## Frontend

The React frontend is in `frontend/`.

```bash
cd frontend
npm install
npm run dev
```

To build a production bundle:

```bash
VITE_API_URL=$BACKEND_API_URL npm run build
```

## Docker Compose

A simple `docker-compose.yml` is included to run MySQL, the Django API and the
built frontend together:

```bash
docker-compose up --build
```

## OpenAPI Documentation

A basic OpenAPI specification describing the available `/api` endpoints can be
found in `openapi.yaml`.

