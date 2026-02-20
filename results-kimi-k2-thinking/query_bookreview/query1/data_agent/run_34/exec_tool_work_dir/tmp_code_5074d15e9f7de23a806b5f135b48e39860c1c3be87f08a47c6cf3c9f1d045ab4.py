code = """import json
import re

# Load all books
books_file = locals()['var_functions.query_db:28']
with open(books_file, 'r') as f:
    all_books = json.load(f)

# Load all reviews
reviews_file = locals()['var_functions.query_db:42']
with open(reviews_file, 'r') as f:
    all_reviews = json.load(f)

print(f"Total books: {len(all_books)}")
print(f"Total reviews: {len(all_reviews)}")

# Extract years and create book_id to decade mapping
book_to_decade = {}
books_by_decade = {}

for book in all_books:
    book_id = book['book_id']
    details = book.get('details', '')
    
    year = None
    if details:
        # Pattern 1: Month day, year
        match = re.search(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)[^\d]*\d{1,2}[^\d]*(\d{4})', str(details), re.IGNORECASE)
        if match:
            year = int(match.group(1))
        else:
            # Pattern 2: Any 4-digit year
            match = re.search(r'\b(19\d{2}|20[0-2]\d)\b', str(details))
            if match:
                year = int(match.group(1))
    
    if year and 1900 <= year <= 2023:
        decade = f"{year//10*10}s"
        book_to_decade[book_id] = decade
        
        if decade not in books_by_decade:
            books_by_decade[decade] = set()
        books_by_decade[decade].add(book_id)

print(f"\nBooks with extractable years: {len(book_to_decade)}")
print(f"Decades found: {sorted(books_by_decade.keys())}")

# Aggregate ratings by decade
decade_ratings = {}
decade_review_count = {}

for review in all_reviews:
    purchase_id = review['purchase_id']
    rating = float(review['rating'])
    
    # Extract book_id from purchase_id
    if purchase_id.startswith('purchaseid_'):
        book_id = purchase_id.replace('purchaseid_', 'bookid_')
    else:
        continue
    
    # Check if we have decade info for this book
    if book_id in book_to_decade:
        decade = book_to_decade[book_id]
        
        if decade not in decade_ratings:
            decade_ratings[decade] = []
        decade_ratings[decade].append(rating)
        
        if decade not in decade_review_count:
            decade_review_count[decade] = set()
        decade_review_count[decade].add(book_id)

# Calculate average ratings per decade, filter by at least 10 distinct books
results = []
for decade in decade_ratings:
    distinct_books = len(decade_review_count[decade])
    if distinct_books >= 10:
        avg_rating = sum(decade_ratings[decade]) / len(decade_ratings[decade])
        results.append({
            'decade': decade,
            'avg_rating': avg_rating,
            'distinct_books': distinct_books,
            'total_reviews': len(decade_ratings[decade])
        })

# Sort by average rating descending
results.sort(key=lambda x: x['avg_rating'], reverse=True)

print(f"\nDecades with at least 10 distinct books:")
for r in results:
    print(f"  {r['decade']}: avg={r['avg_rating']:.3f}, books={r['distinct_books']}, reviews={r['total_reviews']}")

# Return the best decade
if results:
    best_decade = results[0]['decade']
else:
    best_decade = "No decade with at least 10 books found"

result = {
    'best_decade': best_decade,
    'all_decades': results
}

print("__RESULT__:")
print(json.dumps(result, indent=2))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review'], 'var_functions.query_db:6': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}, {'book_id': 'bookid_6', 'details': 'This book, published independently on December 30, 2021, is written in English and consists of 24 pages. It has an ISBN 13 of 979-8528537702 and weighs 3.2 ounces. The dimensions of the book are 7 x 0.06 x 9 inches.'}, {'book_id': 'bookid_7', 'details': 'The book, published by Guilford in its second edition in January 2004, is also noted as the 8082nd edition from January 1, 1994. It has a remarkably light item weight of just 0.01 ounces.'}, {'book_id': 'bookid_8', 'details': 'This book, published by Make Community, LLC, in its second edition on September 22, 2015, is available in English and spans 352 pages in paperback format. It has an ISBN of 9781680450262 for the 10-digit version and 978-1680450262 for the 13-digit version. The content is suitable for readers aged 11 to 17 years. The book weighs 2.91 pounds and its dimensions are 8 inches in width, 0.5 inches in thickness, and 10 inches in height.'}, {'book_id': 'bookid_9', 'details': 'This book, published independently on September 25, 2019, is written in English and spans 367 pages. It is available in paperback format and has an ISBN-10 of 1694621731 and an ISBN-13 of 978-1694621733. The item weighs 1.38 pounds and measures 6 x 0.92 x 9 inches.'}, {'book_id': 'bookid_10', 'details': 'This book, published by WallBuilder Press in its first edition on November 8, 2004, is available in English and comprises 51 pages in paperback format. It has an ISBN-10 of 1932225323 and an ISBN-13 of 978-1932225327, with a total item weight of 3.52 ounces.'}], 'var_functions.query_db:8': 'file_storage/functions.query_db:8.json', 'var_functions.execute_python:16': {'total_books': 200, 'books_with_year': 3, 'sample_books': [{'book_id': 'bookid_1', 'publication_year': nan, 'decade': None}, {'book_id': 'bookid_2', 'publication_year': nan, 'decade': None}, {'book_id': 'bookid_3', 'publication_year': nan, 'decade': None}, {'book_id': 'bookid_4', 'publication_year': nan, 'decade': None}, {'book_id': 'bookid_5', 'publication_year': nan, 'decade': None}, {'book_id': 'bookid_6', 'publication_year': nan, 'decade': None}, {'book_id': 'bookid_7', 'publication_year': 2004.0, 'decade': '2000s'}, {'book_id': 'bookid_8', 'publication_year': nan, 'decade': None}, {'book_id': 'bookid_9', 'publication_year': nan, 'decade': None}, {'book_id': 'bookid_10', 'publication_year': nan, 'decade': None}]}, 'var_functions.query_db:22': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}, {'book_id': 'bookid_6', 'details': 'This book, published independently on December 30, 2021, is written in English and consists of 24 pages. It has an ISBN 13 of 979-8528537702 and weighs 3.2 ounces. The dimensions of the book are 7 x 0.06 x 9 inches.'}, {'book_id': 'bookid_7', 'details': 'The book, published by Guilford in its second edition in January 2004, is also noted as the 8082nd edition from January 1, 1994. It has a remarkably light item weight of just 0.01 ounces.'}, {'book_id': 'bookid_8', 'details': 'This book, published by Make Community, LLC, in its second edition on September 22, 2015, is available in English and spans 352 pages in paperback format. It has an ISBN of 9781680450262 for the 10-digit version and 978-1680450262 for the 13-digit version. The content is suitable for readers aged 11 to 17 years. The book weighs 2.91 pounds and its dimensions are 8 inches in width, 0.5 inches in thickness, and 10 inches in height.'}, {'book_id': 'bookid_9', 'details': 'This book, published independently on September 25, 2019, is written in English and spans 367 pages. It is available in paperback format and has an ISBN-10 of 1694621731 and an ISBN-13 of 978-1694621733. The item weighs 1.38 pounds and measures 6 x 0.92 x 9 inches.'}, {'book_id': 'bookid_10', 'details': 'This book, published by WallBuilder Press in its first edition on November 8, 2004, is available in English and comprises 51 pages in paperback format. It has an ISBN-10 of 1932225323 and an ISBN-13 of 978-1932225327, with a total item weight of 3.52 ounces.'}, {'book_id': 'bookid_11', 'details': 'Published by Caxton Press on January 1, 1993, this book is available in English and spans 407 pages. It has an ISBN-10 of 0893011673 and an ISBN-13 of 978-0893011673. Weighing 1.51 pounds, the book measures 6.05 inches in width, 1.14 inches in depth, and 9.03 inches in height.'}, {'book_id': 'bookid_12', 'details': 'This book, published by Lisette Marshall on May 29, 2022, is written in English and is available in paperback, comprising 215 pages. It has an ISBN 10 number of 9083256898 and an ISBN 13 number of 978-9083256894. The item weighs 11.4 ounces and has dimensions of 6 x 0.54 x 9 inches.'}, {'book_id': 'bookid_13', 'details': 'The book, published by Central Avenue Publishing on January 24, 2023, is available in English and comes in paperback format, consisting of 144 pages. It has an ISBN-10 number of 1771682760 and an ISBN-13 number of 978-1771682763. The item weighs 5.1 ounces and has dimensions of 5.25 x 0.4 x 8 inches.'}, {'book_id': 'bookid_14', 'details': 'The book, published by Jessica Mathews, LLC on November 13, 2019, is written in English and features a paperback format comprising 26 pages. It has an ISBN-10 of 1087848539 and an ISBN-13 of 978-1087848532. Suitable for readers aged 3 to 8 years, it is appropriate for students in Kindergarten through 3rd grade. The item weighs 3.03 ounces and has dimensions of 8.5 x 0.05 x 11 inches.'}, {'book_id': 'bookid_15', 'details': 'The book is published by Kegan Paul and is a first edition released on November 15, 2000. It is written in English and is available in hardcover, comprising 348 pages. The ISBN-10 for this edition is 0710306911, while the ISBN-13 is 978-0710306913. The item weighs 2.23 pounds and has dimensions of 5.5 x 1.25 x 8.5 inches.'}, {'book_id': 'bookid_16', 'details': 'This book is published by Prentice Hall College Division and is in its third edition, released on January 1, 1997. It is written in English and is available in paperback, consisting of 390 pages. The ISBN-10 for this book is 0130840963, while the ISBN-13 is 978-0130840967. The item weighs 1.3 pounds and has dimensions of 7.01 x 0.67 x 9.17 inches.'}, {'book_id': 'bookid_17', 'details': 'This book, published by Edelsa Grupo Didascalia in a September 1, 1987 edition, is written in Spanish and consists of 44 pages. It has an ISBN-10 number of 8477110190 and an ISBN-13 number of 978-8477110194. The item weighs 2.05 ounces and has dimensions of 5.12 x 0.16 x 7.48 inches.'}, {'book_id': 'bookid_18', 'details': 'The book, published by Gale, Sabin Americana on February 21, 2012, is written in English and is available in paperback format, comprising 26 pages. It has an ISBN-10 of 1275627234 and an ISBN-13 of 978-1275627239. The item weighs 2.4 ounces and has dimensions of 7.44 x 0.05 x 9.69 inches.'}, {'book_id': 'bookid_19', 'details': "The book, published by Foundation Press in its 2013th edition on March 22, 2013, is available in English and spans 355 pages. It has an ISBN-10 number of 1609303687 and an ISBN-13 number of 978-1609303686. Weighing 1.5 pounds, the book's dimensions are 7 inches in width, 0.5 inches in thickness, and 9.75 inches in height."}, {'book_id': 'bookid_20', 'details': 'The book, published by Soho Crime in a revised edition on July 1, 2003, is available in English and has a total print length of 372 pages. It has a file size of 2295 KB and supports various features such as Text to Speech, a screen reader, enhanced typesetting, X-Ray, Word Wise, and sticky notes on Kindle Scribe.'}], 'var_functions.query_db:28': 'file_storage/functions.query_db:28.json', 'var_functions.query_db:36': 'file_storage/functions.query_db:36.json', 'var_functions.query_db:42': 'file_storage/functions.query_db:42.json'}

exec(code, env_args)
