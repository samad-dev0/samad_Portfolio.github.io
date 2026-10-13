import json
import logging
import secrets
import urllib.parse
import urllib.request
from smtplib import SMTPException

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ContactMessageForm, LoginForm, RegisterForm
from .models import ContactMessage, Metric, PortfolioProfile, Service, Skill

logger = logging.getLogger(__name__)
User = get_user_model()


def send_contact_confirmation_email(request, contact, profile):
    subject = "Confirmation de réception de votre message"
    email_body = (
        f"Salut {contact.name},\n\n"
        "Nous vous remercions d’avoir pris le temps de nous contacter via notre portfolio.\n\n"
        "Votre demande de rendez-vous a bien été enregistrée.\n"
        "Nous vous contacterons prochainement pour confirmer les modalités.\n"
        "Si vous avez des informations complémentaires à nous communiquer concernant votre projet, "
        "vous pouvez simplement répondre à cet e-mail.\n\n"
        "Cordialement,\n\n"
        "Sam\n"
        "Développeur Web & Applications"
    )
    email_sent = 0
    try:
        confirmation = EmailMessage(
            subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [contact.email],
            reply_to=[profile.email],
        )
        email_sent = confirmation.send(fail_silently=False)
    except (OSError, SMTPException):
        logger.exception("Could not send contact confirmation email")
        email_sent = 0

    if email_sent and settings.EMAIL_BACKEND == "django.core.mail.backends.console.EmailBackend":
        messages.success(
            request,
            "Votre message est enregistré. L’e-mail de confirmation est affiché dans la console de développement.",
        )
    elif email_sent:
        messages.success(request, "Votre message est enregistré et un e-mail de confirmation vous a été envoyé.")
    else:
        messages.warning(
            request,
            "Votre message est enregistré, mais l’e-mail de confirmation n’a pas pu être envoyé.",
        )


def _process_pending_contact_message(request, user, profile):
    data = request.session.pop("pending_contact_data", None)
    if not data:
        return False

    name = (data.get("name") or "").strip() or user.get_full_name() or user.username
    email = user.email or (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()
    message_text = (data.get("message") or "").strip()

    if message_text and email:
        contact = ContactMessage.objects.create(
            user=user,
            name=name,
            email=email,
            phone=phone,
            message=message_text,
        )
        send_contact_confirmation_email(request, contact, profile)
        return True
    return False


def home(request):
    profile, _ = PortfolioProfile.objects.get_or_create(pk=1)
    if request.method == "POST":
        if not request.user.is_authenticated:
            request.session["pending_contact_data"] = {
                "name": request.POST.get("name", ""),
                "email": request.POST.get("email", ""),
                "phone": request.POST.get("phone", ""),
                "message": request.POST.get("message", ""),
            }
            messages.info(
                request,
                "Veuillez vous connecter avec Google ou votre adresse e-mail pour enregistrer vos informations et valider l’envoi de votre message.",
            )
            login_url = reverse("login")
            return redirect(f"{login_url}?next={reverse('home')}#contact")

        contact_form = ContactMessageForm(request.POST, user=request.user)
        if contact_form.is_valid():
            contact = contact_form.save(commit=False)
            contact.user = request.user
            contact.save()
            send_contact_confirmation_email(request, contact, profile)
            return redirect(f"{reverse('home')}#contact")
    else:
        contact_form = ContactMessageForm(user=request.user)

    context = {
        "profile": profile,
        "metrics": Metric.objects.all(),
        "services": Service.objects.all(),
        "skills": Skill.objects.all(),
        "contact_form": contact_form,
    }
    return render(request, "index.html", context)


def auth_login_view(request):
    profile, _ = PortfolioProfile.objects.get_or_create(pk=1)
    next_url = request.GET.get("next") or request.POST.get("next") or f"{reverse('home')}#contact"

    if request.user.is_authenticated:
        _process_pending_contact_message(request, request.user, profile)
        return redirect(next_url)

    has_pending = bool(request.session.get("pending_contact_data"))
    active_tab = "login"

    login_form = LoginForm()
    register_form = RegisterForm()

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "login":
            active_tab = "login"
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = login_form.cleaned_data["user"]
                login(request, user)
                had_pending = _process_pending_contact_message(request, user, profile)
                if not had_pending:
                    messages.success(request, f"Connexion réussie. Bienvenue, {user.first_name or user.username} !")
                return redirect(next_url)
        elif action == "register":
            active_tab = "register"
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                had_pending = _process_pending_contact_message(request, user, profile)
                if not had_pending:
                    messages.success(request, f"Compte créé avec succès ! Bienvenue, {user.first_name or user.username}.")
                return redirect(next_url)

    context = {
        "profile": profile,
        "login_form": login_form,
        "register_form": register_form,
        "active_tab": active_tab,
        "next_url": next_url,
        "has_pending": has_pending,
        "google_client_id": getattr(settings, "GOOGLE_CLIENT_ID", ""),
    }
    return render(request, "auth.html", context)


def auth_logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect("home")


def google_login_view(request):
    client_id = getattr(settings, "GOOGLE_CLIENT_ID", "")
    if not client_id:
        messages.warning(
            request,
            "La connexion Google n’est pas encore configurée (GOOGLE_CLIENT_ID absent dans les paramètres). "
            "Vous pouvez vous connecter ou vous inscrire avec votre e-mail et mot de passe ci-dessous.",
        )
        next_url = request.GET.get("next") or f"{reverse('home')}#contact"
        return redirect(f"{reverse('login')}?next={urllib.parse.quote(next_url)}")

    state = secrets.token_urlsafe(32)
    request.session["google_oauth_state"] = state
    next_url = request.GET.get("next") or request.POST.get("next") or f"{reverse('home')}#contact"
    request.session["google_oauth_next"] = next_url

    redirect_uri = request.build_absolute_uri(reverse("google_callback"))
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "prompt": "select_account",
    }
    google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
    return redirect(google_auth_url)


def google_callback_view(request):
    profile, _ = PortfolioProfile.objects.get_or_create(pk=1)
    client_id = getattr(settings, "GOOGLE_CLIENT_ID", "")
    client_secret = getattr(settings, "GOOGLE_CLIENT_SECRET", "")
    expected_state = request.session.pop("google_oauth_state", None)
    next_url = request.session.pop("google_oauth_next", None) or f"{reverse('home')}#contact"

    state = request.GET.get("state")
    code = request.GET.get("code")
    error = request.GET.get("error")

    if error or not code or not state or state != expected_state:
        messages.error(request, "Échec de l’authentification avec Google. Veuillez réessayer.")
        return redirect("login")

    redirect_uri = request.build_absolute_uri(reverse("google_callback"))

    try:
        token_data = urllib.parse.urlencode(
            {
                "code": code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            }
        ).encode("utf-8")

        req = urllib.request.Request(
            "https://oauth2.googleapis.com/token",
            data=token_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            token_json = json.loads(resp.read().decode("utf-8"))

        access_token = token_json.get("access_token")
        if not access_token:
            messages.error(request, "Impossible d’obtenir le jeton d’accès Google.")
            return redirect("login")

        userinfo_req = urllib.request.Request(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        with urllib.request.urlopen(userinfo_req, timeout=10) as resp:
            user_info = json.loads(resp.read().decode("utf-8"))

        email = (user_info.get("email") or "").strip().lower()
        if not email:
            messages.error(request, "Votre compte Google n’a pas fourni d’adresse e-mail valide.")
            return redirect("login")

        first_name = user_info.get("given_name") or ""
        last_name = user_info.get("family_name") or ""
        name = user_info.get("name") or ""
        if not first_name and name:
            parts = name.split(" ", 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ""

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            base_username = email.split("@")[0].replace(".", "_")[:25]
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}_{counter}"
                counter += 1

            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
        else:
            if first_name and not user.first_name:
                user.first_name = first_name
            if last_name and not user.last_name:
                user.last_name = last_name
            user.save()

        login(request, user)
        had_pending = _process_pending_contact_message(request, user, profile)
        if not had_pending:
            messages.success(request, f"Ravi de vous voir, {user.first_name or user.username} ! Vous êtes connecté via Google.")

        return redirect(next_url)

    except Exception:
        logger.exception("Erreur lors de l’authentification Google")
        messages.error(request, "Une erreur est survenue lors de la communication avec Google.")
        return redirect("login")
