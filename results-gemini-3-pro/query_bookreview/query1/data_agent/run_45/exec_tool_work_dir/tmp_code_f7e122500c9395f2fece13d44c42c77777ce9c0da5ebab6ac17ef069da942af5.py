code = """import json
import pandas as pd
import re

# Load data
with open(locals()['var_function-call-17089505080740516011'], 'r') as f:
    books_data = json.load(f)

with open(locals()['var_function-call-17089505080740517494'], 'r') as f:
    reviews_data = json.load(f)

df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

def extract_id(s, prefix):
    if pd.isna(s): return None
    if s.startswith(prefix):
        return int(s[len(prefix):])
    return None

df_books['id'] = df_books['book_id'].apply(lambda x: extract_id(x, 'bookid_'))
df_reviews['id'] = df_reviews['purchase_id'].apply(lambda x: extract_id(x, 'purchaseid_'))
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

book_ratings = df_reviews.groupby('id')['rating'].mean().reset_index()
book_ratings.columns = ['id', 'avg_rating']

df_merged = pd.merge(df_books, book_ratings, on='id', how='inner')

def get_year_v3(text):
    if not text: return None
    match = re.search(r'[A-Z][a-z]+ \d{1,2}, (\d{4})', text)
    if match:
        y = int(match.group(1))
        if 1900 <= y <= 2023: return y
    match = re.search(r'[A-Z][a-z]+ (\d{4})', text)
    if match:
        y = int(match.group(1))
        if 1900 <= y <= 2023: return y
    match = re.search(r'(?:published|released).*?(\d{4})', text, re.IGNORECASE)
    if match:
        y = int(match.group(1))
        if 1900 <= y <= 2023: return y
    return None

df_merged['year'] = df_merged['details'].apply(get_year_v3)
df_merged = df_merged.dropna(subset=['year'])
df_merged['decade'] = (df_merged['year'] // 10) * 10
df_merged['decade_str'] = df_merged['decade'].astype(int).astype(str) + "s"

# Get review counts
review_counts = df_reviews.groupby('id').size().reset_index(name='review_count')
df_merged = pd.merge(df_merged, review_counts, on='id')

# Group by decade
decade_groups = df_merged.groupby('decade_str')

results = []
for decade, group in decade_groups:
    weighted_avg = (group['avg_rating'] * group['review_count']).sum() / group['review_count'].sum()
    unweighted_avg = group['avg_rating'].mean()
    book_count = group['id'].nunique()
    results.append({
        'decade': decade,
        'book_count': book_count,
        'weighted_avg': weighted_avg,
        'unweighted_avg': unweighted_avg
    })

results_df = pd.DataFrame(results)
qualified = results_df[results_df['book_count'] >= 10].sort_values('unweighted_avg', ascending=False)

print("__RESULT__:")
print(qualified.to_json(orient='records'))"""

env_args = {'var_function-call-3377596527049625595': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'title': 'Chaucer'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.', 'title': 'Notes from a Kidwatcher'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.', 'title': 'Service: A Navy SEAL at War'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.', 'title': 'Parker & Knight'}], 'var_function-call-3377596527049622968': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-17132736443979893994': [{'count': '200'}], 'var_function-call-17132736443979893135': [{'COUNT(*)': '1833'}], 'var_function-call-17089505080740516011': 'file_storage/function-call-17089505080740516011.json', 'var_function-call-17089505080740517494': 'file_storage/function-call-17089505080740517494.json', 'var_function-call-4616104232894204324': [{'decade_str': '1980s', 'book_count': 11, 'decade_avg_rating': 4.5481993852}, {'decade_str': '2020s', 'book_count': 21, 'decade_avg_rating': 4.5253052503}, {'decade_str': '2010s', 'book_count': 88, 'decade_avg_rating': 4.4051393366}, {'decade_str': '2000s', 'book_count': 46, 'decade_avg_rating': 4.3435505032}, {'decade_str': '1990s', 'book_count': 17, 'decade_avg_rating': 4.1764122316}], 'var_function-call-4107809609342769839': [{'decade_str': '1980s', 'book_count': 11, 'avg_rating_of_books': 4.5481993852}, {'decade_str': '2020s', 'book_count': 21, 'avg_rating_of_books': 4.5253052503}, {'decade_str': '2010s', 'book_count': 88, 'avg_rating_of_books': 4.4051393366}, {'decade_str': '2000s', 'book_count': 47, 'avg_rating_of_books': 4.3575175138}, {'decade_str': '1990s', 'book_count': 16, 'avg_rating_of_books': 4.124937996}], 'var_function-call-16280952315052372791': [{'decade_str': '2020s', 'avg_review_rating': 4.6636363636, 'book_count': 21}, {'decade_str': '2010s', 'avg_review_rating': 4.6085918854, 'book_count': 88}, {'decade_str': '2000s', 'avg_review_rating': 4.2762237762, 'book_count': 47}, {'decade_str': '1980s', 'avg_review_rating': 4.2083333333, 'book_count': 11}, {'decade_str': '1990s', 'avg_review_rating': 3.8208955224, 'book_count': 16}], 'var_function-call-16018646876134722176': {'books_min': 1, 'books_max': 200, 'reviews_min': 1, 'reviews_max': 200, 'common_ids': 200}, 'var_function-call-14917902879284863808': [{'decade_str': '1980s', 'book_count': 11, 'avg_rating_of_books': 4.5481993852}, {'decade_str': '2020s', 'book_count': 21, 'avg_rating_of_books': 4.5253052503}, {'decade_str': '2010s', 'book_count': 88, 'avg_rating_of_books': 4.4051393366}, {'decade_str': '2000s', 'book_count': 46, 'avg_rating_of_books': 4.3435505032}, {'decade_str': '1990s', 'book_count': 17, 'avg_rating_of_books': 4.1764122316}]}

exec(code, env_args)
