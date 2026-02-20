code = """import json
import re
import pandas as pd

# Load data
with open(locals()['var_function-call-11409792330757935845'], 'r') as f:
    books = json.load(f)

with open(locals()['var_function-call-11409792330757936310'], 'r') as f:
    reviews = json.load(f)

# Regex for date
# Matches "January 1, 2004" or "January 2004"
date_pattern = re.compile(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+(?:\d{1,2},\s+)?(\d{4})')

book_decade_map = {}
book_ids = set()

# Process books
for b in books:
    bid_str = b.get('book_id')
    details = b.get('details', '')
    
    # Extract ID number
    # Assuming format bookid_X
    try:
        bid_num = int(bid_str.split('_')[1])
    except:
        continue
        
    # Extract Year
    match = date_pattern.search(details)
    if match:
        year = int(match.group(1))
        decade = (year // 10) * 10
        decade_str = f"{decade}s"
        book_decade_map[bid_num] = decade_str
        book_ids.add(bid_num)
    else:
        # Try finding just a 4 digit year if specific pattern fails, but be careful
        # details often contains ISBNs which are numbers.
        # Let's rely on the month pattern as it is safer.
        pass

# Process reviews
decade_ratings = {} # decade -> list of ratings
decade_books = {} # decade -> set of book_nums

for r in reviews:
    pid_str = r.get('purchase_id')
    rating_str = r.get('rating')
    
    try:
        pid_num = int(pid_str.split('_')[1])
        rating = float(rating_str)
    except:
        continue
    
    if pid_num in book_decade_map:
        dec = book_decade_map[pid_num]
        
        if dec not in decade_ratings:
            decade_ratings[dec] = []
            decade_books[dec] = set()
            
        decade_ratings[dec].append(rating)
        decade_books[dec].add(pid_num)

# Calculate stats
results = []
for dec in decade_ratings:
    num_books = len(decade_books[dec])
    if num_books >= 10:
        avg_rating = sum(decade_ratings[dec]) / len(decade_ratings[dec])
        results.append({
            'decade': dec,
            'avg_rating': avg_rating,
            'num_books': num_books,
            'num_reviews': len(decade_ratings[dec])
        })

# Sort by avg rating
results.sort(key=lambda x: x['avg_rating'], reverse=True)

print("__RESULT__:")
print(json.dumps(results))"""

env_args = {'var_function-call-17705164638168250041': ['books_info'], 'var_function-call-17705164638168251200': ['review'], 'var_function-call-15262951358326656759': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-15262951358326655588': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-1406188345692772182': [{'count': '200'}], 'var_function-call-1406188345692772571': [{'COUNT(*)': '1833'}], 'var_function-call-11409792330757935845': 'file_storage/function-call-11409792330757935845.json', 'var_function-call-11409792330757936310': 'file_storage/function-call-11409792330757936310.json'}

exec(code, env_args)
