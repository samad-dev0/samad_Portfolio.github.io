from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models


def create_initial_content(apps, schema_editor):
    profile_model = apps.get_model("portfolio", "PortfolioProfile")
    metric_model = apps.get_model("portfolio", "Metric")
    service_model = apps.get_model("portfolio", "Service")
    skill_model = apps.get_model("portfolio", "Skill")

    profile_model.objects.get_or_create(pk=1)
    metric_model.objects.bulk_create([
        metric_model(value="10", title="Produits numériques", position=1),
        metric_model(value="60+", title="Client de confiance", position=2),
        metric_model(value="200+", title="Plus de 200 projets réalisés", position=3),
        metric_model(value="3", title="Experience", position=4),
    ])
    service_model.objects.bulk_create([
        service_model(title="Annalyste des données", description="Collecte et organisation des données, analyse et interprétation, visualisation, rapports et recommandations, prédictions ou machine learning simples.", position=1),
        service_model(title="Web Development", description="Création de sites web et d'applications web, maintenance, amélioration de la vitesse de chargement et sécurité des données.", position=2),
        service_model(title="Intelligence artificielle", description="Chatbots intelligents, traduction automatique, sites multilingues, détection automatique des attaques et blocage des comportements suspects.", icon_class="fa-solid fa-sitemap", position=3),
    ])
    skill_model.objects.bulk_create([
        skill_model(name="CSS", level=80, position=1),
        skill_model(name="HTML", level=90, position=2),
        skill_model(name="JavaScript", level=50, position=3),
        skill_model(name="PHP", level=70, position=4),
        skill_model(name="Python (Django)", level=80, position=5),
        skill_model(name="MySQL", level=90, position=6),
    ])


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="ContactMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="Nom")),
                ("email", models.EmailField(max_length=254, verbose_name="Email")),
                ("phone", models.CharField(blank=True, max_length=40, verbose_name="Téléphone")),
                ("message", models.TextField(verbose_name="Message")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Reçu le")),
                ("is_read", models.BooleanField(default=False, verbose_name="Lu")),
            ],
            options={"verbose_name": "message de contact", "verbose_name_plural": "messages de contact", "ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Metric",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("value", models.CharField(max_length=30, verbose_name="Valeur")),
                ("title", models.CharField(max_length=120, verbose_name="Libellé")),
                ("position", models.PositiveSmallIntegerField(default=0, verbose_name="Ordre")),
            ],
            options={"verbose_name": "chiffre clé", "verbose_name_plural": "chiffres clés", "ordering": ["position", "id"]},
        ),
        migrations.CreateModel(
            name="PortfolioProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("brand_name", models.CharField(default="Le_microsoft", max_length=80, verbose_name="Nom affiché")),
                ("title_line_1", models.CharField(default="Développeur web", max_length=100, verbose_name="Titre, ligne 1")),
                ("title_line_2", models.CharField(default="senior basé", max_length=100, verbose_name="Titre, ligne 2")),
                ("title_line_3", models.CharField(default="au TOGO", max_length=100, verbose_name="Titre, ligne 3")),
                ("experience", models.CharField(default="Plus de 3 ans d'expérience", max_length=120, verbose_name="Expérience")),
                ("about_heading", models.CharField(default="Développeur D'application senior", max_length=120, verbose_name="Titre de présentation")),
                ("bio_first", models.TextField(default="Je suis titulaire d’une licence a Esiba et j’ai effectué un stage professionnel au Ministere de la communication et des medias (radio kr), attesté par une certification de preuve.", verbose_name="Présentation, paragraphe 1")),
                ("bio_second", models.TextField(default="J’ai développé une application de stockage et de gestion d’audios et d’informations, permettant l’enregistrement, la consultation et l’administration des contenus audio, accompagnés de leurs données descriptives, au sein d’une interface centralisée.", verbose_name="Présentation, paragraphe 2")),
                ("full_name", models.CharField(default="TOUDJANI", max_length=120, verbose_name="Nom")),
                ("email", models.EmailField(default="samadtoudjani0@gmail.com", max_length=254, verbose_name="Email")),
                ("phone", models.CharField(default="+228 91 30 68 69", max_length=40, verbose_name="Téléphone")),
                ("cv_url", models.URLField(blank=True, verbose_name="Lien vers le CV")),
            ],
            options={"verbose_name": "profil", "verbose_name_plural": "profil"},
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120, verbose_name="Titre")),
                ("description", models.TextField(verbose_name="Description")),
                ("icon_class", models.CharField(default="fa-solid fa-code", max_length=80, verbose_name="Classe d'icône Font Awesome")),
                ("position", models.PositiveSmallIntegerField(default=0, verbose_name="Ordre")),
            ],
            options={"verbose_name": "service", "verbose_name_plural": "services", "ordering": ["position", "id"]},
        ),
        migrations.CreateModel(
            name="Skill",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80, verbose_name="Compétence")),
                ("level", models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="Niveau (%)")),
                ("position", models.PositiveSmallIntegerField(default=0, verbose_name="Ordre")),
            ],
            options={"verbose_name": "compétence", "verbose_name_plural": "compétences", "ordering": ["position", "id"]},
        ),
        migrations.RunPython(create_initial_content, migrations.RunPython.noop),
    ]
