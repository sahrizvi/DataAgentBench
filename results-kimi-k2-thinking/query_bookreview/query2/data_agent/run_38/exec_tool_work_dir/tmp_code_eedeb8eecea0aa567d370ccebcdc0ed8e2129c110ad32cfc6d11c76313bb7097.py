code = """import json
import re

# Load the books data
books_file = var_functions.query_db:2
print(f"Books file path: {books_file}")

with open(books_file, 'r') as f:
    content = f.read()
    print(f"Content type: {type(content)}")
    print(f"Content length: {len(content)}")
    print(f"First 200 chars: {content[:200]}")
    
    # Parse the JSON
    if content.strip().startswith('['):
        # It's a JSON array
        books_data = json.loads(content)
    else:
        # It might be a string representation
        books_data = eval(content)

print(f"Books data type: {type(books_data)}")
print(f"Books data length: {len(books_data)}")

# Load the reviews data
reviews_file = var_functions.query_db:4
print(f"Reviews file path: {reviews_file}")

with open(reviews_file, 'r') as f:
    content = f.read()
    print(f"Content type: {type(content)}")
    print(f"Content length: {len(content)}")
    
    if content.strip().startswith('['):
        reviews_data = json.loads(content)
    else:
        reviews_data = eval(content)

print(f"Reviews data type: {type(reviews_data)}")
print(f"Reviews data length: {len(reviews_data)}")

# Now do the analysis
lit_fiction_books = []
for book in books_data:
    if isinstance(book, dict) and 'written in English' in book.get('details', ''):
        lit_fiction_books.append({
            'book_id': book['book_id'],
            'title': book['title'],
            'categories': book['categories'],
            'details': book['details']
        })

print(f"English Literature & Fiction books: {len(lit_fiction_books)}")

# Create a mapping of book_id to reviews
book_reviews = {}
for review in reviews_data:
    if not isinstance(review, dict):
        continue
        
    purchase_id = review.get('purchase_id', '')
    rating_str = review.get('rating', '0')
    
    try:
        rating = float(rating_str)
    except:
        continue
    
    match = re.match(r'purchaseid_(\d+)', purchase_id)
    if match:
        book_num = match.group(1)
        book_id = f'bookid_{book_num}'
        
        if book_id not in book_reviews:
            book_reviews[book_id] = []
        book_reviews[book_id].append(rating)

print(f"Books with reviews: {len(book_reviews)}")

# Calculate average ratings for Literature & Fiction books
perfect_books = []
for book in lit_fiction_books:
    book_id = book['book_id']
    if book_id in book_reviews:
        ratings = book_reviews[book_id]
        if len(ratings) == 0:
            continue
            
        avg_rating = sum(ratings) / len(ratings)
        
        if abs(avg_rating - 5.0) < 0.001:
            perfect_books.append({
                'title': book['title'],
                'book_id': book_id,
                'average_rating': round(avg_rating, 2),
                'review_count': len(ratings),
                'categories': book['categories']
            })

print(f"Books with perfect 5.0 rating: {len(perfect_books)}")

# Sort by review count (more reviews = more reliable)
perfect_books.sort(key=lambda x: x['review_count'], reverse=True)

# Prepare result
result = json.dumps(perfect_books, indent=2)
print('__RESULT__:')
print(result)"""

env_args = {'var_functions.query_db:0': 'file_storage/functions.query_db:0.json', 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:4': 'file_storage/functions.query_db:4.json'}

exec(code, env_args)
