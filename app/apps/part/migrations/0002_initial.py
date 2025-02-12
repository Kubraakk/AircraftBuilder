# Generated by Django 4.2.19 on 2025-02-12 07:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("part", "0001_initial"),
        ("teams", "0001_initial"),
        ("aircraft", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="part",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_created",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created by",
            ),
        ),
        migrations.AddField(
            model_name="part",
            name="team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="produced_parts",
                to="teams.team",
            ),
        ),
        migrations.AddField(
            model_name="part",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_updated",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Updated by",
            ),
        ),
        migrations.AddField(
            model_name="inventory",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_created",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created by",
            ),
        ),
        migrations.AddField(
            model_name="inventory",
            name="part",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="part.part"
            ),
        ),
        migrations.AddField(
            model_name="inventory",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_updated",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Updated by",
            ),
        ),
        migrations.AddField(
            model_name="assemblypartusage",
            name="assembly",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="part.assembly"
            ),
        ),
        migrations.AddField(
            model_name="assemblypartusage",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_created",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created by",
            ),
        ),
        migrations.AddField(
            model_name="assemblypartusage",
            name="part",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="part.part"
            ),
        ),
        migrations.AddField(
            model_name="assemblypartusage",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_updated",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Updated by",
            ),
        ),
        migrations.AddField(
            model_name="assembly",
            name="aircraft",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="aircraft.aircraft",
            ),
        ),
        migrations.AddField(
            model_name="assembly",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_created",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Created by",
            ),
        ),
        migrations.AddField(
            model_name="assembly",
            name="parts_used",
            field=models.ManyToManyField(
                through="part.AssemblyPartUsage", to="part.part"
            ),
        ),
        migrations.AddField(
            model_name="assembly",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_updated",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Updated by",
            ),
        ),
    ]
