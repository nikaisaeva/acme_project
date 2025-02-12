# Импортируем настройки проекта.
from django.conf import settings

# Добавьте новые строчки с импортами классов.
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

# Импортируем функцию, позволяющую серверу разработки отдавать файлы.
from django.conf.urls.static import static
# Импортируем информацию из настроек.
from django.conf import settings

from django.contrib import admin
from django.urls import include, path
# К импортам из django.urls добавьте импорт функции reverse_lazy
from django.urls import include, path, reverse_lazy

urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('birthday/', include('birthday.urls')),
    # Подключаем urls.py приложения для работы с пользователями.
    path('auth/', include('django.contrib.auth.urls')),
    # Создание нового объекта в модели регистрации нового пользователя
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('pages:homepage'),
        ),
        name='registration',
    ),
# В конце добавляем к списку вызов функции static.
]

# Если проект запущен в режиме разработки...
if settings.DEBUG:
    import debug_toolbar
    # Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

# Подключаем функцию static() к urlpatterns:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.page_not_found'