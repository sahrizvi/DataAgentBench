code = """import pandas as pd
import re
import json

# Load data
with open(locals()['var_function-call-9654581938833205007']) as f:
    books = json.load(f)
with open(locals()['var_function-call-9654581938833204166']) as f:
    reviews = json.load(f)

print(f"Loaded {len(books)} books and {len(reviews)} reviews.")

# Process books
book_data = []
for b in books:
    bid_str = b['book_id']
    match = re.search(r'\d+', bid_str)
    if not match:
        continue
    bid = int(match.group())
    details = b['details']
    # Extract year: look for 19xx or 20xx
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', details)
    if years:
        year = int(years[0]) 
        decade = (year // 10) * 10
        book_data.append({'id': bid, 'year': year, 'decade': decade})
    
print(f"Extracted data for {len(book_data)} books.")
if book_data:
    print(f"Sample book: {book_data[0]}")
    
df_books = pd.DataFrame(book_data)
if df_books.empty:
    print("df_books is empty!")
else:
    print(f"df_books columns: {df_books.columns.tolist()}")

# Process reviews
review_data = []
for r in reviews:
    pid_str = r['purchase_id']
    match = re.search(r'\d+', pid_str)
    if not match:
        continue
    pid = int(match.group())
    rating = float(r['rating'])
    review_data.append({'id': pid, 'rating': rating})
    
print(f"Extracted data for {len(review_data)} reviews.")
if review_data:
    print(f"Sample review: {review_data[0]}")

df_reviews = pd.DataFrame(review_data)
if df_reviews.empty:
    print("df_reviews is empty!")
else:
    print(f"df_reviews columns: {df_reviews.columns.tolist()}")

if not df_books.empty and not df_reviews.empty:
    merged = pd.merge(df_reviews, df_books, on='id', how='inner')
    print(f"Merged rows: {len(merged)}")
    decade_stats = merged.groupby('decade').agg(
        distinct_books=('id', 'nunique'),
        avg_rating=('rating', 'mean')
    ).reset_index()
    print("Decade stats:")
    print(decade_stats.to_json(orient='records'))
else:
    print("Cannot proceed with merge.")

print("__RESULT__:")
print(json.dumps("DEBUG_DONE"))"""

env_args = {'var_function-call-13366482996862838801': ['books_info'], 'var_function-call-13366482996862839796': ['review'], 'var_function-call-14784826910390619232': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-14784826910390618829': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-5735080624127152271': [{'book_id': 'bookid_186'}], 'var_function-call-17037478580475657313': [{'count': '200'}], 'var_function-call-17037478580475656736': [{'count(*)': '1833'}], 'var_function-call-9654581938833205007': 'file_storage/function-call-9654581938833205007.json', 'var_function-call-9654581938833204166': 'file_storage/function-call-9654581938833204166.json'}

exec(code, env_args)
