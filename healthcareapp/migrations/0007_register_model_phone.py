# Generated by Django 5.0.7 on 2024-08-16 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("healthcareapp", "0006_remove_register_model_phoneno"),
    ]

    operations = [
        migrations.AddField(
            model_name="register_model",
            name="phone",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]