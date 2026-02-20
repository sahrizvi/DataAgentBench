code = """import json
import re
import pandas as pd

# Get file paths from variables
books_file = locals()['var_function-call-3974352914324142375']
reviews_file = locals()['var_function-call-12365344636262352208']

# Load data
with open(books_file, 'r') as f:
    books_data = json.load(f)

with open(reviews_file, 'r') as f:
    reviews_data = json.load(f)

# Create DataFrames
df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

# Extract year from details
def extract_year(details):
    if not isinstance(details, str):
        return None
    match = re.search(r'(?:published|released).*?(\d{4})', details, re.IGNORECASE)
    if match:
        return int(match.group(1))
    matches = re.findall(r'\b(19\d{2}|20[0-2]\d)\b', details)
    if matches:
        return int(matches[0])
    return None

df_books['year'] = df_books['details'].apply(extract_year)
df_books = df_books.dropna(subset=['year'])
df_books['id_num'] = df_books['book_id'].astype(str).str.extract(r'(\d+)').astype(int)

df_reviews['id_num'] = df_reviews['purchase_id'].astype(str).str.extract(r'(\d+)').astype(int)
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
df_reviews = df_reviews.dropna(subset=['rating'])

# Merge
merged = pd.merge(df_reviews, df_books[['id_num', 'year']], on='id_num', how='inner')

# Decade
def get_decade(year):
    return f"{int(year // 10 * 10)}s"

merged['decade'] = merged['year'].apply(get_decade)

# Method 1: Average of all ratings
stats_1 = merged.groupby('decade').agg(
    distinct_books=('id_num', 'nunique'),
    average_rating=('rating', 'mean')
).reset_index()
stats_1 = stats_1[stats_1['distinct_books'] >= 10].sort_values('average_rating', ascending=False)

# Method 2: Average of book averages
book_avg = merged.groupby(['decade', 'id_num'])['rating'].mean().reset_index()
stats_2 = book_avg.groupby('decade').agg(
    distinct_books=('id_num', 'count'), # count of books
    average_book_rating=('rating', 'mean')
).reset_index()
stats_2 = stats_2[stats_2['distinct_books'] >= 10].sort_values('average_book_rating', ascending=False)

print("__RESULT__:")
print(json.dumps({
    "method_1": stats_1.to_dict(orient='records'),
    "method_2": stats_2.to_dict(orient='records')
}))"""

env_args = {'var_function-call-9073474900337945762': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-9362835081464333326': [{'cnt': '1833'}], 'var_function-call-3383126299682018077': [{'cnt': '200'}], 'var_function-call-3974352914324142375': 'file_storage/function-call-3974352914324142375.json', 'var_function-call-12365344636262352208': 'file_storage/function-call-12365344636262352208.json', 'var_function-call-12338988772550627997': {'decade': '2020s', 'average_rating': 4.663636363636364, 'distinct_books': 21, 'all_decades': [{'decade': '1880s', 'distinct_books': 1, 'average_rating': 4.25}, {'decade': '1930s', 'distinct_books': 2, 'average_rating': 5.0}, {'decade': '1940s', 'distinct_books': 1, 'average_rating': 5.0}, {'decade': '1970s', 'distinct_books': 2, 'average_rating': 4.285714285714286}, {'decade': '1980s', 'distinct_books': 11, 'average_rating': 4.208333333333333}, {'decade': '1990s', 'distinct_books': 16, 'average_rating': 3.8208955223880596}, {'decade': '2000s', 'distinct_books': 47, 'average_rating': 4.276223776223776}, {'decade': '2010s', 'distinct_books': 88, 'average_rating': 4.608591885441528}, {'decade': '2020s', 'distinct_books': 21, 'average_rating': 4.663636363636364}]}}

exec(code, env_args)
