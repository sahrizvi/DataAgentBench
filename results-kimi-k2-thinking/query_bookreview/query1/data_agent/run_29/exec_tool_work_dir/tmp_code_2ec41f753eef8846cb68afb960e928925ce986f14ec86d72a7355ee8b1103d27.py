code = """import json
import re

# Load the full books data file
books_path = locals()['var_functions.query_db:5']
with open(books_path, 'r', encoding='utf-8') as f:
    books_data = json.load(f)

# Load the reviews data
reviews_path = locals()['var_functions.query_db:6']
with open(reviews_path, 'r', encoding='utf-8') as f:
    reviews_data = json.load(f)

print(f"Total books loaded: {len(books_data)}")
print(f"Total reviews loaded: {len(reviews_data)}")

# Extract year from details field using multiple patterns
pattern1 = r'published on\s+(?:[^,]+,\s*)?(\d{4})'
pattern2 = r'released on\s+(?:[^,]+,\s*)?(\d{4})'
pattern3 = r'first edition[^\d]*(\d{4})'
pattern4 = r'(?:January|February|March|April|May|June|July|August|September|October|November|December)[^\d]*(\d{4})'

books_with_years = []
year_counts = {}

for book in books_data:
    details = book.get('details', '')
    year = None
    
    for pattern in [pattern1, pattern2, pattern3, pattern4]:
        match = re.search(pattern, details, re.IGNORECASE)
        if match:
            year = int(match.group(1))
            break
    
    if year and 1900 <= year <= 2023:
        book['published_year'] = year
        decade = str(year//10*10) + 's'
        book['decade'] = decade
        books_with_years.append(book)
        year_counts[decade] = year_counts.get(decade, 0) + 1

print(f"Books with valid publication years: {len(books_with_years)}")

# Show decade distribution
print("Decade distribution:")
for decade in sorted(year_counts.keys()):
    count = year_counts[decade]
    print(f"  {decade}: {count} books")

# Create mapping from book_id to decade
book_to_decade = {}
for book in books_with_years:
    book_to_decade[book['book_id']] = book['decade']

# Match reviews to books and aggregate ratings by decade
decade_ratings = {}
decade_books = {}
for decade in year_counts.keys():
    decade_ratings[decade] = []
    decade_books[decade] = set()

matched_reviews = 0
for review in reviews_data:
    purchase_id = review.get('purchase_id')
    if purchase_id and purchase_id in book_to_decade:
        try:
            rating = float(review.get('rating', 0))
            if rating > 0:
                decade = book_to_decade[purchase_id]
                decade_ratings[decade].append(rating)
                decade_books[decade].add(purchase_id)
                matched_reviews += 1
        except (ValueError, TypeError):
            continue

print(f"Matched reviews to books: {matched_reviews}")

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

print("Decades with at least 10 books:")
for r in results:
    print(f"  {r['decade']}: avg rating {r['avg_rating']}, {r['num_books']} books, {r['num_reviews']} reviews")

best_decade = results[0] if results else None
if best_decade:
    print(f"Best decade: {best_decade['decade']}")

print("__RESULT__:")
print(json.dumps({
    'eligible_decades': results,
    'best_decade': best_decade
}))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.query_db:6': 'file_storage/functions.query_db:6.json', 'var_functions.execute_python:8': {'books_count': 10, 'sample_book': {'title': 'Chaucer', 'subtitle': 'Hardcover – Import, January 1, 2004', 'author': '{"avatar": "https://m.media-amazon.com/images/I/21Je2zja9pL._SY600_.jpg", "name": "Peter Ackroyd", "about": ["Peter Ackroyd, (born 5 October 1949) is an English biographer, novelist and critic with a particular interest in the history and culture of London. For his novels about English history and culture and his biographies of, among others, William Blake, Charles Dickens, T. S. Eliot and Sir Thomas More, he won the Somerset Maugham Award and two Whitbread Awards. He is noted for the volume of work he has produced, the range of styles therein, his skill at assuming different voices and the depth of his research.", "He was elected a fellow of the Royal Society of Literature in 1984 and appointed a Commander of the Order of the British Empire in 2003.", "Bio from Wikipedia, the free encyclopedia."]}', 'rating_number': '29', 'features': '[]', 'description': '[]', 'price': '8.23', 'store': 'Peter Ackroyd (Author)', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'book_id': 'bookid_1', 'published_year': 2004, 'decade': '2000s'}}}

exec(code, env_args)
