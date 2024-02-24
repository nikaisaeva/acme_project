from django.contrib import admin

from .models import Birthday, Tag

# Зарегистирировали модель в админке
admin.site.register(Birthday)
admin.site.register(Tag)