code = """import json
import re
import pandas as pd

# Load data
with open(locals()['var_function-call-12676996466119317051'], 'r') as f:
    books = json.load(f)
with open(locals()['var_function-call-9741256298441356484'], 'r') as f:
    reviews = json.load(f)

# Process books to extract year
book_years = {}
for book in books:
    b_id = book['book_id']
    details = book.get('details', '')
    if not details:
        continue
    
    # Try to find year
    # Patterns: "published ... 2004", "released ... 1999"
    # match year between 1900 and 2023
    
    # We look for a year that is likely the publication year.
    # Strategy: Find all 4-digit numbers 19xx or 20xx.
    # Prioritize those following "published" or "released".
    
    candidates = []
    # Find all (19|20)\d{2}
    matches = list(re.finditer(r'(?:published|released).*?(\b(19|20)\d{2}\b)', details, re.IGNORECASE))
    if matches:
        year = int(matches[0].group(1))
        book_years[b_id] = year
    else:
        # Fallback: just finding a year
        matches_all = re.findall(r'\b(19|20)\d{2}\b', details)
        if matches_all:
            # Take the first one found?
            # Filter out if it looks like part of ISBN?
            # ISBN usually has dashes or is long, but here we look for word boundary 4 digits.
            # But "ISBN-10 of 0701169850" -> "9850" might be matched if year range was wider, but we use 19xx/20xx.
            # "ISBN-13 of 978-0701169855" -> "1985" might be inside? No, "978..."
            # Let's just take the first valid year.
            year = int(matches_all[0])
            book_years[b_id] = year

# Convert reviews to DataFrame
df_reviews = pd.DataFrame(reviews)
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

# Map purchase_id to book_id
# purchaseid_X -> bookid_X
df_reviews['book_id'] = df_reviews['purchase_id'].str.replace('purchaseid', 'bookid')

# Merge
df_reviews['year'] = df_reviews['book_id'].map(book_years)

# Drop reviews with no year
df_merged = df_reviews.dropna(subset=['year']).copy()
df_merged['year'] = df_merged['year'].astype(int)

# Calculate decade
df_merged['decade'] = (df_merged['year'] // 10) * 10
df_merged['decade_str'] = df_merged['decade'].astype(str) + 's'

# Group by decade
decade_stats = df_merged.groupby('decade_str').agg(
    distinct_books=('book_id', 'nunique'),
    avg_rating=('rating', 'mean')
).reset_index()

# Filter
qualified_decades = decade_stats[decade_stats['distinct_books'] >= 10]

# Sort by avg_rating
result = qualified_decades.sort_values(by='avg_rating', ascending=False)

print("__RESULT__:")
print(result.to_json(orient='records'))"""

env_args = {'var_function-call-14391079220039824156': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-12032611119589619147': [{'count': '200'}], 'var_function-call-14893637540441165934': [{'COUNT(*)': '1833'}], 'var_function-call-12676996466119317051': 'file_storage/function-call-12676996466119317051.json', 'var_function-call-9741256298441356484': 'file_storage/function-call-9741256298441356484.json'}

exec(code, env_args)
