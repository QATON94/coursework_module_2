import json
from pathlib import Path

import pytest

from src.services import simple_search


@pytest.fixture()
def test_transactions():
    file_transactions = [
        {
            "Дата операции": "20.07.2019 15:25:01",
            "Дата платежа": "22.07.2019",
            "Номер карты": "*4556",
            "Статус": "OK",
            "Сумма операции": -5000.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -5000.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Наличные",
            "MCC": 6011,
            "Описание": "Снятие в банкомате Сбербанк",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 5000.0,
        },
        {
            "Дата операции": "19.07.2019 22:02:30",
            "Дата платежа": "21.07.2019",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -149.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -149.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Топливо",
            "MCC": 5541,
            "Описание": "Circle K",
            "Бонусы (включая кэшбэк)": 2,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 149.0,
        },
        {
            "Дата операции": "19.07.2019 18:24:31",
            "Дата платежа": "20.07.2019",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -1400.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -1400.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Госуслуги",
            "MCC": 9311,
            "Описание": "Госуслуги",
            "Бонусы (включая кэшбэк)": 28,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 1400.0,
        },
        {
            "Дата операции": "17.07.2019 15:05:27",
            "Дата платежа": "19.07.2019",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -25.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -25.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Дом и ремонт",
            "MCC": 5200,
            "Описание": "OOO Nadezhda",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 25.0,
        },
        {
            "Дата операции": "17.07.2019 15:01:15",
            "Дата платежа": "19.07.2019",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -27.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -27.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Дом и ремонт",
            "MCC": 5200,
            "Описание": "OOO Nadezhda",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 27.0,
        },
        {
            "Дата операции": "16.07.2019 16:30:10",
            "Дата платежа": "18.07.2019",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -49.8,
            "Валюта операции": "RUB",
            "Сумма платежа": -49.8,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Супермаркеты",
            "MCC": 5411,
            "Описание": "SPAR",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 49.8,
        },
        {
            "Дата операции": "16.07.2019 16:13:54",
            "Дата платежа": "17.07.2019",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -114.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -114.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Фастфуд",
            "MCC": 5814,
            "Описание": "IP Yakubovskaya M. V.",
            "Бонусы (включая кэшбэк)": 2,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 114.0,
        },
        {
            "Дата операции": "10.06.2019 11:37:34",
            "Дата платежа": "12.06.2019",
            "Номер карты": "*4556",
            "Статус": "OK",
            "Сумма операции": -235.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -235.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": 11,
            "Категория": "Транспорт",
            "MCC": 4121,
            "Описание": "Яндекс Такси",
            "Бонусы (включая кэшбэк)": 11,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 235.0,
        },
        {
            "Дата операции": "08.06.2019 17:47:05",
            "Дата платежа": "11.06.2019",
            "Номер карты": "*4556",
            "Статус": "OK",
            "Сумма операции": -279.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -279.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": 13,
            "Категория": "Транспорт",
            "MCC": 4121,
            "Описание": "Яндекс Такси",
            "Бонусы (включая кэшбэк)": 13,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 279.0,
        },
    ]
    return file_transactions


def test_simple_search(test_transactions):
    simple_search(test_transactions, "Транспорт")
    ROOT_PATH = Path(__file__).parent.parent
    filename = ROOT_PATH.joinpath("data", "search_result.json")
    with open(filename, "r", encoding="utf=8") as f:
        return_func = json.load(f)
    assert return_func == [
        {
            "Дата операции": "10.06.2019 11:37:34",
            "Дата платежа": "12.06.2019",
            "Номер карты": "*4556",
            "Статус": "OK",
            "Сумма операции": -235.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -235.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": 11,
            "Категория": "Транспорт",
            "MCC": 4121,
            "Описание": "Яндекс Такси",
            "Бонусы (включая кэшбэк)": 11,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 235.0,
        },
        {
            "Дата операции": "08.06.2019 17:47:05",
            "Дата платежа": "11.06.2019",
            "Номер карты": "*4556",
            "Статус": "OK",
            "Сумма операции": -279.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -279.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": 13,
            "Категория": "Транспорт",
            "MCC": 4121,
            "Описание": "Яндекс Такси",
            "Бонусы (включая кэшбэк)": 13,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 279.0,
        },
    ]
