from fastapi import FastAPI, status, HTTPException
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

@app.put("/birthdays/{birthday_id}", response_model=Birthday)
async def update_birthday(birthday_id: int, birthday_in: BirthdayCreate):
    existing_birthday = next((b for b in fake_database if b.id == birthday_id), None)

    if not existing_birthday:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie znaleziono urodzin o podanym ID")

    existing_birthday.name = birthday_in.name
    existing_birthday.surname = birthday_in.surname
    existing_birthday.date_of_birth = birthday_in.date_of_birth
    return existing_birthday

@app.delete("/birthdays/{birthday_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_birthday(birthday_id: int):
    existing_birthday = next((b for b in fake_database if b.id == birthday_id), None)

    if not existing_birthday:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie znaleziono urodzin o podanym ID")

    fake_database.remove(existing_birthday)
    return None