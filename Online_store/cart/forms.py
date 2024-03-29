from django import forms
# Импорт модуля forms из фреймворка Django для использования классов и функций, связанных с формами

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]
# Создание списка кортежей для определения вариантов выбора количества продукта.
# Каждый кортеж содержит число и его строковое представление. range(1, 21) генерирует числа от 1 до 20

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int)

    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
