from decimal import Decimal
from uuid import uuid4, UUID

import pytest
import json

from account.account import Account, CurrencyMismatchError


class TestAccount:
    def test_account_create(self) -> None:
        # Первый аккаунт и его данные
        account = Account(
            id_=uuid4(),
            currency="KZT",
            balance=Decimal(10),
        )

        # Обязательная проверка что элемент который мы создали явяляется типом Account
        assert isinstance(account, Account)
        # Проверка что баланс == 10
        assert account.balance == 10

        # Второй аккаунт и его данные
        account2 = Account(
            id_=uuid4(),
            currency="KZT",
            balance=Decimal(5),
        )

        # Проверка что у второго аккаунта баланс больше чем у первого при инструкции(в Аккаунт)с учетмо валюты
        assert account2 < account

    # Блок с ошибкой по валютам, ниже обработчик пропустит, так как разные валюты при инструкции
    def test_errors(self) -> None:
        account = Account(
            id_=uuid4(),
            currency="KZT",
            balance=Decimal(10),
        )

        account2 = Account(
            id_=uuid4(),
            currency="USD",
            balance=Decimal(5),
        )
        # Обрабатываем с инструкцией по проверки величины валюты
        with pytest.raises(CurrencyMismatchError):
            assert account2 < account

    # Блок конвертации данных в джейсон формат и обратно
    def test_json_import_export(self) -> None:
        account_id = uuid4()
        account = Account.random()

        json_account = account.to_json()
        assert json.loads(json_account) == {
            "id": str(account.id_),
            "currency": "KZT",
            "balance": account.balance,
        }
        # print(json_account)

    def test_account_from_json(self) -> None:
        test_json = '{"id": "f1972d7f-9dcd-4d72-8263-f2c920ae14a9", "currency": "KZT", "balance": 10.0}'

        account = Account.from_json(test_json)
        assert isinstance(account, Account)
        assert account.id_ == UUID("f1972d7f-9dcd-4d72-8263-f2c920ae14a9")
        assert account.balance == Decimal(10)
        assert account.currency == "KZT"

    # Заключительная проверка между конвертациями данных в джейсон и обратно,

    def test_to_json_from_json(self) -> None:
        account = Account.random()
        account2 = Account.from_json(account.to_json())
        assert account2 == account
