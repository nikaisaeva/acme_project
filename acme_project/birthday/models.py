from django.db import models

# Импортируется функция-валидатор.
from .validators import real_age

# Импортируем функцию reverse() для получения ссылки на объект.
from django.urls import reverse

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
    
    class Meta:
        verbose_name = 'День рождения'
        verbose_name_plural = 'Дни рождения'
    def get_absolute_url(self):
    # С помощью функции reverse() возвращаем URL объекта.
        return reverse('birthday:detail', kwargs={'pk': self.pk})
