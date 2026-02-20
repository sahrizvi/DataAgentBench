code = """import json
import os
import re

# Load both datasets
books_file = "file_storage/functions.query_db:32.json"
reviews_file = "file_storage/functions.query_db:33.json"

with open(books_file, 'r') as f:
    books = json.load(f)

with open(reviews_file, 'r') as f:
    reviews = json.load(f)

# Extract numeric IDs and create dicts
for book in books:
    match = re.search(r'bookid_(\d+)', book['book_id'])
    if match:
        book['numeric_id'] = int(match.group(1))

for review in reviews:
    match = re.search(r'purchaseid_(\d+)', review['purchase_id'])
    if match:
        review['numeric_id'] = int(match.group(1))

# Create book dict by numeric_id
books_dict = {book['numeric_id']: book for book in books}

# Calculate average rating per book
from collections import defaultdict
book_ratings = defaultdict(list)

for review in reviews:
    if 'numeric_id' in review:
        numeric_id = review['numeric_id']
        if numeric_id in books_dict:
            book_ratings[numeric_id].append(float(review['rating']))

# Calculate averages and filter books with rating >= 4.5
results = []
for book_id, ratings in book_ratings.items():
    if book_id in books_dict:
        avg_rating = sum(ratings) / len(ratings)
        if avg_rating >= 4.5:
            book = books_dict[book_id]
            results.append({
                'title': book['title'],
                'author': book['author'],
                'average_rating': round(avg_rating, 2),
                'review_count': len(ratings)
            })

# Sort by average rating (descending) and then by review count (descending)
results = sorted(results, key=lambda x: (-x['average_rating'], -x['review_count']))

print('__RESULT__:')
print(json.dumps(results))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review'], 'var_functions.query_db:7': [], 'var_functions.execute_python:12': ['var_functions.list_db:0', 'var_functions.query_db:2', 'var_functions.list_db:5', 'var_functions.query_db:7'], 'var_functions.query_db:14': [{'categories': '["Books", "Literature & Fiction", "History & Criticism"]'}, {'categories': '["Books", "Reference", "Words, Language & Grammar"]'}, {'categories': '["Books", "Biographies & Memoirs", "Leaders & Notable People"]'}, {'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'categories': '["Books", "Mystery, Thriller & Suspense", "Thrillers & Suspense"]'}, {'categories': '["Books", "Arts & Photography", "History & Criticism"]'}, {'categories': '["Books", "Parenting & Relationships", "Parenting"]'}, {'categories': '["Books", "Engineering & Transportation", "Engineering"]'}, {'categories': '["Books", "Literature & Fiction", "Genre Fiction"]'}, {'categories': '["Books", "Education & Teaching", "Schools & Teaching"]'}], 'var_functions.query_db:18': 'file_storage/functions.query_db:18.json', 'var_functions.query_db:20': 'file_storage/functions.query_db:20.json', 'var_functions.query_db:24': 'file_storage/functions.query_db:24.json', 'var_functions.query_db:26': 'file_storage/functions.query_db:26.json', 'var_functions.query_db:28': 'file_storage/functions.query_db:28.json', 'var_functions.execute_python:30': ['var_functions.query_db:2', 'var_functions.query_db:7', 'var_functions.query_db:14', 'var_functions.query_db:18', 'var_functions.query_db:20', 'var_functions.query_db:24', 'var_functions.query_db:26', 'var_functions.query_db:28'], 'var_functions.query_db:32': 'file_storage/functions.query_db:32.json', 'var_functions.query_db:33': 'file_storage/functions.query_db:33.json', 'var_functions.execute_python:36': {'books_key': 'var_functions.query_db:32', 'reviews_key': 'var_functions.query_db:33', 'all_keys': [{'var_functions.query_db:2': 'file_storage/functions.query_db:2.json'}, {'var_functions.query_db:18': 'file_storage/functions.query_db:18.json'}, {'var_functions.query_db:20': 'file_storage/functions.query_db:20.json'}, {'var_functions.query_db:24': 'file_storage/functions.query_db:24.json'}, {'var_functions.query_db:26': 'file_storage/functions.query_db:26.json'}]}, 'var_functions.execute_python:38': ['var_functions.query_db:2', 'var_functions.query_db:18', 'var_functions.query_db:20', 'var_functions.query_db:24', 'var_functions.query_db:26', 'var_functions.query_db:28', 'var_functions.query_db:32', 'var_functions.query_db:33'], 'var_functions.execute_python:40': {'books_count': 25, 'reviews_count': 329, 'sample_book': {'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'author': 'None'}, 'sample_review': {'rating': '5', 'purchase_id': 'purchaseid_8'}}}

exec(code, env_args)
