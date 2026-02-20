code = """import json
import pandas as pd
import ast

# Load the data
books_file = locals()['var_functions.query_db:5']
reviews_file = locals()['var_functions.query_db:8']

with open(books_file, 'r') as f:
    books_data = json.load(f)

with open(reviews_file, 'r') as f:
    reviews_data = json.load(f)

books_df = pd.DataFrame(books_data)
reviews_df = pd.DataFrame(reviews_data)

# Examine categories structure
print('Sample categories values:')
for i, cat in enumerate(books_df['categories'].head(5)):
    print(f"{i}: {cat[:100]}")

# Check if any books have Children's Books category
childrens_books = []
for i, row in books_df.iterrows():
    try:
        cats = ast.literal_eval(row['categories'])
        if isinstance(cats, list) and any('Children' in str(cat) for cat in cats):
            childrens_books.append(row)
    except:
        pass

result = {
    'total_books': len(books_df),
    'children_books_found': len(childrens_books),
    'sample_children_books': [b['title'] for b in childrens_books[:10]] if childrens_books else []
}

print('__RESULT__:')
print(json.dumps(result))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.query_db:8': 'file_storage/functions.query_db:8.json', 'var_functions.execute_python:10': {'books_columns': ['title', 'subtitle', 'author', 'rating_number', 'features', 'description', 'price', 'store', 'categories', 'details', 'book_id'], 'reviews_columns': ['rating', 'title', 'text', 'review_time', 'helpful_vote', 'verified_purchase', 'purchase_id'], 'sample_book_ids': ['bookid_1', 'bookid_2', 'bookid_3', 'bookid_4', 'bookid_5', 'bookid_6', 'bookid_7', 'bookid_8', 'bookid_9', 'bookid_10'], 'sample_purchase_ids': ['purchaseid_186', 'purchaseid_191', 'purchaseid_190', 'purchaseid_8', 'purchaseid_178', 'purchaseid_186', 'purchaseid_76', 'purchaseid_186', 'purchaseid_115', 'purchaseid_167']}}

exec(code, env_args)
