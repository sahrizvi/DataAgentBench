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

# Sample some book_ids and purchase_ids to understand the format
print("Sample book_ids from books_data:")
for i, book in enumerate(books_data[:5]):
    print(f"  {book.get('book_id')}")

print("\nSample purchase_ids from reviews_data:")
for i, review in enumerate(reviews_data[:5]):
    print(f"  {review.get('purchase_id')}")

# Extract numeric IDs
book_numeric_ids = {}
for book in books_data:
    book_id = book.get('book_id', '')
    match = re.search(r'bookid_(\d+)', book_id)
    if match:
        book_numeric_ids[match.group(1)] = book

review_numeric_ids = {}
for review in reviews_data:
    purchase_id = review.get('purchase_id', '')
    match = re.search(r'purchaseid_(\d+)', purchase_id)
    if match:
        review_numeric_ids[match.group(1)] = review

print(f"\nBooks with numeric IDs: {len(book_numeric_ids)}")
print(f"Reviews with numeric IDs: {len(review_numeric_ids)}")

# Check for matching numeric IDs
matching_ids = set(book_numeric_ids.keys()) & set(review_numeric_ids.keys())
print(f"Matching numeric IDs: {len(matching_ids)}")

# Show some examples
if matching_ids:
    print("\nSample matching IDs:")
    for idx in list(matching_ids)[:3]:
        print(f"  ID: {idx}")
        print(f"    Book: {book_numeric_ids[idx].get('title')}")
        print(f"    Review rating: {review_numeric_ids[idx].get('rating')}")

print("__RESULT__:")
print(json.dumps({
    'book_numeric_ids_count': len(book_numeric_ids),
    'review_numeric_ids_count': len(review_numeric_ids),
    'matching_ids_count': len(matching_ids),
    'sample_match': list(matching_ids)[:3] if matching_ids else []
}))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.query_db:6': 'file_storage/functions.query_db:6.json', 'var_functions.execute_python:8': {'books_count': 10, 'sample_book': {'title': 'Chaucer', 'subtitle': 'Hardcover – Import, January 1, 2004', 'author': '{"avatar": "https://m.media-amazon.com/images/I/21Je2zja9pL._SY600_.jpg", "name": "Peter Ackroyd", "about": ["Peter Ackroyd, (born 5 October 1949) is an English biographer, novelist and critic with a particular interest in the history and culture of London. For his novels about English history and culture and his biographies of, among others, William Blake, Charles Dickens, T. S. Eliot and Sir Thomas More, he won the Somerset Maugham Award and two Whitbread Awards. He is noted for the volume of work he has produced, the range of styles therein, his skill at assuming different voices and the depth of his research.", "He was elected a fellow of the Royal Society of Literature in 1984 and appointed a Commander of the Order of the British Empire in 2003.", "Bio from Wikipedia, the free encyclopedia."]}', 'rating_number': '29', 'features': '[]', 'description': '[]', 'price': '8.23', 'store': 'Peter Ackroyd (Author)', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'book_id': 'bookid_1', 'published_year': 2004, 'decade': '2000s'}}, 'var_functions.execute_python:12': {'eligible_decades': [], 'best_decade': None}}

exec(code, env_args)
