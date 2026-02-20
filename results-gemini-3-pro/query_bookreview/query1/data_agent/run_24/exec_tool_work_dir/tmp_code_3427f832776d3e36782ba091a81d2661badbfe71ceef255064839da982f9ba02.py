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

# Extract IDs
def extract_id(s):
    if not isinstance(s, str): return None
    m = re.search(r'(\d+)$', s)
    return int(m.group(1)) if m else None

books_df['book_num'] = books_df['book_id'].apply(extract_id)
reviews_df['purchase_num'] = reviews_df['purchase_id'].apply(extract_id)

# Stats
num_books = len(books_df)
num_reviews = len(reviews_df)
common_ids = set(books_df['book_num']).intersection(set(reviews_df['purchase_num']))
num_common = len(common_ids)

# Extract Year
def extract_year(text):
    if not isinstance(text, str): return None
    # Look for 4 digits (19xx or 20xx)
    matches = re.findall(r'\b(19\d{2}|20\d{2})\b', text)
    if matches:
        return int(matches[0])
    return None

books_df['year'] = books_df['details'].apply(extract_year)
books_with_year = books_df.dropna(subset=['year'])
num_books_with_year = len(books_with_year)

# Calculate Decade
books_with_year['decade'] = (books_with_year['year'] // 10) * 10
books_with_year['decade_label'] = books_with_year['decade'].astype(int).astype(str) + "s"

# Merge
merged_df = pd.merge(reviews_df, books_with_year, left_on='purchase_num', right_on='book_num', how='inner')
num_merged = len(merged_df)

# Convert rating
merged_df['rating'] = pd.to_numeric(merged_df['rating'], errors='coerce')
merged_df = merged_df.dropna(subset=['rating'])

# Group by Decade
decade_stats = merged_df.groupby('decade_label').agg(
    distinct_books=('book_num', 'nunique'),
    avg_rating=('rating', 'mean')
).reset_index()

# Filter
qualified = decade_stats[decade_stats['distinct_books'] >= 10].copy()

debug_info = {
    "num_books": num_books,
    "num_reviews": num_reviews,
    "num_common_ids": num_common,
    "num_books_with_year": num_books_with_year,
    "num_merged": num_merged,
    "decade_stats": decade_stats.to_dict(orient='records'),
    "qualified": qualified.to_dict(orient='records')
}

print("__RESULT__:")
print(json.dumps(debug_info))"""

env_args = {'var_function-call-1972179510569002468': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-4538444698924124667': [{'COUNT(*)': '1833'}], 'var_function-call-1245807085132264558': [{'count': '200'}], 'var_function-call-11217342331341158317': 'file_storage/function-call-11217342331341158317.json', 'var_function-call-18352100415714738754': 'file_storage/function-call-18352100415714738754.json', 'var_function-call-929890728202468694': {'error': 'No qualified decade found'}, 'var_function-call-4961246982507686762': {'error': 'No decade meets criteria', 'stats': []}, 'var_function-call-1585524080417120906': {'status': 'debug_printed'}}

exec(code, env_args)
