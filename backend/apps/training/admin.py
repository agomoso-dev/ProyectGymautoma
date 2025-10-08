from django.contrib import admin
from .models import (
    Rutina,
    Entrenamientos,
    Series,
    LesionesEntrenamientos
)

admin.site.register(Rutina)
admin.site.register(Entrenamientos)
admin.site.register(Series)
admin.site.register(LesionesEntrenamientos)
