from django.shortcuts import render, get_object_or_404
# Импортируются функция render, которая соединяет данные с шаблоном и возвращает HTTP-ответ
# функция get_object_or_404, которая пытается получить объект по
# заданным критериям или возвращает HTTP 404, если объект не найден.

from .models import Category, Product



# Импортируются модели Category и Product для использования в этой функции.


def product_list(request, category_slug=None):
    # Эта функция используется для обработки HTTP-запросов на просмотр списка продуктов
    # request и необязательный аргумент category_slug, по умолчанию равный None.

    category = None
    # !!!# Инициализация переменной category значением None
    # !!!# которая будет использоваться для хранения категории, если таковая найдется.
    # !!!# это если вдруг не будет категории??

    categories = Category.objects.all()
    # Получение всех объектов Category из базы данных.

    products = Product.objects.filter(available=True)
    # Получение всех доступных (available=True) объектов Product.

    if category_slug:
        # Проверка, был ли передан category_slug в функцию.

        category = get_object_or_404(Category, slug=category_slug)
        # Если category_slug был предоставлен, попытка найти объект Category с
        # соответствующим slug. Если категория не найдена, будет возвращён ответ HTTP 404.

        products = products.filter(category=category)
        # Если категория найдена, дальнейшая фильтрация списка продуктов по этой категории.

    return render(request,
                  'shop/product/list.html',
                  {'catagory': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    # request (объект запроса HTTP)
    # id (числовой идентификатор продукта)
    # slug (слаг продукта, используемый для SEO-оптимизированных URL).

    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    # Вызов функции get_object_or_404, которая попытается получить объект Product
    # с указанными id и slug, а также у которого свойство available равно True.
    # Если объект не найден, будет возвращён HTTP-ответ 404 (страница не найдена).

    #cart_product_form = CartAddProductForm()
#!!!# Создание экземпляра формы CartAddProductForm
    # не понимаю что это

    return render(request,
                  'shop/product/detail.html',
                  {'product':product,})
                   #'cart_product_form':cart_product_form})