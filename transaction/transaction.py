import json
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID, uuid4
import random

from account.account import CurrencyMismatchError


# Объявление классса Транзакции (его тела)и его полей - их типы
@dataclass
class Transaction:
    id_: UUID
    source_account: UUID
    target_account: UUID
    balance_brutto: Decimal
    balance_netto: Decimal
    currency: str
    status: str

# Инструкция для проверки баланса аккаунтов с условным оператором по признаку совпадения валюты
    def __lt__(self, other: "Transaction") -> bool:
        assert isinstance(other, Transaction)
        if self.currency != other.currency:
            raise CurrencyMismatchError
        return self.balance_brutto < other.balance_brutto or self.balance_netto <= other.balance_netto

    def tr_to_json(self) -> str:
        json_repr = {
            "id": str(self.id_),
            "source_id": str(self.source_account),
            "target_id": str(self.target_account),
            "balance_brut": float(self.balance_brutto),
            "balance_net": float(self.balance_netto),
            "currency": self.currency,
            "status": self.status,
        }
        return json.dumps(json_repr)

    # Метод который генерирует объекты
    @classmethod
    def tr_from_json(cls, json_str: str) -> "Transaction":   #Factory
        obj = json.loads(json_str)
        return Transaction(
            id_=UUID(obj["id"]),
            source_account=UUID(obj["source_id"]),
            target_account=UUID(obj["target_id"]),
            balance_brutto=Decimal(obj["balance_brut"]),
            balance_netto=Decimal(obj["balance_net"]),
            currency=obj["currency"],
            status=obj["status"],
        )

    @classmethod
    def random(cls) -> "Transaction":   # Factory
        return Transaction(
            id_=uuid4(),
            source_account=uuid4(),
            target_account=uuid4(),
            balance_brutto=Decimal(random.randint(501, 1000)),
            balance_netto=Decimal(random.randint(1, 500)),
            currency="KZT",
            status="Approved",
        )

