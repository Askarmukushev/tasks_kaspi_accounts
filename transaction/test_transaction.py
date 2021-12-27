from decimal import Decimal
from uuid import uuid4, UUID

import pytest
import json

from account.account import CurrencyMismatchError
from transaction.transaction import Transaction


class TestTransaction:
    def test_account_create(self) -> None:
        # Первая транзакция и ее данные
        transaction = Transaction(
            id_=uuid4(),
            source_account=uuid4(),
            target_account=uuid4(),
            balance_brutto=Decimal(20),
            balance_netto=Decimal(15),
            currency="KZT",
            status="Approved",
        )

        # Обязательная проверка что элемент который мы создали явяляется типом Transaction
        assert isinstance(transaction, Transaction)
        # Проверка что баланс == 10
        assert transaction.balance_brutto == 20 and transaction.balance_netto == 15
        print(transaction.balance_brutto, transaction.balance_netto)

        # Вторая транзакция и ее данные
        transaction2 = Transaction(
            id_=uuid4(),
            source_account=uuid4(),
            target_account=uuid4(),
            balance_brutto=Decimal(40),
            balance_netto=Decimal(33),
            currency="KZT",
            status="Approved",
        )

        '''Проверка что у второго аккаунта транзакция баланса меньше чем у первого 
        при инструкции(в Аккаунт)с учетмо валюты'''
        assert transaction < transaction2

# Блок с ошибкой по валютам, ниже обработчик пропустит, так как разные валюты при инструкции
    def test_transaction_error(self) -> None:
        transaction = Transaction(
            id_=uuid4(),
            source_account=uuid4(),
            target_account=uuid4(),
            balance_brutto=Decimal(20),
            balance_netto=Decimal(15),
            currency="KZT",
            status="Approved",
        )

        transaction2 = Transaction(
            id_=uuid4(),
            source_account=uuid4(),
            target_account=uuid4(),
            balance_brutto=Decimal(40),
            balance_netto=Decimal(33),
            currency="USD",
            status="Approved",
        )

        # Обрабатываем с инструкцией по проверки величины валюты
        with pytest.raises(CurrencyMismatchError):
            assert transaction2 < transaction

    # Блок конвертации данных в джейсон формат и обратно, с данными Транзакции с блока рандомизации
    def test_json_imp_exp_tr(self) -> None:
        transaction=Transaction.random()

        json_transaction = transaction.tr_to_json()
        assert json.loads(json_transaction) == {
            "id": str(transaction.id_),
            "source_id": str(transaction.source_account),
            "target_id": str(transaction.target_account),
            "balance_brut": transaction.balance_brutto,
            "balance_net": transaction.balance_netto,
            "currency": "KZT",
            "status": "Approved",
        }
        print(json_transaction)

    def test_transaction_from_json(self) -> None:
        test_json = '{"id": "dbf4b9f1-7b1b-4c9a-8dff-36ade14dc48a", "source_id": "85085e23-e46d-487a-a447-d3a6d91a0177", "target_id": "116dd660-9192-4907-a3c6-73e1c1ee4204", "balance_brut": 20.0, "balance_net": 15.0, "currency": "KZT", "status": "Approved"}'
        transaction = Transaction.tr_from_json(test_json)
        assert isinstance(transaction, Transaction)
        assert transaction.id_ == UUID("dbf4b9f1-7b1b-4c9a-8dff-36ade14dc48a")
        assert transaction.source_account == UUID("85085e23-e46d-487a-a447-d3a6d91a0177")
        assert transaction.target_account == UUID("116dd660-9192-4907-a3c6-73e1c1ee4204")
        assert transaction.balance_brutto == Decimal(20)
        assert transaction.balance_netto == Decimal(15)
        assert transaction.currency == "KZT"
        assert transaction.status == "Approved"

    # Заключительная проверка между конвертациями данных в джейсон и обратно,
    def test_to_json_from_json(self) -> None:
        transaction = Transaction.random()
        transaction2 = Transaction.tr_from_json(transaction.tr_to_json())
        assert transaction2 == transaction

