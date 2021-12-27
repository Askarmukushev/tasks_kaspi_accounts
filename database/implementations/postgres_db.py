from typing import List
from uuid import UUID, uuid4
import psycopg2
import pandas as pd

from pandas import DataFrame, Series
from account.account import Account
from database.database import AccountDatabase
from database.database import ObjectNotFound


class AccountDatabasePostgres(AccountDatabase):
    def __init__(self, connection: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = psycopg2.connect(connection)
        # курсор
        cur = self.conn.cursor()
        # Создание таблицы accounts и ее полей
        cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id varchar primary key ,
            currency varchar ,
            balance decimal 
        );
        """)
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

    # _save - он сохраняет то что было в update и делает insert
    def _save(self, account: Account) -> None:
        if account.id_ is None:
            account.id_ = uuid4()
        # курсор
        cur = self.conn.cursor()
        # update данных таблицы accounts
        cur.execute("""
            UPDATE accounts SET currency = %s, balance =  %s WHERE id =%s;
        """, (account.currency, account.balance, str(account.id_)))
        rows_count = cur.rowcount
        self.conn.commit()

        print("ROWS COUNT", rows_count)
        if rows_count == 0:
            cur = self.conn.cursor()
            # Инсерт данных в таблицу accounts
            cur.execute("""
                        INSERT INTO accounts (id, currency, balance) VALUES (%s, %s, %s);
                        """, (str(account.id_), account.currency, account.balance))
            self.conn.commit()

    def cleat_all_data(self) -> None:
        cur = self.conn.cursor()
        # Инсерт данных в таблицу accounts
        cur.execute("DELETE FROM accounts;")
        self.conn.commit()

    def get_objects(self) -> List[Account]:
        # курсор
        cur = self.conn.cursor()
# вывод данных из таблицы accounts для печати - print(all_accounts) в файле test_databases.py в терминале
        cur.execute("""SELECT * FROM accounts;""")
        data = cur.fetchall()
        cols = [x[0] for x in cur.description]
        df = pd.DataFrame(data, columns=cols)
        return [self.pandas_row_to_account(row) for index, row in df.iterrows()]

    def pandas_row_to_account(self, row: Series) -> Account:
        return Account(
            id_=UUID(row["id"]),
            currency=row["currency"],
            balance=row["balance"],
        )

    # Подаем айдишник и мы хотим найти наш объект в списке айдишников
    def get_object(self, id_: UUID) -> Account:
        # курсор
        cur = self.conn.cursor()
        # вывод данных из таблицы accounts для печати - print(all_accounts) в файле test_databases.py в терминале
        cur.execute("SELECT * FROM accounts WHERE id = %s;", (str(id_),))
        print("Trying to find", str(id_))
        data = cur.fetchall()
        if len(data) == 0:
            raise ObjectNotFound
        # cur.fetchall() вернет нам (пример) это: (98359412,"KZT", 34533.33)
        # и эти колонки data[0], data[1], data[2] могут прийти в разном порядке, но не факт - просто никто не обещает
        # и мы эти айди карренси и баланс с помощью данной конструкции мы превращаем в список колонок
        # ниже будет принты этих данных
        cols = [x[0] for x in cur.description]
        # ниже три принта вывведут то что нам нужно просто для себя чтобы вивһдеть как это все выйдет
        # print("-------", data)
        # print("-------", cur.description)
        # print("-------", cols)
        df = pd.DataFrame(data, columns=cols)
        return self.pandas_row_to_account(row=df.iloc[0])

        # This is the implementation without Pandas
        # for i in range(len(cols)):
        #     if str(cols[i]) == "id":
        #         account_id = data[0][i]
        #     if str(cols[i]) == "balance":
        #         account_balance = data[0][i]
        #     if str(cols[i]) == "currency":
        #         account_currency = data[0][i]
        # return Account(
        #     id_=UUID(account_id),
        #     balance=account_balance,
        #     currency=account_currency,
        # )

