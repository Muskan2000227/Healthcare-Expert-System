# Generated by Django 5.0.7 on 2024-09-07 16:53

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("healthcareapp", "0022_delete_supplement_model"),
    ]

    operations = [
        migrations.CreateModel(
            name="supplement_model",
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
                ("supplement_name", models.CharField(max_length=200)),
                ("overview_drug", ckeditor.fields.RichTextField(blank=True, null=True)),
                ("uses_drug", ckeditor.fields.RichTextField(blank=True, null=True)),
                (
                    "sideeffects_drug",
                    ckeditor.fields.RichTextField(blank=True, null=True),
                ),
                (
                    "precaution_drug",
                    ckeditor.fields.RichTextField(blank=True, null=True),
                ),
                (
                    "interactions_Drug",
                    ckeditor.fields.RichTextField(blank=True, null=True),
                ),
                ("dosing_Drug", ckeditor.fields.RichTextField(blank=True, null=True)),
                ("othername", models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]
