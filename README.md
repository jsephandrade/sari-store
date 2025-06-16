# Sari-Sari Store Sample

This repository contains a sample implementation of a Sari-Sari store web application with an **utang** (credit) management system. The backend is built with **Django** and **Django REST Framework** while the frontend uses **Vite**, **React** and **Tailwind CSS**.

## Backend

The Django project lives in the `backend/` directory. Main features:

- Models for `Product`, `Category`, `Customer`, `UtangEntry`, `Payment` and `Sale`.
- JWT authentication using `djangorestframework-simplejwt`.
- CRUD API endpoints for products, categories, customers and sales.
- Endpoints to manage utang entries, record payments and track price adjustments.

Create a virtual environment and install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

The backend reads its MySQL credentials from environment variables so it can
connect to a live database or fall back to SQLite for tests. Set the following
variables before running migrations:

```
export DB_ENGINE=django.db.backends.mysql
export DB_NAME=sari_store_db
export DB_USER=sari_admin
export DB_PASSWORD=hotmariaclara24
export DB_HOST=localhost
export DB_PORT=3306
```

Run migrations to create the schema:

```bash
python manage.py migrate
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

## Frontend

The `frontend/` directory contains a Vite React project configured with Tailwind CSS. It demonstrates the basic components and routing for the store dashboard, products, customers and utang ledger. The dashboard aggregates sales and balances with quick links into each module, and a simple POS screen updates inventory and utang in real time.

Install dependencies and start the dev server:

```bash
cd frontend
npm install
npm run dev
```

This is a minimal example intended for educational purposes. Use it as a starting point for a more complete application.
