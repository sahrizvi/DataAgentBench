code = """import json
import re

# Load the books data
books_path = locals()['var_functions.query_db:5']
with open(books_path, 'r', encoding='utf-8') as f:
    books_data = json.load(f)

# Load the reviews data
reviews_path = locals()['var_functions.query_db:6']
with open(reviews_path, 'r', encoding='utf-8') as f:
    reviews_data = json.load(f)

print(f"Loaded {len(books_data)} books and {len(reviews_data)} reviews")

# Extract publication year and create decade mapping
book_decade_map = {}
decade_counts = {}

for book in books_data:
    book_id = book.get('book_id', '')
    details = book.get('details', '')
    
    # Extract numeric ID
    id_match = re.search(r'bookid_(\d+)', book_id)
    if not id_match:
        continue
    numeric_id = id_match.group(1)
    
    # Extract year from details
    year = None
    patterns = [
        r'published on[^\d]*(\d{4})',
        r'released on[^\d]*(\d{4})', 
        r'first edition[^\d]*(\d{4})',
        r'(?:January|February|March|April|May|June|July|August|September|October|November|December)[^\d]*(\d{4})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, details, re.IGNORECASE)
        if match:
            year = int(match.group(1))
            break
    
    if year and 1900 <= year <= 2023:
        decade = str(year // 10 * 10) + 's'
        book_decade_map[numeric_id] = decade
        decade_counts[decade] = decade_counts.get(decade, 0) + 1

print(f"Books with valid years: {len(book_decade_map)}")
print(f"Decade distribution: {sorted(decade_counts.items())}")

# Process reviews and aggregate by decade
decade_ratings = {}
decade_books = {}

for review in reviews_data:
    purchase_id = review.get('purchase_id', '')
    rating_str = review.get('rating', '0')
    
    # Extract numeric ID from purchase_id
    id_match = re.search(r'purchaseid_(\d+)', purchase_id)
    if not id_match:
        continue
    numeric_id = id_match.group(1)
    
    # Check if this book has decade info
    if numeric_id not in book_decade_map:
        continue
    
    try:
        rating = float(rating_str)
        if rating <= 0 or rating > 5:
            continue
    except (ValueError, TypeError):
        continue
    
    decade = book_decade_map[numeric_id]
    
    if decade not in decade_ratings:
        decade_ratings[decade] = []
        decade_books[decade] = set()
    
    decade_ratings[decade].append(rating)
    decade_books[decade].add(numeric_id)

print(f"Processed reviews for {len(decade_ratings)} decades")

# Calculate average ratings for decades with at least 10 distinct books
results = []
for decade in sorted(decade_ratings.keys()):
    num_books = len(decade_books[decade])
    num_reviews = len(decade_ratings[decade])
    
    if num_books >= 10 and num_reviews > 0:
        avg_rating = sum(decade_ratings[decade]) / num_reviews
        results.append({
            'decade': decade,
            'avg_rating': round(avg_rating, 3),
            'num_books': num_books,
            'num_reviews': num_reviews
        })

# Sort by average rating descending
results.sort(key=lambda x: x['avg_rating'], reverse=True)

print(f"Found {len(results)} eligible decades")
for r in results:
    print(f"  {r['decade']}: {r['avg_rating']} ({r['num_books']} books, {r['num_reviews']} reviews)")

# Get best decade
best_decade = results[0] if results else None
print(f"Best decade: {best_decade['decade']}")

print("__RESULT__:")
print(json.dumps({
    'best_decade': best_decade,
    'all_eligible': results,
    'total_books_mapped': len(book_decade_map)
}))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.query_db:6': 'file_storage/functions.query_db:6.json', 'var_functions.execute_python:8': {'books_count': 10, 'sample_book': {'title': 'Chaucer', 'subtitle': 'Hardcover – Import, January 1, 2004', 'author': '{"avatar": "https://m.media-amazon.com/images/I/21Je2zja9pL._SY600_.jpg", "name": "Peter Ackroyd", "about": ["Peter Ackroyd, (born 5 October 1949) is an English biographer, novelist and critic with a particular interest in the history and culture of London. For his novels about English history and culture and his biographies of, among others, William Blake, Charles Dickens, T. S. Eliot and Sir Thomas More, he won the Somerset Maugham Award and two Whitbread Awards. He is noted for the volume of work he has produced, the range of styles therein, his skill at assuming different voices and the depth of his research.", "He was elected a fellow of the Royal Society of Literature in 1984 and appointed a Commander of the Order of the British Empire in 2003.", "Bio from Wikipedia, the free encyclopedia."]}', 'rating_number': '29', 'features': '[]', 'description': '[]', 'price': '8.23', 'store': 'Peter Ackroyd (Author)', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'book_id': 'bookid_1', 'published_year': 2004, 'decade': '2000s'}}, 'var_functions.execute_python:12': {'eligible_decades': [], 'best_decade': None}, 'var_functions.query_db:16': [{'book_id': 'bookid_1'}, {'book_id': 'bookid_2'}, {'book_id': 'bookid_3'}, {'book_id': 'bookid_4'}, {'book_id': 'bookid_5'}]}

exec(code, env_args)
