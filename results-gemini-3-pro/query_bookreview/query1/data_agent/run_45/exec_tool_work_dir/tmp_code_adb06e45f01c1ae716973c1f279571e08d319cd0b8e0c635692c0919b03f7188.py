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

# Extract ID number
def extract_id(s, prefix):
    if pd.isna(s): return None
    # Remove prefix
    if s.startswith(prefix):
        return int(s[len(prefix):])
    return None

df_books['id'] = df_books['book_id'].apply(lambda x: extract_id(x, 'bookid_'))
df_reviews['id'] = df_reviews['purchase_id'].apply(lambda x: extract_id(x, 'purchaseid_'))

# Convert rating to float
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

# Calculate average rating per book
book_ratings = df_reviews.groupby('id')['rating'].mean().reset_index()
book_ratings.columns = ['id', 'avg_rating']

# Merge
df_merged = pd.merge(df_books, book_ratings, on='id', how='inner')

# Extract year from details
# Pattern: Month Day, Year -> e.g. "January 1, 2004"
# Also need to handle "September 1, 1987"
# Regex: one or more letters, space, 1-2 digits, comma, space, 4 digits.
year_pattern = re.compile(r'([A-Z][a-z]+ \d{1,2}, (\d{4}))')

def get_year(text):
    if not text: return None
    match = year_pattern.search(text)
    if match:
        return int(match.group(2))
    # Fallback: look for just 4 digits if date not found?
    # But risky due to ISBN.
    # Let's check if there are other patterns if many are missing.
    return None

df_merged['year'] = df_merged['details'].apply(get_year)

# Check for missing years
missing_years = df_merged[df_merged['year'].isnull()]
print(f"Total books with ratings: {len(df_merged)}")
print(f"Books with missing years: {len(missing_years)}")
if len(missing_years) > 0:
    print("Sample missing details:", missing_years['details'].head().tolist())

# Calculate decade
df_merged = df_merged.dropna(subset=['year'])
df_merged['decade'] = (df_merged['year'] // 10) * 10
df_merged['decade_str'] = df_merged['decade'].astype(int).astype(str) + "s"

# Group by decade
decade_stats = df_merged.groupby('decade_str').agg(
    book_count=('id', 'nunique'),
    decade_avg_rating=('avg_rating', 'mean')
).reset_index()

# Filter for at least 10 distinct books
qualified_decades = decade_stats[decade_stats['book_count'] >= 10].copy()

# Sort by rating
qualified_decades = qualified_decades.sort_values(by='decade_avg_rating', ascending=False)

print("__RESULT__:")
print(qualified_decades.to_json(orient='records'))"""

env_args = {'var_function-call-3377596527049625595': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'title': 'Chaucer'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.', 'title': 'Notes from a Kidwatcher'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.', 'title': 'Service: A Navy SEAL at War'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.', 'title': 'Parker & Knight'}], 'var_function-call-3377596527049622968': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-17132736443979893994': [{'count': '200'}], 'var_function-call-17132736443979893135': [{'COUNT(*)': '1833'}], 'var_function-call-17089505080740516011': 'file_storage/function-call-17089505080740516011.json', 'var_function-call-17089505080740517494': 'file_storage/function-call-17089505080740517494.json'}

exec(code, env_args)
