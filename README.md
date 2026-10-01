# Portfolio Django

Le portfolio utilise Django et SQLite. Le profil, les chiffres clés, les services et les compétences se modifient dans l'administration. Les messages du formulaire sont enregistrés et consultables dans l'administration.

## Installation Windows

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Ouvrir http://127.0.0.1:8000/ pour le portfolio et http://127.0.0.1:8000/admin/ pour l'administration.

Les ressources d'origine restent dans `assets/` et sont servies par Django en développement. Pour la production, configurer `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0`, `DJANGO_ALLOWED_HOSTS` et collecter les fichiers statiques avec `python manage.py collectstatic`.

## Courriels de confirmation

Après l'enregistrement d'un message, le portfolio envoie automatiquement le courriel de confirmation à l'adresse saisie dans le formulaire. Configure le SMTP dans l'environnement avant de démarrer Django (exemple PowerShell avec Gmail et un mot de passe d'application) :

```powershell
$env:EMAIL_HOST = "smtp.gmail.com"
$env:EMAIL_PORT = "587"
$env:EMAIL_USE_TLS = "1"
$env:EMAIL_HOST_USER = "votre-adresse@gmail.com"
$env:EMAIL_HOST_PASSWORD = "votre-mot-de-passe-d-application"
$env:DEFAULT_FROM_EMAIL = $env:EMAIL_HOST_USER
python manage.py runserver
```

Ne mets pas le mot de passe SMTP dans les fichiers du projet. En développement sans serveur SMTP configuré, Django affiche le courriel dans la console du serveur. Les réponses du destinataire sont adressées à l'e-mail de contact du profil.
