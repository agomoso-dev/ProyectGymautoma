from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# ==================== GRUPO 1: PERFIL Y CONFIGURACIÓN ====================

class Objetivo(models.Model):
    """Objetivos de entrenamiento: Hipertrofia, Pérdida de peso, Fuerza, etc."""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Objetivos"
    
    def __str__(self):
        return self.nombre


class Estado(models.Model):
    """Estados físicos: Bien, Fatigado, Lesionado, etc."""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    nivel = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1=Bien, 5=Excesivamente fatigado"
    )
    
    class Meta:
        verbose_name_plural = "Estados"
    
    def __str__(self):
        return self.nombre


class Perfil(models.Model):
    """Perfil de usuario - ENTIDAD CENTRAL PRINCIPAL"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    nombre_completo = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=20, choices=[
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro')
    ])
    altura = models.DecimalField(max_digits=5, decimal_places=2, help_text="Altura en cm")
    peso_actual = models.DecimalField(max_digits=5, decimal_places=2, help_text="Peso en kg")
    
    # Relaciones N:1
    objetivo = models.ForeignKey(Objetivo, on_delete=models.SET_NULL, null=True, related_name='perfiles')
    rutina = models.ForeignKey('training.Rutina', on_delete=models.SET_NULL, null=True, blank=True, related_name='perfiles')       
    
    # Relación N:M con Estado
    estados = models.ManyToManyField(Estado, through='PerfilEstado', related_name='perfiles')
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Perfiles"
    
    def __str__(self):
        return self.nombre_completo


class PerfilEstado(models.Model):
    """Tabla intermedia para la relación N:M entre Perfil y Estado"""
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    grupo_muscular = models.CharField(max_length=100, help_text="Ej: Bíceps, Hombros, Piernas")
    nivel_fatiga = models.CharField(max_length=50, choices=[
        ('bien', 'Bien'),
        ('poco_fatigado', 'Poco fatigado'),
        ('fatigado', 'Fatigado'),
        ('muy_fatigado', 'Muy fatigado'),
        ('excesivamente_fatigado', 'Excesivamente fatigado')
    ])
    fecha_registro = models.DateTimeField(auto_now_add=True)
    notas = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Perfil Estados"
        ordering = ['-fecha_registro']
    
    def __str__(self):
        return f"{self.perfil.nombre_completo} - {self.grupo_muscular}: {self.nivel_fatiga}"


class ConfiguracionUsuario(models.Model):
    """Configuración personal del usuario (1:1 con Perfil)"""
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE, related_name='configuracion')
    idioma = models.CharField(max_length=10, default='es')
    unidad_peso = models.CharField(max_length=10, choices=[('kg', 'Kilogramos'), ('lb', 'Libras')], default='kg')
    unidad_distancia = models.CharField(max_length=10, choices=[('km', 'Kilómetros'), ('mi', 'Millas')], default='km')
    notificaciones_activas = models.BooleanField(default=True)
    tema_oscuro = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Configuraciones de Usuario"
    
    def __str__(self):
        return f"Configuración de {self.perfil.nombre_completo}"


class LesionesRestricciones(models.Model):
    """Lesiones y restricciones médicas del perfil"""
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='lesiones')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    grupo_muscular_afectado = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_recuperacion_estimada = models.DateField(null=True, blank=True)
    activa = models.BooleanField(default=True)
    nivel_gravedad = models.CharField(max_length=20, choices=[
        ('leve', 'Leve'),
        ('moderada', 'Moderada'),
        ('grave', 'Grave')
    ])
    
    # Relación N:M con Entrenamientos
    entrenamientos_afectados = models.ManyToManyField('training.Entrenamientos', through='training.LesionesEntrenamientos', related_name='lesiones')
    
    class Meta:
        verbose_name_plural = "Lesiones y Restricciones"
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"{self.nombre} - {self.perfil.nombre_completo}"

