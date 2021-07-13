# Übersicht

Der Server besteht aus den Technologien:
[Python](https://www.python.org/)
[Django](https://www.djangoproject.com/),
[Django Rest Framework](https://www.django-rest-framework.org/)
und [PostgreSQL](https://www.postgresql.org/).

## Installation

Zum Testen ist es am einfachsten [Docker](https://www.docker.com/) zu benutzen.
Zum Entwickeln lohnt es sich mehr die benötigten Technologien manuell zu installieren.

### Manuelle Installation

#### Downloads

1. Installiere [Python 3.9](https://www.python.org/downloads/release/python-390/)
2. Installiere [PostgreSQL](https://www.postgresql.org/download/)
3. Installiere [pip](https://pypi.org/project/pip/)

#### Zubereitung

1. Installiere die packages mit pip: `pip install -r requirements.txt`
2. Erstelle eine Rolle in PostgreSQL: `CREATE ROLE tabool_django_role WITH SUPERUSER LOGIN PASSWORD 'password'`
3. Erstelle eine Datenbank in PostgreSQL: `CREATE DATABASE tabool_django_database WITH OWNER tabool_django_role`
4. Tabellen, Indizes, etc. werden von Django automatisch angewendet: 
   (im Ordner `backend` folgendes eingeben) `./manage.py migrate`
   
#### Starten

**Testen** ` ./manage.py test --settings project.test_settings`

Am besten sollte man den Server testen bevor man ihn startet, um sicherzugehen, dass alles klappt.

1. [Rufe die Python-Shell auf](https://python.land/installing-python/starting-python)
2. Importiere das package: `from backend.apps.debug_utils import *`
3. Lade die Dummy-Daten: `create_test_env()` - Es wird eine Exception geworfen werden, die kann
einfach ignoriert werden für den Moment. Über der Exception stehen Anmeldedaten für die erstellten Benutzer.

**Starten**  `./manage.py runserver`

Mit diesem Befehl wird der Server gestartet. Man kann jedoch nichts sehen wenn man auf `127.0.0.1:8000` geht.

Der Server dient nur als API, [tabool-website](https://github.com/Myzel394/tabool-website) dient als Frontend.

#### Dummy-Daten laden

Um nicht alle Daten selbst per Hand erstellen zu müssen, kann man zufällige Daten schnell erzeugen lassen.


---

Wenn die Tests alle geklappt haben und der Server gestartet ist, dann ist das schon sehr gut :).
Es kann am Anfang durchaus schwierig sein das alles zum Laufen zu bringen. Nicht verzweifeln!
Wenn ein Fehler passiert, kann man ihn erstmal googeln und ansonsten versuchen selbst zu lösen.
