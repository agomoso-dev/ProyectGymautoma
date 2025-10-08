from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.profile_config.models import Perfil

class Nutricion(models.Model):
    """Registro nutricional del perfil"""
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='registros_nutricion')
    fecha = models.DateField()
    calorias_objetivo = models.IntegerField(help_text="Calorías diarias objetivo")
    calorias_consumidas = models.IntegerField(default=0)
    proteinas_gramos = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    carbohidratos_gramos = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    grasas_gramos = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    agua_litros = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    notas = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Nutrición"
        ordering = ['-fecha']
        unique_together = ['perfil', 'fecha']
    
    def __str__(self):
        return f"Nutrición {self.perfil.nombre_completo} - {self.fecha}"


class PlanesNutricionales(models.Model):
    """Planes nutricionales asociados a un registro de nutrición"""
    nutricion = models.ForeignKey(Nutricion, on_delete=models.CASCADE, related_name='planes')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo_dieta = models.CharField(max_length=50, choices=[
        ('definicion', 'Definición'),
        ('volumen', 'Volumen'),
        ('mantenimiento', 'Mantenimiento'),
        ('cetogenica', 'Cetogénica'),
        ('vegetariana', 'Vegetariana'),
        ('vegana', 'Vegana')
    ])
    duracion_semanas = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Planes Nutricionales"
    
    def __str__(self):
        return f"{self.nombre} - {self.tipo_dieta}"
