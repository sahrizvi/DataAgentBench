code = """import json
import re
from collections import defaultdict, Counter

# Get file paths from variables
books_file = None
reviews_file = None

for key, value in locals().items():
    if isinstance(value, str) and value.endswith('.json'):
        if 'books' in value or 'query_db:34' in key:
            books_file = value
        else:
            reviews_file = value

# Load data
with open(books_file, 'r') as f:
    books = json.load(f)

with open(reviews_file, 'r') as f:
    reviews = json.load(f)

# Map books to decades
book_to_decade = {}
decade_counts = Counter()

for book in books:
    details = book.get('details', '')
    book_id = book.get('book_id', '')
    
    # Find first valid year
    year = None
    for y in re.findall(r'(\d{4})', details):
        y_int = int(y)
        if 1900 <= y_int <= 2023:
            year = y_int
            break
    
    if year is None:
        continue
    
    decade = str(year // 10 * 10) + 's'
    
    # Get numeric book ID
    id_match = re.search(r'bookid_(\d+)', book_id)
    if id_match:
        numeric_id = id_match.group(1)
        book_to_decade[numeric_id] = decade
        decade_counts[decade] += 1

# Aggregate ratings by decade
ratings_by_decade = defaultdict(list)
books_by_decade = defaultdict(set)
matched_reviews = 0

for review in reviews:
    purchase_id = review.get('purchase_id', '')
    rating = review.get('rating', '0')
    
    id_match = re.search(r'purchaseid_(\d+)', purchase_id)
    if id_match:
        numeric_id = id_match.group(1)
        if numeric_id in book_to_decade:
            try:
                rating_val = float(rating)
                if 1 <= rating_val <= 5:
                    decade = book_to_decade[numeric_id]
                    ratings_by_decade[decade].append(rating_val)
                    books_by_decade[decade].add(numeric_id)
                    matched_reviews += 1
            except:
                pass

# Find decade with highest average rating (at least 10 books)
best_decade = None
best_avg_rating = 0
best_num_books = 0
best_num_reviews = 0

for decade in ratings_by_decade:
    num_books = len(books_by_decade[decade])
    if num_books >= 10:
        ratings = ratings_by_decade[decade]
        avg_rating = sum(ratings) / len(ratings)
        if avg_rating > best_avg_rating:
            best_avg_rating = avg_rating
            best_decade = decade
            best_num_books = num_books
            best_num_reviews = len(ratings)

result = {
    'decade': best_decade,
    'avg_rating': round(best_avg_rating, 3),
    'num_books': best_num_books,
    'num_reviews': best_num_reviews
}

print('__RESULT__:')
print(json.dumps(result))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.query_db:6': 'file_storage/functions.query_db:6.json', 'var_functions.execute_python:8': {'books_count': 10, 'sample_book': {'title': 'Chaucer', 'subtitle': 'Hardcover – Import, January 1, 2004', 'author': '{"avatar": "https://m.media-amazon.com/images/I/21Je2zja9pL._SY600_.jpg", "name": "Peter Ackroyd", "about": ["Peter Ackroyd, (born 5 October 1949) is an English biographer, novelist and critic with a particular interest in the history and culture of London. For his novels about English history and culture and his biographies of, among others, William Blake, Charles Dickens, T. S. Eliot and Sir Thomas More, he won the Somerset Maugham Award and two Whitbread Awards. He is noted for the volume of work he has produced, the range of styles therein, his skill at assuming different voices and the depth of his research.", "He was elected a fellow of the Royal Society of Literature in 1984 and appointed a Commander of the Order of the British Empire in 2003.", "Bio from Wikipedia, the free encyclopedia."]}', 'rating_number': '29', 'features': '[]', 'description': '[]', 'price': '8.23', 'store': 'Peter Ackroyd (Author)', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'book_id': 'bookid_1', 'published_year': 2004, 'decade': '2000s'}}, 'var_functions.execute_python:12': {'eligible_decades': [], 'best_decade': None}, 'var_functions.query_db:16': [{'book_id': 'bookid_1'}, {'book_id': 'bookid_2'}, {'book_id': 'bookid_3'}, {'book_id': 'bookid_4'}, {'book_id': 'bookid_5'}], 'var_functions.execute_python:28': {'decade': None, 'avg_rating': 0}, 'var_functions.query_db:30': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}, {'book_id': 'bookid_6', 'details': 'This book, published independently on December 30, 2021, is written in English and consists of 24 pages. It has an ISBN 13 of 979-8528537702 and weighs 3.2 ounces. The dimensions of the book are 7 x 0.06 x 9 inches.'}, {'book_id': 'bookid_7', 'details': 'The book, published by Guilford in its second edition in January 2004, is also noted as the 8082nd edition from January 1, 1994. It has a remarkably light item weight of just 0.01 ounces.'}, {'book_id': 'bookid_8', 'details': 'This book, published by Make Community, LLC, in its second edition on September 22, 2015, is available in English and spans 352 pages in paperback format. It has an ISBN of 9781680450262 for the 10-digit version and 978-1680450262 for the 13-digit version. The content is suitable for readers aged 11 to 17 years. The book weighs 2.91 pounds and its dimensions are 8 inches in width, 0.5 inches in thickness, and 10 inches in height.'}, {'book_id': 'bookid_9', 'details': 'This book, published independently on September 25, 2019, is written in English and spans 367 pages. It is available in paperback format and has an ISBN-10 of 1694621731 and an ISBN-13 of 978-1694621733. The item weighs 1.38 pounds and measures 6 x 0.92 x 9 inches.'}, {'book_id': 'bookid_10', 'details': 'This book, published by WallBuilder Press in its first edition on November 8, 2004, is available in English and comprises 51 pages in paperback format. It has an ISBN-10 of 1932225323 and an ISBN-13 of 978-1932225327, with a total item weight of 3.52 ounces.'}, {'book_id': 'bookid_11', 'details': 'Published by Caxton Press on January 1, 1993, this book is available in English and spans 407 pages. It has an ISBN-10 of 0893011673 and an ISBN-13 of 978-0893011673. Weighing 1.51 pounds, the book measures 6.05 inches in width, 1.14 inches in depth, and 9.03 inches in height.'}, {'book_id': 'bookid_12', 'details': 'This book, published by Lisette Marshall on May 29, 2022, is written in English and is available in paperback, comprising 215 pages. It has an ISBN 10 number of 9083256898 and an ISBN 13 number of 978-9083256894. The item weighs 11.4 ounces and has dimensions of 6 x 0.54 x 9 inches.'}, {'book_id': 'bookid_13', 'details': 'The book, published by Central Avenue Publishing on January 24, 2023, is available in English and comes in paperback format, consisting of 144 pages. It has an ISBN-10 number of 1771682760 and an ISBN-13 number of 978-1771682763. The item weighs 5.1 ounces and has dimensions of 5.25 x 0.4 x 8 inches.'}, {'book_id': 'bookid_14', 'details': 'The book, published by Jessica Mathews, LLC on November 13, 2019, is written in English and features a paperback format comprising 26 pages. It has an ISBN-10 of 1087848539 and an ISBN-13 of 978-1087848532. Suitable for readers aged 3 to 8 years, it is appropriate for students in Kindergarten through 3rd grade. The item weighs 3.03 ounces and has dimensions of 8.5 x 0.05 x 11 inches.'}, {'book_id': 'bookid_15', 'details': 'The book is published by Kegan Paul and is a first edition released on November 15, 2000. It is written in English and is available in hardcover, comprising 348 pages. The ISBN-10 for this edition is 0710306911, while the ISBN-13 is 978-0710306913. The item weighs 2.23 pounds and has dimensions of 5.5 x 1.25 x 8.5 inches.'}, {'book_id': 'bookid_16', 'details': 'This book is published by Prentice Hall College Division and is in its third edition, released on January 1, 1997. It is written in English and is available in paperback, consisting of 390 pages. The ISBN-10 for this book is 0130840963, while the ISBN-13 is 978-0130840967. The item weighs 1.3 pounds and has dimensions of 7.01 x 0.67 x 9.17 inches.'}, {'book_id': 'bookid_17', 'details': 'This book, published by Edelsa Grupo Didascalia in a September 1, 1987 edition, is written in Spanish and consists of 44 pages. It has an ISBN-10 number of 8477110190 and an ISBN-13 number of 978-8477110194. The item weighs 2.05 ounces and has dimensions of 5.12 x 0.16 x 7.48 inches.'}, {'book_id': 'bookid_18', 'details': 'The book, published by Gale, Sabin Americana on February 21, 2012, is written in English and is available in paperback format, comprising 26 pages. It has an ISBN-10 of 1275627234 and an ISBN-13 of 978-1275627239. The item weighs 2.4 ounces and has dimensions of 7.44 x 0.05 x 9.69 inches.'}, {'book_id': 'bookid_19', 'details': "The book, published by Foundation Press in its 2013th edition on March 22, 2013, is available in English and spans 355 pages. It has an ISBN-10 number of 1609303687 and an ISBN-13 number of 978-1609303686. Weighing 1.5 pounds, the book's dimensions are 7 inches in width, 0.5 inches in thickness, and 9.75 inches in height."}, {'book_id': 'bookid_20', 'details': 'The book, published by Soho Crime in a revised edition on July 1, 2003, is available in English and has a total print length of 372 pages. It has a file size of 2295 KB and supports various features such as Text to Speech, a screen reader, enhanced typesetting, X-Ray, Word Wise, and sticky notes on Kindle Scribe.'}], 'var_functions.query_db:32': [{'total_books': '200'}], 'var_functions.query_db:34': 'file_storage/functions.query_db:34.json', 'var_functions.query_db:36': [{'review_count': '1833'}], 'var_functions.execute_python:40': {'best_decade': None, 'all_eligible': []}, 'var_functions.execute_python:42': {'decade': '2010s', 'avg_rating': 4.333, 'num_books': 88, 'num_reviews': 9}, 'var_functions.query_db:44': 'file_storage/functions.query_db:44.json'}

exec(code, env_args)
