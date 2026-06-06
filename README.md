# Birthday Tracker API

API do zarządzania urodzinami znajomych i wysyłania przypomnień. Projekt budowany w oparciu o czystą architekturę, SOLID i nowoczesny stack Pythona.

## Technologie
* Python 3.12+
* FastAPI
* Pydantic v2
* Uvicorn

## Zaimplementowane Endpointy (In-Memory)
* `GET /` - Root aplikacji
* `POST /birthdays` - Dodawanie nowych urodzin
* `GET /birthdays` - Pobieranie wszystkich urodzin
* `PUT /birthdays/{id}` - Aktualizacja danych
* `DELETE /birthdays/{id}` - Usuwanie rekordu