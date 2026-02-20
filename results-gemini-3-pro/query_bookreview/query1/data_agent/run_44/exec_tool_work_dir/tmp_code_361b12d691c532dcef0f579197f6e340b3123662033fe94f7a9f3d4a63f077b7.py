code = """import json
import pandas as pd
import re
import os

# Load data
with open(locals()['var_function-call-17298644812689446293'], 'r') as f:
    books_data = json.load(f)
with open(locals()['var_function-call-9570983987664028606'], 'r') as f:
    review_data = json.load(f)

df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(review_data)

# Extract extract key for joining
def extract_id(s):
    if '_' in s:
        return s.split('_')[1]
    return s

df_books['join_id'] = df_books['book_id'].apply(extract_id)
df_reviews['join_id'] = df_reviews['purchase_id'].apply(extract_id)

# Extract year from details
def extract_year(details):
    if not isinstance(details, str):
        return None
    
    # Pattern 1: published ... 2004
    # Look for year in the vicinity of "published"
    match = re.search(r'published.*?\b([12]\d{3})\b', details, re.IGNORECASE)
    if match:
        y = int(match.group(1))
        if 1900 <= y <= 2025:
            return y
            
    # Pattern 2: Explicit date format like "January 1, 2004" or "May 1996"
    # This is useful if "published" keyword is far or missing but a clear date exists
    match = re.search(r'[A-Z][a-z]+\s(?:\d{1,2},?\s)?([12]\d{3})', details)
    if match:
        y = int(match.group(1))
        if 1900 <= y <= 2025:
            return y
            
    # Pattern 3: Any 4 digit year
    matches = re.findall(r'\b([12]\d{3})\b', details)
    for m in matches:
        y = int(m)
        if 1900 <= y <= 2025:
            return y
            
    return None

df_books['year'] = df_books['details'].apply(extract_year)

# Filter out books without year
df_books = df_books.dropna(subset=['year'])
df_books['year'] = df_books['year'].astype(int)

# Merge
# We only care about books that have been rated.
# So we merge reviews to books.
# Convert rating to float
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
df_reviews = df_reviews.dropna(subset=['rating'])

merged = pd.merge(df_reviews, df_books, on='join_id', how='inner')

# Calculate decade
merged['decade'] = (merged['year'] // 10) * 10
merged['decade_str'] = merged['decade'].astype(str) + 's'

# Group by decade
stats = merged.groupby('decade_str').agg(
    distinct_books=('book_id', 'nunique'),
    avg_rating=('rating', 'mean')
).reset_index()

# Filter for decades with at least 10 distinct books
stats_filtered = stats[stats['distinct_books'] >= 10]

# Find max avg rating
if not stats_filtered.empty:
    best_decade = stats_filtered.loc[stats_filtered['avg_rating'].idxmax()]
    result = best_decade['decade_str']
    # Debug print
    print("Decade Stats:")
    print(stats_filtered)
else:
    result = "No decade meets criteria"

print('__RESULT__:')
print(json.dumps(result))"""

env_args = {'var_function-call-8065903626328758421': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-17298644812689446293': 'file_storage/function-call-17298644812689446293.json', 'var_function-call-9570983987664028606': 'file_storage/function-call-9570983987664028606.json'}

exec(code, env_args)
