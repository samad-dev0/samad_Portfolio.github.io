from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio", "0002_portfolioprofile_social_urls"),
    ]

    operations = [
        migrations.AddField(
            model_name="portfolioprofile",
            name="tiktok_url",
            field=models.URLField(blank=True, verbose_name="Profil TikTok"),
        ),
        migrations.AddField(
            model_name="portfolioprofile",
            name="whatsapp_url",
            field=models.URLField(blank=True, verbose_name="Lien WhatsApp"),
        ),
        migrations.AddField(
            model_name="portfolioprofile",
            name="telegram_url",
            field=models.URLField(blank=True, verbose_name="Profil Telegram"),
        ),
    ]
