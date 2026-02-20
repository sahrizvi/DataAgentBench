code = """import json
import re

# Load data
file_books = locals()['var_function-call-17578456053743105324']
file_reviews = locals()['var_function-call-12400972779654688605']

with open(file_books, 'r') as f:
    books_data = json.load(f)
with open(file_reviews, 'r') as f:
    reviews_data = json.load(f)

# Extract years
book_years = {}
for book in books_data:
    bid = book['book_id']
    match = re.search(r'(?:published|released).*?(\d{4})', book.get('details', ''), re.IGNORECASE)
    if match:
        year = int(match.group(1))
        num_id = bid.split('_')[1] if '_' in bid else bid
        book_years[num_id] = year

# Group reviews by book
book_reviews = {} 
for review in reviews_data:
    pid = review['purchase_id']
    num_id = pid.split('_')[1] if '_' in pid else pid
    if num_id in book_years:
        if num_id not in book_reviews:
            book_reviews[num_id] = []
        try:
            r = float(review['rating'])
            book_reviews[num_id].append(r)
        except:
            pass

print("__RESULT__:")
results = []
for decade_start in [1980, 1990, 2000, 2010, 2020]:
    books_in_decade = []
    total_ratings = []
    book_avgs = []
    
    for num_id, year in book_years.items():
        if (year // 10) * 10 == decade_start:
            ratings = book_reviews.get(num_id, [])
            if ratings:
                avg = sum(ratings) / len(ratings)
                books_in_decade.append({'id': num_id, 'avg': avg, 'count': len(ratings)})
                total_ratings.extend(ratings)
                book_avgs.append(avg)
    
    if len(books_in_decade) >= 10:
        avg_all = sum(total_ratings) / len(total_ratings)
        avg_books = sum(book_avgs) / len(book_avgs)
        
        results.append({
            'decade': f"{decade_start}s",
            'n_books': len(books_in_decade),
            'avg_all_reviews': avg_all,
            'avg_of_books': avg_books,
            'top_book_count': max([b['count'] for b in books_in_decade]) if books_in_decade else 0
        })

print(json.dumps(results))"""

env_args = {'var_function-call-4960458581660214722': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-5604823520361681521': [{'count': '200'}], 'var_function-call-13013353557435363717': [{'COUNT(*)': '1833'}], 'var_function-call-17578456053743105324': 'file_storage/function-call-17578456053743105324.json', 'var_function-call-12400972779654688605': 'file_storage/function-call-12400972779654688605.json', 'var_function-call-12629485189769827550': [{'decade': '2020s', 'average_rating': 4.663636363636364, 'book_count': 21}, {'decade': '2010s', 'average_rating': 4.608591885441528, 'book_count': 88}, {'decade': '2000s', 'average_rating': 4.276223776223776, 'book_count': 47}, {'decade': '1980s', 'average_rating': 4.208333333333333, 'book_count': 11}, {'decade': '1990s', 'average_rating': 3.8208955223880596, 'book_count': 16}], 'var_function-call-4120372095613511804': [{'decade': '2010s', 'avg_all_reviews': 4.608591885441528, 'avg_of_books': 4.405139336568189, 'n_books': 88}, {'decade': '2020s', 'avg_all_reviews': 4.663636363636364, 'avg_of_books': 4.52530525030525, 'n_books': 21}, {'decade': '2000s', 'avg_all_reviews': 4.276223776223776, 'avg_of_books': 4.357517513775337, 'n_books': 47}, {'decade': '1990s', 'avg_all_reviews': 3.8208955223880596, 'avg_of_books': 4.124937996031746, 'n_books': 16}, {'decade': '1980s', 'avg_all_reviews': 4.208333333333333, 'avg_of_books': 4.5481993851559075, 'n_books': 11}]}

exec(code, env_args)
