code = """import json
import re
import pandas as pd

# Get file paths from variables
books_file = locals()['var_function-call-3974352914324142375']
reviews_file = locals()['var_function-call-12365344636262352208']

# Load data
with open(books_file, 'r') as f:
    books_data = json.load(f)

with open(reviews_file, 'r') as f:
    reviews_data = json.load(f)

# Create DataFrames
df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

# Extract year from details
def extract_year(details):
    # Pattern: Look for 4 digits 19xx or 20xx
    # Priority given to "published ... YYYY" or "released ... YYYY"
    # But often the year is just present.
    # Let's look for "published.*?(\d{4})"
    if not isinstance(details, str):
        return None
    
    # Try to find a year associated with "published" or "released"
    match = re.search(r'(?:published|released).*?(\d{4})', details, re.IGNORECASE)
    if match:
        return int(match.group(1))
    
    # Fallback: finding any 19xx or 20xx date
    # We want to be careful not to pick up other numbers, so let's look for 19xx or 20xx
    # and maybe verify it's a plausible year (1900-2024)
    # Also handle "first edition ... 1994" etc.
    matches = re.findall(r'\b(19\d{2}|20[0-2]\d)\b', details)
    if matches:
        # If multiple years, maybe take the earliest? Or the first mentioned?
        # Usually the first mentioned is the publication date.
        return int(matches[0])
    return None

df_books['year'] = df_books['details'].apply(extract_year)

# Filter out books with no valid year
df_books = df_books.dropna(subset=['year'])

# Extract numeric ID for join
# book_id: bookid_X -> X
# purchase_id: purchaseid_X -> X
# Note: purchase_id is in review table, book_id in books_info
# Let's extract X.
df_books['id_num'] = df_books['book_id'].astype(str).str.extract(r'(\d+)').astype(int)
df_reviews['id_num'] = df_reviews['purchase_id'].astype(str).str.extract(r'(\d+)').astype(int)

# Merge
# We want to keep reviews that match books with years
merged = pd.merge(df_reviews, df_books[['id_num', 'year']], on='id_num', how='inner')

# Convert rating to float
merged['rating'] = pd.to_numeric(merged['rating'], errors='coerce')
merged = merged.dropna(subset=['rating'])

# Determine decade
# Decade: 1980s, 1990s, etc.
def get_decade(year):
    return f"{int(year // 10 * 10)}s"

merged['decade'] = merged['year'].apply(get_decade)

# Group by decade
# We need distinct books count and average rating
decade_stats = merged.groupby('decade').agg(
    distinct_books=('id_num', 'nunique'),
    average_rating=('rating', 'mean')
).reset_index()

# Filter: at least 10 distinct books
qualified_decades = decade_stats[decade_stats['distinct_books'] >= 10].copy()

# Sort by average rating descending
qualified_decades = qualified_decades.sort_values(by='average_rating', ascending=False)

# Prepare result
if not qualified_decades.empty:
    best_decade = qualified_decades.iloc[0]
    result = {
        "decade": best_decade['decade'],
        "average_rating": best_decade['average_rating'],
        "distinct_books": int(best_decade['distinct_books']),
        "all_decades": decade_stats.to_dict(orient='records')
    }
else:
    result = {
        "error": "No decade meets criteria",
        "all_decades": decade_stats.to_dict(orient='records')
    }

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_function-call-9073474900337945762': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-9362835081464333326': [{'cnt': '1833'}], 'var_function-call-3383126299682018077': [{'cnt': '200'}], 'var_function-call-3974352914324142375': 'file_storage/function-call-3974352914324142375.json', 'var_function-call-12365344636262352208': 'file_storage/function-call-12365344636262352208.json'}

exec(code, env_args)
