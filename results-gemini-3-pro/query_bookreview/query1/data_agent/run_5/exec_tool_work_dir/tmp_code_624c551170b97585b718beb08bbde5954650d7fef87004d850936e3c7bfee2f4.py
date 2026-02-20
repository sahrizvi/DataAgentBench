code = """import json
import re

# Load data
with open(locals()['var_function-call-2311230859303334761'], 'r') as f:
    books = json.load(f)
with open(locals()['var_function-call-2311230859303334210'], 'r') as f:
    reviews = json.load(f)

# Parse books
book_years = {}
date_pattern = re.compile(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+(\d{4})\b', re.IGNORECASE)
year_pattern = re.compile(r'\b(19\d{2}|20\d{2})\b')

print(f"Total books: {len(books)}")
print(f"Sample book IDs: {[b['book_id'] for b in books[:5]]}")

parsed_count = 0
for b in books:
    bid_str = b['book_id']
    try:
        bid = int(bid_str.split('_')[-1])
    except ValueError:
        continue

    details = b['details']
    year = None
    
    match = date_pattern.search(details)
    if match:
        year = int(match.group(1))
    else:
        matches = year_pattern.findall(details)
        if matches:
            year = int(matches[0])
            
    if year:
        book_years[bid] = year
        parsed_count += 1

print(f"Books with parsed year: {parsed_count}")
print(f"Sample parsed years: {list(book_years.items())[:5]}")

# Aggregate reviews
decade_ratings = {} 
decade_books = {}   

print(f"Total reviews: {len(reviews)}")
print(f"Sample purchase IDs: {[r['purchase_id'] for r in reviews[:5]]}")

matched_reviews = 0
unique_books_in_reviews = set()

for r in reviews:
    pid_str = r['purchase_id']
    try:
        pid = int(pid_str.split('_')[-1])
    except ValueError:
        continue

    if pid in book_years:
        matched_reviews += 1
        unique_books_in_reviews.add(pid)
        year = book_years[pid]
        decade = (year // 10) * 10
        decade_str = f"{decade}s"
        
        try:
            rating = float(r['rating'])
        except (ValueError, TypeError):
            continue
            
        if decade_str not in decade_ratings:
            decade_ratings[decade_str] = []
            decade_books[decade_str] = set()
            
        decade_ratings[decade_str].append(rating)
        decade_books[decade_str].add(pid)

print(f"Matched reviews: {matched_reviews}")
print(f"Unique books in matched reviews: {len(unique_books_in_reviews)}")

# Show decade stats
stats = []
for dec in decade_books:
    stats.append({
        "decade": dec, 
        "book_count": len(decade_books[dec]),
        "review_count": len(decade_ratings[dec])
    })
print(f"Decade stats: {stats}")

print("__RESULT__:")
print(json.dumps(stats))"""

env_args = {'var_function-call-6260492085605663425': ['books_info'], 'var_function-call-6260492085605666322': ['review'], 'var_function-call-6260492085605665123': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-2251594135074204042': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-17579650686641542669': [{'count': '200'}], 'var_function-call-17579650686641541368': [{'COUNT(*)': '1833'}], 'var_function-call-2311230859303334761': 'file_storage/function-call-2311230859303334761.json', 'var_function-call-2311230859303334210': 'file_storage/function-call-2311230859303334210.json', 'var_function-call-6427252765627234448': []}

exec(code, env_args)
