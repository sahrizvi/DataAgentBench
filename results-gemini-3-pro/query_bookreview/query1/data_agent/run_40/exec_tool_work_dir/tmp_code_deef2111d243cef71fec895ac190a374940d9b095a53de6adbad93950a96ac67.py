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

# Helper function to extract year
def extract_year(text):
    if not isinstance(text, str):
        return None
    # Try pattern: "published ... [Year]"
    match = re.search(r'(?:published|released).*?\b((?:19|20)\d{2})\b', text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    
    # Try pattern: just a 4-digit year (1900-2023)
    matches = re.findall(r'\b(19\d{2}|20[0-2]\d)\b', text)
    if matches:
        return int(matches[0])
    return None

df_books['year'] = df_books['details'].apply(extract_year)

# Check extraction success
print("Sample years:")
print(df_books[['details', 'year']].head().to_string())

# Helper function to extract ID
def extract_id(text, prefix):
    if not isinstance(text, str):
        return None
    try:
        # Check if text starts with prefix
        if text.startswith(prefix):
            return int(text[len(prefix):])
        # Maybe fuzzy join means just matching numbers regardless of prefix?
        # Or maybe bookid_1 matches purchaseid_1?
        # Let's try stripping non-digits
        digits = re.sub(r'\D', '', text)
        if digits:
            return int(digits)
        return None
    except:
        return None

df_books['id_num'] = df_books['book_id'].apply(lambda x: extract_id(x, 'bookid_'))
df_reviews['id_num'] = df_reviews['purchase_id'].apply(lambda x: extract_id(x, 'purchaseid_'))

print("Sample IDs:")
print(df_books[['book_id', 'id_num']].head().to_string())
print(df_reviews[['purchase_id', 'id_num']].head().to_string())

# Drop missing year books
df_books = df_books.dropna(subset=['year'])

# Convert to decade
df_books['decade'] = (df_books['year'] // 10) * 10
df_books['decade_str'] = df_books['decade'].astype(int).astype(str) + 's'

# Merge on id_num
merged = pd.merge(df_reviews, df_books, on='id_num', how='inner')
print(f"Merged count: {len(merged)}")

# Aggregation
decade_stats = merged.groupby('decade_str').agg(
    avg_rating=('rating', 'mean'),
    book_count=('id_num', 'nunique')
).reset_index()

print("Decade stats:")
print(decade_stats)

filtered_decades = decade_stats[decade_stats['book_count'] >= 10].copy()

if not filtered_decades.empty:
    top_decade = filtered_decades.sort_values(by='avg_rating', ascending=False).iloc[0]
    print("__RESULT__:")
    print(json.dumps(top_decade['decade_str']))
else:
    print("__RESULT__:")
    print(json.dumps("No matching decade"))"""

env_args = {'var_function-call-17059339761565009177': [{'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'book_id': 'bookid_1'}, {'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.', 'book_id': 'bookid_2'}, {'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.', 'book_id': 'bookid_3'}, {'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.', 'book_id': 'bookid_4'}, {'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.', 'book_id': 'bookid_5'}], 'var_function-call-9213104948124402828': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-7911499635210337761': [{'count': '200'}], 'var_function-call-8929464142869219078': [{'count(*)': '1833'}], 'var_function-call-17894281087799120001': 'file_storage/function-call-17894281087799120001.json', 'var_function-call-10804233732653904371': 'file_storage/function-call-10804233732653904371.json', 'var_function-call-14339715515068141070': [], 'var_function-call-15495888401854620138': 'No matching decade', 'var_function-call-11996045412878413355': 'No matching decade'}

exec(code, env_args)
