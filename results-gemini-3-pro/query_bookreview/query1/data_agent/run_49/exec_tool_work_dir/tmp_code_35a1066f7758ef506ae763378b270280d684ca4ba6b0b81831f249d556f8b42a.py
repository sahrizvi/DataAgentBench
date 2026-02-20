code = """import pandas as pd
import json
import re

# Load data
with open(locals()['var_function-call-17584423273886338862'], 'r') as f:
    books_data = json.load(f)

with open(locals()['var_function-call-9381740438124898103'], 'r') as f:
    reviews_data = json.load(f)

df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

def extract_year(details):
    if not isinstance(details, str):
        return None
    # Try different patterns
    # 1. "published ... [Month] [Day], [Year]" or similar
    match = re.search(r'(?:published|released).*?(\d{4})', details, re.IGNORECASE)
    if match:
        year = int(match.group(1))
        if 1900 <= year <= 2025:
            return year
    
    # 2. "published ... [Month] [Year]"
    # 3. Just a year if "published" is present nearby
    return None

df_books['year'] = df_books['details'].apply(extract_year)
# Drop NaN years
df_books_valid = df_books.dropna(subset=['year']).copy()
df_books_valid['year'] = df_books_valid['year'].astype(int)

# Group by decade
df_books_valid['decade'] = (df_books_valid['year'] // 10) * 10
df_books_valid['decade_str'] = df_books_valid['decade'].astype(str) + "s"

# Parse IDs
df_books_valid['id_num'] = df_books_valid['book_id'].str.extract(r'(\d+)').astype(int)
df_reviews['id_num'] = df_reviews['purchase_id'].str.extract(r'(\d+)').astype(int)
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

# Join
merged = pd.merge(df_reviews, df_books_valid, on='id_num', how='inner')

# Calculate stats per decade
stats = merged.groupby('decade_str').agg(
    avg_rating=('rating', 'mean'),
    distinct_books=('id_num', 'nunique'),
    count_reviews=('rating', 'count')
).reset_index()

# Filter for >= 10 distinct books
valid_decades = stats[stats['distinct_books'] >= 10]

print("__RESULT__:")
print(valid_decades.to_json(orient='records'))"""

env_args = {'var_function-call-7846935078876793979': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-4565000254805596521': [{'count': '200'}], 'var_function-call-6157774012479870483': [{'COUNT(*)': '1833'}], 'var_function-call-17584423273886338862': 'file_storage/function-call-17584423273886338862.json', 'var_function-call-9381740438124898103': 'file_storage/function-call-9381740438124898103.json', 'var_function-call-9833549063634245984': {'decade': '2020s', 'average_rating': 4.663636363636364, 'distinct_books': 21}}

exec(code, env_args)
