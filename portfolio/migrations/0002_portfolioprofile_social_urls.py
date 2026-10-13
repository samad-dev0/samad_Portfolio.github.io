from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="portfolioprofile",
            name="facebook_url",
            field=models.URLField(blank=True, verbose_name="Profil Facebook"),
        ),
        migrations.AddField(
            model_name="portfolioprofile",
            name="twitter_url",
            field=models.URLField(blank=True, verbose_name="Profil Twitter / X"),
        ),
        migrations.AddField(
            model_name="portfolioprofile",
            name="youtube_url",
            field=models.URLField(blank=True, verbose_name="Chaîne YouTube"),
        ),
        migrations.AddField(
            model_name="portfolioprofile",
            name="linkedin_url",
            field=models.URLField(blank=True, verbose_name="Profil LinkedIn"),
        ),
        migrations.AddField(
            model_name="portfolioprofile",
            name="instagram_url",
            field=models.URLField(blank=True, verbose_name="Profil Instagram"),
        ),
    ]
