from uuid import uuid4

import pytest

from account.account import Account
from database.implementations.pandas_db import AccountDatabasePandas
from database.implementations.postgres_db import AccountDatabasePostgres
from database.implementations.ram import AccountDatabaseRAM
from database.database import ObjectNotFound


class TestRAMDatabase:
    def test_all_dbs(self) -> None:
        connection = "dbname = Kaspi_Tasks port=25060 user=postgres password = klnH436QFV5323 host = localhost"
        all_implementations = [AccountDatabaseRAM, AccountDatabasePandas]
        for implementation in all_implementations:
            print()
            print("------------- Now testing", implementation.__name__)
            if implementation == AccountDatabasePostgres:
                database = AccountDatabasePostgres(connection=connection)
            else:
                database = implementation()
            account = Account.random()
            account2 = Account.random()
            # Сохранить аккаунт в бд
            database.save(account)
            database.save(account2)
            got_account = database.get_object(account.id_)
            assert account == got_account

            # Проверка если мы подали неправильный айди
            with pytest.raises(ObjectNotFound):
                database.get_object(uuid4())

            if implementation == AccountDatabaseRAM:
                all_objects = database.get_objects()
                assert len(all_objects) == 2
                for acc in all_objects:
                    assert isinstance(acc, Account)

            account.currency = "USD"
            database.save(account)
            got_account = database.get_object(account.id_)
            assert account == got_account

    def a_test_all_dbs_persistence(self) -> None:
        connection = "dbname = Kaspi_Tasks port=25060 user=postgres password = klnH436QFV5323 host = localhost"
        all_implementations = [AccountDatabasePandas]

        for implementation in all_implementations:
            print()
            print("------------- Now testing persistence", implementation.__name__)
            if implementation == AccountDatabasePostgres:
                database = AccountDatabasePostgres(connection=connection)
            else:
                database = implementation()
            account = Account.random()
            account2 = Account.random()
            # Сохранить аккаунт в бд
            database.save(account)
            database.save(account2)

            database = implementation()

            got_account = database.get_object(account.id_)
            assert account == got_account

            # Проверка если мы подали неправильный айди
            with pytest.raises(ObjectNotFound):
                database.get_object(uuid4())


def test_connection() -> None:
    connection = "dbname = Kaspi_Tasks port=25060 user=postgres password = klnH436QFV5323 host = localhost"
    database = AccountDatabasePostgres(connection=connection)
    database.save(Account.random())
    all_accounts = database.get_objects()
    print(all_accounts)
    database.close_connection()

