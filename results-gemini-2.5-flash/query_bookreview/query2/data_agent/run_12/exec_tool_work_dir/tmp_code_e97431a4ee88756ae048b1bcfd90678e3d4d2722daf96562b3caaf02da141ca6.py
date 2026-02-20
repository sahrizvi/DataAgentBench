code = """import pandas as pd
import json

books_info_path = locals()['var_function-call-17824411837542225066']
with open(books_info_path, 'r') as f:
    books_data = json.load(f)

books_df = pd.DataFrame(books_data)

english_literature_books = books_df[
    (books_df['details'].astype(str).str.contains('English'))
]

book_ids_to_query = english_literature_books['book_id'].tolist()

print('__RESULT__:')
print(json.dumps(book_ids_to_query))"""

env_args = {'var_function-call-12682074861259270425': [], 'var_function-call-1741328765349052838': 'file_storage/function-call-1741328765349052838.json', 'var_function-call-4542417935703696844': [], 'var_function-call-14227793904686681405': [{'book_id': 'bookid_1'}, {'book_id': 'bookid_9'}, {'book_id': 'bookid_13'}, {'book_id': 'bookid_30'}, {'book_id': 'bookid_36'}, {'book_id': 'bookid_37'}, {'book_id': 'bookid_38'}, {'book_id': 'bookid_39'}, {'book_id': 'bookid_44'}, {'book_id': 'bookid_49'}, {'book_id': 'bookid_55'}, {'book_id': 'bookid_69'}, {'book_id': 'bookid_70'}, {'book_id': 'bookid_74'}, {'book_id': 'bookid_77'}, {'book_id': 'bookid_82'}, {'book_id': 'bookid_84'}, {'book_id': 'bookid_89'}, {'book_id': 'bookid_92'}, {'book_id': 'bookid_93'}, {'book_id': 'bookid_98'}, {'book_id': 'bookid_99'}, {'book_id': 'bookid_101'}, {'book_id': 'bookid_106'}, {'book_id': 'bookid_109'}, {'book_id': 'bookid_111'}, {'book_id': 'bookid_122'}, {'book_id': 'bookid_137'}, {'book_id': 'bookid_142'}, {'book_id': 'bookid_144'}, {'book_id': 'bookid_161'}, {'book_id': 'bookid_167'}, {'book_id': 'bookid_171'}, {'book_id': 'bookid_177'}, {'book_id': 'bookid_179'}, {'book_id': 'bookid_180'}, {'book_id': 'bookid_182'}, {'book_id': 'bookid_187'}, {'book_id': 'bookid_188'}, {'book_id': 'bookid_195'}], 'var_function-call-17824411837542225066': 'file_storage/function-call-17824411837542225066.json', 'var_function-call-11063697169384407301': 'file_storage/function-call-11063697169384407301.json'}

exec(code, env_args)
