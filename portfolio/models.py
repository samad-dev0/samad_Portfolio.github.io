from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class PortfolioProfile(models.Model):
    brand_name = models.CharField("Nom affiché", max_length=80, default="Le_microsoft")
    title_line_1 = models.CharField("Titre, ligne 1", max_length=100, default="Développeur web")
    title_line_2 = models.CharField("Titre, ligne 2", max_length=100, default="senior basé")
    title_line_3 = models.CharField("Titre, ligne 3", max_length=100, default="au TOGO")
    experience = models.CharField("Expérience", max_length=120, default="Plus de 3 ans d'expérience")
    about_heading = models.CharField("Titre de présentation", max_length=120, default="Développeur D'application senior")
    bio_first = models.TextField("Présentation, paragraphe 1", default="Je suis titulaire d’une licence a Esiba et j’ai effectué un stage professionnel au Ministere de la communication et des medias (radio kr), attesté par une certification de preuve.")
    bio_second = models.TextField("Présentation, paragraphe 2", default="J’ai développé une application de stockage et de gestion d’audios et d’informations, permettant l’enregistrement, la consultation et l’administration des contenus audio, accompagnés de leurs données descriptives, au sein d’une interface centralisée.")
    full_name = models.CharField("Nom", max_length=120, default="TOUDJANI")
    email = models.EmailField("Email", default="samadtoudjani0@gmail.com")
    phone = models.CharField("Téléphone", max_length=40, default="+228 91 30 68 69")
    cv_url = models.URLField("Lien vers le CV", blank=True)

    class Meta:
        verbose_name = "profil"
        verbose_name_plural = "profil"

    def __str__(self):
        return self.brand_name


class Metric(models.Model):
    value = models.CharField("Valeur", max_length=30)
    title = models.CharField("Libellé", max_length=120)
    position = models.PositiveSmallIntegerField("Ordre", default=0)

    class Meta:
        ordering = ["position", "id"]
        verbose_name = "chiffre clé"
        verbose_name_plural = "chiffres clés"

    def __str__(self):
        return f"{self.value} - {self.title}"


class Service(models.Model):
    title = models.CharField("Titre", max_length=120)
    description = models.TextField("Description")
    icon_class = models.CharField("Classe d'icône Font Awesome", max_length=80, default="fa-solid fa-code")
    position = models.PositiveSmallIntegerField("Ordre", default=0)

    class Meta:
        ordering = ["position", "id"]
        verbose_name = "service"
        verbose_name_plural = "services"

    def __str__(self):
        return self.title


class Skill(models.Model):
    name = models.CharField("Compétence", max_length=80)
    level = models.PositiveSmallIntegerField(
        "Niveau (%)", validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    position = models.PositiveSmallIntegerField("Ordre", default=0)

    class Meta:
        ordering = ["position", "id"]
        verbose_name = "compétence"
        verbose_name_plural = "compétences"

    def __str__(self):
        return f"{self.name} ({self.level} %)"


class ContactMessage(models.Model):
    name = models.CharField("Nom", max_length=120)
    email = models.EmailField("Email")
    phone = models.CharField("Téléphone", max_length=40, blank=True)
    message = models.TextField("Message")
    created_at = models.DateTimeField("Reçu le", auto_now_add=True)
    is_read = models.BooleanField("Lu", default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "message de contact"
        verbose_name_plural = "messages de contact"

    def __str__(self):
        return f"{self.name} - {self.created_at:%Y-%m-%d %H:%M}"
