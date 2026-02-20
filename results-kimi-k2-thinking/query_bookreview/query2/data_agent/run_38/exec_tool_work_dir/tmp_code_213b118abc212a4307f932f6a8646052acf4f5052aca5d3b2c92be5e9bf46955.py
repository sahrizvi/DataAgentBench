code = """import json

# Access the books data from storage
books_data = locals().get('var_functions.query_db:2', [])

# Access the reviews data from storage  
reviews_data = locals().get('var_functions.query_db:4', [])

print(f"Books data type: {type(books_data)}")
print(f"Books data length: {len(books_data) if books_data else 'None'}")

print(f"Reviews data type: {type(reviews_data)}")
print(f"Reviews data length: {len(reviews_data) if reviews_data else 'None'}")

# If the data is actually file paths, let's check that
if isinstance(books_data, str) and '.json' in books_data:
    print(f"Books is a file path: {books_data}")
    with open(books_data, 'r') as f:
        books_content = json.load(f)
    print(f"Loaded books from file: {len(books_content)} records")
else:
    books_content = books_data

if isinstance(reviews_data, str) and '.json' in reviews_data:
    print(f"Reviews is a file path: {reviews_data}")
    with open(reviews_data, 'r') as f:
        reviews_content = json.load(f)
    print(f"Loaded reviews from file: {len(reviews_content)} records")
else:
    reviews_content = reviews_data

# Now let's do the actual analysis
import re

# Filter for English books in Literature & Fiction
english_lit_books = []
for book in books_content:
    if 'written in English' in book.get('details', ''):
        english_lit_books.append({
            'book_id': book['book_id'],
            'title': book['title']
        })

print(f"English Literature & Fiction books: {len(english_lit_books)}")

# Map reviews to books
book_ratings = {}
for review in reviews_content:
    purchase_id = review.get('purchase_id', '')
    rating = float(review.get('rating', 0))
    
    match = re.match(r'purchaseid_(\d+)', purchase_id)
    if match:
        book_id = f'bookid_{match.group(1)}'
        if book_id not in book_ratings:
            book_ratings[book_id] = []
        book_ratings[book_id].append(rating)

print(f"Books with reviews: {len(book_ratings)}")

# Find perfect 5.0 books
perfect_books = []
for book in english_lit_books:
    book_id = book['book_id']
    if book_id in book_ratings:
        ratings = book_ratings[book_id]
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            if abs(avg_rating - 5.0) < 0.001:
                perfect_books.append({
                    'title': book['title'],
                    'book_id': book_id,
                    'average_rating': round(avg_rating, 2),
                    'review_count': len(ratings)
                })

# Sort by review count
perfect_books.sort(key=lambda x: x['review_count'], reverse=True)

print(f"Perfect 5.0 rating books: {len(perfect_books)}")
result = json.dumps(perfect_books, indent=2)

print('__RESULT__:')
print(result)"""

env_args = {'var_functions.query_db:0': 'file_storage/functions.query_db:0.json', 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:4': 'file_storage/functions.query_db:4.json'}

exec(code, env_args)
