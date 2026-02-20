code = """import json
import re

# Access stored results using locals() with the correct key format
book_years_path = locals()['var_functions.query_db:10']
reviews_path = locals()['var_functions.query_db:16']

with open(book_years_path, 'r') as f:
    book_years = json.load(f)

with open(reviews_path, 'r') as f:
    reviews = json.load(f)

# Calculate decades
decade_stats = {}

for book in book_years:
    book_id = book['book_id']
    year = int(book['publication_year'])
    
    # Skip invalid years
    if year < 1900 or year > 2023:
        continue
        
    decade = (year // 10) * 10
    
    if decade not in decade_stats:
        decade_stats[decade] = {'books': set(), 'ratings': []}
    
    decade_stats[decade]['books'].add(book_id)

# Now process reviews
purchase_to_bookid = {}
for book in book_years:
    purchase_id = book['book_id'].replace('bookid_', 'purchaseid_')
    purchase_to_bookid[purchase_id] = book['book_id']

for review in reviews:
    purchase_id = review['purchase_id']
    rating = float(review['rating'])
    
    # Find corresponding book_id
    if purchase_id in purchase_to_bookid:
        book_id = purchase_to_bookid[purchase_id]
        
        # Find the book's decade
        for book in book_years:
            if book['book_id'] == book_id:
                year = int(book['publication_year'])
                
                if year < 1900 or year > 2023:
                    continue
                    
                decade = (year // 10) * 10
                
                if decade in decade_stats:
                    decade_stats[decade]['ratings'].append(rating)
                break

# Now filter decades with at least 10 distinct books and calculate average rating
decade_results = []
for decade, stats in decade_stats.items():
    distinct_books = len(stats['books'])
    if distinct_books >= 10 and len(stats['ratings']) > 0:
        avg_rating = sum(stats['ratings']) / len(stats['ratings'])
        decade_results.append({
            'decade': f"{decade}s",
            'average_rating': avg_rating,
            'distinct_books': distinct_books,
            'total_ratings': len(stats['ratings'])
        })

# Sort by average rating descending
decade_results.sort(key=lambda x: x['average_rating'], reverse=True)

print('__RESULT__:')
print(json.dumps(decade_results[:10], indent=2))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.query_db:6': [{'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}, {'book_id': 'bookid_6', 'details': 'This book, published independently on December 30, 2021, is written in English and consists of 24 pages. It has an ISBN 13 of 979-8528537702 and weighs 3.2 ounces. The dimensions of the book are 7 x 0.06 x 9 inches.'}, {'book_id': 'bookid_7', 'details': 'The book, published by Guilford in its second edition in January 2004, is also noted as the 8082nd edition from January 1, 1994. It has a remarkably light item weight of just 0.01 ounces.'}, {'book_id': 'bookid_8', 'details': 'This book, published by Make Community, LLC, in its second edition on September 22, 2015, is available in English and spans 352 pages in paperback format. It has an ISBN of 9781680450262 for the 10-digit version and 978-1680450262 for the 13-digit version. The content is suitable for readers aged 11 to 17 years. The book weighs 2.91 pounds and its dimensions are 8 inches in width, 0.5 inches in thickness, and 10 inches in height.'}, {'book_id': 'bookid_9', 'details': 'This book, published independently on September 25, 2019, is written in English and spans 367 pages. It is available in paperback format and has an ISBN-10 of 1694621731 and an ISBN-13 of 978-1694621733. The item weighs 1.38 pounds and measures 6 x 0.92 x 9 inches.'}, {'book_id': 'bookid_10', 'details': 'This book, published by WallBuilder Press in its first edition on November 8, 2004, is available in English and comprises 51 pages in paperback format. It has an ISBN-10 of 1932225323 and an ISBN-13 of 978-1932225327, with a total item weight of 3.52 ounces.'}, {'book_id': 'bookid_12', 'details': 'This book, published by Lisette Marshall on May 29, 2022, is written in English and is available in paperback, comprising 215 pages. It has an ISBN 10 number of 9083256898 and an ISBN 13 number of 978-9083256894. The item weighs 11.4 ounces and has dimensions of 6 x 0.54 x 9 inches.'}], 'var_functions.query_db:8': 'file_storage/functions.query_db:8.json', 'var_functions.query_db:10': 'file_storage/functions.query_db:10.json', 'var_functions.query_db:12': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}, {'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_76', 'rating': '5'}, {'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_115', 'rating': '5'}, {'purchase_id': 'purchaseid_167', 'rating': '2'}], 'var_functions.query_db:16': 'file_storage/functions.query_db:16.json', 'var_functions.execute_python:18': ['var_functions.list_db:0', 'var_functions.list_db:2', 'var_functions.query_db:5', 'var_functions.query_db:6', 'var_functions.query_db:8', 'var_functions.query_db:10', 'var_functions.query_db:12', 'var_functions.query_db:16']}

exec(code, env_args)
