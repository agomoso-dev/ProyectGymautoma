from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.profile_config.models import Perfil
from apps.training.models import Entrenamientos

class Progresion(models.Model):
    """Registro de progreso del usuario"""
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='progresos')
    entrenamiento = models.ForeignKey(Entrenamientos, on_delete=models.CASCADE, related_name='progresos')
    fecha = models.DateTimeField(auto_now_add=True)
    peso_corporal_kg = models.DecimalField(max_digits=5, decimal_places=2)
    duracion_minutos = models.IntegerField()
    calorias_quemadas = models.IntegerField(default=0)
    nivel_intensidad = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Nivel de intensidad del 1 al 10"
    )
    completado = models.BooleanField(default=True)
    notas = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Progresión"
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.perfil.nombre_completo} - {self.entrenamiento.nombre} - {self.fecha.date()}"


class Reportes(models.Model):
    """Reportes generados por el usuario"""
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='reportes')
    tipo_reporte = models.CharField(max_length=50, choices=[
        ('semanal', 'Semanal'),
        ('mensual', 'Mensual'),
        ('trimestral', 'Trimestral'),
        ('personalizado', 'Personalizado')
    ])
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    entrenamientos_completados = models.IntegerField(default=0)
    calorias_totales_quemadas = models.IntegerField(default=0)
    peso_inicial_kg = models.DecimalField(max_digits=5, decimal_places=2)
    peso_final_kg = models.DecimalField(max_digits=5, decimal_places=2)
    observaciones = models.TextField(blank=True)
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Reportes"
        ordering = ['-fecha_generacion']
    
    def __str__(self):
        return f"Reporte {self.tipo_reporte} - {self.perfil.nombre_completo} ({self.fecha_inicio} a {self.fecha_fin})"
