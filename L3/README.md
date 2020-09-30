# ORM та міграції

В даній лабораторній роботі потрібно описати структуру бази даних для системи, створити ORM-моделі, що представляють таблиці в базі даних за допомогою [SQLAlchemy](https://www.sqlalchemy.org/) ORM та створити скрипти міграцій для створення таблиць для кожної з моделей за допомогою [Alembic](https://alembic.sqlalchemy.org/en/latest/).

## Хід роботи

1. Описати структуру бази даних, зробити діаграму з таблицями та зв'язками між ними
2. Встановити одну з реляційних СУБД, які SQLAlchemy [підтримує](https://docs.sqlalchemy.org/en/13/dialects/)  (PostgreSQL, MySQL чи іншу)
3. Вручну створити у базі даних необхідні таблиці
4. Створити SQLAlchemy ORM моделі для таблиць та спробувати використати їх для операцій над базою даних; видалити створені таблиці перед наступним кроком
5. Створити автоматично-згенерований скрипт міграції за допомогою Alembic

## Критерії оцінювання

1. Описана структура бази даних для системи на наявна діаграма
2. Усі таблиці описані SQLAlchemy ORM моделями
3. Створено скрипт міграції для створення таблиць для моделей
    > якщо alembic ініційовано в директорій `./alembic`, то в директорії `./alembic/versions` має бути Python-файл з непустими функціями `upgrade` та `downgrade`
4. Таблиці в базі даних створені за допомогою Alembic міграцій
    > в базі даних серед інших таблиць має бути таблиця `alembic_version` з версією застосованої міграції

## Виконання лабораторної роботи

### Описати структуру бази даних

В системі будуть наступні таблиці
* users
* wallets
* transactions

Таблиця `wallets` буде зв'язана з таблицею `users`, а таблиця `transactions` буде зв'язана з таблицею `wallets`.

![Діаграма](./src/database.png)

### Встановити СУБД

```shell script
$ sudo apt-get -y install postgresql
```

або через докер
```shell script
$ make db
```

### Вручну створити таблиці

Запустити [скрипт](./src/create_tables.sql) для ручного створення таблиць
```shell script
$ PGPASSWORD=123456 psql -h localhost -U postgres -d postgres -f src/create_tables.sql
```
Перевірити що таблиці створені
```shell script
$ PGPASSWORD=123456 psql -h localhost -U postgres -d postgres -c '\d'
```

### Створити SQLAlchemy ORM моделі

Встановити залежності
```shell script
$ echo "sqlalchemy" >> requirements.txt
$ echo "psycopg2-binary" >> requirements.txt
$ pip install -Ur requirements.txt
```

Створено [скрипт](./src/models.py) з SQLAlchemy ORM моделями.

Перевірити з'єднання SQLALchemy до БД і операції з моделями за допомогою іншого [скрипта](./src/check_models.py)
```shell script
$ python src/check_models.py
```
Перевірити, що до бази даних були додані нові записи
```shell script
$ PGPASSWORD=123456 psql -h localhost -U postgres -d postgres -c 'select * from users;'
 uid |        email        | password | first_name | last_name 
-----+---------------------+----------+------------+-----------
   1 | example@example.com |          | First      | Last
(1 row)

$ PGPASSWORD=123456 psql -h localhost -U postgres -d postgres -c 'select * from wallets;'
 uid |   name    | funds | owner_uid 
-----+-----------+-------+-----------
   1 | My wallet |    90 |         1
   2 | My wallet |   110 |         1
(2 rows)

$ PGPASSWORD=123456 psql -h localhost -U postgres -d postgres -c 'select * from transactions;'
 uid | from_wallet_uid | to_wallet_uid | amount |          datetime          
-----+-----------------+---------------+--------+----------------------------
   1 |               1 |             2 |     10 | 2020-09-21 20:31:28.078417
(1 row)
```

Видалити всі таблиці перед початком наступного кроку.

### Створити Alembic міграції

Встановити залежності
```shell script
$ echo "alembic" >> requirements.txt
$ pip install -r requirements.txt
```

Ініціювати Alembic
```shell script
$ alembic init alembic
```

Модифікувати `alembic/env.py` вказавши адресу до БД та базову модель для автоматичної генерації міграцій 
```python
...
import os
from models import BaseModel
...
config.set_main_option(
    "sqlalchemy.url", 
    os.getenv("DB_URI", "postgres://postgres:123456@localhost:5432/postgres"),
)
...
target_metadata = BaseModel.metadata
...
```

Створити файл міграції
```shell script
$ PYTHONPATH=${PWD}:${PYTHONPATH} alembic revision -m "add models" --autogenerate
```
Створено файл в директорій `./alembic/versions`.

Застосувати створену міграцію
```shell script
$ PYTHONPATH=${PWD}:${PYTHONPATH} alembic upgrade head
```

Перевірити, що міграція створила таблиці для моделей та в таблицю `alembic_version` записана версія останньої міграції
```shell script
$ PGPASSWORD=123456 psql -h localhost -U postgres -d postgres -c '\d'
...
$ PGPASSWORD=123456 psql -h localhost -U postgres -d postgres -c 'select * from alembic_version'
...
```

Перевірити що операції зі створеними через міграції таблицями працюють так само коректно
```shell script
$ python src/check_models.py
```
