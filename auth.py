from fastapi import APIRouter, HTTPException
from models.users import UserSignup, UserLogin
import bcrypt
import jwt
from datetime import datetime, timedelta

router=APIRouter()
JWT_SECRET="vaultmini_secret_key"
users={}

@router.post("/signup")
def signup(data:UserSignup):
    if data.username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_pw = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())
    users[data.username] = hashed_pw
    return {"msg": "User created"}

@router.post("/login")
def login(data:UserLogin):
    if data.username not in users:
        raise HTTPException(status_code=400, detail="User not found")
    if not bcrypt.checkpw(data.password.encode(), users[data.username]):
        raise HTTPException(status_code=401, detail="Incorrect password")
    payload={
        "sub": data.username,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return {"access_token": token}