# 🚀 How to Run the Application

Follow these steps to run the Chemical Equipment Parameter Visualizer. You will need **3 separate terminals**.

## 🔑 Login Credentials (For All Apps)
- **Username:** `admin`
- **Password:** `admin123`

---

## 1️⃣ Step 1: Start the Backend (REQUIRED)
The backend must be running for the web and desktop apps to work.

1. Open **Terminal 1**.
2. Run the following commands:

```powershell
# Activate the virtual environment
.\venv\Scripts\activate

# Navigate to backend directory
cd backend

# Start the server
python manage.py runserver
```

✅ **Success:** You should see `Starting development server at http://127.0.0.1:8000/`

---

## 2️⃣ Step 2: Run the Web Application
1. Open **Terminal 2**.
2. Run the following commands:

```powershell
# Navigate to web frontend
cd web-frontend

# Start the React app
npm start
```

✅ **Success:** The browser will open `http://localhost:3000`. Login with the credentials above.

---

## 3️⃣ Step 3: Run the Desktop Application
1. Open **Terminal 3**.
2. Run the following commands:

```powershell
# Activate the virtual environment
.\venv\Scripts\activate

# Navigate to desktop frontend
cd desktop-frontend

# Run the application
python main.py
```

✅ **Success:** The desktop application window will appear. Login with the credentials above.

---

## 📝 Usage Tips
- **Upload Data:** Use the `Upload CSV` button in either app to upload `backend/sample_data.csv`.
- **View Analytics:** Both apps show charts and summaries automatically after selecting a dataset.
- **Generate Reports:** Click "Download PDF Report" to get a detailed PDF analysis.

---

## 🛑 Troubleshooting
- **Connection Refused:** Ensure the backend (Terminal 1) is running and shows no errors.
- **Login Failed:** Double-check username (`admin`) and password (`admin123`).
- **Desktop App Crashes:** Ensure you activated the virtual environment (`.\venv\Scripts\activate`) before running `python main.py`.
