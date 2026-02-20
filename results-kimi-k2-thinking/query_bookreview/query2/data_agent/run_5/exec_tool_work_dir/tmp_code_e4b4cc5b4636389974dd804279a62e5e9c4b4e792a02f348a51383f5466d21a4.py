code = """import json
# Get the books data
books_file = 'var_functions.query_db:36'
if books_file in locals():
    books_data = locals()['var_functions.query_db:36']
else:
    books_data = []

if isinstance(books_data, str) and books_data.endswith('.json'):
    with open(books_data, 'r') as f:
        books_data = json.load(f)

# Get review data
reviews_file = 'var_functions.query_db:18'
if reviews_file in locals():
    reviews_data = locals()['var_functions.query_db:18']
else:
    reviews_data = []

if isinstance(reviews_data, str) and reviews_data.endswith('.json'):
    with open(reviews_data, 'r') as f:
        reviews_data = json.load(f)

# Process review data to find perfect 5.0 ratings
review_groups = {}
for review in reviews_data:
    purchase_id = review['purchase_id']
    rating = float(review['rating'])
    if purchase_id not in review_groups:
        review_groups[purchase_id] = []
    review_groups[purchase_id].append(rating)

perfect_books = []
for purchase_id, ratings in review_groups.items():
    avg = sum(ratings) / len(ratings)
    if avg == 5.0:
        # Map purchaseid_X to bookid_X
        book_id = purchase_id.replace('purchaseid', 'bookid')
        perfect_books.append({
            'book_id': book_id,
            'purchase_id': purchase_id,
            'review_count': len(ratings),
            'avg_rating': avg
        })

# Create a lookup for literature books
lit_books_lookup = {}
for book in books_data:
    lit_books_lookup[book['book_id']] = book

# Find intersection
perfect_lit_books = []
for pb in perfect_books:
    if pb['book_id'] in lit_books_lookup:
        book_info = lit_books_lookup[pb['book_id']]
        perfect_lit_books.append({
            'title': book_info['title'],
            'book_id': pb['book_id'],
            'review_count': pb['review_count'],
            'details': book_info['details']
        })

# Format result
result = {
    'found_books': len(perfect_lit_books),
    'books': perfect_lit_books
}

print('__RESULT__:')
print(json.dumps(result, indent=2))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:4': [{'title': 'Chaucer', 'subtitle': 'Hardcover – Import, January 1, 2004', 'author': '{"avatar": "https://m.media-amazon.com/images/I/21Je2zja9pL._SY600_.jpg", "name": "Peter Ackroyd", "about": ["Peter Ackroyd, (born 5 October 1949) is an English biographer, novelist and critic with a particular interest in the history and culture of London. For his novels about English history and culture and his biographies of, among others, William Blake, Charles Dickens, T. S. Eliot and Sir Thomas More, he won the Somerset Maugham Award and two Whitbread Awards. He is noted for the volume of work he has produced, the range of styles therein, his skill at assuming different voices and the depth of his research.", "He was elected a fellow of the Royal Society of Literature in 1984 and appointed a Commander of the Order of the British Empire in 2003.", "Bio from Wikipedia, the free encyclopedia."]}', 'rating_number': '29', 'features': '[]', 'description': '[]', 'price': '8.23', 'store': 'Peter Ackroyd (Author)', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'book_id': 'bookid_1'}], 'var_functions.list_db:6': ['review'], 'var_functions.query_db:12': 'file_storage/functions.query_db:12.json', 'var_functions.query_db:14': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_functions.query_db:16': 'file_storage/functions.query_db:16.json', 'var_functions.query_db:18': 'file_storage/functions.query_db:18.json', 'var_functions.query_db:20': 'file_storage/functions.query_db:20.json', 'var_functions.execute_python:26': 'Test successful', 'var_functions.query_db:28': [{'book_count': '200'}], 'var_functions.query_db:30': 'file_storage/functions.query_db:30.json', 'var_functions.execute_python:34': {'total_unique_books': 200, 'perfect_rating_books': 83, 'perfect_ids_sample': ['purchaseid_83', 'purchaseid_38', 'purchaseid_7', 'purchaseid_6', 'purchaseid_174']}, 'var_functions.query_db:36': 'file_storage/functions.query_db:36.json'}

exec(code, env_args)
