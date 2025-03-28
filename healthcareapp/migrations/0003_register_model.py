# Generated by Django 5.0.7 on 2024-08-07 16:49

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("healthcareapp", "0002_alter_contact_model_message_alter_contact_model_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="register_model",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", ckeditor.fields.RichTextField()),
                ("email", models.EmailField(max_length=254)),
                ("passw", models.CharField(max_length=40)),
                ("cpassw", models.CharField(max_length=40)),
            ],
        ),
    ]
