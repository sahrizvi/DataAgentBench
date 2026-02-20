code = """import json, re, pandas as pd, os
# Load books_info data
books_path = locals()['var_functions.query_db:2']
# books_path is a string path to a json file containing list of records
with open(books_path, 'r') as f:
    books_raw = json.load(f)
# Create DataFrame
books_df = pd.DataFrame(books_raw)
# Define function to extract publication year from details string

def extract_year(text):
    # find all 4-digit numbers between 1900-2023
    matches = re.findall(r'\b(19\d{2}|20[0-2]\d)\b', text)
    if not matches:
        return None
    # convert to int
    years = [int(y) for y in matches]
    # Return the earliest year (min) to get original publication if multiple
    return min(years)

books_df['year'] = books_df['details'].apply(extract_year)
# Extract numeric id from book_id like 'bookid_123'
books_df['book_num_id'] = books_df['book_id'].str.extract(r'(\d+)').astype(int)
# Load reviews
reviews_path = locals()['var_functions.query_db:3']
with open(reviews_path, 'r') as f:
    reviews_raw = json.load(f)
reviews_df = pd.DataFrame(reviews_raw)
# Extract numeric id from purchase_id like 'purchaseid_186'
reviews_df['review_num_id'] = reviews_df['purchase_id'].str.extract(r'(\d+)').astype(int)
# Merge books and reviews on numeric id
merged = pd.merge(books_df, reviews_df, left_on='book_num_id', right_on='review_num_id', how='inner')
# Filter rows where year is not null
merged = merged.dropna(subset=['year'])
# Cast rating to float
merged['rating'] = merged['rating'].astype(float)
# Compute decade
merged['decade'] = (merged['year'] // 10) * 10
# Group by decade: compute distinct book count and average rating
grouped = merged.groupby('decade').agg(
    distinct_books=('book_num_id', lambda x: x.nunique()),
    avg_rating=('rating', 'mean')
).reset_index()
# Filter decades with at least 10 distinct books that have ratings
filtered = grouped[grouped['distinct_books'] >= 10]
# Find decade with highest avg_rating
top_decade = filtered.loc[filtered['avg_rating'].idxmax()]
# Format decade string
decade_label = f"{int(top_decade['decade'])}s"
result = {'decade': decade_label, 'avg_rating': round(top_decade['avg_rating'], 3), 'distinct_books': int(top_decade['distinct_books'])}
# Print result following required format
print('__RESULT__:')
print(json.dumps(result, ensure_ascii=False))"""

env_args = {'var_functions.query_db:0': [{'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}, {'details': 'This book, published independently on December 30, 2021, is written in English and consists of 24 pages. It has an ISBN 13 of 979-8528537702 and weighs 3.2 ounces. The dimensions of the book are 7 x 0.06 x 9 inches.'}, {'details': 'The book, published by Guilford in its second edition in January 2004, is also noted as the 8082nd edition from January 1, 1994. It has a remarkably light item weight of just 0.01 ounces.'}, {'details': 'This book, published by Make Community, LLC, in its second edition on September 22, 2015, is available in English and spans 352 pages in paperback format. It has an ISBN of 9781680450262 for the 10-digit version and 978-1680450262 for the 13-digit version. The content is suitable for readers aged 11 to 17 years. The book weighs 2.91 pounds and its dimensions are 8 inches in width, 0.5 inches in thickness, and 10 inches in height.'}, {'details': 'This book, published independently on September 25, 2019, is written in English and spans 367 pages. It is available in paperback format and has an ISBN-10 of 1694621731 and an ISBN-13 of 978-1694621733. The item weighs 1.38 pounds and measures 6 x 0.92 x 9 inches.'}, {'details': 'This book, published by WallBuilder Press in its first edition on November 8, 2004, is available in English and comprises 51 pages in paperback format. It has an ISBN-10 of 1932225323 and an ISBN-13 of 978-1932225327, with a total item weight of 3.52 ounces.'}], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review'], 'var_functions.query_db:6': 'file_storage/functions.query_db:6.json'}

exec(code, env_args)
