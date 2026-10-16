# KanMind

KanMind ist eine REST-API für die Organisation von Boards, Tasks und Kommentaren.  
Sie unterstützt Benutzer-Authentifizierung, Board-Mitglieder, Aufgaben mit Bearbeitung und Review sowie Kommentare zu einzelnen Tasks.

## Technologien

- Python
- Django
- Django REST Framework
- Token Authentication
- SQLite
- Git & GitHub

## Voraussetzungen

Für die lokale Nutzung werden benötigt:

- Git
- Eine aktuelle Python-3-Version
- `pip`

## Projekt klonen

```bash
git clone https://github.com/nolticodes/KanMind.git
cd KanMind
```

## Installation

### macOS / Linux

Virtuelle Umgebung erstellen und aktivieren:

```bash
python3 -m venv env
source env/bin/activate
```

Abhängigkeiten installieren:

```bash
python3 -m pip install -r requirements.txt
```

### Windows

Virtuelle Umgebung erstellen und aktivieren:

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

Abhängigkeiten installieren:

```powershell
python -m pip install -r requirements.txt
```

### Environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-django-secret-key
```

The `.env` file is required locally but is excluded from version control.

### macOS / Linux: Datenbank und Server

Migrationen ausführen:

```bash
python3 manage.py migrate
```

Optional: Admin-Benutzer erstellen:

```bash
python3 manage.py createsuperuser
```

Server starten:

```bash
python3 manage.py runserver
```

### Windows: Datenbank und Server

Migrationen ausführen:

```powershell
python manage.py migrate
```

Optional: Admin-Benutzer erstellen:

```powershell
python manage.py createsuperuser
```

Server starten:

```powershell
python manage.py runserver
```

Die API ist anschließend unter [http://127.0.0.1:8000/](http://127.0.0.1:8000/) erreichbar.

## Authentifizierung

Für geschützte Endpoints wird Token Authentication verwendet.

Nach einem erfolgreichen Login liefert die API einen Token zurück. Dieser wird bei weiteren Requests im Header mitgesendet:

```text
Authorization: Token <dein-token>
```

Beispiel für den Login-Request:

```json
{
  "email": "deine-email@example.com",
  "password": "dein-passwort"
}
```

## API-Bereiche

Die API umfasst unter anderem folgende Bereiche:

| Bereich | Funktion |
|---|---|
| Authentifizierung | Login und Token-basierter Zugriff |
| Boards | Boards erstellen, anzeigen und bearbeiten |
| Tasks | Tasks erstellen, aktualisieren, löschen und zuweisen |
| Assigned Tasks | Tasks abrufen, die dem eingeloggten Nutzer zugewiesen sind |
| Reviewing Tasks | Tasks abrufen, bei denen der eingeloggte Nutzer als Reviewer eingetragen ist |
| Kommentare | Kommentare zu Tasks erstellen, auflisten und löschen |
| E-Mail-Check | Benutzer über ihre E-Mail-Adresse suchen |

## Projektstruktur

```text
KanMind/
├── auth_app/
│   ├── api/
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── migrations/
│   ├── models.py
│   └── admin.py
│
├── kanban_app/
│   ├── api/
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── migrations/
│   ├── models.py
│   └── admin.py
│
├── core/
├── manage.py
├── requirements.txt
└── db.sqlite3
```

## Admin-Bereich

Nach dem Anlegen eines Superusers ist der Django-Admin unter folgender Adresse erreichbar:

```text
http://127.0.0.1:8000/admin/
```

Dort können Benutzer, Boards, Tasks und Kommentare direkt verwaltet werden.