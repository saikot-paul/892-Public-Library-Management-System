from fastapi import APIRouter, HTTPException
from backend.users.grpc_server.firestore_db import db

router = APIRouter()

