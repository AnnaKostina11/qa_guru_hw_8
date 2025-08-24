"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(product.quantity) is True # запрашиваемое равно доступному количеству
        assert product.check_quantity(product.quantity - 1) is True # запрашиваемое на 1 меньше доступного количества
        assert product.check_quantity(product.quantity + 1) is False # запрашиваемое на 1 больше доступного количества
        assert product.check_quantity(0) is True # запрашиваем 0 товаров

    def test_product_buy(self, product):
       # TODO напишите проверки на метод buy
       available_quantity = product.quantity
       quantity = product.quantity - 1 # покупаем меньше на 1, чем доступно
       product.buy(quantity)
       assert product.quantity == available_quantity - quantity

       available_quantity = product.quantity
       quantity = product.quantity # кол-во покупки = кол-ву доступного
       product.buy(quantity)
       assert product.quantity == available_quantity - quantity


    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        available_quantity = product.quantity
        quantity = product.quantity + 1 # покупаем больше на 1, чем доступно
        with pytest.raises(ValueError) as e:
            product.buy(quantity)
        assert product.quantity == available_quantity and "Не хватает продуктов" in str(e.value)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    @pytest.fixture
    def cart(self):
        return Cart()

    def test_cart_add_one_product(self, product, cart):
        cart.add_product(product, 1)  # добавляем 1 продукт в корзину
        assert cart.products[product] == 1 # проверяем, что в корзине 1 товар

    def test_cart_add_products(self, product, cart):
        cart.add_product(product, 4)  # добавляем 4 продукта в корзину
        assert cart.products[product] == 4 # проверяем, что в корзине 4 товара

    def test_cart_add_identical_products(self, product, cart):
        cart.add_product(product, 1) # добавляем 1 продукт в корзину
        cart.add_product(product, 9) # добавляем 9 продуктов в корзину
        assert cart.products[product] == 10 # проверяем, что в корзине 10 одинаковых продуктов

    def test_cart_remove_one_product(self, product, cart):
        cart.add_product(product, 10)
        cart.remove_product(product, 1) # удаляем 1 продукт из корзины
        assert cart.products[product] == 9 # проверяем, что осталось 9

    def test_cart_remove_all_product(self, product, cart):
        cart.add_product(product, 10)
        cart.remove_product(product)  # удаляем без указания количества
        assert product not in cart.products  # проверяем, что корзина пустая

    def test_cart_remove_more_products(self, product, cart):
        cart.add_product(product, 10)
        cart.remove_product(product, 11)  # удаляем больше, чем в корзине
        assert product not in cart.products  # проверяем, что корзина пустая

    def test_cart_remove_same_number_products(self, product, cart):
        cart.add_product(product, 10)
        cart.remove_product(product, 10)  # удаляем кол-во = кол-ву в корзине
        assert product not in cart.products  # проверяем, что корзина пустая

    def test_cart_clear(self, product, cart):
        cart.add_product(product, 100) # добавляем 100 в корзину
        cart.clear() # очищаем корзину
        assert product not in cart.products

    def test_cart_get_total_price(self, product, cart):
        cart.add_product(product, 1)
        cart.add_product(product, 2)
        cart.add_product(product, 8)
        assert cart.get_total_price() == product.price * 1 + product.price * 2 + product.price * 8 # стоимость корзины = стоимость всех товаров


    def test_cart_buy(self, product, cart):
        product.quantity = 5
        cart.add_product(product, 10)  # покупаем больше, чем есть
        with pytest.raises(ValueError):
            cart.buy()