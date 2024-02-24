# Импортируем классы CBV
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
# Ипмортируем функцию возращения на страницу после удаления объекта
from django.urls import reverse_lazy, reverse

# Импортируем класс BirthdayForm, чтобы создать экземпляр формы.
from .forms import BirthdayForm, CongratulationForm

# Импортируем модель
from .models import Birthday, Congratulation

# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown

# Импорт миксина декоратора
from django.contrib.auth.mixins import LoginRequiredMixin

# import get_object_or_404()
from django.shortcuts import get_object_or_404, redirect

# импорты для функции поздравления


# Наследуем класс от встроенного ListView:
class BirthdayListView(ListView):
    """Функция отображает список записей"""
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # По умолчанию этот класс 
    # выполняет запрос queryset = Birthday.objects.all(),
    # но мы его переопределим:
    queryset = Birthday.objects.prefetch_related('tags').select_related('author')
    # ...сортировку, которая будет применена при выводе списка объектов:
    ordering = 'id'
    # ...и даже настройки пагинации:
    paginate_by = 10


class BirthdayCreateView(LoginRequiredMixin, CreateView):
    """Функция создания записи"""
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # Этот класс сам может создать форму на основе модели!
    # Указываем имя формы:
    form_class = BirthdayForm

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)


class BirthdayUpdateView(LoginRequiredMixin, UpdateView):
    """"Функция редактирования записи"""
    model = Birthday
    # Этот класс сам может создать форму на основе модели!
    # Указываем имя формы:
    form_class = BirthdayForm

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект по первичному ключу и автору или вызываем 404 ошибку.
        get_object_or_404(Birthday, pk=kwargs['pk'], author=request.user)
        # Если объект был найден, то вызываем родительский метод,
        # чтобы работа CBV продолжилась.
        return super().dispatch(request, *args, **kwargs)


class BirthdayDeleteView(LoginRequiredMixin, DeleteView):
    """Функция удаления записи"""
    model =Birthday
    # Указываем namespace:name страницы, куда будет перенаправлен пользователь
    # после удаления объекта:
    success_url = reverse_lazy('birthday:list')

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект по первичному ключу и автору или вызываем 404 ошибку.
        get_object_or_404(Birthday, pk=kwargs['pk'], author=request.user)
        # Если объект был найден, то вызываем родительский метод,
        # чтобы работа CBV продолжилась.
        return super().dispatch(request, *args, **kwargs)


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
        # Записываем в переменную form пустой объект формы.
        context['form'] = CongratulationForm()
        # Запрашиваем все поздравления для выбранного дня рождения.
        context['congratulations'] = (
            # Дополнительно подгружаем авторов комментариев,
            # чтобы избежать множества запросов к БД.
            self.object.congratulations.select_related('author')
        )
        # Возвращаем словарь контекста.
        return context


class CongratulationCreateView(LoginRequiredMixin, CreateView):
    birthday = None
    model = Congratulation
    form_class = CongratulationForm

    # Переопределяем dispatch()
    def dispatch(self, request, *args, **kwargs):
        self.birthday = get_object_or_404(Birthday, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    # Переопределяем form_valid()
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.birthday = self.birthday
        return super().form_valid(form)

    # Переопределяем get_success_url()
    def get_success_url(self):
        return reverse('birthday:detail', kwargs={'pk': self.birthday.pk})

