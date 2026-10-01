from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import ContactMessage, PortfolioProfile


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="portfolio@example.com",
)
class ContactConfirmationEmailTests(TestCase):
    def test_valid_contact_sends_confirmation_to_sender(self):
        response = self.client.post(
            reverse("home"),
            {
                "name": "Awa Mensah",
                "email": "awa@example.com",
                "phone": "+228 90 00 00 00",
                "message": "Parlons de mon projet.",
            },
        )

        self.assertRedirects(response, reverse("home"))
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        confirmation = mail.outbox[0]
        self.assertEqual(confirmation.to, ["awa@example.com"])
        self.assertEqual(confirmation.reply_to, [PortfolioProfile.objects.get(pk=1).email])
        self.assertIn("Salut Awa Mensah,", confirmation.body)
        self.assertIn("Votre demande de rendez-vous a bien été enregistrée.", confirmation.body)
        self.assertIn("Développeur Web & Applications", confirmation.body)
