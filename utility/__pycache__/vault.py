from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
import jwt
from database import conn, cursor

router = APIRouter()
SECRET_KEY = "secret"  # same as auth

class VaultEntry(BaseModel):
    key: str
    value: str

@router.post("/store")
def store_secret(entry: VaultEntry, token: str = Header(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cursor.execute("INSERT INTO vault (user_id, key, value) VALUES (%s, %s, %s)",
    (user["id"], entry.key, entry.value))
    conn.commit()
    return {"message": "Secret stored"}

@router.get("/vault")
def get_vault(token: str = Header(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    cursor.execute("SELECT key, value FROM vault WHERE user_id = %s", (user["id"],))
    data = cursor.fetchall()
    return {"vault": data}