from pydantic import BaseModel, Field, computed_field
from datetime import date

class BirthdayCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Imię solenizanta/solenizantki")
    surname: str = Field(..., min_length=2, max_length=50, description="Nazwisko solenizanta/solenizantki")
    date_of_birth: date = Field(..., description="Data urodzenia w formacie YYYY-MM-DD")

class Birthday(BirthdayCreate):
    id: int

    @computed_field(description="Wiek solenizanta/solenizantki obliczany na podstawie daty urodzenia")
    @property
    def age(self) -> int:
        today = date.today()
        age = today.year - self.date_of_birth.year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        return age

    @computed_field(description="Ilość dni do następnych urodzin")
    @property
    def days_until_next_birthday(self) -> int:
        today = date.today()
        try:
            next_birthday = self.date_of_birth.replace(year=today.year)
        except ValueError:
            next_birthday = self.date_of_birth.replace(year=today.year, month=3, day=1)

        if next_birthday < today:
            try:
                next_birthday = next_birthday.replace(year=today.year + 1)
            except ValueError:
                next_birthday = next_birthday.replace(year=today.year + 1, month=3, day=1)

        return (next_birthday - today).days

    @computed_field(description="Czy solenizant/solenizantka ma dzisiaj urodziny")
    @property
    def is_birthday_today(self) -> bool:
        today = date.today()
        return (today.month, today.day) == (self.date_of_birth.month, self.date_of_birth.day)