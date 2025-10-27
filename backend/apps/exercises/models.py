from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.training.models import Entrenamientos


'''
@ ==================== Categorias de Ejercicios ====================
'''
class CategoriasEjercicios(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

'''
@ ==================== Grupos Musculares ====================
'''

class GruposMusculares(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    region_corporal = models.CharField(max_length=50, choices=[
    ('superior', 'Tren Superior'),
    ('inferior', 'Tren Inferior'),
    ('core', 'Core'),
    ('total', 'Cuerpo Completo')
    ])

    def __str__(self):
        return self.nombre

'''
@ ==================== Equipamientos ====================
'''

class Equipamiento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

'''
@ ==================== Tipo de atributo ====================
'''

class TipoAtributo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

'''
@ ==================== Opciones de atributo ====================
'''

class OpcionAtributo(models.Model):
    tipo = models.ForeignKey(TipoAtributo, on_delete=models.CASCADE, related_name='opciones')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tipo.nombre}: {self.nombre}"

'''
@ ==================== Subopcion de Atributo ====================
'''
class SubOpcionAtributo(models.Model):
    opcion_padre = models.ForeignKey(OpcionAtributo, on_delete=models.CASCADE, related_name='subopciones')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.opcion_padre} → {self.nombre}"

'''
@ ==================== Ejercicios ====================
'''
class Ejercicios(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    instrucciones = models.TextField()

    categoria = models.ForeignKey(CategoriasEjercicios, on_delete=models.SET_NULL, null=True, related_name='ejercicios')
    grupos_musculares = models.ManyToManyField(GruposMusculares, through='EjerciciosGruposMusculares', related_name='ejercicios')
    equipamiento = models.ManyToManyField(Equipamiento, through='EjerciciosEquipamiento', related_name='ejercicios')
    atributos = models.ManyToManyField(SubOpcionAtributo, through='EjercicioAtributo', related_name='ejercicios')

    nivel_dificultad = models.CharField(max_length=20, choices=[
        ('principiante', 'Principiante'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado')
    ])

    def __str__(self):
        return self.nombre

'''
@ ==================== Ejercicio y atributos ====================
'''
class EjercicioAtributo(models.Model):
    ejercicio = models.ForeignKey(Ejercicios, on_delete=models.CASCADE, related_name='rel_atributos')
    subatributo = models.ForeignKey(SubOpcionAtributo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ejercicio.nombre} - {self.subatributo}"

'''
@ ==================== Entrenamientos y Ejercicios ====================
'''
class EntrenamientosEjercicios(models.Model):
    """Relación N:M entre Entrenamientos y Ejercicios"""
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

'''
@ ==================== Ejercicios y Grupos Musculares ====================
'''
class EjerciciosGruposMusculares(models.Model):
    """Relación N:M entre Ejercicios y Grupos Musculares"""
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

    def __str__(self):
        return f"{self.ejercicio.nombre} - {self.grupo_muscular.nombre} ({self.nivel_enfoque})"

'''
@ ==================== Ejercicios y Equipamiento ====================
'''
class EjerciciosEquipamiento(models.Model):
    """Relación N:M entre Ejercicios y Equipamiento"""
    ejercicio = models.ForeignKey(Ejercicios, on_delete=models.CASCADE)
    equipamiento = models.ForeignKey(Equipamiento, on_delete=models.CASCADE)
    es_obligatorio = models.BooleanField(default=True)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        obligatorio = "Obligatorio" if self.es_obligatorio else "Opcional"
        return f"{self.ejercicio.nombre} - {self.equipamiento.nombre} ({obligatorio})"






'''
@ ==================== Multimedia de Ejercicios ====================
'''
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
    
    def __str__(self):
        return f"{self.ejercicio.nombre} - {self.tipo} - {self.titulo}"


