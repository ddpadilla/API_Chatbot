from django.db import models


class Mensajes(models.Model):
    pregunta = models.TextField(max_length=500)
    respuesta = models.TextField(max_length=500)
    fecha_creacion = models.DateTimeField(auto_now_add=True)


class Periodo(models.Model):
    nombre_periodo = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField()


class Evento(models.Model):
    EVENT_TYPES = [
        ('MAT', 'Matrícula'),
        ('EXA', 'Examen'),
        ('IND', 'Inducción'),
        ('GRD', 'Graduación'),
        ('OTR', 'Otro'),
    ]

    nombre_evento = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField(blank=True, null=True)
    tipo_evento = models.CharField(
        max_length=3,
        choices=EVENT_TYPES,
        default='OTR',
        help_text="Selecciona el tipo de evento",
    )
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, related_name="events")


class Examen(models.Model):
    tipo_examen = models.CharField(max_length=200)
    modalidad = models.CharField(max_length=200)
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField(blank=True, null=True)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, related_name="exams")


class RequisitosGraduacion(models.Model):
    descripcion = models.TextField()
    fecha_tentativa = models.DateField()
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, related_name="graduation_requirements")


class FechasImportantes(models.Model):
    nombre_evento = models.CharField(max_length=200)
    fecha = models.DateField()
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, related_name="important_dates")





