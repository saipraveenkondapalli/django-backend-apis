# Generated by Django 5.0.1 on 2024-01-13 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0006_website_license_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='website',
            name='url',
            field=models.URLField(default='google.co'),
            preserve_default=False,
        ),
    ]
