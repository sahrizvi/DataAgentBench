code = """import json
import re
import pandas as pd

# Load data
with open(locals()['var_function-call-7590782948468719994'], 'r') as f:
    books = json.load(f)

with open(locals()['var_function-call-5850723410427978002'], 'r') as f:
    reviews = json.load(f)

# Helper to extract year
def extract_year(text):
    if not text:
        return None
    # Regex for "Month Day, Year" or "Month Year"
    # We prioritize the first occurrence
    match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(?:\d{1,2},\s)?(\d{4})', text)
    if match:
        return int(match.group(2))
    return None

# Helper to normalize ID
# bookid_XX -> XX
# purchaseid_XX -> XX
def normalize_id(id_str):
    if '_' in id_str:
        return id_str.split('_')[1]
    return id_str

# Process books
book_years = {}
for b in books:
    bid = normalize_id(b['book_id'])
    y = extract_year(b['details'])
    if y:
        book_years[bid] = y

# Process reviews and aggregate
decade_stats = {} # decade -> {'books': set(), 'ratings': []}

for r in reviews:
    pid = normalize_id(r['purchase_id'])
    rating = float(r['rating'])
    
    if pid in book_years:
        year = book_years[pid]
        decade_start = (year // 10) * 10
        decade = f"{decade_start}s"
        
        if decade not in decade_stats:
            decade_stats[decade] = {'books': set(), 'ratings': []}
        
        decade_stats[decade]['books'].add(pid)
        decade_stats[decade]['ratings'].append(rating)

# Filter and find max
results = []
for dec, stats in decade_stats.items():
    if len(stats['books']) >= 10:
        avg_rating = sum(stats['ratings']) / len(stats['ratings'])
        results.append({'decade': dec, 'avg_rating': avg_rating, 'num_books': len(stats['books'])})

# Sort by avg_rating descending
results.sort(key=lambda x: x['avg_rating'], reverse=True)

print("__RESULT__:")
print(json.dumps(results))"""

env_args = {'var_function-call-6595877591326038469': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-958935905527809359': [{'count': '200'}], 'var_function-call-4679598201093351069': [{'count(*)': '1833'}], 'var_function-call-7590782948468719994': 'file_storage/function-call-7590782948468719994.json', 'var_function-call-5850723410427978002': 'file_storage/function-call-5850723410427978002.json'}

exec(code, env_args)
