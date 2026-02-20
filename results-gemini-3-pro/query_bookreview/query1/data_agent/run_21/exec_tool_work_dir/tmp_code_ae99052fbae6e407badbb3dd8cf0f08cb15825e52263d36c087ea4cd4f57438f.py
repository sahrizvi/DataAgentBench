code = """import json
import re
import pandas as pd

# Load data
with open('var_function-call-17597170398027844549.json', 'r') as f:
    books = json.load(f)
with open('var_function-call-5746103583818394624.json', 'r') as f:
    reviews = json.load(f)

# Create DataFrames
df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Extract ID from book_id and purchase_id
def extract_id(s):
    m = re.search(r'_(\d+)$', s)
    if m:
        return int(m.group(1))
    return None

df_books['id'] = df_books['book_id'].apply(extract_id)
df_reviews['id'] = df_reviews['purchase_id'].apply(extract_id)

# Merge
# We want to keep reviews that match books
df_merged = pd.merge(df_reviews, df_books, on='id', how='inner')

# Extract year from details
def extract_year(text):
    if not text:
        return None
    # Look for years 1900-2023
    # Avoid things like "2013th"
    # Regex to find 4 digit number starting with 19 or 20
    # Capture the number
    matches = re.finditer(r'\b(19\d{2}|20[0-2]\d)\b', text)
    candidates = []
    for m in matches:
        # Check if followed by edition suffix
        start, end = m.span()
        # Look ahead a bit
        suffix = text[end:end+5]
        if re.match(r'(st|nd|rd|th)', suffix):
            continue
        candidates.append(int(m.group(1)))
    
    if candidates:
        # Heuristic: usually the date comes with a month
        # Or take the first one found that looks valid
        # In the examples, "released on January 1, 2004", 2004 is found.
        # "published ... in its 2013th edition on March 22, 2013" -> 2013th skipped, 2013 taken.
        # "8082nd edition from January 1, 1994" -> 1994 taken. 
        # But wait, bookid_7 text: "published ... in its second edition in January 2004, is also noted as the 8082nd edition from January 1, 1994."
        # Which decade? Usually the edition being sold. 2004.
        # So taking the first valid year seems correct as the description usually starts with the current edition info.
        return candidates[0]
    return None

df_merged['year'] = df_merged['details'].apply(extract_year)

# Drop rows where year is null
df_merged = df_merged.dropna(subset=['year'])

# Calculate decade
df_merged['decade'] = (df_merged['year'] // 10) * 10
df_merged['decade_str'] = df_merged['decade'].astype(int).astype(str) + 's'

# Convert rating to float
df_merged['rating'] = df_merged['rating'].astype(float)

# Group by decade
stats = df_merged.groupby('decade_str').agg(
    avg_rating=('rating', 'mean'),
    distinct_books=('id', 'nunique'),
    count_reviews=('rating', 'count')
).reset_index()

# Filter
filtered_stats = stats[stats['distinct_books'] >= 10].copy()

# Sort by avg_rating
filtered_stats = filtered_stats.sort_values(by='avg_rating', ascending=False)

print("__RESULT__:")
print(json.dumps(filtered_stats.to_dict(orient='records')))"""

env_args = {'var_function-call-6975577752223171344': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-11336959198502457448': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-15446129666109339953': [{'count': '200'}], 'var_function-call-2982058341310667547': [{'count(*)': '1833'}], 'var_function-call-17597170398027844549': 'file_storage/function-call-17597170398027844549.json', 'var_function-call-5746103583818394624': 'file_storage/function-call-5746103583818394624.json'}

exec(code, env_args)
