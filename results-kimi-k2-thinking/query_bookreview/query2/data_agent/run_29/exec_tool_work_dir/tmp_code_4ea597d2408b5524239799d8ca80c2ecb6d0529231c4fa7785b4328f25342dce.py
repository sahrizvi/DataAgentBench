code = """import json
import pandas as pd
import sqlite3
import ast

# Load the books data from the file
books_file = var_functions.query_db_6
with open(books_file, 'r') as f:
    books = json.load(f)

# Convert to DataFrame
df_books = pd.DataFrame(books)

# Check the structure of the data
print('__RESULT__:')
print(json.dumps({
    "num_books": len(df_books),
    "columns": list(df_books.columns),
    "sample_categories": df_books['categories'].head(3).tolist()
}))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review'], 'var_functions.query_db:6': 'file_storage/functions.query_db:6.json'}

exec(code, env_args)
