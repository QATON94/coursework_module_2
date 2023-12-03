import datetime
import json
from typing import Optional, Callable
import pandas as pd


def save_file(func: Callable) -> Callable:
    """Декоратор, который записывает результат вызова функции в файл"""
    def wrapper(*args: tuple, **kwargs: dict) -> None:
        func_return = func(*args, **kwargs)
        with open('Spending by category.json', 'w', encoding='utf=8') as f:
            json.dump(func_return, f, ensure_ascii=False)
        return None
    return wrapper



@save_file
def spending_by_category(transactions:list[dict],
                         category: str,
                         date: datetime = datetime.datetime.now()) -> list:
    """
    Функция получает список транзакций, категорию транзакций и время.
    Возвращает траты по заданной категории за последние 3 месяца.
    :param transactions: Список транзакций
    :param category: Поиск по категории
    :param date: опциональная дата
    :return: Отфильтрованный список
    """
    df = pd.DataFrame(transactions)
    df = df.convert_dtypes()
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    last_day = datetime.datetime(year=date.year, month=date.month, day=date.day)
    first_day = last_day - datetime.timedelta(days=90)
    data_month = df[(df['Дата операции'] > first_day) & (df['Дата операции'] < last_day)]

    data_month = data_month.groupby('Категория')

    cost_category = []
    for row in data_month:
        if row[0] == category:
            for i in range(len(row[1])):
                row_cost = {'Дата операции': str(row[1]['Дата операции'].values[i]),
                            'Сумма платежа': row[1]['Сумма платежа'].values[i]}
                cost_category.append(row_cost)

    return cost_category
