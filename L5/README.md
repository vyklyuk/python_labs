# Автентифікація і авторизація

В даній лабораторній порібно реалідізувати автентифікацію та авторизацію користувачів для розробленого REST API. Автентифікація є перевіркою того, що запит відбувається від імені конкретного користувача. Авторизація є перевіркою того чи має конкретний користувач доступ до конкретної операції над певним ресурсом.

Для автентифікації до REST API замість типової для веб-сторінок моделі автентифікації на базі HTTP-cookie як правило виконують так звану [HTTP автентифікацію](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication). Зі сторони клієнта HTTP автентифікація виконується за допомогою хедера `Authorization`. Значення даного хедера можуть мати різні [схеми автентифікації](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication#Authentication_schemes), та . Ми будемо розглядати дві такі схеми, а саме: Basic та Bearer.

При Basic смемі значення хедера виглядає наступним чином: `Basic <credentials>`. Де `<credentials>` це закодована в Base64 стрічка наступного виду: `username:password`.

При Bearer схемі значення хедера виглядає наступним чином: `Bearer <credentials>`. Де `<credentials>` є токеном автентифікації. Оригінально дану схему створили для токенів згенерованих при OAuth 2.0 авторизації, однак Bearer схеми використовуються для передачі токерів різного формату, як наприклад JWT-токени. Іноді для передачі JWT-токенів вказують схему `JWT`, однак вона не включена в офіційний стандарт.

## Варіанти

Номер варіанту визначається номером студента в журналі.

Залежно від номеру визначається схема HTTP автентифікації, яку потрібно реалізувати:
* непарні номери - Basic
* парні номери - Bearer (з JWT-токеном)

## Рекомендації

* Для спрощення реалізації Basic-автентифікації можна використати пакет [flask-HTTPAuth](https://flask-httpauth.readthedocs.io/en/latest/#basic-authentication-examples)
* Для спрощення реалізації JWT-автентифікації можна використати пакет [Flask-JWT](https://pythonhosted.org/Flask-JWT/)

## Хід роботи

1. Реалізувати автентифікацію користувачів обраним механіхмом, обмежити доступ до операцій над ресурсами для запитів, що не відповідають обраному механізму автентифікації
2. Реалізувати авторизацію користувачів, перевіряти права доступу для того чи іншого користувача, повертати ресурси, що належать конкретному користувачеві
3. При необхідності передбачити наявність супер-користувача для здійснення усіх чи певних операцій
4. Перевірити коректність роботи автентифікації та авторизації здійснивши кілька запитів до системи

## Критерії оцінювання

1. Продемонстрована реалізація автентифікації та авторизації користувачів в коді системи
2. Продемонстрована автентифікація користувача та виконання певних операцій з системою через виконання запитів до системи

## Виконання лабораторної роботи

### Реалізувати автентифікацію та авторизацію

Встановити залежності
```shell script
$ echo "Flask-JWT" >> requirements.txt
$ pip install -Ur requirements.txt

```

Модифікувати код проекту щоб добавитви JWT автентифікацію

Модифікувати код проекту щоб добавитви перевірку прав доступу користувачів до ресурсів (авторизацію)

### Перевірити коректність роботи

Стартувати систему
```shell script
$ make run-with-flask
```

Виконати ряд запитів до системи для перевірки роботи 
```shell script
$ sudo apt-get install jq
$ source functions.sh
$ AUTH_USERNAME=admin-aec8084845b41a6952d46cbaa1c9b798659487ffd133796d95d05ba45d9096c2 AUTH_PASSWORD=super-secret EMAIL="test_1@example.com" PASSWORD=123 python-uni-create-user
$ AUTH_USERNAME=admin-aec8084845b41a6952d46cbaa1c9b798659487ffd133796d95d05ba45d9096c2 AUTH_PASSWORD=super-secret EMAIL=test_2@example.com PASSWORD=123 python-uni-create-user
$ AUTH_USERNAME=test_1@example.com AUTH_PASSWORD=123 WALLET_NAME=WalletA python-uni-create-wallet
$ AUTH_USERNAME=test_2@example.com AUTH_PASSWORD=123 WALLET_NAME=WalletB python-uni-create-wallet
$ AUTH_USERNAME=test_1@example.com AUTH_PASSWORD=123 python-uni-list-wallets
$ AUTH_USERNAME=admin-aec8084845b41a6952d46cbaa1c9b798659487ffd133796d95d05ba45d9096c2 AUTH_PASSWORD=super-secret FROM_WALLET=0 TO_WALLET=1 AMOUNT=100 python-uni-send-funds
$ AUTH_USERNAME=test_1@example.com AUTH_PASSWORD=123 python-uni-list-wallets
$ AUTH_USERNAME=test_1@example.com AUTH_PASSWORD=123 FROM_WALLET=1 TO_WALLET=2 AMOUNT=10 python-uni-send-funds
$ AUTH_USERNAME=test_1@example.com AUTH_PASSWORD=123 python-uni-list-wallets
$ AUTH_USERNAME=test_2@example.com AUTH_PASSWORD=123 python-uni-list-wallets
```

Знищити базу даних
```shell script
$ make db-down
```
