from rest_framework import serializers
from .models import Periodo, Evento, Examen, RequisitosGraduacion, FechasImportantes, Mensajes


class MensajesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensajes
        fields = ['pregunta', 'respuesta', 'fecha_creacion']


class PeriodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Periodo
        fields = ['nombre_periodo', 'fecha_inicio', 'fecha_finalizacion']


class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = ['nombre_evento', 'descripcion', 'fecha_inicio', 'fecha_finalizacion', 'tipo_evento']


class ExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examen
        fields = ['tipo_examen', 'modalidad', 'fecha_inicio', 'fecha_finalizacion']


class RequisitosGraduacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequisitosGraduacion
        fields = ['descripcion', 'fecha_tentativa']


class FechasImportantesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FechasImportantes
        fields = ['nombre_evento', 'fecha']
