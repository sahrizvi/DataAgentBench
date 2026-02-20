code = """import json
import re
from collections import defaultdict

# Read full datasets
books_file_path = locals()['var_functions.query_db:6']
reviews_file_path = locals()['var_functions.query_db:14']

with open(books_file_path, 'r') as f:
    books = json.load(f)

with open(reviews_file_path, 'r') as f:
    reviews = json.load(f)

# Extract publication decade from books
year_pattern = r'(\d{4})'
books_dict = {}

for book in books:
    details = book.get('details', '')
    book_id = book.get('book_id', '')
    
    # Extract numeric ID from book_id
    book_num_match = re.search(r'bookid_(\d+)', book_id, re.IGNORECASE)
    book_num = int(book_num_match.group(1)) if book_num_match else None
    
    # Find publication year
    years = re.findall(year_pattern, details)
    pub_year = None
    for year in years:
        year_int = int(year)
        if 1900 <= year_int <= 2023:
            pub_year = year_int
            break
    
    if pub_year and book_num:
        decade = f"{pub_year//10*10}s"
        books_dict[book_num] = {
            'book_id': book_id,
            'pub_year': pub_year,
            'decade': decade
        }

# Process reviews - group by book number
reviews_by_book = defaultdict(list)

for review in reviews:
    purchase_id = review.get('purchase_id', '')
    rating = review.get('rating')
    
    # Extract numeric ID from purchase_id
    pur_num_match = re.search(r'purchaseid_(\d+)', purchase_id, re.IGNORECASE)
    pur_num = int(pur_num_match.group(1)) if pur_num_match else None
    
    # Convert rating to float
    try:
        rating_float = float(rating) if rating is not None else None
    except (ValueError, TypeError):
        rating_float = None
    
    if pur_num and rating_float is not None and pur_num in books_dict:
        reviews_by_book[pur_num].append(rating_float)

# Calculate average rating per book and then per decade
book_ratings = {}
for book_num, ratings in reviews_by_book.items():
    if ratings:
        book_ratings[book_num] = sum(ratings) / len(ratings)

# Group books by decade and calculate average rating per decade
decade_stats = defaultdict(lambda: {'books': [], 'ratings': [], 'count': 0})

for book_num, avg_rating in book_ratings.items():
    if book_num in books_dict:
        decade = books_dict[book_num]['decade']
        decade_stats[decade]['books'].append(book_num)
        decade_stats[decade]['ratings'].append(avg_rating)
        decade_stats[decade]['count'] += 1

# Calculate decade averages
results = []
for decade, stats in decade_stats.items():
    if stats['count'] >= 10:  # At least 10 distinct books
        avg_rating = sum(stats['ratings']) / len(stats['ratings'])
        results.append({
            'decade': decade,
            'avg_rating': round(avg_rating, 3),
            'book_count': stats['count'],
            'total_ratings': len(stats['ratings'])
        })

# Sort by average rating descending
results_sorted = sorted(results, key=lambda x: x['avg_rating'], reverse=True)

print('__RESULT__:')
print(json.dumps({
    'decade_rankings': results_sorted,
    'decades_considered': len(results_sorted),
    'total_books_matched': len(book_ratings)
}))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': [{'title': 'Chaucer', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'book_id': 'bookid_1'}, {'title': 'Notes from a Kidwatcher', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.', 'categories': '["Books", "Reference", "Words, Language & Grammar"]', 'book_id': 'bookid_2'}, {'title': 'Service: A Navy SEAL at War', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.', 'categories': '["Books", "Biographies & Memoirs", "Leaders & Notable People"]', 'book_id': 'bookid_3'}, {'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]', 'book_id': 'bookid_4'}, {'title': 'Parker & Knight', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.', 'categories': '["Books", "Mystery, Thriller & Suspense", "Thrillers & Suspense"]', 'book_id': 'bookid_5'}], 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.query_db:6': 'file_storage/functions.query_db:6.json', 'var_functions.execute_python:10': {'total_books': 200, 'books_with_years': 190, 'sample_books': [{'book_id': 'bookid_1', 'pub_year': 2004, 'decade': '2000s'}, {'book_id': 'bookid_2', 'pub_year': 1996, 'decade': '1990s'}, {'book_id': 'bookid_3', 'pub_year': 2012, 'decade': '2010s'}, {'book_id': 'bookid_4', 'pub_year': 2013, 'decade': '2010s'}, {'book_id': 'bookid_5', 'pub_year': 2014, 'decade': '2010s'}, {'book_id': 'bookid_6', 'pub_year': 2021, 'decade': '2020s'}, {'book_id': 'bookid_7', 'pub_year': 2004, 'decade': '2000s'}, {'book_id': 'bookid_8', 'pub_year': 2015, 'decade': '2010s'}, {'book_id': 'bookid_9', 'pub_year': 2019, 'decade': '2010s'}, {'book_id': 'bookid_10', 'pub_year': 2004, 'decade': '2000s'}]}, 'var_functions.list_db:12': ['review'], 'var_functions.query_db:14': 'file_storage/functions.query_db:14.json', 'var_functions.execute_python:16': 'file_storage/functions.execute_python:16.json', 'var_functions.execute_python:18': {'total_books': 200, 'total_reviews': 1833, 'sample_books': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}], 'sample_reviews': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}]}, 'var_functions.execute_python:20': {'books_with_decades': 190, 'valid_reviews': 1833, 'sample_books': [{'book_num': 1, 'book_id': 'bookid_1', 'pub_year': 2004, 'decade': '2000s'}, {'book_num': 2, 'book_id': 'bookid_2', 'pub_year': 1996, 'decade': '1990s'}, {'book_num': 3, 'book_id': 'bookid_3', 'pub_year': 2012, 'decade': '2010s'}, {'book_num': 4, 'book_id': 'bookid_4', 'pub_year': 2013, 'decade': '2010s'}, {'book_num': 5, 'book_id': 'bookid_5', 'pub_year': 2014, 'decade': '2010s'}], 'sample_reviews': [{'pur_num': 186, 'purchase_id': 'purchaseid_186', 'rating': 4.0}, {'pur_num': 191, 'purchase_id': 'purchaseid_191', 'rating': 4.0}, {'pur_num': 190, 'purchase_id': 'purchaseid_190', 'rating': 4.0}, {'pur_num': 8, 'purchase_id': 'purchaseid_8', 'rating': 5.0}, {'pur_num': 178, 'purchase_id': 'purchaseid_178', 'rating': 4.0}]}}

exec(code, env_args)
