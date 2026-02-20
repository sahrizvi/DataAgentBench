code = """import json
import pandas as pd

# Read the full result
with open('var_functions.query_db:5.json', 'r') as f:
    books_data = json.load(f)

# Convert to DataFrame to explore
df_books = pd.DataFrame(books_data)

print("Books database shape:", df_books.shape)
print("\nFirst few rows:")
print(df_books.head())
print("\nColumns:")
print(df_books.columns.tolist())
print("\nDetails column content for first book:")
print(df_books.iloc[0]['details'])"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json'}

exec(code, env_args)
