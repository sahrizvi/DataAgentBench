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

# Parse year from details
def extract_year(details):
    # Regex for "published ... [Month] [Day], [Year]" or "released ... [Month] [Day], [Year]"
    # Also "published ... [Month] [Year]"
    # Looking for 4 digits after "published" or "released"
    match = re.search(r'(?:published|released).*?(\d{4})', details, re.IGNORECASE)
    if match:
        year = int(match.group(1))
        # Valid range check
        if 1900 <= year <= 2025:
            return year
    
    # Fallback: look for any 4 digits if not found (less reliable, but maybe necessary)
    # But usually details field is consistent. Let's stick to the keyword one first.
    return None

df_books['year'] = df_books['details'].apply(extract_year)

# Drop books without year
df_books = df_books.dropna(subset=['year'])
df_books['year'] = df_books['year'].astype(int)

# Create decade column
# 1980s means 1980-1989. 
df_books['decade'] = (df_books['year'] // 10) * 10
df_books['decade_str'] = df_books['decade'].astype(str) + "s"

# Prepare Join Keys
# book_id is like "bookid_1", purchase_id is like "purchaseid_1"
# We extract the ID number.
df_books['id_num'] = df_books['book_id'].str.extract(r'(\d+)').astype(int)
df_reviews['id_num'] = df_reviews['purchase_id'].str.extract(r'(\d+)').astype(int)

# Filter reviews for valid ratings
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
df_reviews = df_reviews.dropna(subset=['rating'])

# Join reviews with books
merged = pd.merge(df_reviews, df_books, on='id_num', how='inner')

# Calculate distinct rated books per decade
decade_stats = merged.groupby('decade_str').agg(
    distinct_books=('id_num', 'nunique'),
    avg_rating=('rating', 'mean')
).reset_index()

# Filter decades with at least 10 distinct books
valid_decades = decade_stats[decade_stats['distinct_books'] >= 10]

# Find the decade with highest average rating
if not valid_decades.empty:
    best_decade = valid_decades.loc[valid_decades['avg_rating'].idxmax()]
    result = {
        "decade": best_decade['decade_str'],
        "average_rating": best_decade['avg_rating'],
        "distinct_books": int(best_decade['distinct_books'])
    }
else:
    result = {"error": "No decade meets the criteria"}

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_function-call-7846935078876793979': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-4565000254805596521': [{'count': '200'}], 'var_function-call-6157774012479870483': [{'COUNT(*)': '1833'}], 'var_function-call-17584423273886338862': 'file_storage/function-call-17584423273886338862.json', 'var_function-call-9381740438124898103': 'file_storage/function-call-9381740438124898103.json'}

exec(code, env_args)
