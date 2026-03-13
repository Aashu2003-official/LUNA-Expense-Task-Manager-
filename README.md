# LUNA

A lightweight Django productivity app for managing daily tasks and tracking expenses.

## ✅ Deploying to Render

This project is configured to run on [Render](https://render.com) using a **Web Service** + **PostgreSQL**.

### 1) Push this repo to GitHub

Render deploys directly from a GitHub repo. Make sure your code is pushed to a GitHub repository.

### 2) Create a new Web Service on Render

1. Go to Render and create a **New Web Service**.
2. Connect your GitHub repo containing this project.
3. Choose the branch to deploy (e.g., `main`).
4. Set the **Build Command**:

```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
```

5. Set the **Start Command**:

```bash
gunicorn LUNA.wsgi --log-file -
```

6. Set the **Environment** to `Python 3.12` (or compatible).

### 3) Add a PostgreSQL Database (recommended)

1. Add a **PostgreSQL** add-on on Render (from the dashboard -> "Databases").
2. Once created, Render will automatically inject a `DATABASE_URL` environment variable.

### 4) Configure environment variables

In the Render dashboard, set the following environment variables for the Web Service:

- `DJANGO_SECRET_KEY` – a random secret (do **not** use the default value in production)
- `DJANGO_DEBUG` – `False` for production
- `DJANGO_ALLOWED_HOSTS` – your Render service URL (e.g. `myapp.onrender.com`)

> Tip: For local development, you can keep the defaults (`DEBUG=True`, `ALLOWED_HOSTS=localhost`).

### 5) Add `ALLOWED_HOSTS` for Render

Render’s hostname will look like `your-service-name.onrender.com`. Add this to `DJANGO_ALLOWED_HOSTS`.

### 6) (Optional) Local development

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

If you want help setting up a Render service or running the first deploy, just let me know.