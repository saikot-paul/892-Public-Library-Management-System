# 892-Public-Library-Management-System

## Make sure to add CORS Browser extention

virtual environment for backend:
cd backend
./venv/Scripts/activate

py bookGRPCServer.py
py -m uvicorn BookGRPCClient:app --port 5000

frontend:
npm run dev
