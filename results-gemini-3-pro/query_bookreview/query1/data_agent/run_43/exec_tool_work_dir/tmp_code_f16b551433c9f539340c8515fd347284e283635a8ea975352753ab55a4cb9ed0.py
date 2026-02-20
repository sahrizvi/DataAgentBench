code = """import json
import pandas as pd
import re

# Load data
with open(locals()['var_function-call-3976821729234494295'], 'r') as f:
    books_data = json.load(f)

with open(locals()['var_function-call-6586759856090264971'], 'r') as f:
    reviews_data = json.load(f)

debug_info = {}
debug_info['books_len'] = len(books_data)
debug_info['first_book'] = books_data[0] if books_data else None

debug_info['reviews_len'] = len(reviews_data)
debug_info['first_review'] = reviews_data[0] if reviews_data else None

b = books_data[0]
b_id_str = b.get('book_id', '')
match = re.search(r'bookid_(\d+)', b_id_str)
debug_info['book_id_match'] = match.group(1) if match else "No match"

r = reviews_data[0]
p_id_str = r.get('purchase_id', '')
match_r = re.search(r'purchaseid_(\d+)', p_id_str)
debug_info['review_id_match'] = match_r.group(1) if match_r else "No match"

# Now try to process all books and see how many we get
books = []
for b in books_data:
    b_id_str = b.get('book_id', '')
    match = re.search(r'bookid_(\d+)', b_id_str)
    if not match:
        continue
    b_id = int(match.group(1))
    
    details = b.get('details', '')
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', details)
    
    year = None
    if years:
        # Prioritize years near "published" or "released"
        # For simplicity in this check, just take the first one found in the string
        # Or define a regex for "published ... year"
        pub_match = re.search(r'(published|released).*?(\d{4})', details, re.IGNORECASE)
        if pub_match:
            year = int(pub_match.group(2))
        else:
            year = int(years[0])
            
    if year:
        books.append({'id': b_id, 'year': year})

debug_info['processed_books_count'] = len(books)
if books:
    debug_info['first_processed_book'] = books[0]

reviews = []
for r in reviews_data:
    p_id_str = r.get('purchase_id', '')
    match = re.search(r'purchaseid_(\d+)', p_id_str)
    if not match:
        continue
    p_id = int(match.group(1))
    try:
        rating = float(r.get('rating', 0))
    except:
        rating = 0.0
    reviews.append({'id': p_id, 'rating': rating})

debug_info['processed_reviews_count'] = len(reviews)
if reviews:
    debug_info['first_processed_review'] = reviews[0]

print("__RESULT__:")
print(json.dumps(debug_info))"""

env_args = {'var_function-call-12979837913567543210': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-9572130716804409115': [{'count': '200'}], 'var_function-call-2053256737704530069': [{'COUNT(*)': '1833'}], 'var_function-call-3976821729234494295': 'file_storage/function-call-3976821729234494295.json', 'var_function-call-6586759856090264971': 'file_storage/function-call-6586759856090264971.json', 'var_function-call-9408202312610352031': 'Debug done'}

exec(code, env_args)
