from pydantic import BaseModel, Field
from datetime import date

class BirthdayCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Imię solenizanta/solenizantki")
    surname: str = Field(..., min_length=2, max_length=50, description="Nazwisko solenizanta/solenizantki")
    date_of_birth: date = Field(..., description="Data urodzenia w formacie YYYY-MM-DD")

# Pełny model, który zwracamy do klienta (dziedziczy pola z BirthdayCreate i dodaje ID)
class Birthday(BirthdayCreate):
    id: int