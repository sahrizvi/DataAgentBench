code = """import json
import re
from collections import defaultdict

# Load English Literature & Fiction books and reviews from the stored variables
books = locals()['var_functions.query_db:32']
reviews = locals()['var_functions.query_db:24']

print(f'Number of books: {len(books)}')
print(f'Number of reviews: {len(reviews)}')

# Extract numeric IDs for books
books_numeric = {}
for book in books:
    book_id = book['book_id']
    match = re.search(r'(\d+)', book_id)
    if match:
        num_id = int(match.group(1))
        books_numeric[num_id] = book

# Compute average rating per numeric purchase_id
ratings = defaultdict(list)
for rev in reviews:
    try:
        rating = float(rev['rating'])
        purchase_id = rev['purchase_id']
        match = re.search(r'(\d+)', purchase_id)
        if match:
            num_id = int(match.group(1))
            ratings[num_id].append(rating)
    except Exception as e:
        continue

# Compute averages
averages = {pid: (sum(vals)/len(vals) if vals else 0.0) for pid, vals in ratings.items()}

print(f'Books with numeric IDs: {len(books_numeric)}')
print(f'Purchase IDs with reviews: {len(averages)}')
print(f'Sample averages: {list(averages.items())[:10]}')

# Check some book IDs that might have 5.0 ratings
perfect_books = []
for num_id, avg in averages.items():
    if abs(avg - 5.0) < 1e-9:
        if num_id in books_numeric:
            book = books_numeric[num_id]
            perfect_books.append({**book, 'average_rating': avg, 'review_count': len(ratings[num_id])})
        else:
            print(f"Found perfect rating for purchaseid_{num_id} but no matching bookid_{num_id}")

print(f'Perfect 5.0 rating books: {len(perfect_books)}')
for b in perfect_books:
    print(f"  - {b['title']} (ID: {b['book_id']}, Reviews: {b['review_count']})")

# Let's also check books with some reviews to understand the distribution
books_with_reviews = []
for num_id, book in books_numeric.items():
    if num_id in averages:
        avg = averages[num_id]
        review_count = len(ratings[num_id])
        books_with_reviews.append({
            'book_id': book['book_id'],
            'title': book['title'],
            'average_rating': avg,
            'review_count': review_count
        })

# Sort by review count descending to see most reviewed books
books_with_reviews.sort(key=lambda x: x['review_count'], reverse=True)
print(f'\nTop 10 most reviewed books:')
for b in books_with_reviews[:10]:
    print(f"  - {b['title']}: {b['average_rating']:.2f} ({b['review_count']} reviews)")

# Check if any have exactly 5.0
perfect = [b for b in books_with_reviews if abs(b['average_rating'] - 5.0) < 1e-9]
print(f'\nBooks with exactly 5.0 average rating: {len(perfect)}')
for b in perfect:
    print(f"  - {b['title']} (ID: {b['book_id']}, Reviews: {b['review_count']})")

# Output result
print('__RESULT__:')
print(json.dumps(perfect))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:4': [{'book_id': 'bookid_1', 'title': 'Chaucer', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'title': 'Notes from a Kidwatcher', 'categories': '["Books", "Reference", "Words, Language & Grammar"]', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'title': 'Service: A Navy SEAL at War', 'categories': '["Books", "Biographies & Memoirs", "Leaders & Notable People"]', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'title': 'Parker & Knight', 'categories': '["Books", "Mystery, Thriller & Suspense", "Thrillers & Suspense"]', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}, {'book_id': 'bookid_6', 'title': 'Writings from a Black Woman Living in the Land of the "Free": Strength, Power, Resilience', 'categories': '["Books", "Arts & Photography", "History & Criticism"]', 'details': 'This book, published independently on December 30, 2021, is written in English and consists of 24 pages. It has an ISBN 13 of 979-8528537702 and weighs 3.2 ounces. The dimensions of the book are 7 x 0.06 x 9 inches.'}, {'book_id': 'bookid_7', 'title': "Child Development: A Practitioner's Guide:2nd (Second) edition", 'categories': '["Books", "Parenting & Relationships", "Parenting"]', 'details': 'The book, published by Guilford in its second edition in January 2004, is also noted as the 8082nd edition from January 1, 1994. It has a remarkably light item weight of just 0.01 ounces.'}, {'book_id': 'bookid_8', 'title': 'Make: Electronics: Learning Through Discovery', 'categories': '["Books", "Engineering & Transportation", "Engineering"]', 'details': 'This book, published by Make Community, LLC, in its second edition on September 22, 2015, is available in English and spans 352 pages in paperback format. It has an ISBN of 9781680450262 for the 10-digit version and 978-1680450262 for the 13-digit version. The content is suitable for readers aged 11 to 17 years. The book weighs 2.91 pounds and its dimensions are 8 inches in width, 0.5 inches in thickness, and 10 inches in height.'}, {'book_id': 'bookid_9', 'title': 'Reunion: The Children of Lauderdale Park', 'categories': '["Books", "Literature & Fiction", "Genre Fiction"]', 'details': 'This book, published independently on September 25, 2019, is written in English and spans 367 pages. It is available in paperback format and has an ISBN-10 of 1694621731 and an ISBN-13 of 978-1694621733. The item weighs 1.38 pounds and measures 6 x 0.92 x 9 inches.'}, {'book_id': 'bookid_10', 'title': 'Four Centuries of American Education', 'categories': '["Books", "Education & Teaching", "Schools & Teaching"]', 'details': 'This book, published by WallBuilder Press in its first edition on November 8, 2004, is available in English and comprises 51 pages in paperback format. It has an ISBN-10 of 1932225323 and an ISBN-13 of 978-1932225327, with a total item weight of 3.52 ounces.'}], 'var_functions.list_db:6': ['review'], 'var_functions.query_db:8': 'file_storage/functions.query_db:8.json', 'var_functions.query_db:10': 'file_storage/functions.query_db:10.json', 'var_functions.query_db:12': 'file_storage/functions.query_db:12.json', 'var_functions.query_db:14': 'file_storage/functions.query_db:14.json', 'var_functions.query_db:16': 'file_storage/functions.query_db:16.json', 'var_functions.query_db:18': 'file_storage/functions.query_db:18.json', 'var_functions.query_db:20': 'file_storage/functions.query_db:20.json', 'var_functions.query_db:24': 'file_storage/functions.query_db:24.json', 'var_functions.query_db:26': 'file_storage/functions.query_db:26.json', 'var_functions.list_db:30': ['books_info'], 'var_functions.query_db:32': [{'book_id': 'bookid_1', 'title': 'Chaucer'}, {'book_id': 'bookid_9', 'title': 'Reunion: The Children of Lauderdale Park'}, {'book_id': 'bookid_13', 'title': 'Girl Made of Glass'}, {'book_id': 'bookid_30', 'title': 'Sugary Sweets (A Taste of Love Series)'}, {'book_id': 'bookid_36', 'title': 'Therapy Mammals'}, {'book_id': 'bookid_37', 'title': "A Most Dangerous Book: Tacitus's Germania from the Roman Empire to the Third Reich"}, {'book_id': 'bookid_38', 'title': 'The Prophet: With Original 1923 Illustrations by the Author'}, {'book_id': 'bookid_39', 'title': 'The Melancholy Strumpet Master'}, {'book_id': 'bookid_44', 'title': 'Reptilian'}, {'book_id': 'bookid_49', 'title': 'Primeval: A Journal of the Uncanny - Issue #1'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)'}, {'book_id': 'bookid_69', 'title': 'Out of Sheer Rage: Wrestling with D. H. Lawrence'}, {'book_id': 'bookid_70', 'title': 'Polly and the Shadow Goblin: Book 2, Mother of Witches'}, {'book_id': 'bookid_74', 'title': 'Child Of The King A Journey of Hope Book 1: Earthly Story With A Heavenly Message'}, {'book_id': 'bookid_77', 'title': 'One September Morning'}, {'book_id': 'bookid_82', 'title': 'Fire Cracker'}, {'book_id': 'bookid_84', 'title': 'Local Honey'}, {'book_id': 'bookid_89', 'title': "I'll Ride For My Hood: A Salty Love Story"}, {'book_id': 'bookid_92', 'title': 'Outage'}, {'book_id': 'bookid_93', 'title': 'Simantov'}, {'book_id': 'bookid_98', 'title': 'Hollywood Confessions: Hollywood Headlines Book #3 (Hollywood Headlines Mysteries)'}, {'book_id': 'bookid_99', 'title': 'Buddy the Soldier Bear'}, {'book_id': 'bookid_101', 'title': 'Knowing When To Die: Uncollected Stories'}, {'book_id': 'bookid_106', 'title': 'Looking for Peyton Place: A Novel'}, {'book_id': 'bookid_109', 'title': 'All the Way to the Gallows'}, {'book_id': 'bookid_111', 'title': 'Can You Buy Me The Wind?'}, {'book_id': 'bookid_122', 'title': 'Childe Harold of Dysna'}, {'book_id': 'bookid_137', 'title': 'Oligarchy'}, {'book_id': 'bookid_142', 'title': 'The Jordan Tracks'}, {'book_id': 'bookid_144', 'title': 'Forged in Blood (Freehold)'}, {'book_id': 'bookid_161', 'title': "Time's Demon: BOOK II OF THE ISLEVALE CYCLE"}, {'book_id': 'bookid_167', 'title': 'Dead Silence'}, {'book_id': 'bookid_171', 'title': 'Exits, Desires, & Slow Fires'}, {'book_id': 'bookid_177', 'title': 'Kennebago Moments'}, {'book_id': 'bookid_179', 'title': 'A Cherry Cola Christmas (A Cherry Cola Book Club Novel)'}, {'book_id': 'bookid_180', 'title': 'The Sludge'}, {'book_id': 'bookid_182', 'title': 'Liza of Lambeth'}, {'book_id': 'bookid_187', 'title': 'Consort (A Dark(ish) Faerie Tale Book 3)'}, {'book_id': 'bookid_188', 'title': "The Vampyre and Other Tales of the Macabre (Oxford World's Classics)"}, {'book_id': 'bookid_195', 'title': 'Something That Feels Like Truth (Switchgrass Books)'}], 'var_functions.execute_python:34': [], 'var_functions.execute_python:36': []}

exec(code, env_args)
