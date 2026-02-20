code = """import json
import pandas as pd

books_data = pd.read_json(locals()['var_function-call-11272966320864587591'])

def parse_categories(categories_str):
    try:
        return json.loads(categories_str)
    except:
        return []

books_data['categories_list'] = books_data['categories'].apply(parse_categories)

literature_fiction_books = books_data[books_data['categories_list'].apply(lambda x: 'Literature & Fiction' in x)]

english_literature_fiction_books = literature_fiction_books[literature_fiction_books['details'].str.contains('English', na=False)]

print("__RESULT__:")
print(english_literature_fiction_books[['book_id', 'title']].to_json(orient='records'))"""

env_args = {'var_function-call-16511819307130799169': ['books_info'], 'var_function-call-382231788195853622': ['review'], 'var_function-call-11272966320864587591': 'file_storage/function-call-11272966320864587591.json'}

exec(code, env_args)
