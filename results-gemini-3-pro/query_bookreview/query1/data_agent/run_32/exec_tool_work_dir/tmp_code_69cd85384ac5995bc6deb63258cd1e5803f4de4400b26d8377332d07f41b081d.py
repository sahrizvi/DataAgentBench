code = """import json
import re

# Load data
with open(locals()['var_function-call-7590782948468719994'], 'r') as f:
    books = json.load(f)

with open(locals()['var_function-call-5850723410427978002'], 'r') as f:
    reviews = json.load(f)

def extract_year(text):
    if not text:
        return None
    match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(?:\d{1,2},\s)?(\d{4})', text)
    if match:
        return int(match.group(2))
    return None

def normalize_id(id_str):
    if '_' in id_str:
        return id_str.split('_')[1]
    return id_str

book_years = {}
for b in books:
    bid = normalize_id(b['book_id'])
    y = extract_year(b['details'])
    if y:
        book_years[bid] = y

# Group reviews by book
book_reviews = {} # bid -> list of ratings
for r in reviews:
    pid = normalize_id(r['purchase_id'])
    rating = float(r['rating'])
    if pid not in book_reviews:
        book_reviews[pid] = []
    book_reviews[pid].append(rating)

# Aggregate by decade
decade_stats = {} # decade -> {'book_avgs': [], 'all_ratings': [], 'book_ids': set()}

for bid, ratings in book_reviews.items():
    if bid in book_years:
        year = book_years[bid]
        decade = f"{(year // 10) * 10}s"
        
        if decade not in decade_stats:
            decade_stats[decade] = {'book_avgs': [], 'all_ratings': [], 'book_ids': set()}
        
        avg_book = sum(ratings) / len(ratings)
        decade_stats[decade]['book_avgs'].append(avg_book)
        decade_stats[decade]['all_ratings'].extend(ratings)
        decade_stats[decade]['book_ids'].add(bid)

results = []
for dec, stats in decade_stats.items():
    if len(stats['book_ids']) >= 10:
        avg_of_reviews = sum(stats['all_ratings']) / len(stats['all_ratings'])
        avg_of_books = sum(stats['book_avgs']) / len(stats['book_avgs'])
        results.append({
            'decade': dec, 
            'avg_of_reviews': avg_of_reviews, 
            'avg_of_books': avg_of_books,
            'num_books': len(stats['book_ids'])
        })

results.sort(key=lambda x: x['avg_of_reviews'], reverse=True)

print("__RESULT__:")
print(json.dumps(results))"""

env_args = {'var_function-call-6595877591326038469': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-958935905527809359': [{'count': '200'}], 'var_function-call-4679598201093351069': [{'count(*)': '1833'}], 'var_function-call-7590782948468719994': 'file_storage/function-call-7590782948468719994.json', 'var_function-call-5850723410427978002': 'file_storage/function-call-5850723410427978002.json', 'var_function-call-7577815354814176917': [{'decade': '2020s', 'avg_rating': 4.663636363636364, 'num_books': 21}, {'decade': '2010s', 'avg_rating': 4.608591885441528, 'num_books': 88}, {'decade': '2000s', 'avg_rating': 4.276223776223776, 'num_books': 47}, {'decade': '1980s', 'avg_rating': 4.208333333333333, 'num_books': 11}, {'decade': '1990s', 'avg_rating': 3.8208955223880596, 'num_books': 16}]}

exec(code, env_args)
