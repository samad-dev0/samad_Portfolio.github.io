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

Les ressources d'origine restent dans `assets/`. WhiteNoise les sert en production après `python manage.py collectstatic`.

## Déploiement Render

Le dépôt inclut `render.yaml` pour créer le service web Render. Avant le premier déploiement :

1. Envoie le projet sur GitHub.
2. Crée une base PostgreSQL dans Render. Choisis le plan et la région selon tes besoins, puis copie son **Internal Database URL**.
3. Dans Render, crée un Blueprint depuis le dépôt. Lorsqu'il te le demande, renseigne `DATABASE_URL` avec l'**Internal Database URL** de la base PostgreSQL.
4. Render construit les fichiers statiques, applique les migrations puis démarre Gunicorn. `DJANGO_SECRET_KEY` est générée par Render et `DEBUG` reste désactivé.

Ne mets pas l'URL de base, de secret ou de mot de passe dans Git. SQLite reste utilisé en local; en production, le service refuse de démarrer sans `DATABASE_URL` pour éviter de perdre les données au redémarrage. Le SMTP est facultatif pour le lancement, mais doit être configuré dans les variables Render (`EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`) pour envoyer les confirmations de contact. Si tu ajoutes un domaine personnalisé, ajoute-le aussi à `DJANGO_ALLOWED_HOSTS` et `DJANGO_CSRF_TRUSTED_ORIGINS`.

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
