# Generated by Django 5.0.7 on 2024-11-02 11:26

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("healthcareapp", "0025_disease"),
    ]

    operations = [
        migrations.CreateModel(
            name="Blogs",
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
                ("title", ckeditor.fields.RichTextField(blank=True, null=True)),
                ("desc", ckeditor.fields.RichTextField(blank=True, null=True)),
                ("image", models.ImageField(upload_to="images/")),
                ("bywho", ckeditor.fields.RichTextField(blank=True, null=True)),
                ("wdate", ckeditor.fields.RichTextField(blank=True, null=True)),
            ],
        ),
    ]
