code = """import json
import re

# Load the books data
books_file = var_functions.query_db:2
with open(books_file, 'r') as f:
    books_data = json.load(f)

# Load the reviews data
reviews_file = var_functions.query_db:4
with open(reviews_file, 'r') as f:
    reviews_data = json.load(f)

print(f"Total books in Literature & Fiction category: {len(books_data)}")
print(f"Total reviews: {len(reviews_data)}")

# Extract book IDs for Literature & Fiction books
lit_fiction_books = []
for book in books_data:
    # Check if it's English-language (looking for "written in English" in details)
    if 'written in English' in book.get('details', ''):
        lit_fiction_books.append({
            'book_id': book['book_id'],
            'title': book['title'],
            'categories': book['categories'],
            'details': book['details']
        })

print(f"English-language Literature & Fiction books: {len(lit_fiction_books)}")

# Create a mapping of book_id to reviews
book_reviews = {}
for review in reviews_data:
    purchase_id = review['purchase_id']
    rating = float(review['rating'])
    
    # Extract the numeric part from purchase_id (e.g., "purchaseid_186" -> "186")
    match = re.match(r'purchaseid_(\d+)', purchase_id)
    if match:
        book_num = match.group(1)
        # Map to book_id format
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
        avg_rating = sum(ratings) / len(ratings)
        
        # Check if perfect 5.0 rating
        if abs(avg_rating - 5.0) < 0.001:  # Floating point comparison
            perfect_books.append({
                'title': book['title'],
                'book_id': book_id,
                'average_rating': avg_rating,
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
