# Generated by Django 5.0.7 on 2024-09-07 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("healthcareapp", "0021_supplement_model"),
    ]

    operations = [
        migrations.DeleteModel(
            name="supplement_model",
        ),
    ]
