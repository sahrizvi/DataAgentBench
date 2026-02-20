code = """import pandas as pd
import json
import re

# Load data
books_data = json.load(open('var_function-call-11951794239785044405.json'))
reviews_data = json.load(open('var_function-call-11355008030497697797.json'))

df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

# Extract integer ID from book_id and purchase_id
def extract_id(s):
    match = re.search(r'(\d+)$', s)
    if match:
        return int(match.group(1))
    return None

df_books['id'] = df_books['book_id'].apply(lambda x: extract_id(x) if x else None)
df_reviews['id'] = df_reviews['purchase_id'].apply(lambda x: extract_id(x) if x else None)

# Extract Year from details
# Pattern: "published ... on [Month] [Day], [Year]" or "released on [Month] [Day], [Year]" or "edition on [Month] [Day], [Year]"
# Or simply find the first 4 digit year in the range 1900-2024.
def extract_year(s):
    if not s:
        return None
    # Look for 4 digits
    matches = re.findall(r'\b(19\d{2}|20\d{2})\b', s)
    if matches:
        # If multiple, usually the publication date is early or part of a full date string.
        # Let's try to be more specific if possible.
        # "published ... on ... Year"
        # "released on ... Year"
        # Let's try to parse dates. But regex is robust enough for simple year extraction if we trust the text.
        # In the examples: "January 1, 2004" -> 2004. "May 20, 1996" -> 1996.
        # "2013th edition on March 22, 2013" -> 2013.
        # "8082nd edition from January 1, 1994" -> 1994.
        # It seems taking the year associated with a date pattern is best.
        # But simply taking the first valid year often works.
        # Let's prioritize years appearing after "published" or "released".
        
        # specific search for date pattern like "Month dd, yyyy" or "Month yyyy"
        date_match = re.search(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+(19\d{2}|20\d{2})', s)
        if date_match:
            return int(date_match.group(1))
        
        # Fallback to just finding year
        return int(matches[0])
    return None

df_books['year'] = df_books['details'].apply(extract_year)

# Drop books with no year
df_books_clean = df_books.dropna(subset=['year'])

# Merge
# inner join to keep only rated books
merged = pd.merge(df_reviews, df_books_clean, on='id', how='inner')

# Add Decade
# 1980s means 1980-1989.
merged['decade'] = (merged['year'] // 10) * 10
merged['decade_str'] = merged['decade'].astype(int).astype(str) + "s"

# Group by Decade
# We need:
# 1. Count of distinct books (id)
# 2. Average rating (mean of rating column)
# Note: rating in review is likely string or float. Check type.
merged['rating'] = pd.to_numeric(merged['rating'], errors='coerce')

decade_stats = merged.groupby('decade_str').agg(
    distinct_books=('id', 'nunique'),
    avg_rating=('rating', 'mean'),
    review_count=('rating', 'count')
).reset_index()

# Filter
filtered_decades = decade_stats[decade_stats['distinct_books'] >= 10]

# Find max
if not filtered_decades.empty:
    best_decade = filtered_decades.loc[filtered_decades['avg_rating'].idxmax()]
    result = best_decade['decade_str']
    debug_info = filtered_decades[['decade_str', 'distinct_books', 'avg_rating']].to_dict(orient='records')
else:
    result = "No decade meets criteria"
    debug_info = decade_stats[['decade_str', 'distinct_books', 'avg_rating']].to_dict(orient='records')

print("__RESULT__:")
print(json.dumps({"answer": result, "debug": debug_info}))"""

env_args = {'var_function-call-272452347185540501': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-7758564921818992438': [{'count': '200'}], 'var_function-call-18259465167187388799': [{'count(*)': '1833'}], 'var_function-call-11951794239785044405': 'file_storage/function-call-11951794239785044405.json', 'var_function-call-11355008030497697797': 'file_storage/function-call-11355008030497697797.json'}

exec(code, env_args)
