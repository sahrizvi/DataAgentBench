code = """import json
import os

# Load books data
books_file = "file_storage/functions.query_db:32.json"
reviews_file = "file_storage/functions.query_db:33.json"

with open(books_file, 'r') as f:
    books = json.load(f)

with open(reviews_file, 'r') as f:
    reviews = json.load(f)

print('__RESULT__:')
print(json.dumps({
    "books_count": len(books),
    "reviews_count": len(reviews),
    "sample_book": books[0] if books else None,
    "sample_review": reviews[0] if reviews else None
}))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review'], 'var_functions.query_db:7': [], 'var_functions.execute_python:12': ['var_functions.list_db:0', 'var_functions.query_db:2', 'var_functions.list_db:5', 'var_functions.query_db:7'], 'var_functions.query_db:14': [{'categories': '["Books", "Literature & Fiction", "History & Criticism"]'}, {'categories': '["Books", "Reference", "Words, Language & Grammar"]'}, {'categories': '["Books", "Biographies & Memoirs", "Leaders & Notable People"]'}, {'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'categories': '["Books", "Mystery, Thriller & Suspense", "Thrillers & Suspense"]'}, {'categories': '["Books", "Arts & Photography", "History & Criticism"]'}, {'categories': '["Books", "Parenting & Relationships", "Parenting"]'}, {'categories': '["Books", "Engineering & Transportation", "Engineering"]'}, {'categories': '["Books", "Literature & Fiction", "Genre Fiction"]'}, {'categories': '["Books", "Education & Teaching", "Schools & Teaching"]'}], 'var_functions.query_db:18': 'file_storage/functions.query_db:18.json', 'var_functions.query_db:20': 'file_storage/functions.query_db:20.json', 'var_functions.query_db:24': 'file_storage/functions.query_db:24.json', 'var_functions.query_db:26': 'file_storage/functions.query_db:26.json', 'var_functions.query_db:28': 'file_storage/functions.query_db:28.json', 'var_functions.execute_python:30': ['var_functions.query_db:2', 'var_functions.query_db:7', 'var_functions.query_db:14', 'var_functions.query_db:18', 'var_functions.query_db:20', 'var_functions.query_db:24', 'var_functions.query_db:26', 'var_functions.query_db:28'], 'var_functions.query_db:32': 'file_storage/functions.query_db:32.json', 'var_functions.query_db:33': 'file_storage/functions.query_db:33.json', 'var_functions.execute_python:36': {'books_key': 'var_functions.query_db:32', 'reviews_key': 'var_functions.query_db:33', 'all_keys': [{'var_functions.query_db:2': 'file_storage/functions.query_db:2.json'}, {'var_functions.query_db:18': 'file_storage/functions.query_db:18.json'}, {'var_functions.query_db:20': 'file_storage/functions.query_db:20.json'}, {'var_functions.query_db:24': 'file_storage/functions.query_db:24.json'}, {'var_functions.query_db:26': 'file_storage/functions.query_db:26.json'}]}, 'var_functions.execute_python:38': ['var_functions.query_db:2', 'var_functions.query_db:18', 'var_functions.query_db:20', 'var_functions.query_db:24', 'var_functions.query_db:26', 'var_functions.query_db:28', 'var_functions.query_db:32', 'var_functions.query_db:33']}

exec(code, env_args)
