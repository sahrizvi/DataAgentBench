code = """import json
import re

# Load data from files
books_file = locals()['var_functions.execute_python:22']
reviews_file = locals()['var_functions.query_db:18']

with open(books_file, 'r') as f:
    books_data = json.load(f)

with open(reviews_file, 'r') as f:
    reviews_data = json.load(f)

print(f'Books: {len(books_data)}, Reviews: {len(reviews_data)}')

# Create mapping: numeric_id -> book info (including decade)
book_map = {}
for book in books_data:
    book_map[book['numeric_id']] = book

print(f'Book map created with {len(book_map)} entries')
print(f'Sample book map: {list(book_map.items())[:3]}')

# Process reviews and match with books
matched_reviews = []
for review in reviews_data:
    # Extract numeric ID from purchase_id
    match = re.search(r'purchaseid_(\d+)', review['purchase_id'])
    if match:
        purchase_num_id = int(match.group(1))
        # Look up the book
        if purchase_num_id in book_map:
            book = book_map[purchase_num_id]
            matched_reviews.append({
                'book_id': book['book_id'],
                'numeric_id': purchase_num_id,
                'decade': book['decade'],
                'rating': float(review['rating'])
            })

print(f'Matched reviews: {len(matched_reviews)}')
print(f'Sample matched: {matched_reviews[:5]}')

# Group by decade and calculate stats
from collections import defaultdict

decade_stats = defaultdict(lambda: {'books': set(), 'total_rating': 0, 'count': 0})

for review in matched_reviews:
    decade = review['decade']
    decade_stats[decade]['books'].add(review['book_id'])
    decade_stats[decade]['total_rating'] += review['rating']
    decade_stats[decade]['count'] += 1

# Calculate averages and filter decades with at least 10 distinct books
decade_results = []
for decade, stats in decade_stats.items():
    num_books = len(stats['books'])
    if num_books >= 10:
        avg_rating = stats['total_rating'] / stats['count']
        decade_results.append({
            'decade': decade,
            'avg_rating': avg_rating,
            'num_books': num_books,
            'total_reviews': stats['count']
        })

# Sort by average rating descending
decade_results.sort(key=lambda x: x['avg_rating'], reverse=True)

print(f'Decades with >=10 books: {len(decade_results)}')
for result in decade_results:
    print(f"{result['decade']}: avg={result['avg_rating']:.3f}, books={result['num_books']}, reviews={result['total_reviews']}")

# Return the top result
top_decade = decade_results[0] if decade_results else None
result_json = json.dumps(top_decade)
print('__RESULT__:')
print(result_json)"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:4': [{'book_id': 'bookid_1', 'title': 'Chaucer', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'title': 'Notes from a Kidwatcher', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'title': 'Service: A Navy SEAL at War', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'title': 'Parker & Knight', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}, {'book_id': 'bookid_6', 'title': 'Writings from a Black Woman Living in the Land of the "Free": Strength, Power, Resilience', 'details': 'This book, published independently on December 30, 2021, is written in English and consists of 24 pages. It has an ISBN 13 of 979-8528537702 and weighs 3.2 ounces. The dimensions of the book are 7 x 0.06 x 9 inches.'}, {'book_id': 'bookid_7', 'title': "Child Development: A Practitioner's Guide:2nd (Second) edition", 'details': 'The book, published by Guilford in its second edition in January 2004, is also noted as the 8082nd edition from January 1, 1994. It has a remarkably light item weight of just 0.01 ounces.'}, {'book_id': 'bookid_8', 'title': 'Make: Electronics: Learning Through Discovery', 'details': 'This book, published by Make Community, LLC, in its second edition on September 22, 2015, is available in English and spans 352 pages in paperback format. It has an ISBN of 9781680450262 for the 10-digit version and 978-1680450262 for the 13-digit version. The content is suitable for readers aged 11 to 17 years. The book weighs 2.91 pounds and its dimensions are 8 inches in width, 0.5 inches in thickness, and 10 inches in height.'}, {'book_id': 'bookid_9', 'title': 'Reunion: The Children of Lauderdale Park', 'details': 'This book, published independently on September 25, 2019, is written in English and spans 367 pages. It is available in paperback format and has an ISBN-10 of 1694621731 and an ISBN-13 of 978-1694621733. The item weighs 1.38 pounds and measures 6 x 0.92 x 9 inches.'}, {'book_id': 'bookid_10', 'title': 'Four Centuries of American Education', 'details': 'This book, published by WallBuilder Press in its first edition on November 8, 2004, is available in English and comprises 51 pages in paperback format. It has an ISBN-10 of 1932225323 and an ISBN-13 of 978-1932225327, with a total item weight of 3.52 ounces.'}], 'var_functions.query_db:6': 'file_storage/functions.query_db:6.json', 'var_functions.query_db:8': 'file_storage/functions.query_db:8.json', 'var_functions.query_db:10': 'file_storage/functions.query_db:10.json', 'var_functions.execute_python:16': 'file_storage/functions.execute_python:16.json', 'var_functions.query_db:18': 'file_storage/functions.query_db:18.json', 'var_functions.query_db:20': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_functions.execute_python:22': 'file_storage/functions.execute_python:22.json'}

exec(code, env_args)
