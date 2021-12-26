from dataclasses import  dataclass
from typing import List
from uuid import UUID


@dataclass
# Объявление классса Кастомер (его тела)и его полей - их типы
class Customer:
    id_: UUID
    age: int
    first_name: str
    last_name: str
    accounts: List[UUID]

    # Инструкция для проверки возраста или фамилии или имени
    def __lt__(self, other) -> bool:
        return self.age < other.age or self.last_name < other.last_name or self.first_name <= other.first_name


# Старый код
#    def __str__(self):
#        return f"Customer: {self.last_name} {self.first_name}"

# Старый код
'''
    def __init__(self, id_, age, first_name, last_name):
        self.id_ = id_
        self.age = age
        self.first_name = first_name
        self.last_name = last_name
'''

