# Minimal FastAPI Backend Skeleton

This is a lightweight backend skeleton using FastAPI.

## Requirements

- Python 3.7+

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

1. Run the server:
   ```bash
   # Using python directly (recommended) on port 8001
   python -m app.main
   
   # OR if you have uvicorn in your PATH
   uvicorn app.main:app --port 8001 --reload
   ```

2. Access the health check endpoint:
   - URL: `http://127.0.0.1:8001/health`
   - Response: `{"status": "ok"}`

   - ReDoc: `http://127.0.0.1:8001/redoc`

## Running the Frontend

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```

2.  Start the development server:
    ```bash
    npm run dev
    ```

3.  Access the app: `http://localhost:5173`

## How to Test
1.  **Login**: Use the "Sign In" or "Create Account" tabs.
2.  **Wellness Chat**: Go to `Dashboard` -> `Wellness Chat` -> Send a message.

