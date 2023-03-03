from fastapi import FastAPI, Request,  HTTPException
from core.models.database import users
from core.utils.crypto import get_or_create_token, get_user_by_token, hash_text, is_valid_password

app = FastAPI()

@app.get("/")
def all_users():
    return list(users.find({},{"_id":0}))

@app.post("/register")
async def register(request: Request):
    json_body = await request.json()
    user = users.find_one({"nickname": json_body["nickname"]})
    if user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe.")
    json_body["password"] = hash_text(json_body["password"])
    new_user = users.insert_one(json_body)
    created_user = users.find_one({"_id": new_user.inserted_id})
    return {**created_user, "_id": str(new_user.inserted_id)}


@app.get("/login")
async def login(request: Request):
    json_body = await request.json()
    nickname, password = json_body["nickname"], json_body["password"]
    if not is_valid_password(nickname, password):
        raise HTTPException(status_code=400, detail="El nombre de usuario o la contraseña es incorrecta.")
    user = users.find_one({"nickname": nickname})
    return {"token": get_or_create_token(user)}


@app.get("/profile")
async def get_profile(request: Request):
    token = request.headers["Authorization"]
    
    if not token:
        raise HTTPException(status_code=401, detail="El token no fue especificado.")
    user = get_user_by_token(token)
    
    return {**user, "_id": str(user["_id"])}