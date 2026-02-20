code = """import json
import pandas as pd

# Get the path to the books data file
books_data_path = var_functions.query_db:5

# Load and inspect the data
with open(books_data_path, 'r') as f:
    books_data = json.load(f)

books_df = pd.DataFrame(books_data)
print(f"Number of books in Literature & Fiction category: {len(books_df)}")
print(f"Columns: {books_df.columns.tolist()}")
print("\nFirst few rows with rating_number:")
print(books_df[['title', 'book_id', 'rating_number']].head())
print("\nrating_number data type and sample values:")
print(books_df['rating_number'].dtype)
print(books_df['rating_number'].unique()[:10])"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json'}

exec(code, env_args)
