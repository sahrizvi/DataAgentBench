code = """import json
import pandas as pd
import re

# Load data
with open(locals()['var_function-call-6301853962559315633'], 'r') as f:
    books_data = json.load(f)
with open(locals()['var_function-call-6301853962559313766'], 'r') as f:
    reviews_data = json.load(f)

# Helper functions
def extract_id(s):
    if not s: return None
    digits = "".join([c for c in str(s) if c.isdigit()])
    return int(digits) if digits else None

def extract_year(s):
    if not s: return None
    words = str(s).replace(',', ' ').replace('.', ' ').split()
    candidates = []
    for w in words:
        clean_w = "".join([c for c in w if c.isdigit()])
        if len(clean_w) == 4:
            y = int(clean_w)
            if 1900 <= y <= 2023:
                candidates.append(y)
    if candidates: return candidates[0]
    return None

def get_decade(year):
    if not year: return None
    return f"{str(year)[:3]}0s"

# Process books
df_books = pd.DataFrame(books_data)
df_books['id_num'] = df_books['book_id'].apply(extract_id)
df_books['year'] = df_books['details'].apply(extract_year)
df_books['decade'] = df_books['year'].apply(get_decade)

# Process reviews
df_reviews = pd.DataFrame(reviews_data)
df_reviews['id_num'] = df_reviews['purchase_id'].apply(extract_id)
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

# Filter
df_books = df_books.dropna(subset=['year', 'id_num'])
df_reviews = df_reviews.dropna(subset=['id_num', 'rating'])

# Merge
merged = pd.merge(df_reviews, df_books, on='id_num', how='inner')

# Inspect 1980s
dec_80s = merged[merged['decade'] == '1980s']
print("1980s Summary:")
print(dec_80s.groupby('id_num').agg({'rating': ['mean', 'count']}))

# Inspect 2020s
dec_20s = merged[merged['decade'] == '2020s']
print("2020s Summary:")
print(dec_20s.groupby('id_num').agg({'rating': ['mean', 'count']}))

print("__RESULT__:")
print("Done")"""

env_args = {'var_function-call-1202846484715802993': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-1202846484715804780': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-11990365395883407811': [{'count': '200'}], 'var_function-call-11990365395883408638': [{'count(*)': '1833'}], 'var_function-call-6301853962559315633': 'file_storage/function-call-6301853962559315633.json', 'var_function-call-6301853962559313766': 'file_storage/function-call-6301853962559313766.json', 'var_function-call-15083493677186756819': {'error': 'No decade met criteria'}, 'var_function-call-11754914075906924054': {'books_sample': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'id_num': 1, 'year': None, 'decade': None}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.', 'id_num': 2, 'year': None, 'decade': None}], 'reviews_sample': [{'purchase_id': 'purchaseid_186', 'rating': 4, 'id_num': 186}, {'purchase_id': 'purchaseid_191', 'rating': 4, 'id_num': 191}]}, 'var_function-call-7065132102717144929': [], 'var_function-call-7780553485220311114': {'decade': '2020s', 'distinct_books': 21, 'avg_rating': 4.663636363636364}, 'var_function-call-11995001176608342593': [{'decade': '2020s', 'distinct_books': 21, 'avg_rating': 4.6636363636}, {'decade': '2010s', 'distinct_books': 88, 'avg_rating': 4.6085918854}, {'decade': '2000s', 'distinct_books': 47, 'avg_rating': 4.2762237762}, {'decade': '1980s', 'distinct_books': 11, 'avg_rating': 4.2083333333}, {'decade': '1990s', 'distinct_books': 16, 'avg_rating': 3.8208955224}], 'var_function-call-4816144183882379371': [{'decade': '1980s', 'distinct_books': 11, 'avg_rating': 4.5481993852}, {'decade': '2020s', 'distinct_books': 21, 'avg_rating': 4.5253052503}, {'decade': '2010s', 'distinct_books': 88, 'avg_rating': 4.4051393366}, {'decade': '2000s', 'distinct_books': 47, 'avg_rating': 4.3575175138}, {'decade': '1990s', 'distinct_books': 16, 'avg_rating': 4.124937996}]}

exec(code, env_args)
