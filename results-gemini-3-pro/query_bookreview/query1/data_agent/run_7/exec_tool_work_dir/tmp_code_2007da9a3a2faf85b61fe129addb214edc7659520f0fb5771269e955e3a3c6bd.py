code = """import json
import re
import pandas as pd

# Load data
with open(locals()['var_function-call-12676996466119317051'], 'r') as f:
    books = json.load(f)
with open(locals()['var_function-call-9741256298441356484'], 'r') as f:
    reviews = json.load(f)

# 1. Check book IDs and details
print("Sample books:")
for i, b in enumerate(books[:3]):
    print(f"ID: {b['book_id']}, Details: {b.get('details')[:50]}...")

# 2. Extract years
book_years = {}
for book in books:
    b_id = book['book_id']
    details = book.get('details', '')
    if not details:
        continue
    
    # Simple regex for year: 19xx or 20xx
    # We want to capture a year.
    # Try finding all years.
    years = re.findall(r'\b(19\d{2}|20[0-2]\d)\b', details)
    if years:
        # Take the first year found
        book_years[b_id] = int(years[0])

print(f"Found years for {len(book_years)} books out of {len(books)}")
print("Sample years:", list(book_years.items())[:5])

# 3. Check review IDs
df_reviews = pd.DataFrame(reviews)
print("Sample purchase_ids:", df_reviews['purchase_id'].head().tolist())

# 4. Map purchase_id to book_id
# Check if purchase_id starts with 'purchaseid_'
# Replace 'purchaseid_' with 'bookid_'
df_reviews['mapped_book_id'] = df_reviews['purchase_id'].str.replace('purchaseid_', 'bookid_')
# Wait, check exact format.
# "purchaseid_186" -> "bookid_186"
# "purchaseid" -> "bookid"
# If it is "purchaseid_186", replace("purchaseid", "bookid") -> "bookid_186". Correct.

# Check if mapped_book_id exists in book_years
mapped_ids = set(df_reviews['mapped_book_id'])
book_ids = set(book_years.keys())
common = mapped_ids.intersection(book_ids)
print(f"Common IDs: {len(common)}")
print("Sample common IDs:", list(common)[:5])

# 5. Merge
df_reviews['year'] = df_reviews['mapped_book_id'].map(book_years)
print("Reviews with year:", df_reviews['year'].notna().sum())

# 6. Group by decade
df_merged = df_reviews.dropna(subset=['year']).copy()
df_merged['year'] = df_merged['year'].astype(int)
df_merged['decade'] = (df_merged['year'] // 10) * 10
df_merged['decade_str'] = df_merged['decade'].astype(str) + 's'

decade_stats = df_merged.groupby('decade_str').agg(
    distinct_books=('mapped_book_id', 'nunique'),
    avg_rating=('rating', 'mean') # Rating is object? convert to float first
).reset_index()

print("Decade Stats:")
print(decade_stats)

print("__RESULT__:")
print("done")"""

env_args = {'var_function-call-14391079220039824156': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-12032611119589619147': [{'count': '200'}], 'var_function-call-14893637540441165934': [{'COUNT(*)': '1833'}], 'var_function-call-12676996466119317051': 'file_storage/function-call-12676996466119317051.json', 'var_function-call-9741256298441356484': 'file_storage/function-call-9741256298441356484.json', 'var_function-call-4533316282141004050': []}

exec(code, env_args)
