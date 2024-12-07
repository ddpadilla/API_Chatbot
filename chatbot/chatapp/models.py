from django.db import models


class Mensajes(models.Model):
    pregunta = models.TextField(max_length=500)
    respuesta = models.TextField(max_length=500)
    fecha_creacion = models.DateTimeField(auto_now_add=True)


class Periodo(models.Model):
    nombre_periodo = models.CharField(max_length=50)  # Ejemplo: "Periodo I UNITEC/CEUTEC"
    fecha_inicio = models.DateField()  # Fecha de inicio del periodo
    fecha_finalizacion = models.DateField()  # Fecha de fin del periodo


class Evento(models.Model):
    EVENT_TYPES = [
        ('MAT', 'Matrícula'),
        ('EXA', 'Examen'),
        ('IND', 'Inducción'),
        ('GRD', 'Graduación'),
        ('OTR', 'Otro'),
    ]

    nombre_evento = models.CharField(max_length=200)  # Nombre del evento o actividad
    descripcion = models.TextField(blank=True, null=True)  # Detalles adicionales
    fecha_inicio = models.DateField()  # Fecha de inicio
    fecha_finalizacion = models.DateField(blank=True, null=True)  # Fecha de fin (opcional)
    tipo_evento = models.CharField(
        max_length=3,
        choices=EVENT_TYPES,
        default='OTR',
        help_text="Selecciona el tipo de evento",
    )  # Tipo de evento
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, related_name="events")


class Examen(models.Model):
    tipo_examen = models.CharField(max_length=200)  # Ejemplo: "Examen de suficiencia de grado"
    modalidad = models.CharField(max_length=200)  # Modalidad del examen
    fecha_inicio = models.DateField()  # Fecha de inicio del examen
    fecha_finalizacion = models.DateField(blank=True, null=True)  # Fecha de fin (si aplica)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, related_name="exams")


class RequisitosGraduacion(models.Model):
    descripcion = models.TextField()  # Descripción de los requisitos o actividades
    fecha_tentativa = models.DateField()  # Fecha tentativa para cumplir el requisito
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, related_name="graduation_requirements")


class FechasImportantes(models.Model):
    nombre_evento = models.CharField(max_length=200)  # Nombre del evento importante
    fecha = models.DateField()  # Fecha exacta
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, related_name="important_dates")





