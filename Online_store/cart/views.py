from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


# Декоратор, который указывает, что представление может быть вызвано только с помощью HTTP-метода POST,
# обеспечивая, что данные можно добавить в корзину только через POST-запрос
# Это представление для добавления продуквато в корзину или обновления количества для существующих продуктов
@require_POST
def cart_add(request, product_id):
    # функция принимает объект запроса request и идентификатор продукта product_id в качестве параметров.

    cart = Cart(request)
    # Создание экземпляра класса Cart, который представляет корзину пользователя.

    product = get_object_or_404(Product, id=product_id)
    # Получение объекта продукта с соответствующим product_id или возврат
    # HTTP-ответа 404, если такой продукт не найден.

    form = CartAddProductForm(request.POST)
    # Создание экземпляра формы CartAddProductForm, привязывая к ней данные POST-запроса.

    if form.is_valid():
        # Проверка формы на валидность. Если форма заполнена корректно,
        # происходит переход к следующим шагам.

        cd = form.cleaned_data
        # Получение "очищенных" данных формы, то есть данных, которые
        # были проверены и преобразованы к соответствующим Python-типам.

        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
        # Вызов метода add объекта корзины для добавления или обновления количества продукта. Передача
        # объекта продукта, выбранного количества и указания, следует ли обновить количество продукта в корзине.

        return redirect('cart:cart_detail')
        # Перенаправление пользователя на URL с именем 'cart_detail'




# слайд 33
# получает id продукта в качестве параметра, мы извлекаем продукт с заданным id и удаляем его из корзины,
# затем перенапрявляем пользователя на URL адрес cart_detail.
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'update': True})

    return render(request, 'cart/detail.html',{'cart':cart})


# сайд 36
# кнопка "добавить в корзину"
def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product':product,
                   'cart_product_form': cart_product_form})





