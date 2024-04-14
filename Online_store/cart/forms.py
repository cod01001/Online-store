from django import forms
# Импорт модуля forms из фреймворка Django для использования классов и функций, связанных с формами

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]
# Создание списка кортежей для определения вариантов выбора количества продукта.
# Каждый кортеж содержит число и его строковое представление. range(1, 21) генерирует числа от 1 до 20

class CartAddProductForm(forms.Form):
    # Определение класса формы CartAddProductForm, который наследуется от
    # стандартного класса формы Django — forms.Form.

    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int)
    # позволяет пользователю выбрать количество между 1-20. Мы использукм поле TypedChoiceField с coerce=int
    # для преобразования ввода в цулое число.

    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
    # позволяет указать следует ли добавлять сумму к любому существующему значению в карзине для данного продукта
    # (False) или если существующее значение должно быть обновлено с заданным значением (True). для этого
    # поля используется графический элемент HiddenInput поскольку не требуется показывать его пользователю.





















