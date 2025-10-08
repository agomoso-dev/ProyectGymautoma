from django.contrib import admin
from .models import (
    Objetivo, 
    Estado, 
    Perfil, 
    PerfilEstado,
    ConfiguracionUsuario, 
    LesionesRestricciones
)

admin.site.register(Objetivo)
admin.site.register(Estado)
admin.site.register(Perfil)
admin.site.register(PerfilEstado)
admin.site.register(ConfiguracionUsuario)
admin.site.register(LesionesRestricciones)
