import json


def simple_search(transactions: list[dict], word_search: str) -> None:
    result_search = []
    for row in transactions:
        if (row['Категория'] == word_search) or (row['Описание'] == word_search):
            result_search.append(row)

    with open('search_result.json', 'w', encoding='utf=8') as f:
        json.dump(result_search, f, ensure_ascii=False)
