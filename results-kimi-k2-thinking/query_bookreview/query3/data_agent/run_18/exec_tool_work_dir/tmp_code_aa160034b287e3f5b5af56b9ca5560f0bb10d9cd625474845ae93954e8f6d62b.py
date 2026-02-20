code = """import json
import pandas as pd

# Load the full data
books_file = var_functions.query_db:5
reviews_file = var_functions.query_db:8

with open(books_file, 'r') as f:
    books_data = json.load(f)

with open(reviews_file, 'r') as f:
    reviews_data = json.load(f)

# Create DataFrames
books_df = pd.DataFrame(books_data)
reviews_df = pd.DataFrame(reviews_data)

# Check the structure
print('__RESULT__:')
print(json.dumps({
    'books_columns': list(books_df.columns),
    'reviews_columns': list(reviews_df.columns),
    'sample_book_ids': books_df['book_id'].head(10).tolist(),
    'sample_purchase_ids': reviews_df['purchase_id'].head(10).tolist()
}, indent=2))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.query_db:8': 'file_storage/functions.query_db:8.json'}

exec(code, env_args)
