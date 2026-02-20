code = """import json
import re

# Access the stored results using the exact keys provided
lit_fiction_books = var_functions.query_db__10
all_reviews = var_functions.query_db__11

# Extract the numeric IDs for books and map to book data
books_dict = {}
english_lit_books = []

for book in lit_fiction_books:
    match = re.search(r'bookid_(\d+)', book['book_id'])
    if match:
        book_num = int(match.group(1))
        books_dict[book_num] = {
            'book_id': book['book_id'],
            'title': book['title'],
            'categories': book['categories'],
            'details': book['details']
        }
        
        # Check if it's an English book (in Literature & Fiction category and English language)
        if 'English' in book['details']:
            english_lit_books.append(book)

# Process reviews to find those with perfect 5.0 average
review_ratings = {}
for review in all_reviews:
    match = re.search(r'purchaseid_(\d+)', review['purchase_id'])
    if match:
        purchase_num = int(match.group(1))
        rating = float(review['rating'])
        
        if purchase_num not in review_ratings:
            review_ratings[purchase_num] = []
        review_ratings[purchase_num].append(rating)

# Find English Literature & Fiction books with perfect 5.0 average
perfect_english_books = []
for i, book in enumerate(english_lit_books):
    match = re.search(r'bookid_(\d+)', book['book_id'])
    if match:
        book_num = int(match.group(1))
        if book_num in review_ratings:
            ratings = review_ratings[book_num]
            avg_rating = sum(ratings) / len(ratings)
            if abs(avg_rating - 5.0) < 0.001:  # Check for perfect 5.0
                perfect_english_books.append({
                    'book_id': book['book_id'],
                    'title': book['title'],
                    'categories': book['categories'],
                    'details': book['details'],
                    'avg_rating': round(avg_rating, 2),
                    'review_count': len(ratings)
                })

# Sort by title for consistent output
perfect_english_books.sort(key=lambda x: x['title'])

print('__RESULT__:')
print(json.dumps(perfect_english_books, indent=2))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:1': ['review'], 'var_functions.query_db:4': [{'book_id': 'bookid_1', 'title': 'Chaucer', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'title': 'Notes from a Kidwatcher', 'categories': '["Books", "Reference", "Words, Language & Grammar"]', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'title': 'Service: A Navy SEAL at War', 'categories': '["Books", "Biographies & Memoirs", "Leaders & Notable People"]', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'title': 'Parker & Knight', 'categories': '["Books", "Mystery, Thriller & Suspense", "Thrillers & Suspense"]', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_functions.query_db:5': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_functions.query_db:10': 'file_storage/functions.query_db:10.json', 'var_functions.query_db:11': 'file_storage/functions.query_db:11.json', 'var_functions.query_db:12': [{'book_id': 'bookid_1', 'title': 'Chaucer', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_9', 'title': 'Reunion: The Children of Lauderdale Park', 'categories': '["Books", "Literature & Fiction", "Genre Fiction"]', 'details': 'This book, published independently on September 25, 2019, is written in English and spans 367 pages. It is available in paperback format and has an ISBN-10 of 1694621731 and an ISBN-13 of 978-1694621733. The item weighs 1.38 pounds and measures 6 x 0.92 x 9 inches.'}, {'book_id': 'bookid_13', 'title': 'Girl Made of Glass', 'categories': '["Books", "Literature & Fiction", "Poetry"]', 'details': 'The book, published by Central Avenue Publishing on January 24, 2023, is available in English and comes in paperback format, consisting of 144 pages. It has an ISBN-10 number of 1771682760 and an ISBN-13 number of 978-1771682763. The item weighs 5.1 ounces and has dimensions of 5.25 x 0.4 x 8 inches.'}, {'book_id': 'bookid_30', 'title': 'Sugary Sweets (A Taste of Love Series)', 'categories': '["Books", "Literature & Fiction", "Humor & Satire"]', 'details': 'This book, published by CreateSpace Independent Publishing Platform on August 18, 2016, is written in English and is available in paperback, consisting of 140 pages. It has an ISBN-10 of 1536832286 and an ISBN-13 of 978-1536832280. The item weighs 6.6 ounces and its dimensions are 5.51 x 0.33 x 8.5 inches.'}, {'book_id': 'bookid_36', 'title': 'Therapy Mammals', 'categories': '["Books", "Literature & Fiction", "Genre Fiction"]', 'details': 'This book, published by Rare Bird Books as part of the Barnacle Books series on June 12, 2018, is written in English and consists of 376 pages. It has an ISBN-10 of 194557299X and an ISBN-13 of 978-1945572999. Weighing 12.8 ounces, its dimensions are 5.5 x 1 x 8.5 inches.'}, {'book_id': 'bookid_37', 'title': "A Most Dangerous Book: Tacitus's Germania from the Roman Empire to the Third Reich", 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'details': 'This illustrated edition, published by W. W. Norton & Company on May 2, 2011, is available in English and features a hardcover format comprising 304 pages. The book has an ISBN-10 of 0393062651 and an ISBN-13 of 978-0393062656. It weighs 1.03 pounds and has dimensions of 5.8 x 1.1 x 8.6 inches.'}, {'book_id': 'bookid_38', 'title': 'The Prophet: With Original 1923 Illustrations by the Author', 'categories': '["Books", "Literature & Fiction", "Poetry"]', 'details': 'The book, published by Suzeteo Enterprises on February 14, 2019, is available in English and consists of 48 pages. It has an ISBN-10 of 1947844938 and an ISBN-13 of 978-1947844933. The Lexile measure for this book is 990L. Weighing 2.08 ounces, its dimensions are 5 inches in width, 0.1 inches in thickness, and 8 inches in height.'}, {'book_id': 'bookid_39', 'title': 'The Melancholy Strumpet Master', 'categories': '["Books", "Literature & Fiction", "Humor & Satire"]', 'details': 'This book, published independently on February 19, 2023, is written in English and spans 257 pages in paperback format. It has an ISBN 13 of 979-8378201969 and weighs 14.1 ounces. The dimensions of the book are 5.5 x 0.65 x 8.5 inches.'}, {'book_id': 'bookid_44', 'title': 'Reptilian', 'categories': '["Books", "Literature & Fiction", "Genre Fiction"]', 'details': 'This book was published on January 2, 2019, and is available in English. The file size is 1532 KB, and it allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is activated, and sticky notes can be used on Kindle Scribe. The print length of the book is 201 pages.'}, {'book_id': 'bookid_49', 'title': 'Primeval: A Journal of the Uncanny - Issue #1', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'details': 'This book, published by Blood Bound Books in its Issue #1 edition on August 31, 2013, is available in English and comprises 102 pages. It has an ISBN-10 number of 1940250064 and an ISBN-13 number of 978-1940250069. The item weighs 5 ounces and its dimensions are 5.5 x 0.24 x 8.5 inches.'}], 'var_functions.query_db:13': [{'purchase_id': 'purchaseid_101', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_105', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_108', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_110', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_114', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_116', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_117', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_118', 'avg_rating': '5.0', 'review_count': '6'}, {'purchase_id': 'purchaseid_12', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_121', 'avg_rating': '5.0', 'review_count': '1'}]}

exec(code, env_args)
