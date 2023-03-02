from fastapi import FastAPI, Request
from core.models.database import users

app = FastAPI()

@app.get("/")
def all_users():
    return list(users.find())

@app.post("/register")
async def register(request: Request):
    json_body = await request.json()
    new_user = users.insert_one(json_body)
    created_user = users.find_one({"_id": new_user.inserted_id})
    return {**created_user, "_id": str(new_user.inserted_id)}
