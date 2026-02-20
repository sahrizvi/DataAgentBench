code = """import json
import os

# Access the stored result using locals()
books_file_path = locals()['var_functions.query_db:5']

print(f"File path: {books_file_path}")

# Load the data from file
with open(books_file_path, 'r') as f:
    books_data = json.load(f)

print(f"Total books in Literature & Fiction: {len(books_data)}")

# Analyze rating_number field
ratings = []
for book in books_data:
    try:
        rating = float(book.get('rating_number', 0))
        ratings.append(rating)
    except (ValueError, TypeError):
        continue

print(f"Unique rating values: {sorted(set(ratings))}")
print(f"Sample books with their ratings:")
for i, book in enumerate(books_data[:5]):
    print(f"  {book['title']}: {book['rating_number']}")

# Filter books with perfect 5.0 rating
perfect_books = [book for book in books_data if str(book.get('rating_number', '')).strip() == '5.0']

print(f"\nBooks with exactly 5.0 rating: {len(perfect_books)}")
for book in perfect_books:
    print(f"  - {book['title']} (ID: {book['book_id']}, Rating: {book['rating_number']})")

__RESULT__:
print(f"Preliminary analysis complete")"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json'}

exec(code, env_args)
