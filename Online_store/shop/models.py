from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    # создание столбца в базе данных с именем name
    # присвоение name значение CharField (текстовое значение)
    # (max_length=200) задает максимальное значение 200 символов
    # (db_index=True) создает индекс в базе данных по этому полю

    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    # создание столбца в базе данных с именем slug
    # !!!# присвоение slug значение SlugField предназначенных для хранения коротних меток
    # (max_length=200) задает максимальное значение 200 символов
    # (db_index=True) создает индекс в базе данных по этому полю
    # (unique=True) следит за уникальностью каждой ячейки в таблице

    class Meta:
        # Вложенный класс Meta определяет дополнительные параметры модели Category.

        ordering = ('name',)
        # ordering создание сортировки объектов по полю 'name' в алфавитном
        # порядке при запросах к базе данных. Кортеж с одним элементом указывает
        # на то, что сортировка будет выполняться по возрастанию.
        # Если бы перед 'name' стоял знак минус (например, '-name'),
        # сортировка происходила бы по убыванию.

        verbose_name = 'Categories'
        # verbose_name Устанавливает человекочитаемое имя для одного
        # объекта модели, которое будет использоваться в интерфейсе
        # администратора Django. В данном случае для одной категории будет
        # показано слово "Категория".

        verbose_name_plural = 'Categories'
        # аналогично verbose_name

    def __str__(self):
        return self.name
    # Определение магического метода __str__
    # в Django использует для отображения объекта
    # модели в виде строки удобной для чтения.

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])



class Product(models.Model):
    # Определение класса Product, наследующего
    # от models.Model, что делает его моделью базы данных в Django.

    category = models.ForeignKey(Category, related_name='products',on_delete=models.CASCADE)
    #  ForeignKey связывающее продукты с категорией
    #  Это создаёт отношение "многие к одному" между продуктами и категориями
    #  related_name='products' позволяет обращаться к продуктам из объекта категории

    name = models.CharField(max_length=200, db_index=True)
    # Поле name является строковым полем
    # (CharField) с максимальной длиной 200 символов и индексированием в базе данных
    # db_index=True для более быстрого поиска по этому полю.

    slug = models.SlugField(max_length=200, db_index=True)
    # Поле slug использует SlugField, который  ограничен 200 символами и индексирован
    # Оно предназначено для использования в URL-адресах и
    # должно быть уникальным для каждого продукта
    # это URL продукта

    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    # Поле image определено как ImageField который используется для загрузки изображений
    # upload_to задаёт путь  для сохранения изображений и blank=True
    # позволяет полю быть пустым

    description = models.TextField(blank=True)
    # Поле description определено как TextField, которое может хранить
    # более длинный текст и может быть пустым (blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Поле price является десятичным полем (DecimalField) с максимальным
    # количеством цифр 10 и 2 знаками после запятой, что подходит для представления цен

    stock = models.PositiveIntegerField()
    # Поле stock представляет собой положительное целое число (PositiveIntegerField)
    # что может использоваться для хранения количества товара на складе

    available = models.BooleanField(default=True)
    # Поле available — это булево поле (BooleanField) с значением по умолчанию True
    # которое можно использовать для отслеживания доступности продукта

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Поля created и updated используют DateTimeField для отслеживания времени
    # создания и последнего обновления продукта соответственно.
    # auto_now_add=True устанавливает дату и время при создании объекта
    # auto_now=True — при каждом обновлении объекта.

    class Meta:
        # Вложенный класс Meta определяет дополнительные параметры модели Product.

        ordering = ('name',)
        # указывает на сортировку по имени продукта.

        index_together = (('id', 'slug'),)
#!!!!!!!# Указывает на создание составного индекса для полей id и slug,
#!!!!!!!# что может улучшить производительность при выполнении запросов,
#!!!!!!!# включающих оба эти поля.
    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])
