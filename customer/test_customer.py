from decimal import Decimal
from uuid import uuid4

from account.account import Account
from customer.customer import Customer


class TestCustomer:
    def test_two_plus_two(self) -> None:
        assert 2 + 2 == 4

        # Ниже указали какие данные к какому полю относятся
        # Мы хотим задать кастомеру что он правильно работает, где казали поля  и данные к ним
    def test_customer_create(self) -> None:
        customer_id = uuid4()
        customer = Customer(
            id_=customer_id,
            first_name="Askar",
            last_name="Mukushev",
            age=24,
            accounts=[],
        )

        # Создадим такого же идентичного кастомера
        customer2 = Customer(
            id_=customer_id,
            first_name="Askar",
            last_name="Mukushev",
            age=24,
            accounts=[],
        )

        # Проверка создался ли кастомер
        assert customer.id_ == customer_id
        assert customer.first_name == "Askar"
        assert customer.last_name == "Mukushev"
        # Обязательная проверка что элемент который мы создали явяляется типом Кастомер
        assert isinstance(customer, Customer)
        # Проверка идентичности двух кастомеров
        assert customer == customer2
        # Проверка неидентичности айдишников двух кастомеров
        assert id(customer) != id(customer2)

        '''Проверка на разницу в размере(возраст, имя или фамилия в алфавитном порядке) 
         - инструкция к проверке в кастомере)'''
        assert customer < customer2

    def test_customer_with_accounts(self) -> None:
        account1_id = uuid4()
        account2_id = uuid4()
        account1 = Account(
            id_=account1_id,
            currency="KZT",
            balance=Decimal(1000),
        )
        account2 = Account(
            id_=account2_id,
            currency="KZT",
            balance=Decimal(500),
        )