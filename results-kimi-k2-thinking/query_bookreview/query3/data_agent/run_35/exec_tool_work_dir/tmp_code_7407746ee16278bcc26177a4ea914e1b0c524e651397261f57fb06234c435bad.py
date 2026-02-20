code = """import json
import pandas as pd
import re

# Load all books and reviews
books_file = locals()['var_functions.query_db:18']
reviews_file = locals()['var_functions.query_db:15']

with open(books_file, 'r') as f:
    books = json.load(f)

with open(reviews_file, 'r') as f:
    reviews = json.load(f)

# Convert to DataFrames
df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Filter children's books (looking for "Children's Books" in categories)
childrens_books = []
for book in books:
    categories_str = book.get('categories', '')
    if "Children's Books" in categories_str:
        childrens_books.append(book)

df_childrens = pd.DataFrame(childrens_books)

print('__RESULT__:')
print(json.dumps({
    "total_books": len(df_books),
    "total_reviews": len(df_reviews),
    "childrens_books_count": len(df_childrens),
    "sample_categories": df_childrens[['book_id', 'title', 'categories']].head(5).to_dict('records')
}))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:3': 'file_storage/functions.query_db:3.json', 'var_functions.execute_python:10': {'available_vars': ['var_functions.list_db:0', 'var_functions.query_db:2', 'var_functions.query_db:3', '__builtins__', 'json', 'pd', 're'], 'var_types': {'var_functions.list_db:0': "<class 'list'>", 'var_functions.query_db:2': "<class 'str'>", 'var_functions.query_db:3': "<class 'str'>", '__builtins__': "<class 'dict'>", 'json': "<class 'module'>"}}, 'var_functions.execute_python:12': {'books_count': 25, 'reviews_count': 100, 'sample_book_keys': ['title', 'subtitle', 'author', 'rating_number', 'features', 'description', 'price', 'store', 'categories', 'details', 'book_id'], 'sample_review_keys': ['rating', 'title', 'text', 'review_time', 'helpful_vote', 'verified_purchase', 'purchase_id']}, 'var_functions.query_db:15': 'file_storage/functions.query_db:15.json', 'var_functions.query_db:18': 'file_storage/functions.query_db:18.json'}

exec(code, env_args)
