code = """import json
import pandas as pd
import re

# Read the full data from the stored files
books_file = var_functions.query_db:20
reviews_file = var_functions.query_db:18

# Read the full data
if isinstance(books_file, str) and books_file.endswith('.json'):
    with open(books_file, 'r') as f:
        books_data = json.load(f)
else:
    books_data = books_file

if isinstance(reviews_file, str) and reviews_file.endswith('.json'):
    with open(reviews_file, 'r') as f:
        reviews_data = json.load(f)
else:
    reviews_data = reviews_file

# Convert to DataFrames
books_df = pd.DataFrame(books_data)
reviews_df = pd.DataFrame(reviews_data)

# Filter for Literature & Fiction books (categories is stored as a string representation of list)
lit_fiction_books = []
for _, book in books_df.iterrows():
    try:
        categories_str = book['categories']
        # Parse the string representation of list
        if isinstance(categories_str, str) and 'Literature & Fiction' in categories_str:
            # Check if it's written in English
            details = str(book.get('details', ''))
            if 'English' in details:
                lit_fiction_books.append({
                    'book_id': book['book_id'],
                    'title': book['title'],
                    'details': details
                })
    except:
        continue

lit_fiction_df = pd.DataFrame(lit_fiction_books)

# Check sample data
print('__RESULT__:')
print(f"Total Literature & Fiction books in English: {len(lit_fiction_df)}")
print(f"Sample books: {lit_fiction_df.head().to_dict(orient='records')}")
print(f"Sample reviews: {reviews_df.head().to_dict(orient='records')}")"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:4': [{'title': 'Chaucer', 'subtitle': 'Hardcover – Import, January 1, 2004', 'author': '{"avatar": "https://m.media-amazon.com/images/I/21Je2zja9pL._SY600_.jpg", "name": "Peter Ackroyd", "about": ["Peter Ackroyd, (born 5 October 1949) is an English biographer, novelist and critic with a particular interest in the history and culture of London. For his novels about English history and culture and his biographies of, among others, William Blake, Charles Dickens, T. S. Eliot and Sir Thomas More, he won the Somerset Maugham Award and two Whitbread Awards. He is noted for the volume of work he has produced, the range of styles therein, his skill at assuming different voices and the depth of his research.", "He was elected a fellow of the Royal Society of Literature in 1984 and appointed a Commander of the Order of the British Empire in 2003.", "Bio from Wikipedia, the free encyclopedia."]}', 'rating_number': '29', 'features': '[]', 'description': '[]', 'price': '8.23', 'store': 'Peter Ackroyd (Author)', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'book_id': 'bookid_1'}], 'var_functions.list_db:6': ['review'], 'var_functions.query_db:12': 'file_storage/functions.query_db:12.json', 'var_functions.query_db:14': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_functions.query_db:16': 'file_storage/functions.query_db:16.json', 'var_functions.query_db:18': 'file_storage/functions.query_db:18.json', 'var_functions.query_db:20': 'file_storage/functions.query_db:20.json'}

exec(code, env_args)
