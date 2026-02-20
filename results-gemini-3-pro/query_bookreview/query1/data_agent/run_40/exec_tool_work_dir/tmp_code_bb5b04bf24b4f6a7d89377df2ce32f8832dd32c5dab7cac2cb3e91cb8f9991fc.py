code = """import pandas as pd
import json
import re

# Load data
with open(locals()['var_function-call-17894281087799120001'], 'r') as f:
    books_data = json.load(f)
with open(locals()['var_function-call-10804233732653904371'], 'r') as f:
    reviews_data = json.load(f)

df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

# Extract year
def extract_year(text):
    if not text:
        return None
    # Look for 'published' or 'released' followed by a year
    # Case insensitive
    # Matches: published ... 1999, released ... 2020
    match = re.search(r'(?:published|released).*?\b((?:19|20)\d{2})\b', text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    
    # Fallback: just look for a year 1900-2023 if the above fails
    # This is riskier but might be needed if "published" keyword is missing or phrased differently.
    # Exclude if it looks like part of ISBN (usually >4 digits, but here looking for exactly 4 digits \b\d{4}\b)
    # But ISBN-10 is 10 digits.
    # Let's try to find a year that is not part of a larger number.
    matches = re.findall(r'\b(19\d{2}|20[0-2]\d)\b', text)
    if matches:
        # If multiple, take the first one? Or maybe the one that isn't page count?
        # Page counts often have "pages" after.
        # Let's verify context for the first match?
        # For now, taking the first valid year found.
        return int(matches[0])
    return None

df_books['year'] = df_books['details'].apply(extract_year)

# Drop books with no year
df_books = df_books.dropna(subset=['year'])

# Convert to decade
df_books['decade'] = (df_books['year'] // 10) * 10
df_books['decade_str'] = df_books['decade'].astype(int).astype(str) + 's'

# Convert rating to float
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

# Merge
# book_id in books, purchase_id in reviews
merged = pd.merge(df_reviews, df_books, left_on='purchase_id', right_on='book_id', how='inner')

# Aggregation
# Filter: decades with at least 10 distinct books
decade_stats = merged.groupby('decade_str').agg(
    avg_rating=('rating', 'mean'),
    book_count=('book_id', 'nunique')
).reset_index()

filtered_decades = decade_stats[decade_stats['book_count'] >= 10].copy()

# Sort by avg_rating desc
result = filtered_decades.sort_values(by='avg_rating', ascending=False)

print("__RESULT__:")
print(result.to_json(orient='records'))"""

env_args = {'var_function-call-17059339761565009177': [{'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'book_id': 'bookid_1'}, {'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.', 'book_id': 'bookid_2'}, {'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.', 'book_id': 'bookid_3'}, {'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.', 'book_id': 'bookid_4'}, {'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.', 'book_id': 'bookid_5'}], 'var_function-call-9213104948124402828': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-7911499635210337761': [{'count': '200'}], 'var_function-call-8929464142869219078': [{'count(*)': '1833'}], 'var_function-call-17894281087799120001': 'file_storage/function-call-17894281087799120001.json', 'var_function-call-10804233732653904371': 'file_storage/function-call-10804233732653904371.json'}

exec(code, env_args)
