code = """import json
import re
import pandas as pd

# Load data
with open(locals()['var_function-call-15402061781472068847'], 'r') as f:
    books_data = json.load(f)

with open(locals()['var_function-call-7488591529204479155'], 'r') as f:
    reviews_data = json.load(f)

# Convert to DataFrame
df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

# Helper to extract ID
def extract_id(s, prefix):
    # s is like 'bookid_1' or 'purchaseid_1'
    # returns 1
    if pd.isna(s): return None
    parts = s.split('_')
    if len(parts) > 1 and parts[1].isdigit():
        return int(parts[1])
    return None

df_books['id_num'] = df_books['book_id'].apply(lambda x: extract_id(x, 'bookid'))
df_reviews['id_num'] = df_reviews['purchase_id'].apply(lambda x: extract_id(x, 'purchaseid'))

# Extract Year from details
# Patterns: "published ... on Month Day, Year" or "released on Month Day, Year"
# Also "published in [Year]"
def extract_year(text):
    if not isinstance(text, str): return None
    # Pattern for "Month Day, Year"
    match = re.search(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+(\d{4})', text)
    if match:
        return int(match.group(1))
    
    # Pattern for "published in Year"
    match = re.search(r'published\s+(?:by\s+[^,]+,\s+)?(?:in\s+[^,]+,\s+)?in\s+(\d{4})', text)
    if match:
        return int(match.group(1))
    
    # Fallback: finding a year 1900-2023 near "published" or "released"
    # match = re.search(r'(?:published|released).*?(\d{4})', text, re.IGNORECASE)
    # if match:
    #     y = int(match.group(1))
    #     if 1900 <= y <= 2023:
    #         return y
            
    # Fallback: Just any 19xx or 20xx year
    matches = re.findall(r'\b(19\d{2}|20\d{2})\b', text)
    if matches:
        # Filter reasonable years
        valid_years = [int(y) for y in matches if 1900 <= int(y) <= 2023]
        if valid_years:
            # If multiple, take the first one? Or max?
            # Usually publication date is early in the text.
            return valid_years[0]
            
    return None

df_books['year'] = df_books['details'].apply(extract_year)

# Check overlap
common_ids = set(df_books['id_num']).intersection(set(df_reviews['id_num']))
print(f"DEBUG: Common IDs count: {len(common_ids)}")
print(f"DEBUG: Total books: {len(df_books)}")
print(f"DEBUG: Total reviews: {len(df_reviews)}")

# Merge
df_merged = pd.merge(df_reviews, df_books, on='id_num', how='inner')
print(f"DEBUG: Merged rows: {len(df_merged)}")

# Filter valid years
df_merged = df_merged.dropna(subset=['year'])
df_merged['rating'] = pd.to_numeric(df_merged['rating'], errors='coerce')

# Add decade
df_merged['decade'] = (df_merged['year'] // 10) * 10
df_merged['decade_str'] = df_merged['decade'].astype(int).astype(str) + 's'

# Group
grouped = df_merged.groupby('decade_str').agg(
    avg_rating=('rating', 'mean'),
    num_books=('id_num', 'nunique'),
    num_reviews=('rating', 'count')
).reset_index()

# Filter
filtered = grouped[grouped['num_books'] >= 10].sort_values('avg_rating', ascending=False)

print("__RESULT__:")
print(filtered.to_json(orient='records'))"""

env_args = {'var_function-call-4281837029161996813': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-11307843335655272800': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-3217839718216727345': [{'count': '200'}], 'var_function-call-479540908686770265': [{'count(*)': '1833'}], 'var_function-call-15402061781472068847': 'file_storage/function-call-15402061781472068847.json', 'var_function-call-7488591529204479155': 'file_storage/function-call-7488591529204479155.json'}

exec(code, env_args)
