from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.training.models import Entrenamientos
class CategoriasEjercicios(models.Model):
    """Categorías de ejercicios: Fuerza, Cardio, Movilidad, etc."""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categorías de Ejercicios"
    
    def __str__(self):
        return self.nombre


class GruposMusculares(models.Model):
    """Grupos musculares: Pecho, Espalda, Piernas, etc."""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    region_corporal = models.CharField(max_length=50, choices=[
        ('superior', 'Tren Superior'),
        ('inferior', 'Tren Inferior'),
        ('core', 'Core/Abdomen'),
        ('total', 'Cuerpo Completo')
    ])
    
    class Meta:
        verbose_name_plural = "Grupos Musculares"
    
    def __str__(self):
        return self.nombre


class Equipamiento(models.Model):
    """Equipamiento necesario para ejercicios"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    disponible_en_casa = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Equipamiento"
    
    def __str__(self):
        return self.nombre


class Ejercicios(models.Model):
    """Catálogo de ejercicios - ENTIDAD CENTRAL TERCIARIA"""
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    instrucciones = models.TextField(help_text="Paso a paso del ejercicio")
    
    # Relación N:1 con Categoría
    categoria = models.ForeignKey(CategoriasEjercicios, on_delete=models.SET_NULL, null=True, related_name='ejercicios')
    
    # Relaciones N:M
    grupos_musculares = models.ManyToManyField(GruposMusculares, through='EjerciciosGruposMusculares', related_name='ejercicios')
    equipamiento = models.ManyToManyField(Equipamiento, through='EjerciciosEquipamiento', related_name='ejercicios')
    
    nivel_dificultad = models.CharField(max_length=20, choices=[
        ('principiante', 'Principiante'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado')
    ])
    calorias_estimadas = models.IntegerField(default=0, help_text="Calorías quemadas por repetición/minuto")
    
    class Meta:
        verbose_name_plural = "Ejercicios"
    
    def __str__(self):
        return self.nombre


class EntrenamientosEjercicios(models.Model):
    """Tabla intermedia para la relación N:M entre Entrenamientos y Ejercicios"""
    entrenamiento = models.ForeignKey(Entrenamientos, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicios, on_delete=models.CASCADE)
    orden = models.IntegerField(default=1)
    series = models.IntegerField(default=3)
    repeticiones = models.IntegerField(default=10)
    peso_recomendado_kg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    tiempo_descanso_segundos = models.IntegerField(default=60)
    notas = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Entrenamientos - Ejercicios"
        ordering = ['entrenamiento', 'orden']
        unique_together = ['entrenamiento', 'ejercicio']
    
    def __str__(self):
        return f"{self.entrenamiento.nombre} - {self.ejercicio.nombre}"


class EjerciciosGruposMusculares(models.Model):
    """Tabla intermedia para la relación N:M entre Ejercicios y Grupos Musculares"""
    ejercicio = models.ForeignKey(Ejercicios, on_delete=models.CASCADE)
    grupo_muscular = models.ForeignKey(GruposMusculares, on_delete=models.CASCADE)
    nivel_enfoque = models.CharField(max_length=20, choices=[
        ('primario', 'Primario'),
        ('secundario', 'Secundario')
    ])
    porcentaje_activacion = models.IntegerField(
        default=50,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Porcentaje de activación muscular"
    )
    
    class Meta:
        verbose_name_plural = "Ejercicios - Grupos Musculares"
        unique_together = ['ejercicio', 'grupo_muscular']
    
    def __str__(self):
        return f"{self.ejercicio.nombre} - {self.grupo_muscular.nombre} ({self.nivel_enfoque})"


class EjerciciosEquipamiento(models.Model):
    """Tabla intermedia para la relación N:M entre Ejercicios y Equipamiento"""
    ejercicio = models.ForeignKey(Ejercicios, on_delete=models.CASCADE)
    equipamiento = models.ForeignKey(Equipamiento, on_delete=models.CASCADE)
    es_obligatorio = models.BooleanField(default=True, help_text="Si es False, es equipamiento opcional/alternativo")
    cantidad = models.IntegerField(default=1, help_text="Cantidad de este equipamiento necesario")
    
    class Meta:
        verbose_name_plural = "Ejercicios - Equipamiento"
        unique_together = ['ejercicio', 'equipamiento']
    
    def __str__(self):
        obligatorio = "Obligatorio" if self.es_obligatorio else "Opcional"
        return f"{self.ejercicio.nombre} - {self.equipamiento.nombre} ({obligatorio})"


class Multimedia(models.Model):
    """Archivos multimedia de ejercicios (videos, imágenes)"""
    ejercicio = models.ForeignKey(Ejercicios, on_delete=models.CASCADE, related_name='multimedia')
    tipo = models.CharField(max_length=20, choices=[
        ('imagen', 'Imagen'),
        ('video', 'Video'),
        ('gif', 'GIF')
    ])
    archivo = models.FileField(upload_to='ejercicios/')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    es_principal = models.BooleanField(default=False)
    orden = models.IntegerField(default=1)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Multimedia"
        ordering = ['ejercicio', 'orden']
    
    def __str__(self):
        return f"{self.ejercicio.nombre} - {self.tipo} - {self.titulo}"


