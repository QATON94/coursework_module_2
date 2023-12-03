import os
from datetime import datetime
from pathlib import Path

from src.logger_config import setup_logging
from src.reports import spending_by_category, save_file
from src.services import simple_search
from src.utils import get_transactions, get_user_settings
from src.views import greetings, get_num_card, get_top_transactions, get_exchange_rate, get_stock_prices, get_page_main
from dotenv import load_dotenv
load_dotenv()

logger = setup_logging()

def main() -> None:
    ROOT_PATH = Path(__file__).parent.parent
    OPERATIONS_JSON = ROOT_PATH.joinpath("data", "operations.xls")

    USER_SETTINGS = ROOT_PATH.joinpath("user_settings.json")
    time_ = datetime.strptime('21.02.2021 06:40:55', '%d.%m.%Y %H:%M:%S')

    api_key = os.getenv('API_KEY')

    user_settings = get_user_settings(USER_SETTINGS)
    user_currencies = user_settings['user_currencies']
    user_stocks = user_settings['user_stocks']
    category = 'Супермаркеты'

    greeting = greetings(time_)
    transactions = get_transactions(OPERATIONS_JSON)
    num_card = get_num_card(transactions)
    top_transactions = get_top_transactions(transactions)
    exchange_rate = get_exchange_rate(user_currencies)
    stock_prices = get_stock_prices(user_stocks, api_key)

    get_page_main(greeting, num_card, top_transactions, exchange_rate, stock_prices)
    simple_search(transactions,'Супермаркеты')
    spending_by_category(transactions, category, time_)

if __name__ == '__main__':
    main()
