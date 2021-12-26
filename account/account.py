from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4
import json
import random


# Класс ошибки неидентичности валют
class CurrencyMismatchError(ValueError):
    pass


@dataclass
# Объявление классса Аккаунт (его тела)и его полей - их типы
class Account:
    id_: Optional[UUID]
    currency: str
    balance: Decimal
# Это все часть домашнего задания2
    #    def save(self):
    #       if no_id_then_save, then assign_id_
    #        ...
    #   def get_objects(self):
    #       ...
    #   def delete(self):
    #        ...

    # Инструкция для проверки баланса аккаунтов с условным оператором по признаку совпадения валюты
    def __lt__(self, other: "Account") -> bool:
        assert isinstance(other, Account)
        if self.currency != other.currency:
            raise CurrencyMismatchError
        return self.balance < other.balance

    def to_json(self) -> str:
        json_repr = {
            "id": str(self.id_),
            "currency": self.currency,
            "balance": float(self.balance),
        }
        return json.dumps(json_repr)

    # Метод который генерирует объекты
    @classmethod
    def from_json(cls, json_str) -> "Account":  # Factory
        obj = json.loads(json_str)
        return Account(
            id_=UUID(obj["id"]),
            currency=obj["currency"],
            balance=Decimal(obj["balance"]),
        )

    # Метод который генерирует объекты с рандомным балансом от 1 до 1000
    @classmethod
    def random(cls) -> "Account":   # Factory
        return Account(
            id_=uuid4(),
            currency="KZT",
            balance=Decimal(random.randint(1, 1000)),
        )
