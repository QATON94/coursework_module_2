import csv
import datetime
from pathlib import Path
from typing import Any, Callable

import pandas as pd
from pandas import DataFrame
from pandas.core.groupby import DataFrameGroupBy


def save_file(file_name):
    def wrapper(func: Callable) -> Callable:
        """Декоратор, который записывает результат вызова функции в файл"""

        def inner(*args: tuple, **kwargs: dict) -> None:
            func_return = func(*args, **kwargs)
            ROOT_PATH = Path(__file__).parent.parent
            filename = ROOT_PATH.joinpath("data", file_name)
            with open(filename, 'w', encoding='utf=8') as f:
                writer = csv.writer(f, delimiter='\n')
                writer.writerow(func_return)
            return None

        return inner

    return wrapper


@save_file('Spending by category.csv')
def spending_by_category(transactions: list[dict],
                         category: str,
                         date_search: Any = datetime.datetime.now()) -> list:
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
    last_day = datetime.datetime(year=date_search.year, month=date_search.month, day=date_search.day)
    first_day = last_day - datetime.timedelta(days=90)
    data_month: DataFrame = df[(df['Дата операции'] > first_day) & (df['Дата операции'] < last_day)]

    data_month_category: DataFrameGroupBy = data_month.groupby('Категория')

    cost_category = []
    for row in data_month_category:
        if row[0] == category:
            for i in range(len(row[1])):
                row_cost = {'Дата операции': str(row[1]['Дата операции'].values[i]),
                            'Сумма платежа': row[1]['Сумма платежа'].values[i]}
                cost_category.append(row_cost)

    return cost_category
