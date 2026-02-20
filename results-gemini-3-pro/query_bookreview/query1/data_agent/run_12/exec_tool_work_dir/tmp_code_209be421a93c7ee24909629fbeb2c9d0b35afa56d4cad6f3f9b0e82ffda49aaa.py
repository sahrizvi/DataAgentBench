code = """import json
import re
import pandas as pd

# Load data
with open('var_function-call-3974352914324142375.json', 'r') as f:
    books = json.load(f)

with open('var_function-call-12365344636262352208.json', 'r') as f:
    reviews = json.load(f)

# Create DataFrames
df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Extract year from details
def extract_year(details):
    # Pattern: Look for 4 digits 19xx or 20xx
    # Priority given to "published ... YYYY" or "released ... YYYY"
    # But often the year is just present.
    # Let's look for "published.*?(\d{4})"
    match = re.search(r'(?:published|released).*?(\d{4})', details, re.IGNORECASE)
    if match:
        return int(match.group(1))
    
    # Fallback: finding any 19xx or 20xx date
    match = re.search(r'\b(19\d{2}|20\d{2})\b', details)
    if match:
        return int(match.group(1))
    return None

df_books['year'] = df_books['details'].apply(extract_year)

# Create join key
# books: bookid_X -> X
# reviews: purchaseid_X -> X
df_books['id_num'] = df_books['book_id'].str.extract(r'(\d+)').astype(int)
df_reviews['id_num'] = df_reviews['purchase_id'].str.extract(r'(\d+)').astype(int)

# Filter out books with no year
df_books = df_books.dropna(subset=['year'])

# Determine decade
# Decade: 1980s, 1990s, etc.
def get_decade(year):
    return f"{int(year // 10 * 10)}s"

df_books['decade'] = df_books['year'].apply(get_decade)

# Join books and reviews
# We want to keep reviews that match books
merged = pd.merge(df_reviews, df_books, on='id_num', how='inner')

# Convert rating to float
merged['rating'] = merged['rating'].astype(float)

# We need to answer: Which decade has the highest average rating among decades with at least 10 distinct books that have been rated?

# Group by decade
decade_stats = merged.groupby('decade').agg(
    distinct_books=('id_num', 'nunique'),
    average_rating=('rating', 'mean')
).reset_index()

# Filter decades with at least 10 distinct books
qualified_decades = decade_stats[decade_stats['distinct_books'] >= 10]

# Find the decade with the highest average rating
if not qualified_decades.empty:
    best_decade = qualified_decades.loc[qualified_decades['average_rating'].idxmax()]
    result = {
        "decade": best_decade['decade'],
        "average_rating": best_decade['average_rating'],
        "distinct_books": best_decade['distinct_books']
    }
else:
    result = "No decade meets the criteria"

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_function-call-9073474900337945762': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-9362835081464333326': [{'cnt': '1833'}], 'var_function-call-3383126299682018077': [{'cnt': '200'}], 'var_function-call-3974352914324142375': 'file_storage/function-call-3974352914324142375.json', 'var_function-call-12365344636262352208': 'file_storage/function-call-12365344636262352208.json'}

exec(code, env_args)
