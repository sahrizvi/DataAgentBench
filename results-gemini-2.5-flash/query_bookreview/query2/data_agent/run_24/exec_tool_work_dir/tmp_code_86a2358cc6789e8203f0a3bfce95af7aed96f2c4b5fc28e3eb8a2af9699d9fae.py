code = """import pandas as pd
import json

books_info_full_path = locals()['var_function-call-18269390333020638437']

with open(books_info_full_path, 'r') as f:
    books_info = json.load(f)

df_books = pd.DataFrame(books_info)

# Filter for 'Literature & Fiction' category and 'English Language' in details
filtered_books = df_books[
    df_books['categories'].apply(lambda x: 'Literature & Fiction' in x) &
    df_books['details'].apply(lambda x: 'English' in x)
]

book_ids_to_query = filtered_books['book_id'].tolist()

print('__RESULT__:')
print(json.dumps(book_ids_to_query))"""

env_args = {'var_function-call-7867270035917113348': [], 'var_function-call-18269390333020638437': 'file_storage/function-call-18269390333020638437.json'}

exec(code, env_args)
