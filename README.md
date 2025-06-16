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

Configure your MySQL connection in `sari_store/settings.py` and run migrations:

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
