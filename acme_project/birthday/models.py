from django.db import models

# Импортируется функция-валидатор.
from .validators import real_age

# Импортируем функцию reverse() для получения ссылки на объект.
from django.urls import reverse

from django.contrib.auth import get_user_model

# Да, именно так всегда и ссылаемся на модель пользователя!
User = get_user_model()

class Tag(models.Model):
    tag = models.CharField('Тег', max_length=20)

    # Переопределяем метод:
    def __str__(self):
        return self.tag

class Birthday(models.Model):
    first_name = models.CharField('Имя',
                                  max_length=20)
    last_name = models.CharField(
        'Фамилия',
        blank=True,
        help_text='Необязательное поле',
        max_length=20
    )
    birthday = models.DateField('Дата рождения',
                                validators=(real_age,))
    image = models.ImageField('Фото',
                              #Директория для загрузки файлов этого поля
                              # Директория с таким названием будет создана в папке, указанной в настройках MEDIA_ROOT
                              upload_to='birthdays_images',
                              blank=True)
    constraints = (
            models.UniqueConstraint(
            # Проверка на уникальность. Указываются поля сочетания которых не должны повторяться
                fields=('first_name', 'last_name', 'birthday'),
                name='Unique person constraint',
            ),
    )
    author = models.ForeignKey(
        User, verbose_name='Автор записи', on_delete=models.CASCADE, null=True
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        blank=True,
        help_text='Удерживайте Ctrl для выбора нескольких вариантов'
    )
 
    class Meta:
        verbose_name = 'День рождения'
        verbose_name_plural = 'Дни рождения'
    def get_absolute_url(self):
    # С помощью функции reverse() возвращаем URL объекта.
        return reverse('birthday:detail', kwargs={'pk': self.pk})

# Модель для поздравлений
class Congratulation(models.Model):
    text = models.TextField('Текст поздравления')
    birthday = models.ForeignKey(
        Birthday, 
        on_delete=models.CASCADE,
        related_name='congratulations',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)
