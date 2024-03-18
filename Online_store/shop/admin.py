from django.contrib import admin
from .models import Category,Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    # поля которые мы выводим в администратор
    prepopulated_fields = {'slug':('name',)}
    # Мы используем атрибут prepopulated_fields, чтобы указать поля в которых
    # значение автоматически задается с использованием значения других полей

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','slug','price','available','created','updated']
    # поля которые мы выводим в администратор

    list_filter = ['available','created','updated']
#!!!# не очень понял зачем создали отдельно

    list_editable = ['price','available']
    # используется для задания полей, которые могут быть отредактированы
    # на странице отображения списка сайта администрирования
    # Это позволит редактировать несколько строк одновременно.
    # Любое поле в list_editable также должно быть указано в атрибуте list_display,
    # поскольку могут быть изменены только отображаемые поля.

    prepopulated_fields = {'slug':('name',)}
    # Мы используем атрибут prepopulated_fields, чтобы указать поля в которых
    # значение автоматически задается с использованием значения других полей


