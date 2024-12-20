# Generated by Django 5.0.7 on 2024-11-10 16:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "healthcareapp",
            "0028_remove_pill_image_url_remove_pill_manufacturer_and_more",
        ),
        ("social_django", "0016_alter_usersocialauth_extra_data"),
    ]

    operations = [
        migrations.AddField(
            model_name="register_model",
            name="google_auth",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="social_django.usersocialauth",
            ),
        ),
    ]
