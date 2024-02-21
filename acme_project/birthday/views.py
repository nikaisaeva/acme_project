# Импортируем классы CBV
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
# Ипмортируем функцию возращения на страницу после удаления объекта
from django.urls import reverse_lazy

# Импортируем класс BirthdayForm, чтобы создать экземпляр формы.
from .forms import BirthdayForm

# Импортируем модель
from .models import Birthday

# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown


# Наследуем класс от встроенного ListView:
class BirthdayListView(ListView):
    """Функция отображает список записей"""
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # ...сортировку, которая будет применена при выводе списка объектов:
    ordering = 'id'
    # ...и даже настройки пагинации:
    paginate_by = 10


class BirthdayCreateView(CreateView):
    """Функция создания записи"""
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # Этот класс сам может создать форму на основе модели!
    # Указываем имя формы:
    form_class = BirthdayForm


class BirthdayUpdateView(UpdateView):
    """"Функция редактирования записи"""
    model = Birthday
    # Этот класс сам может создать форму на основе модели!
    # Указываем имя формы:
    form_class = BirthdayForm


class BirthdayDeleteView(DeleteView):
    """Функция удаления записи"""
    model =Birthday
    # Указываем namespace:name страницы, куда будет перенаправлен пользователь
    # после удаления объекта:
    success_url = reverse_lazy('birthday:list')


class BirthdayDetailView(DetailView):
    """"Функция отображения отдельной записи"""
    model = Birthday

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['birthday_countdown'] = calculate_birthday_countdown(
            # Дату рождения берём из объекта в словаре context:
            self.object.birthday
        )
        # Возвращаем словарь контекста.
        return context
