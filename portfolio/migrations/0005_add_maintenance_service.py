from django.db import migrations


def add_maintenance_service(apps, schema_editor):
    service_model = apps.get_model("portfolio", "Service")
    title = "Maintenance informatique"
    if service_model.objects.filter(title=title).exists():
        return

    last_service = service_model.objects.order_by("-position", "-id").first()
    position = last_service.position + 1 if last_service else 1
    service_model.objects.create(
        title=title,
        description=(
            "Maintenance préventive et corrective des équipements informatiques, diagnostic et dépannage des pannes, "
            "installation et configuration des systèmes et logiciels, sécurisation des données et assistance technique aux utilisateurs."
        ),
        icon_class="fa-solid fa-screwdriver-wrench",
        position=position,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio", "0004_add_partnership_metric"),
    ]

    operations = [
        migrations.RunPython(add_maintenance_service, migrations.RunPython.noop),
    ]
