code = """import json
import re
from collections import defaultdict

# Load books data
books_path_key = None
reviews_path_key = None

for key in list(locals().keys()):
    if 'query_db:5' in key:
        books_path_key = key
    elif 'query_db:6' in key:
        reviews_path_key = key

if not books_path_key or not reviews_path_key:
    print("Could not find data paths")
    exit(1)

books_path = locals()[books_path_key]
reviews_path = locals()[reviews_path_key]

with open(books_path, 'r') as f:
    books_data = json.load(f)

with open(reviews_path, 'r') as f:
    reviews_data = json.load(f)

# Extract decades from books
book_decade = {}
decade_book_count = {}

for book in books_data:
    details = book.get('details', '')
    book_id = book.get('book_id', '')
    
    year_match = re.search(r'(\d{4})', details)
    if year_match:
        year = int(year_match.group(1))
        decade = str(year // 10 * 10) + 's'
        
        # Extract numeric ID
        id_match = re.search(r'\d+', book_id)
        if id_match:
            numeric_id = id_match.group()
            book_decade[numeric_id] = decade
            decade_book_count[decade] = decade_book_count.get(decade, 0) + 1

# Aggregate ratings by decade
decade_ratings = defaultdict(list)
decade_unique_books = defaultdict(set)

for review in reviews_data:
    purchase_id = review.get('purchase_id', '')
    rating = review.get('rating', '0')
    
    id_match = re.search(r'\d+', purchase_id)
    if id_match:
        numeric_id = id_match.group()
        if numeric_id in book_decade:
            try:
                rating_val = float(rating)
                decade = book_decade[numeric_id]
                decade_ratings[decade].append(rating_val)
                decade_unique_books[decade].add(numeric_id)
            except:
                pass

# Find decade with highest average rating (min 10 books)
best_decade = None
best_avg = 0

for decade in decade_ratings:
    if len(decade_unique_books[decade]) >= 10:
        avg_rating = sum(decade_ratings[decade]) / len(decade_ratings[decade])
        if avg_rating > best_avg:
            best_avg = avg_rating
            best_decade = decade

result = {'decade': best_decade, 'avg_rating': round(best_avg, 3)} if best_decade else {'decade': None, 'avg_rating': 0}

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.query_db:6': 'file_storage/functions.query_db:6.json', 'var_functions.execute_python:8': {'books_count': 10, 'sample_book': {'title': 'Chaucer', 'subtitle': 'Hardcover – Import, January 1, 2004', 'author': '{"avatar": "https://m.media-amazon.com/images/I/21Je2zja9pL._SY600_.jpg", "name": "Peter Ackroyd", "about": ["Peter Ackroyd, (born 5 October 1949) is an English biographer, novelist and critic with a particular interest in the history and culture of London. For his novels about English history and culture and his biographies of, among others, William Blake, Charles Dickens, T. S. Eliot and Sir Thomas More, he won the Somerset Maugham Award and two Whitbread Awards. He is noted for the volume of work he has produced, the range of styles therein, his skill at assuming different voices and the depth of his research.", "He was elected a fellow of the Royal Society of Literature in 1984 and appointed a Commander of the Order of the British Empire in 2003.", "Bio from Wikipedia, the free encyclopedia."]}', 'rating_number': '29', 'features': '[]', 'description': '[]', 'price': '8.23', 'store': 'Peter Ackroyd (Author)', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'book_id': 'bookid_1', 'published_year': 2004, 'decade': '2000s'}}, 'var_functions.execute_python:12': {'eligible_decades': [], 'best_decade': None}, 'var_functions.query_db:16': [{'book_id': 'bookid_1'}, {'book_id': 'bookid_2'}, {'book_id': 'bookid_3'}, {'book_id': 'bookid_4'}, {'book_id': 'bookid_5'}]}

exec(code, env_args)
