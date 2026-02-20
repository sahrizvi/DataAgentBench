code = """import pandas as pd
import json

# Access file paths from locals
books_file_path = locals()['var_function-call-11951794239785044405']
reviews_file_path = locals()['var_function-call-11355008030497697797']

with open(books_file_path, 'r') as f:
    books_data = json.load(f)

with open(reviews_file_path, 'r') as f:
    reviews_data = json.load(f)

df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

# Extract integer ID from book_id and purchase_id
def extract_id(s):
    if not isinstance(s, str):
        return None
    import re
    match = re.search(r'(\d+)$', s)
    if match:
        return int(match.group(1))
    return None

df_books['id'] = df_books['book_id'].apply(extract_id)
df_reviews['id'] = df_reviews['purchase_id'].apply(extract_id)

# Extract Year from details
def extract_year(s):
    if not isinstance(s, str):
        return None
    import re
    date_match = re.search(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+(?:\d{1,2},?\s+)?(19\d{2}|20\d{2})', s)
    if date_match:
        return int(date_match.group(1))
    matches = re.findall(r'\b(19\d{2}|20\d{2})\b', s)
    if matches:
        return int(matches[0])
    return None

df_books['year'] = df_books['details'].apply(extract_year)

# Drop books with no year or invalid id
df_books_clean = df_books.dropna(subset=['year', 'id'])
df_reviews_clean = df_reviews.dropna(subset=['id', 'rating'])

# Merge
merged = pd.merge(df_reviews_clean, df_books_clean, on='id', how='inner')
merged['decade'] = (merged['year'] // 10) * 10
merged['decade_str'] = merged['decade'].astype(int).astype(str) + "s"
merged['rating'] = pd.to_numeric(merged['rating'], errors='coerce')

# Calculate Average of Book Averages
# 1. Group by Book and Decade
book_stats = merged.groupby(['decade_str', 'id'])['rating'].mean().reset_index()
book_stats.rename(columns={'rating': 'avg_book_rating'}, inplace=True)

# 2. Group by Decade
decade_stats_by_book = book_stats.groupby('decade_str').agg(
    distinct_books=('id', 'count'),
    avg_of_book_avgs=('avg_book_rating', 'mean')
).reset_index()

# Filter
filtered_by_book = decade_stats_by_book[decade_stats_by_book['distinct_books'] >= 10]

if not filtered_by_book.empty:
    best_by_book = filtered_by_book.loc[filtered_by_book['avg_of_book_avgs'].idxmax()]
    result_by_book = best_by_book['decade_str']
    max_rating_by_book = best_by_book['avg_of_book_avgs']
    debug_by_book = filtered_by_book.to_dict(orient='records')
else:
    result_by_book = "None"
    max_rating_by_book = 0
    debug_by_book = []

print("__RESULT__:")
print(json.dumps({
    "answer_by_book": result_by_book,
    "max_rating_by_book": max_rating_by_book,
    "debug_by_book": debug_by_book
}))"""

env_args = {'var_function-call-272452347185540501': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-7758564921818992438': [{'count': '200'}], 'var_function-call-18259465167187388799': [{'count(*)': '1833'}], 'var_function-call-11951794239785044405': 'file_storage/function-call-11951794239785044405.json', 'var_function-call-11355008030497697797': 'file_storage/function-call-11355008030497697797.json', 'var_function-call-6348051911711359552': {'answer': '2020s', 'avg_rating': 4.663636363636364, 'debug': [{'decade_str': '1980s', 'distinct_books': 11, 'avg_rating': 4.208333333333333}, {'decade_str': '1990s', 'distinct_books': 16, 'avg_rating': 3.8208955223880596}, {'decade_str': '2000s', 'distinct_books': 47, 'avg_rating': 4.276223776223776}, {'decade_str': '2010s', 'distinct_books': 88, 'avg_rating': 4.608591885441528}, {'decade_str': '2020s', 'distinct_books': 21, 'avg_rating': 4.663636363636364}]}}

exec(code, env_args)
