# Generated by Django 5.1.4 on 2024-12-06 23:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chatapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Profesores",
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
                ("nombre", models.CharField(max_length=200)),
                ("apellido", models.CharField(max_length=200)),
                ("email", models.EmailField(max_length=254)),
                ("telefono", models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name="Cursos",
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
                ("nombre", models.CharField(max_length=200)),
                ("codigo", models.CharField(max_length=10)),
                ("descripcion", models.TextField(blank=True)),
                (
                    "profesor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="courses",
                        to="chatapp.profesores",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Seccion",
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
                ("nombre", models.CharField(max_length=10)),
                ("disponible_para_matricula", models.BooleanField(default=True)),
                ("horario", models.CharField(blank=True, max_length=200)),
                ("estudiantes_matriculados", models.PositiveIntegerField(default=0)),
                ("capacidad", models.PositiveIntegerField(default=20)),
                (
                    "curso",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sections",
                        to="chatapp.cursos",
                    ),
                ),
                (
                    "periodo",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="chatapp.periodo",
                    ),
                ),
            ],
        ),
    ]
