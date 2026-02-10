# Deployment Guide for Chemical Equipment Parameter Visualizer

This guide outlines the steps to deploy the web version of the application. The architecture consists of a React frontend and a Django backend.

## Prerequisites

- A GitHub account with this repository pushed.
- Accounts on a cloud hosting provider (e.g., Render, Railway) for the backend.
- Verification (e.g. email/phone) on the chosen platform if required.
- An account on Vercel or Netlify for the frontend.

---

## Part 1: Backend Deployment (Recommended: Render)

We will deploy the Django backend first to get the API URL.

1.  **Log in to Render** (dashboard.render.com).
2.  Click **New +** -> **Web Service**.
3.  Connect your GitHub repository.
4.  Configure the service:
    -   **Name**: `chemical-visualizer-backend` (or similar).
    -   **Root Directory**: `backend` (Important!).
    -   **Runtime**: Python 3.
    -   **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
    -   **Start Command**: `gunicorn backend.wsgi`
5.  **Environment Variables**:
    Add the following environment variables:
    -   `PYTHON_VERSION`: `3.10.12` (or your local version)
    -   `SECRET_KEY`: (Generate a strong random string)
    -   `DEBUG`: `False`
    -   `ALLOWED_HOSTS`: `*` (or your Render URL once known, e.g., `chemical-backend.onrender.com`)
    -   `CORS_ALLOWED_ORIGINS`: (Leave empty for now, we will update this after deploying the frontend)
6.  **Click Create Web Service**.
7.  **Wait for deployment**. Once finished, copy the backend URL (e.g., `https://chemical-impl-backend.onrender.com`).

---

## Part 2: Frontend Deployment (Recommended: Vercel)

Now we deploy the React frontend and connect it to the backend.

1.  **Log in to Vercel** (vercel.com).
2.  Click **Add New...** -> **Project**.
3.  Import your GitHub repository.
4.  Configure the project:
    -   **Framework Preset**: Create React App.
    -   **Root Directory**: Click "Edit" and select `web-frontend`.
    -   **Build Command**: `npm run build` (default).
    -   **Output Directory**: `build` (default).
5.  **Environment Variables**:
    Expand the "Environment Variables" section and add:
    -   `REACT_APP_API_URL`: Paste the backend URL from Part 1. **Important:** Append `/api` to the URL.
        -   Example: `https://chemical-impl-backend.onrender.com/api`
6.  **Click Deploy**.
7.  **Wait for deployment**. Once finished, you will get a frontend URL (e.g., `https://chemical-visualizer.vercel.app`).

---

## Part 3: Final Configuration

Now that the frontend is deployed, we need to tell the backend to allow requests from it.

1.  Go back to your **Render Backend Dashboard**.
2.  Go to **Environment**.
3.  Add/Edit `CORS_ALLOWED_ORIGINS`.
    -   Value: Your Vercel Frontend URL (e.g., `https://chemical-visualizer.vercel.app`).
    -   **Note**: Do not include trailing slashes.
4.  (Optional) Update `ALLOWED_HOSTS` to include your backend domain if you set it to `*` earlier.
5.  **Save Changes**. Render will automatically redeploy.

## Troubleshooting

-   **Database**: This setup uses SQLite which is stored in a file. **Warning**: On Render's free tier, the filesystem is ephemeral, meaning the database will reset every time the app restarts or redeploys.
    -   **Solution**: For persistent data, create a **PostgreSQL** database on Render and add the `DATABASE_URL` environment variable to your Backend service. The code is already configured to use it if present.
-   **Static Files**: If CSS/JS is missing in the backend admin, ensure `whitenoise` is installed and the `collectstatic` command ran successfully.
