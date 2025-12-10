## STOS TECHNOLOGICZNY
- **Python 3.13**
- **Django 6.x**
- **Poetry** – zarządzanie zależnościami
- **SQLite** – używamy domyślnej bazy danych Django

## Instalacja i uruchomienie

### 1. Sklonuj repozytorium
```
git clone https://github.com/<twoje_konto>/trollingo.git
cd trollingo
```

### 2. Zainstaluj se zależności bo używamy poetry, więc nie instalujemy przez pip
```
poetry install
```

### 3. Aktywujemy środowisko
```
.\.venv\Scripts\Activate.ps1
```

### 4. Migracja bazy danych
```
python manage.py migrate
```

### 5. Tworzymy admina
```
python manage.py createsuperuser
```

### 5. Łodpalamy
```
python manage.py runserver
```