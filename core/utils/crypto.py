import hashlib, uuid
from fastapi import HTTPException
from core.models.database import users, tokens



def hash_text(text: str) -> str: 
    return hashlib.sha3_256(text.encode()).hexdigest()

def is_valid_password(nickname: str, password: str) -> bool:
    hashed_password = hash_text(password)
    user = users.find_one({"nickname": nickname})
    return user["password"] == hashed_password

def generate_token(password: str, salt: str) -> str:
    return hash_text(str(password) + salt)

def get_or_create_token(user: dict):
    user_id = user["_id"]

    token = tokens.find_one({"user_id": user_id})
    if token:
        return token["token"]
    
    # Crear nuevo token
    salt = uuid.uuid4().hex
    token = generate_token(user_id, salt)
    tokens.insert_one({"user_id": user_id, "salt": salt, "token": token})
    return token


def get_user_by_token(token: str) -> dict:
    token_name, token = token.split(" ")
    if token_name != "Bearer":
        raise HTTPException(status_code=400, detail="El token no es Bearer.")
    token = tokens.find_one({"token": token})

    if token is None:
        return None
    return  users.find_one({"_id": token["user_id"]})