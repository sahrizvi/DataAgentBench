code = """import json
import re
import pandas as pd

# Load data
with open(locals()['var_function-call-18434172628679819427'], 'r') as f:
    books_data = json.load(f)

with open(locals()['var_function-call-1463227589658029821'], 'r') as f:
    reviews_data = json.load(f)

# Convert to DataFrame
df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

# Process book IDs
# book_id format: "bookid_123" -> 123
def extract_id(s):
    m = re.search(r'\d+', str(s))
    if m:
        return int(m.group(0))
    return None

df_books['id_num'] = df_books['book_id'].apply(extract_id)
df_reviews['id_num'] = df_reviews['purchase_id'].apply(extract_id)

# Process publication year
def extract_year(details):
    if not isinstance(details, str):
        return None
    # Look for patterns like "published ... on [Month] [Day], [Year]" or just a 4 digit year 19xx or 20xx
    # Regex for year: \b(19|20)\d{2}\b
    matches = re.findall(r'\b(19|20)\d{2}\b', details)
    if matches:
        # If multiple years, which one? Usually the first one mentioned or the one associated with publication date.
        # Let's take the first one found.
        # Looking at examples: "released on January 1, 2004", "published ... on May 20, 1996"
        # "8082nd edition from January 1, 1994" -> might be confusing. 
        # But usually the first valid year is good enough.
        return int(matches[0])
    return None

df_books['year'] = df_books['details'].apply(extract_year)
df_books = df_books.dropna(subset=['year'])
df_books['decade'] = (df_books['year'] // 10) * 10
df_books['decade_str'] = df_books['decade'].astype(str) + 's'

# Calculate average rating per book
# First ensure rating is numeric
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
df_reviews = df_reviews.dropna(subset=['rating'])

# Group reviews by book
book_ratings = df_reviews.groupby('id_num')['rating'].mean().reset_index()
book_ratings.columns = ['id_num', 'avg_rating']

# Merge books and ratings
merged = pd.merge(df_books, book_ratings, on='id_num')

# Group by decade
decade_stats = merged.groupby('decade_str').agg(
    book_count=('id_num', 'nunique'),
    decade_avg_rating=('avg_rating', 'mean')
).reset_index()

# Filter for decades with at least 10 distinct books
valid_decades = decade_stats[decade_stats['book_count'] >= 10]

# Find the highest average rating
if not valid_decades.empty:
    best_decade = valid_decades.loc[valid_decades['decade_avg_rating'].idxmax()]
    result = {
        "decade": best_decade['decade_str'],
        "average_rating": best_decade['decade_avg_rating'],
        "book_count": best_decade['book_count']
    }
else:
    result = "No decade meets the criteria."

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_function-call-9666263614484173789': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-18434172628679819427': 'file_storage/function-call-18434172628679819427.json', 'var_function-call-1463227589658029821': 'file_storage/function-call-1463227589658029821.json'}

exec(code, env_args)
