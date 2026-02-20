code = """import json

# Load data files
with open("file_storage/functions.query_db:32.json") as f:
    children_books = json.load(f)
    
with open("file_storage/functions.query_db:33.json") as f:
    reviews_2020 = json.load(f)

# Map book IDs to book info
book_dict = {book['book_id']: book for book in children_books}

# Calculate average ratings for each book
from collections import defaultdict
book_ratings = defaultdict(list)

for review in reviews_2020:
    purchase_id = review['purchase_id']
    book_id = purchase_id.replace('purchaseid_', 'bookid_')
    if book_id in book_dict:
        rating = float(review['rating'])
        book_ratings[book_id].append(rating)

# Filter books with avg rating >= 4.5
results = []
for book_id, ratings in book_ratings.items():
    if len(ratings) > 0:
        avg_rating = sum(ratings) / len(ratings)
        if avg_rating >= 4.5:
            book = book_dict[book_id]
            author_name = 'Unknown'
            if book['author'] != 'None':
                author_name = book['author']
            results.append({
                'title': book['title'],
                'author': author_name,
                'average_rating': round(avg_rating, 2),
                'review_count': len(ratings)
            })

results = sorted(results, key=lambda x: (-x['average_rating'], -x['review_count']))

print('__RESULT__:')
print(json.dumps(results))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review'], 'var_functions.query_db:7': [], 'var_functions.execute_python:12': ['var_functions.list_db:0', 'var_functions.query_db:2', 'var_functions.list_db:5', 'var_functions.query_db:7'], 'var_functions.query_db:14': [{'categories': '["Books", "Literature & Fiction", "History & Criticism"]'}, {'categories': '["Books", "Reference", "Words, Language & Grammar"]'}, {'categories': '["Books", "Biographies & Memoirs", "Leaders & Notable People"]'}, {'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'categories': '["Books", "Mystery, Thriller & Suspense", "Thrillers & Suspense"]'}, {'categories': '["Books", "Arts & Photography", "History & Criticism"]'}, {'categories': '["Books", "Parenting & Relationships", "Parenting"]'}, {'categories': '["Books", "Engineering & Transportation", "Engineering"]'}, {'categories': '["Books", "Literature & Fiction", "Genre Fiction"]'}, {'categories': '["Books", "Education & Teaching", "Schools & Teaching"]'}], 'var_functions.query_db:18': 'file_storage/functions.query_db:18.json', 'var_functions.query_db:20': 'file_storage/functions.query_db:20.json', 'var_functions.query_db:24': 'file_storage/functions.query_db:24.json', 'var_functions.query_db:26': 'file_storage/functions.query_db:26.json', 'var_functions.query_db:28': 'file_storage/functions.query_db:28.json', 'var_functions.execute_python:30': ['var_functions.query_db:2', 'var_functions.query_db:7', 'var_functions.query_db:14', 'var_functions.query_db:18', 'var_functions.query_db:20', 'var_functions.query_db:24', 'var_functions.query_db:26', 'var_functions.query_db:28'], 'var_functions.query_db:32': 'file_storage/functions.query_db:32.json', 'var_functions.query_db:33': 'file_storage/functions.query_db:33.json', 'var_functions.execute_python:36': {'books_key': 'var_functions.query_db:32', 'reviews_key': 'var_functions.query_db:33', 'all_keys': [{'var_functions.query_db:2': 'file_storage/functions.query_db:2.json'}, {'var_functions.query_db:18': 'file_storage/functions.query_db:18.json'}, {'var_functions.query_db:20': 'file_storage/functions.query_db:20.json'}, {'var_functions.query_db:24': 'file_storage/functions.query_db:24.json'}, {'var_functions.query_db:26': 'file_storage/functions.query_db:26.json'}]}, 'var_functions.execute_python:38': ['var_functions.query_db:2', 'var_functions.query_db:18', 'var_functions.query_db:20', 'var_functions.query_db:24', 'var_functions.query_db:26', 'var_functions.query_db:28', 'var_functions.query_db:32', 'var_functions.query_db:33'], 'var_functions.execute_python:40': {'books_count': 25, 'reviews_count': 329, 'sample_book': {'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'author': 'None'}, 'sample_review': {'rating': '5', 'purchase_id': 'purchaseid_8'}}, 'var_functions.execute_python:42': 'file_storage/functions.execute_python:42.json'}

exec(code, env_args)
