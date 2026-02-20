code = """import pandas as pd
import json

books_info_path = locals()['var_function-call-1741328765349052838']
with open(books_info_path, 'r') as f:
    books_data = json.load(f)

books_df = pd.DataFrame(books_data)

english_literature_books = books_df[
    (books_df['categories'].astype(str).str.contains('Literature & Fiction')) &
    (books_df['details'].astype(str).str.contains('Language: English'))
]

book_ids_to_query = english_literature_books['book_id'].tolist()

print('__RESULT__:')
print(json.dumps(book_ids_to_query))"""

env_args = {'var_function-call-12682074861259270425': [], 'var_function-call-1741328765349052838': 'file_storage/function-call-1741328765349052838.json'}

exec(code, env_args)
