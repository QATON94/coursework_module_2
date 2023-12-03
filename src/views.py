import json
import logging
from datetime import datetime
import requests


logger = logging.getLogger(__name__)


def get_page_main(greeting: str, num_card: dict, top_transactions: list[dict], exchange_rate: list,
                  stock_prices: list) -> None:
    """
    Функция получает данные и записывает их в файл
    :param greeting: Положение суток
    :param num_card: Номера карт, сумма кэшбека, сумма расходов
    :param top_transactions: Топ-5 транзакций
    :param exchange_rate: Курс валют
    :param stock_prices: Курс акций
    :return: None
    """
    json_out = {"greeting": str(greeting), "cards": num_card, "top_transactions": top_transactions,
                "currency_rates": exchange_rate, "stock_prices": stock_prices}
    with open('replies.json', 'w') as f:
        json.dump(json_out, f, sort_keys=False, ensure_ascii=False)
    return None


def greetings(time: datetime = datetime.now()) -> str:
    """Функция принимает значение времени и возврощает строку “Добрый ???”, где ???
    - утро/день/вечер/ночь в зависимости от текущего времени
    :param time: datetime
    :return str
    """
    if 5 <= time.hour < 11:
        greeting = 'Доброе утро!'

    elif 11 <= time.hour < 17:
        greeting = 'Добрый день!'

    elif 17 <= time.hour < 23:
        greeting = 'Добрый вечер!'

    else:
        greeting = 'Доброй ночи!'
    return greeting


def get_num_card(transactions: list) -> dict:
    """
    Функция принимает список словаре с транзакциями и возврощает словарь,
    где ключ - номер карты, а значение - список с суммой кэшбека
    и суммой операций по данной карте
    :param transactions: список словаре с транзакциями
    :return num_cards:
    """
    num_cards = {}
    for row in transactions:
        if row['Номер карты'] != 0:
            num_cards[row['Номер карты']] = []
    for i in num_cards.keys():
        cachbak = 0
        expenses = 0
        for row in transactions:
            if row['Номер карты'] == i:
                cachbak += row['Кэшбэк']
                if row['Сумма платежа'] < 0:
                    expenses += row['Сумма платежа']
        card_info = {
            "last_digits": i,
            "total_spent": abs(expenses),
            "cashback": int(cachbak)
        }
        num_cards[i].append(card_info)
    return num_cards


def get_top_transactions(transactions: list) -> list:
    """
    Функция принимает список словаре с транзакциями и возврощает топ-5 операций
    :param transactions: список словаре с транзакциями
    :return top_transactions: список с топ-5 транзакций
    """
    top_transactions = []
    sorted_transactions = sorted(transactions, key=lambda x: abs(x['Сумма платежа']), reverse=True)
    for i in range(5):
        top_transactions.append(sorted_transactions[i])
    return top_transactions


def get_exchange_rate(user_currencies: list) -> list:
    """
    Функция принимает названия курса валют и возврощает список с текущим курсом валют
    :param user_currencies: названия курса валют
    :return: возврощает список с текущим курсом валют
    """
    currency_rates = []
    try:
        cash_rate = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()["Valute"]
        for currenc in user_currencies:
            currenc_valute = cash_rate[currenc]['Value']
            currency_rate = {
                "currency": currenc,
                "rate": currenc_valute
            }
            currency_rates.append(currency_rate)
    except Exception as err:
        logger.error(f"Ошибка: {err}")
    return currency_rates


def get_stock_prices(user_stocks: list, apikey: str) -> list:
    """
    Функция принимает названия курса валют и возврощает список акций по текущему дню
    :param user_stocks: список названий акций который надо получить
    :return stock_prices: список акций по текущему дню
    """
    stock_prices = []
    try:
        url = f'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={apikey}'
        data_ctock = requests.get(url).json()['most_actively_traded']
        for row in data_ctock:
            if row['ticker'] in user_stocks:
                dict_stock = {"stock": row['ticker'], "price": row['price']}
                stock_prices.append(dict_stock)
    except Exception as err:
        logger.error(f"Ошибка: {err}")
    return stock_prices
