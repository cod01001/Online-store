from decimal import Decimal
# Импорт класса Decimal из модуля decimal, который обеспечивает точное
# десятичное арифметическое вычисление.

from django.conf import settings
# Импорт модуля settings из Django, который содержит настройки проекта.

from shop.models import Product
# Импорт класса Product из модуля models в приложении shop.

class Cart(object):
# Это класс Cart который позволит нам управлять корзиной для покупок. Требуется инициализация
# корзины с помощъю объекта request. Мы храним текущую сессию с помощью self.session=request.session
# чтобы сделать его доступным для других методв класса Cart. Во-первых, мы хотим пытаться получить корзину,
# то мы создадим сессию с пустой корзиной, установив пустой словарь в сессиию. Мы ожидаем, что наш словарь
# корзина, будет использовать коды продуктов в качестве ключей и словарь с количеством и ценой в качестве
# значения для каждого ключаю Таким образом, мы можем гарантировать, что не будет добавлен в карзину более
# одного раза, можнго также упростить доступ к данным элементов корзины

    def __init__(self, request):
        # Этот метод вызывается при создании нового экземпляра Cart. Он принимает self,
        # который представляет экземпляр класса, и request, который является объектом запроса Django.
        """
        Initialize the cart.
        """

        self.session = request.session
        # Присваивает свойству session текущего объекта Cart сессию из объекта request.
        # Сессия используется для хранения данных между запросами.

        cart = self.session.get(settings.CART_SESSION_ID)
        # Пытается получить данные корзины из сессии, используя идентификатор корзины,
        # который должен быть определен в настройках (settings.CART_SESSION_ID).

        if not cart:
            # Если корзина не найдена в сессии (т.е., cart равен None или False),
            # создается новая пустая корзина и сохраняется в сессии.
            # save an empty cart in the session

            cart = self.session[settings.CART_SESSION_ID] = {}
            # Создается новый пустой словарь в сессии для хранения данных корзины.

        self.cart = cart
        # Присваивает только что полученные или созданные данные корзины свойству cart текущего объекта Cart.

    def __iter__(self):
        # делает экземпляр Cart итерируемым.

        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()
        # Получает все ключи из словаря cart (которые являются ID продуктов).
        # get the product objects and add them to the cart

        products = Product.objects.filter(id__in=product_ids)
        # Запрашивает из базы данных все объекты Product, чьи ID соответствуют ключам, полученным из словаря cart.
        # почему 2 нижних подчеркивания: В Django ORM двойное нижнее подчёркивание используется для доступа к опциям
        # фильтрации, которые называются "lookups". Lookups позволяют проводить более сложные запросы к базе данных,
        # чем простое сравнение.

        cart = self.cart.copy()
        # Создает копию текущего словаря cart, чтобы можно было модифицировать копию, не затрагивая оригинал.

        for product in products:
            cart[str(product.id)]['product'] = product
            # Цикл for добавляет в копию корзины каждый объект Product, соответствующий ID из корзины.
            # Преобразует ID продукта в строку, использует его как ключ в словаре и
            # устанавливает соответствующий объект Product в словарь.

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
        # цикл for проходит по всем значениям словаря cart (которые теперь включают объекты Product).
        # Сначала преобразует строковую цену в Decimal, чтобы обеспечить точность арифметики.
        # Затем вычисляет общую стоимость позиции как произведение цены и количества.
        # Использует ключевое слово yield, чтобы возвращать каждый элемент как
        # генератор, что позволяет итерироваться по элементам корзины по одному.

    def __len__(self):
        # Определяется специальный метод __len__, который позволяет объекту
        # Python поддерживать встроенную функцию len()
        # Этот метод будет вызываться, когда используеться len() на экземпляре класса Cart
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())
        # Возвращает сумму количеств каждого товара ('quantity') в корзине
        # self.cart.values() возвращает итерируемый объект со всеми значениями в словаре self.cart, где каждый элемент —
        # это словарь с данными о товаре в корзине. Генераторное выражение
        # (item['quantity'] for item in self.cart.values()) создает последовательность количеств каждого товара,
        # а функция sum() суммирует эти значения

    def get_total_price(self):
        # Определяется метод get_total_price, который не принимает никаких аргументов,
        # кроме self (ссылки на текущий экземпляр класса Cart).

        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
        # Возвращает сумму стоимости всех товаров в корзине. Для каждого товара в корзине его цена, приведенная к типу
        # Decimal, умножается на его количество, и результаты всех таких операций суммируются. Использование Decimal
        # обеспечивает точность вычислений, особенно важную при работе с финансовыми данными.

    def clear(self):
        # Определяется метод clear, который позволяет "очистить" корзину, то есть удалить все товары из неё.
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        # Удаляет корзину из сессии. Здесь self.session указывает на объект сессии, который связан с текущим
        # пользовательским запросом, и settings.CART_SESSION_ID — это ключ, по которому корзина хранится в сессии.
        # Команда del удаляет значение, связанное с этим ключом, из объекта сессии.

        self.save()
        # сохранение сессии



    def add(self,product,quantity=1,update_quantity=False):
    # Этот код управляет процессом добавления товаров в корзину покупателя и обеспечивает
    # сохранение данных корзины между различными запросами в сессии пользователя.

        """
        Add a projuct to the cart or update its quantity.
        """

        product_id = str(product.id)
        # Получает идентификатор продукта и преобразует его в строку для
        # использования в качестве ключа в словаре корзины.

        if product_id not in self.cart:
        # Проверяет, существует ли продукт с таким product_id в корзине.

            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
            # eсли продукта еще нет в корзине, создает новую запись с
            # начальным количеством 0 и ценой, преобразованной в строку.

        if update_quantity:
        # Если флаг update_quantity установлен в True, метод обновит количество продукта на указанное значение

            self.cart[product_id]['quantity'] = quantity
            # Устанавливает количество продукта в корзине равным значению параметра quantity

        else:
        # Если флаг update_quantity False, метод увеличит количество продукта в корзине на значение quantity

            self.cart[product_id]['quantity'] += quantity
            # Увеличивает количество продукта на указанное значение quantity.

        self.save()
        # Вызывает метод save, чтобы сохранить изменения в корзине.

    def save(self):
        # Определение метода save, который сохраняет корзину в сессии.
        # mark the session as "modified" to make sure it get saved
        self.session.modified = True
        # Устанавливает флаг modified текущей сессии в True, чтобы указать Django на необходимость сохранения сессии.


    def removed(self,product):
        # Определение метода removed внутри класса Cart. Этот метод принимает два параметра:
        # self — ссылка на текущий экземпляр класса Cart.
        # product — экземпляр класса Product, который необходимо удалить из корзины.

        """
        Remove a product from the cart
        """
        product_id = str(product.id)
        # Получение идентификатора продукта и его преобразование в строку,
        # чтобы использовать его в качестве ключа в словаре, который представляет корзину.

        if product_id in self.cart:
        # Проверка наличия продукта с таким product_id в корзине.

            del self.cart[product_id]
            # Если продукт существует в корзине, он удаляется из неё с использованием ключевого слова del.

            self.save()
            # После удаления продукта из корзины вызывается метод save, чтобы сохранить изменения в корзине


