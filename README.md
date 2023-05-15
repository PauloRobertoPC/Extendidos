# Extendidos

## Preparing Environment


* Installing Virtual Environment
```bash
    python -m venv .venv
```

* Enter In The Virtual Environment
```bash
    source .venv/bin/activate
```

* Upgrade pip in Virtual Environment
```bash
    pip install --upgrade pip 
```

* Install Dependencies in Virtual Environment
```bash
    pip install -r requirements.txt
```

## Run Server

* Make Migration
```bash
    python manage.py makemigrations 
```

* Migrate
```bash
    python manage.py migrate 
```

* Running Server
```bash
    python manage.py runserver 
```
