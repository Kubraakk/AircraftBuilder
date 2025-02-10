# Generated by Django 4.2.19 on 2025-02-10 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("teams", "0001_initial"),
        ("aircraft", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Assembly",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "aircraft",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="aircraft.aircraft",
                    ),
                ),
            ],
            options={
                "verbose_name": "Assembly",
                "verbose_name_plural": "Assemblies",
            },
        ),
        migrations.CreateModel(
            name="Part",
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
                    "name",
                    models.IntegerField(
                        choices=[
                            (1, "Kanat"),
                            (2, "Gövde"),
                            (3, "Kuyruk"),
                            (4, "Aviyonik"),
                        ]
                    ),
                ),
                (
                    "aircraft",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parts",
                        to="aircraft.aircraft",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="produced_parts",
                        to="teams.team",
                    ),
                ),
            ],
            options={
                "verbose_name": "Part",
                "verbose_name_plural": "Parts",
                "unique_together": {("name", "aircraft")},
            },
        ),
        migrations.CreateModel(
            name="Inventory",
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
                ("quantity", models.PositiveIntegerField(default=0)),
                (
                    "part",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="part.part",
                    ),
                ),
            ],
            options={
                "verbose_name": "Inventory",
                "verbose_name_plural": "Inventories",
            },
        ),
        migrations.CreateModel(
            name="AssemblyPartUsage",
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
                ("quantity_used", models.PositiveIntegerField()),
                (
                    "assembly",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="part.assembly",
                    ),
                ),
                (
                    "part",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="part.part",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="assembly",
            name="parts_used",
            field=models.ManyToManyField(
                through="part.AssemblyPartUsage", to="part.part"
            ),
        ),
    ]
