import json
from pathlib import Path


def simple_search(transactions: list[dict], word_search: str) -> None:
    result_search = []
    for row in transactions:
        if (row['Категория'] == word_search) or (row['Описание'] == word_search):
            result_search.append(row)

    ROOT_PATH = Path(__file__).parent.parent
    filename = ROOT_PATH.joinpath("data", "search_result.json")
    with open(filename, 'w', encoding='utf=8') as f:
        json.dump(result_search, f, ensure_ascii=False)
