# Generated by Django 5.0.7 on 2024-08-16 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("healthcareapp", "0005_alter_register_model_dob"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="register_model",
            name="phoneno",
        ),
    ]