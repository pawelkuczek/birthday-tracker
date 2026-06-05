from fastapi import FastAPI
from app.schemas import Birthday, BirthdayCreate
from starlette.status import HTTP_201_CREATED

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

@app.post("/birthdays", response_model=Birthday, status_code=HTTP_201_CREATED)
async def create_birthday(birthday_in: BirthdayCreate):
    global fake_id_counter
    new_birthday = Birthday(id=fake_id_counter, **birthday_in.model_dump())

    fake_database.append(new_birthday)
    fake_id_counter += 1

    return new_birthday

@app.get("/birthdays", response_model=list[Birthday])
async def get_birthdays():
    return fake_database