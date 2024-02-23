from django.contrib import admin

from .models import Birthday

# Зарегистирировали модель в админке
admin.site.register(Birthday)
