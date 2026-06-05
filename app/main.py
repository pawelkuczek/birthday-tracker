from fastapi import FastAPI
from app.schemas import Birthday, BirthdayCreate

app = FastAPI(
    title="Birthday Tracker API",
    description="API do zarządzania urodzinami znajomych",
    version="0.1.0"
)

fake_database: list[Birthday] = []
fake_id_counter = 1

@app.get("/")
async def get_root() -> dict:
    return {"message": "Witaj w Birthday Tracker API!"}