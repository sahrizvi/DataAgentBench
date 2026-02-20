code = """import json
import pandas as pd
import re

# Load the books data
books_file = var_functions.query_db:10
with open(books_file, 'r') as f:
    books_data = json.load(f)

# Load the reviews data
reviews_file = var_functions.query_db:8
with open(reviews_file, 'r') as f:
    reviews_data = json.load(f)

# Convert to DataFrames
books_df = pd.DataFrame(books_data)
reviews_df = pd.DataFrame(reviews_data)

# Extract numeric ID from book_id and purchase_id
books_df['book_num_id'] = books_df['book_id'].str.extract(r'bookid_(\d+)').astype(int)
reviews_df['book_num_id'] = reviews_df['purchase_id'].str.extract(r'purchaseid_(\d+)').astype(int)

# Join on numeric ID
merged_df = pd.merge(books_df, reviews_df, on='book_num_id', how='inner')

# Calculate average rating per book
avg_ratings = merged_df.groupby(['book_num_id', 'title', 'categories', 'details'])['rating'].mean().reset_index()

# Filter for perfect 5.0 rating
perfect_books = avg_ratings[avg_ratings['rating'] == 5.0]

# Filter for English language (check if details contain "English")
perfect_books['is_english'] = perfect_books['details'].str.contains('English', case=False, na=False)
english_perfect_books = perfect_books[perfect_books['is_english'] == True]

# Format the result
result = english_perfect_books[['title', 'categories', 'details', 'rating']].to_dict('records')

print('__RESULT__:')
print(json.dumps(result, indent=2))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:4': 'file_storage/functions.query_db:4.json', 'var_functions.query_db:6': 'file_storage/functions.query_db:6.json', 'var_functions.query_db:8': 'file_storage/functions.query_db:8.json', 'var_functions.query_db:10': 'file_storage/functions.query_db:10.json'}

exec(code, env_args)
