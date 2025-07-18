from fastapi import APIRouter, Depends, Header, HTTPException
from models.password import StorePassword
from utility.crypto import encrypt_password, decrypt_password, generate_key
import jwt

router=APIRouter()
JWT_SECRET="vaultmini_secret_key"

password_vault={} 
user_keys={}       


def get_username(token: str = Header(...)):
    try:
        payload=jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload.get("sub")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/store")
def store_password(data: StorePassword, username: str = Depends(get_username)):
    if not data.service or not data.username or not data.password:
        raise HTTPException(status_code=400, detail="All fields are required")

    key=user_keys.get(username)
    if not key:
        key=generate_key()
        user_keys[username]=key

    try:
        enc_pw=encrypt_password(data.password, key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Encryption failed: {str(e)}")

    entry={
        "service": data.service,
        "username": data.username,
        "password": enc_pw
    }

    password_vault.setdefault(username, []).append(entry)
    return {"msg": "Password stored securely 🔐"}


@router.get("/vault")
def view_vault(username: str=Depends(get_username)):
    key=user_keys.get(username)
    vault=password_vault.get(username, [])

    decrypted=[]
    for entry in vault:
        try:
            decrypted_pw=decrypt_password(entry["password"], key)
        except Exception as e:
            decrypted_pw="[Decryption Error]"

        decrypted.append({
            "service": entry["service"],
            "username": entry["username"],
            "password": decrypted_pw
        })

    return {"vault": decrypted}


@router.delete("/shred")
def shred_passwords(username: str=Depends(get_username)):
    password_vault[username]=[]
    user_keys.pop(username, None)
    return {"msg":"All passwords shredded permanently"}
