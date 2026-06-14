from fastapi import FastAPI, status, HTTPException
from starlette.status import HTTP_201_CREATED
from contextlib import asynccontextmanager
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import engine, Base, SessionLocal
from app.database import engine, Base
from app.models import BirthdayRecord
from app.schemas import Birthday, BirthdayCreate

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)   
    yield    
    await engine.dispose()

async def get_db():
    async with SessionLocal() as session:
        yield session

app = FastAPI(
    title="Birthday Tracker API",
    description="API do zarządzania urodzinami znajomych",
    version="0.1.0",
    lifespan=lifespan
)

@app.get("/")
async def get_root() -> dict:
    return {"message": "Witaj w Birthday Tracker API!"}

@app.post("/birthdays", response_model=Birthday, status_code=HTTP_201_CREATED)
async def create_birthday(birthday_in: BirthdayCreate, db: AsyncSession = Depends(get_db)):
    """
    Tworzy nowy wpis w bazie danych.
    """
    new_birthday = BirthdayRecord(**birthday_in.model_dump())
    db.add(new_birthday)
    await db.commit()
    await db.refresh(new_birthday)

    return new_birthday

@app.get("/birthdays", response_model=list[Birthday])
async def get_birthdays(db: AsyncSession = Depends(get_db)):
    """
    Pobiera wszystkie rekordy z bazy danych.
    """
    query = select(BirthdayRecord)
    result = await db.execute(query)
    return result.scalars().all()

@app.get("/birthdays/upcoming", response_model=list[Birthday])
async def get_upcoming_birthdays(days: int = 30, db: AsyncSession = Depends(get_db)):
    """
    Pobiera osoby z bazy, mapuje je na DTO, filtruje w pamięci RAM i zwraca listę osób, które mają urodziny w ciągu najbliższych X dni.
    """
    query = select(BirthdayRecord)
    result = await db.execute(query)
    db_records = result.scalars().all()
    parsed_birthdays = [Birthday.model_validate(record) for record in db_records]
    upcoming_birthdays = [x for x in parsed_birthdays if x.days_until_next_birthday <= days]
    upcoming_birthdays.sort(key=lambda x: x.days_until_next_birthday)
    return upcoming_birthdays

@app.get("/birthdays/{birthday_id}", response_model=Birthday)
async def get_birthday(birthday_id: int, db: AsyncSession = Depends(get_db)):
    """
    Pobiera konkretnego solenizanta po jego ID.
    """
    query = select(BirthdayRecord).where(BirthdayRecord.id == birthday_id)
    result = await db.execute(query)
    birthday = result.scalar_one_or_none()
    
    if not birthday:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie znaleziono urodzin o podanym ID")

    return birthday

@app.put("/birthdays/{birthday_id}", response_model=Birthday)
async def update_birthday(birthday_id: int, birthday_in: BirthdayCreate, db : AsyncSession = Depends(get_db)):
    """
    Aktualizuje dane solenizanta w bazie.
    """
    query = select(BirthdayRecord).where(BirthdayRecord.id == birthday_id)
    result = await db.execute(query)
    existing_birthday = result.scalar_one_or_none()

    if not existing_birthday:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie znaleziono urodzin o podanym ID")

    existing_birthday.name = birthday_in.name
    existing_birthday.surname = birthday_in.surname
    existing_birthday.date_of_birth = birthday_in.date_of_birth

    await db.commit()
    await db.refresh(existing_birthday)

    return existing_birthday

@app.delete("/birthdays/{birthday_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_birthday(birthday_id: int, db: AsyncSession = Depends(get_db)):
    """
    Usuwa solenizanta z bazy danych.
    """
    query = select(BirthdayRecord).where(BirthdayRecord.id == birthday_id)
    result = await db.execute(query)
    existing_birthday = result.scalar_one_or_none()
    
    if not existing_birthday:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie znaleziono urodzin o podanym ID")

    await db.delete(existing_birthday)
    await db.commit()

    return None