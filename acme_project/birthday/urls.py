from django.urls import path

from . import views

app_name = 'birthday'

urlpatterns = [
    # создание формы
    path('', views.BirthdayCreateView.as_view(), name='create'),
    # отображение списка объектов
    path('list/', views.BirthdayListView.as_view(), name='list'),
    # класс для отображения отдельных объектов
    path('<int:pk>/', views.BirthdayDetailView.as_view(), name='detail'),
    # маршрут формы для редактирования
    path('<int:pk>/edit/', views.BirthdayUpdateView.as_view(), name='edit'),
    # добавляем маршрут для удаления формы
    path('<int:pk>/delete/', views.BirthdayDeleteView.as_view(), name='delete'),
]
