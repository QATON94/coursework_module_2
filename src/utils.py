import json
import logging
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


def get_transactions(file_path: Any) -> list[Any]:
    """Функция открывает файл возврощается список транзакций или пустой список
    param path_: Путь к json файлу с транзакциями
    return: возвращает пустой список если файл не найден, либо список транзакций
    """
    transactions = []
    try:
        transactions_head = []
        df = pd.read_excel(file_path)
        df_n = df.fillna(0)
        transactions_reader = df_n.convert_dtypes()
        columns = transactions_reader.shape[0]
        rows = transactions_reader.shape[1]
        for row in transactions_reader:
            transactions_head.append(row)

        for column in range(0, columns):
            transactions_dict = {}
            for row in range(0, rows):
                transactions_dict[str(transactions_head[row])] = transactions_reader.iloc[column, row]
            transactions.append(transactions_dict)

        for i in range(len(transactions)):
            transactions[i]['Кэшбэк'] = int(transactions[i]['Кэшбэк'])
            transactions[i]['MCC'] = int(transactions[i]['MCC'])
            transactions[i]['Бонусы (включая кэшбэк)'] = int(transactions[i]['Бонусы (включая кэшбэк)'])
            transactions[i]['Округление на инвесткопилку'] = int(transactions[i]['Округление на инвесткопилку'])
    except FileNotFoundError:
        logger.error(f"Файл: {file_path} не найден FileNotFoundError")

    return transactions


def get_user_settings(file_patch) -> dict:
    """
    Функция открывает файл и возврощает список настроек пользователя
    :param file_patch: Путь к файлу
    :return: Список настроек
    """
    try:
        with open(file_patch, encoding='utf=8') as f:
            user_settings = json.load(f)
    except FileNotFoundError:
        logger.error(f"Файл: {file_patch} не найден FileNotFoundError")
        user_settings = []

    return user_settings
