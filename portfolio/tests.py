from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import ContactMessage, Metric, PortfolioProfile, Service


class PortfolioContentTests(TestCase):
    def test_homepage_starts_in_light_theme_with_responsive_hero_shapes(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, '<body data-theme="light">')
        self.assertContains(response, "class=\"hero_shape_desktop\"")
        self.assertContains(response, "class=\"hero_shape_mobile\"")
        self.assertContains(response, "V700H430")
        self.assertContains(response, "portfolio-light-startup")

    def test_homepage_shows_accessible_skill_percentages(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.content.count(b'role="progressbar"'), 19)
        for skill in ("React.js", "Django", "Angular", "Spring Boot", "MySQL"):
            self.assertContains(response, f'aria-label="{skill}"')
        for level in (70, 80, 90, 100):
            self.assertContains(response, f'aria-valuenow="{level}"')

    def test_maintenance_service_is_in_looping_service_carousel(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, 'data-services-carousel')
        self.assertContains(response, 'data-service-prev')
        self.assertContains(response, 'data-service-next')
        self.assertContains(response, "Maintenance informatique")
        self.assertContains(
            response,
            "Maintenance préventive et corrective des équipements informatiques, diagnostic et dépannage des pannes, "
            "installation et configuration des systèmes et logiciels, sécurisation des données et assistance technique aux utilisateurs.",
        )
        self.assertEqual(response.context["services"].count(), 4)

    def test_metrics_are_presented_as_a_looping_carousel_with_partnership_count(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, 'data-metrics-carousel')
        self.assertContains(response, 'data-visible-slides="4"')
        self.assertContains(response, 'data-carousel-prev')
        self.assertContains(response, 'data-carousel-next')
        self.assertContains(response, "8")
        self.assertContains(response, "Partenariats")
        self.assertEqual(response.context["metrics"].count(), 5)

    def test_homepage_uses_profile_data_and_only_shows_configured_social_links(self):
        profile = PortfolioProfile.objects.get(pk=1)
        profile.brand_name = "Profil mis à jour"
        profile.linkedin_url = "https://www.linkedin.com/in/example"
        profile.save()

        response = self.client.get(reverse("home"))

        self.assertContains(response, "Profil mis à jour")
        self.assertContains(response, 'src="/static/img/user2.png?v=portfolio-hero-redesign"')
        self.assertContains(response, 'src="/static/img/site.png?v=20261019"')
        self.assertContains(response, 'alt="Aperçu des interfaces et outils du site SAMDEBUG"')
        self.assertContains(response, 'src="/static/img/securite.png?v=portfolio-security-skill-image"')
        self.assertContains(response, 'alt="Illustration de cybersécurité"')
        self.assertContains(response, 'href="https://www.linkedin.com/in/example"')
        self.assertNotContains(response, 'href="#"')

    def test_homepage_renders_single_bio_paragraph_when_bio_second_is_empty(self):
        profile = PortfolioProfile.objects.get(pk=1)
        self.assertEqual(profile.bio_second, "")
        response = self.client.get(reverse("home"))

        self.assertContains(
            response,
            "Ingénieur en informatique et technologies numériques, "
            "spécialisé en développement d’applications web et mobile, "
            "programmation, gestion de bases de données, ainsi qu’en "
            "installation, configuration et maintenance des réseaux informatiques et télécommunications.",
        )
        self.assertNotContains(response, '<p class="p">')

    def test_homepage_shows_location_map_for_configured_coordinates(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, "Carte indiquant ma position")
        self.assertContains(response, "6.22293° N, 1.18392° E")
        self.assertContains(response, "marker=6.22293%2C1.18392")

    def test_footer_uses_profile_contact_details_and_social_links(self):
        profile = PortfolioProfile.objects.get(pk=1)
        profile.linkedin_url = "https://www.linkedin.com/in/example"
        profile.tiktok_url = "https://www.tiktok.com/@example"
        profile.whatsapp_url = "https://wa.me/22891306869"
        profile.telegram_url = "https://t.me/example"
        profile.save()

        response = self.client.get(reverse("home"))

        self.assertContains(response, "Navigation de pied de page")
        self.assertContains(response, f'href="mailto:{profile.email}"')
        self.assertContains(response, f'href="tel:{profile.phone.replace(" ", "")}"')
        self.assertContains(response, 'aria-label="LinkedIn"')
        self.assertContains(response, 'href="https://www.tiktok.com/@example"')
        self.assertContains(response, 'href="https://wa.me/22891306869"')
        self.assertContains(response, 'href="https://t.me/example"')
        self.assertContains(response, 'aria-label="TikTok"')
        self.assertContains(response, 'aria-label="WhatsApp"')
        self.assertContains(response, 'aria-label="Telegram"')
        self.assertContains(response, "Tous droits réservés.")


from django.contrib.auth import get_user_model

User = get_user_model()


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="portfolio@example.com",
)
class ContactAuthWorkflowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="awamensah",
            email="awa@example.com",
            password="securePassword123",
            first_name="Awa",
            last_name="Mensah",
        )

    def test_unauthenticated_contact_redirects_to_login_and_stores_session(self):
        response = self.client.post(
            reverse("home"),
            {
                "name": "Awa Mensah",
                "email": "awa@example.com",
                "phone": "+228 90 00 00 00",
                "message": "Parlons de mon projet.",
            },
        )

        expected_redirect = f"{reverse('login')}?next={reverse('home')}#contact"
        self.assertRedirects(response, expected_redirect)
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertIn("pending_contact_data", self.client.session)
        self.assertEqual(self.client.session["pending_contact_data"]["message"], "Parlons de mon projet.")

    def test_authenticated_contact_creates_message_and_sends_email(self):
        self.client.login(username="awamensah", password="securePassword123")
        response = self.client.post(
            reverse("home"),
            {
                "name": "Awa Mensah",
                "email": "awa@example.com",
                "phone": "+228 90 00 00 00",
                "message": "Parlons de mon projet.",
            },
        )

        self.assertRedirects(response, f"{reverse('home')}#contact")
        self.assertEqual(ContactMessage.objects.count(), 1)
        contact = ContactMessage.objects.first()
        self.assertEqual(contact.user, self.user)
        self.assertEqual(contact.email, "awa@example.com")
        self.assertEqual(len(mail.outbox), 1)
        confirmation = mail.outbox[0]
        self.assertEqual(confirmation.to, ["awa@example.com"])
        self.assertIn("Salut Awa Mensah,", confirmation.body)
        self.assertIn("Votre demande de rendez-vous a bien été enregistrée.", confirmation.body)

    def test_registration_automatically_sends_pending_contact_message(self):
        # Visitor fills contact form without account
        self.client.post(
            reverse("home"),
            {
                "name": "Koffi Doe",
                "email": "koffi@example.com",
                "phone": "+228 91 00 11 22",
                "message": "Proposition de mission freelance.",
            },
        )

        # Visitor creates account on /connexion/
        reg_response = self.client.post(
            reverse("login"),
            {
                "action": "register",
                "next": f"{reverse('home')}#contact",
                "name": "Koffi Doe",
                "email": "koffi@example.com",
                "password": "myNewPassword123",
                "password_confirm": "myNewPassword123",
            },
        )

        self.assertRedirects(reg_response, f"{reverse('home')}#contact")
        self.assertEqual(ContactMessage.objects.count(), 1)
        contact = ContactMessage.objects.first()
        self.assertEqual(contact.email, "koffi@example.com")
        self.assertEqual(contact.message, "Proposition de mission freelance.")
        self.assertEqual(len(mail.outbox), 1)

    def test_login_with_email_and_password(self):
        response = self.client.post(
            reverse("login"),
            {
                "action": "login",
                "next": f"{reverse('home')}#contact",
                "username_or_email": "awa@example.com",
                "password": "securePassword123",
            },
        )
        self.assertRedirects(response, f"{reverse('home')}#contact")

    def test_logout_redirects_home(self):
        self.client.login(username="awamensah", password="securePassword123")
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("home"))

    def test_google_login_warns_when_client_id_is_missing(self):
        with override_settings(GOOGLE_CLIENT_ID=""):
            response = self.client.get(reverse("google_login"))
            self.assertRedirects(response, f"{reverse('login')}?next=%2F%23contact")
