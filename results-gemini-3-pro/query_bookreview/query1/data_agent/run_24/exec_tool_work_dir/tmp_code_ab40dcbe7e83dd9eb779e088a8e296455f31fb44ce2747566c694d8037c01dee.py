code = """import json
import pandas as pd
import re

# Load data
with open(locals()['var_function-call-11217342331341158317'], 'r') as f:
    books_data = json.load(f)

with open(locals()['var_function-call-18352100415714738754'], 'r') as f:
    reviews_data = json.load(f)

books_df = pd.DataFrame(books_data)
reviews_df = pd.DataFrame(reviews_data)

# Extract ID number
def extract_id(s):
    m = re.search(r'(\d+)$', s)
    return int(m.group(1)) if m else None

books_df['join_id'] = books_df['book_id'].apply(lambda x: extract_id(x) if x else None)
reviews_df['join_id'] = reviews_df['purchase_id'].apply(lambda x: extract_id(x) if x else None)

# Extract Year from details
def extract_year(details):
    # Pattern 1: published ... on Month Day, Year
    # Pattern 2: released ... on Month Day, Year
    # Pattern 3: \d{4}
    # Look for 4 digits in range 1900-2023
    
    # Priority to "published ... Year"
    m = re.search(r'(?:published|released).*?(\d{4})', details, re.IGNORECASE)
    if m:
        y = int(m.group(1))
        if 1900 <= y <= 2023:
            return y
    
    # Fallback: find all 4-digit numbers, pick one that looks like a year
    # Avoid small numbers if possible, but 19xx and 20xx are prime candidates.
    candidates = re.findall(r'\b(19\d{2}|20\d{2})\b', details)
    for c in candidates:
        y = int(c)
        if 1900 <= y <= 2023:
            return y
            
    return None

books_df['year'] = books_df['details'].apply(extract_year)

# Drop books with no year
books_df = books_df.dropna(subset=['year'])

# Calculate Decade
books_df['decade'] = (books_df['year'] // 10) * 10
books_df['decade_str'] = books_df['decade'].astype(int).astype(str) + "s"

# Merge
merged_df = pd.merge(reviews_df, books_df, on='join_id', how='inner')

# Convert rating to float
merged_df['rating'] = pd.to_numeric(merged_df['rating'], errors='coerce')

# Filter valid ratings
merged_df = merged_df.dropna(subset=['rating'])

# Group by Decade
decade_stats = merged_df.groupby('decade_str').agg(
    distinct_books=('join_id', 'nunique'),
    avg_rating=('rating', 'mean')
).reset_index()

# Filter decades with at least 10 distinct books
qualified_decades = decade_stats[decade_stats['distinct_books'] >= 10]

# Find max average rating
if not qualified_decades.empty:
    best_decade = qualified_decades.loc[qualified_decades['avg_rating'].idxmax()]
    result = {
        "best_decade": best_decade['decade_str'],
        "avg_rating": best_decade['avg_rating'],
        "distinct_books": best_decade['distinct_books']
    }
else:
    result = "No decade meets criteria"

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_function-call-1972179510569002468': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-4538444698924124667': [{'COUNT(*)': '1833'}], 'var_function-call-1245807085132264558': [{'count': '200'}], 'var_function-call-11217342331341158317': 'file_storage/function-call-11217342331341158317.json', 'var_function-call-18352100415714738754': 'file_storage/function-call-18352100415714738754.json'}

exec(code, env_args)
