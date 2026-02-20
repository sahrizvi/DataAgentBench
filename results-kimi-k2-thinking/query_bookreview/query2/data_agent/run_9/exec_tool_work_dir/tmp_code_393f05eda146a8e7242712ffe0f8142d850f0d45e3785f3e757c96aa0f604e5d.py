code = """import json
import pandas as pd

# Access the data from storage
books_data = var_functions.query_db:5

# Convert to DataFrame to explore structure
books_df = pd.DataFrame(books_data)
print(f"Number of books in Literature & Fiction category: {len(books_df)}")
print(f"Columns: {books_df.columns.tolist()}")
print("\nFirst few rows with rating_number:")
print(books_df[['title', 'book_id', 'rating_number']].head())

# Also check unique values in rating_number to understand the scale
print("\nUnique rating_number values (sample):")
print(books_df['rating_number'].value_counts().head(10))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json'}

exec(code, env_args)
