code = """import json
import re
import pandas as pd

# Load data
with open(locals()['var_function-call-4581168591792627923'], 'r') as f:
    books_data = json.load(f)

with open(locals()['var_function-call-18354388691561664074'], 'r') as f:
    reviews_data = json.load(f)

# Create DataFrames
df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

# Extract integer ID
def extract_id(s, prefix):
    if pd.isna(s):
        return -1
    # assuming format prefix_NUMBER
    # check if prefix is present
    if s.startswith(prefix):
        try:
            return int(s[len(prefix):])
        except:
            return -1
    # fallback: extract first sequence of digits
    m = re.search(r'\d+', s)
    if m:
        return int(m.group(0))
    return -1

df_books['id_num'] = df_books['book_id'].apply(lambda x: extract_id(x, 'bookid_'))
df_reviews['id_num'] = df_reviews['purchase_id'].apply(lambda x: extract_id(x, 'purchaseid_'))

# Extract Year from details
def extract_year(details):
    if not isinstance(details, str):
        return None
    
    # Priority 1: "on Month Day, Year" or "on Month Day Year"
    # e.g., on January 1, 2004
    m1 = re.search(r'on\s+[A-Za-z]+\s+\d{1,2},?\s+(\d{4})', details)
    if m1:
        return int(m1.group(1))
    
    # Priority 2: "in Month Year"
    m2 = re.search(r'in\s+[A-Za-z]+\s+(\d{4})', details)
    if m2:
        return int(m2.group(1))
        
    # Priority 3: "published ... Year" -- risky, maybe just find a year in 19xx or 20xx
    # Let's try to find any year 1900-2023
    years = re.findall(r'\b(19\d{2}|20[0-2]\d)\b', details)
    if years:
        # If multiple, which one? The text often starts with "Published ...". 
        # Maybe take the first one?
        return int(years[0])
    
    return None

df_books['year'] = df_books['details'].apply(extract_year)

# Drop books without year
df_books = df_books.dropna(subset=['year'])

# Join
# Check for duplicates in books?
# book_id should be unique.
df_books = df_books.drop_duplicates(subset=['id_num'])

merged = pd.merge(df_reviews, df_books, on='id_num', how='inner')

# Convert rating to float
merged['rating'] = pd.to_numeric(merged['rating'], errors='coerce')
merged = merged.dropna(subset=['rating'])

# Add Decade
# Decade definition: 1980s means 1980-1989.
merged['decade_start'] = (merged['year'] // 10) * 10
merged['decade'] = merged['decade_start'].astype(int).astype(str) + 's'

# Aggregation
# Filter decades with >= 10 distinct books
decade_stats = merged.groupby('decade').agg(
    distinct_books=('id_num', 'nunique'),
    avg_rating=('rating', 'mean')
).reset_index()

filtered_decades = decade_stats[decade_stats['distinct_books'] >= 10]

# Sort by avg_rating desc
result = filtered_decades.sort_values(by='avg_rating', ascending=False)

print("__RESULT__:")
print(json.dumps(result.to_dict(orient='records')))"""

env_args = {'var_function-call-2276679140674115627': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-8286769825331596695': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-3347946993610182413': [{'count': '200'}], 'var_function-call-7069546728401593342': [{'COUNT(*)': '1833'}], 'var_function-call-4581168591792627923': 'file_storage/function-call-4581168591792627923.json', 'var_function-call-18354388691561664074': 'file_storage/function-call-18354388691561664074.json'}

exec(code, env_args)
