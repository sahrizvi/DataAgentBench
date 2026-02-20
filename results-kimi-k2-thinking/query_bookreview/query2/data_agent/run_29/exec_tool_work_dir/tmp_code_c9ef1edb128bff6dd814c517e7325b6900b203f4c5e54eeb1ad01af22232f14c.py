code = """import json
import pandas as pd
import re
import ast

# Load books data
books_file = locals()['var_functions.query_db:6']
with open(books_file, 'r') as f:
    books = json.load(f)

# Load reviews data  
reviews_file = locals()['var_functions.query_db:16']
with open(reviews_file, 'r') as f:
    reviews = json.load(f)

# Convert to DataFrames
df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Convert rating to numeric
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'])

# Filter for Literature & Fiction category and English language
def is_literature_fiction(categories_str):
    try:
        categories = ast.literal_eval(categories_str)
        return 'Literature & Fiction' in categories
    except:
        return False

def is_english(details_str):
    return 'English' in details_str

# Apply filters
df_books_filtered = df_books[
    df_books['categories'].apply(is_literature_fiction) & 
    df_books['details'].apply(is_english)
].copy()

# Map book_id to purchase_id format
df_books_filtered['purchase_id'] = df_books_filtered['book_id'].str.replace('bookid_', 'purchaseid_')

# Join with reviews
merged = df_books_filtered.merge(df_reviews, on='purchase_id', how='inner')

# Calculate average rating per book
book_ratings = merged.groupby(['book_id', 'title', 'author', 'categories']).agg({
    'rating': ['mean', 'count']
}).reset_index()

# Flatten column names
book_ratings.columns = ['book_id', 'title', 'author', 'categories', 'avg_rating', 'review_count']

# Filter for perfect 5.0 average rating
perfect_books = book_ratings[book_ratings['avg_rating'] == 5.0]

# Extract author name from the JSON string
def get_author_name(author_str):
    if author_str == 'None' or pd.isna(author_str):
        return 'Unknown Author'
    try:
        author_data = ast.literal_eval(author_str)
        return author_data.get('name', 'Unknown Author')
    except:
        return str(author_str)[:100]  # Return first 100 chars if parsing fails

# Prepare final results
results = []
for _, book in perfect_books.iterrows():
    author_name = get_author_name(book['author'])
    results.append({
        'title': book['title'],
        'author': author_name,
        'category_path': book['categories'],
        'average_rating': book['avg_rating'],
        'review_count': int(book['review_count']),
        'book_id': book['book_id']
    })

# Sort by review count descending for better readability
results = sorted(results, key=lambda x: x['review_count'], reverse=True)

print('__RESULT__:')
print(json.dumps(results, ensure_ascii=False, indent=2))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review'], 'var_functions.query_db:6': 'file_storage/functions.query_db:6.json', 'var_functions.execute_python:12': {'type': "<class 'str'>", 'is_string': True, 'preview': 'file_storage/functions.query_db:6.json'}, 'var_functions.execute_python:14': {'num_books': 40, 'columns': ['book_id', 'title', 'author', 'categories', 'details'], 'sample_categories': ['["Books", "Literature & Fiction", "History & Criticism"]', '["Books", "Literature & Fiction", "Genre Fiction"]', '["Books", "Literature & Fiction", "Poetry"]']}, 'var_functions.query_db:16': 'file_storage/functions.query_db:16.json', 'var_functions.execute_python:18': {'books_count': 40, 'reviews_count': 1325, 'books_columns': ['book_id', 'title', 'author', 'categories', 'details'], 'reviews_columns': ['purchase_id', 'rating']}, 'var_functions.execute_python:22': 'file_storage/functions.execute_python:22.json'}

exec(code, env_args)
