from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.profile_config.models import LesionesRestricciones

class Rutina(models.Model):
    """Rutina de entrenamiento"""
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=50, choices=[
        ('fuerza', 'Fuerza'),
        ('hipertrofia', 'Hipertrofia'),
        ('resistencia', 'Resistencia'),
        ('funcional', 'Funcional'),
        ('cardio', 'Cardio'),
        ('mixto', 'Mixto')
    ])
    duracion_semanas = models.IntegerField()
    dias_semana = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])
    nivel = models.CharField(max_length=20, choices=[
        ('principiante', 'Principiante'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado')
    ])
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Rutinas"
    
    def __str__(self):
        return self.nombre


class Entrenamientos(models.Model):
    """Sesión de entrenamiento - ENTIDAD CENTRAL SECUNDARIA"""
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE, related_name='entrenamientos')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    dia_semana = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])
    duracion_estimada_minutos = models.IntegerField()
    orden = models.IntegerField(default=1)
    
    # Relación N:M con Ejercicios
    ejercicios = models.ManyToManyField('exercises.Ejercicios', through='exercises.EntrenamientosEjercicios', related_name='entrenamientos')
    
    class Meta:
        verbose_name_plural = "Entrenamientos"
        ordering = ['rutina', 'orden']
    
    def __str__(self):
        return f"{self.rutina.nombre} - {self.nombre}"


class Series(models.Model):
    """Series de un entrenamiento"""
    entrenamiento = models.ForeignKey(Entrenamientos, on_delete=models.CASCADE, related_name='series')
    numero_serie = models.IntegerField()
    repeticiones_objetivo = models.IntegerField()
    peso_kg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    tiempo_descanso_segundos = models.IntegerField(default=60)
    notas = models.TextField(blank=True)
    completada = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Series"
        ordering = ['entrenamiento', 'numero_serie']
    
    def __str__(self):
        return f"Serie {self.numero_serie} - {self.entrenamiento.nombre}"


class LesionesEntrenamientos(models.Model):
    """Tabla intermedia para la relación N:M entre Lesiones y Entrenamientos"""
    lesion = models.ForeignKey(LesionesRestricciones, on_delete=models.CASCADE)
    entrenamiento = models.ForeignKey(Entrenamientos, on_delete=models.CASCADE)
    contraindicacion = models.TextField(help_text="Descripción de por qué esta lesión afecta este entrenamiento")
    nivel_riesgo = models.CharField(max_length=20, choices=[
        ('bajo', 'Bajo'),
        ('medio', 'Medio'),
        ('alto', 'Alto'),
        ('prohibido', 'Prohibido')
    ])
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Lesiones - Entrenamientos"
    
    def __str__(self):
        return f"{self.lesion.nombre} afecta a {self.entrenamiento.nombre}"
