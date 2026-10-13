from django.db import migrations


def add_partnership_metric(apps, schema_editor):
    metric_model = apps.get_model("portfolio", "Metric")
    if metric_model.objects.filter(title="Partenariats").exists():
        return

    last_metric = metric_model.objects.order_by("-position", "-id").first()
    position = last_metric.position + 1 if last_metric else 1
    metric_model.objects.create(value="8", title="Partenariats", position=position)


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio", "0003_portfolioprofile_messaging_social_urls"),
    ]

    operations = [
        migrations.RunPython(add_partnership_metric, migrations.RunPython.noop),
    ]
