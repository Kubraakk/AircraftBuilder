# Generated by Django 4.2.19 on 2025-02-12 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Team",
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
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Created at"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Updated at"
                    ),
                ),
                (
                    "name",
                    models.IntegerField(
                        choices=[
                            (1, "Kanat Takımı"),
                            (2, "Gövde Takımı"),
                            (3, "Kuyruk Takımı"),
                            (4, "Aviyonik Takımı"),
                            (5, "Montaj Takımı"),
                        ],
                        unique=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Team",
                "verbose_name_plural": "Teams",
            },
        ),
    ]
