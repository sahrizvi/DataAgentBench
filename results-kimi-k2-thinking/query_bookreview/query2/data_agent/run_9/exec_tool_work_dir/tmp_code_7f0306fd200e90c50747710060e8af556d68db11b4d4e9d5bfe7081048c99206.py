code = """import json
import pandas as pd

# Load the data from previous query
books_path = var_functions.query_db:5
with open(books_path, 'r') as f:
    books_data = json.load(f)

# Convert to DataFrame to explore structure
books_df = pd.DataFrame(books_data)
print(f"Number of books in Literature & Fiction category: {len(books_df)}")
print(f"Columns: {books_df.columns.tolist()}")
print("\nFirst few rows with rating_number:")
print(books_df[['title', 'book_id', 'rating_number']].head())"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json'}

exec(code, env_args)
