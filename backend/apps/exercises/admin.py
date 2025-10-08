from django.contrib import admin
from .models import (
    CategoriasEjercicios,
    GruposMusculares,
    Equipamiento,
    Ejercicios,
    EntrenamientosEjercicios,
    EjerciciosGruposMusculares,
    EjerciciosEquipamiento,
    Multimedia
)

admin.site.register(CategoriasEjercicios)
admin.site.register(GruposMusculares)
admin.site.register(Equipamiento)
admin.site.register(Ejercicios)
admin.site.register(EntrenamientosEjercicios)
admin.site.register(EjerciciosGruposMusculares)
admin.site.register(EjerciciosEquipamiento)
admin.site.register(Multimedia)
