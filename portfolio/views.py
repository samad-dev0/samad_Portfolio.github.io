import logging
from smtplib import SMTPException

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render

from .forms import ContactMessageForm
from .models import Metric, PortfolioProfile, Service, Skill


logger = logging.getLogger(__name__)


def home(request):
    profile, _ = PortfolioProfile.objects.get_or_create(pk=1)
    if request.method == "POST":
        contact_form = ContactMessageForm(request.POST)
        if contact_form.is_valid():
            contact = contact_form.save()
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
            return redirect("home")
    else:
        contact_form = ContactMessageForm()

    context = {
        "profile": profile,
        "metrics": Metric.objects.all(),
        "services": Service.objects.all(),
        "skills": Skill.objects.all(),
        "contact_form": contact_form,
    }
    return render(request, "index.html", context)
