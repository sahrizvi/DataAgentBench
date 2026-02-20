code = """import json
import pandas as pd
import re

# Load data
with open(locals()['var_function-call-14460880874959676585'], 'r') as f:
    books_data = json.load(f)

with open(locals()['var_function-call-2388459642956064486'], 'r') as f:
    reviews_data = json.load(f)

# Create DataFrames
df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

# Process books
def extract_year(text):
    if not text:
        return None
    # Look for 4 digits in the range 1900-2023 associated with published/released
    # Try specific patterns first
    match = re.search(r'(?:published|released).*?(\d{4})', text, re.IGNORECASE)
    if match:
        year = int(match.group(1))
        if 1900 <= year <= 2023:
            return year
    
    # Fallback: finding any 4 digit year, but risky with ISBNs. 
    # Let's rely on published/released keyword as it seems consistent in samples.
    # Check for date patterns like "January 1, 2004" or "May 20, 1996"
    match_date = re.search(r'(\d{4})', text) # Simple fallback if keywords miss, but might hit ISBN.
    # Given the samples, "published" or "released" is almost always there.
    return None

df_books['year'] = df_books['details'].apply(extract_year)
df_books = df_books.dropna(subset=['year'])
df_books['year'] = df_books['year'].astype(int)
df_books['decade'] = (df_books['year'] // 10) * 10
df_books['decade_str'] = df_books['decade'].astype(str) + 's'

# Extract numeric ID for joining
# Book ID: "bookid_1" -> 1
# Purchase ID: "purchaseid_1" -> 1
df_books['id_num'] = df_books['book_id'].str.extract(r'(\d+)').astype(int)
df_reviews['id_num'] = df_reviews['purchase_id'].str.extract(r'(\d+)').astype(int)

# Merge
# We only care about books that have reviews
merged = pd.merge(df_reviews, df_books, on='id_num', how='inner')

# Convert rating to float
merged['rating'] = merged['rating'].astype(float)

# Filter decades with at least 10 distinct books
decade_counts = merged.groupby('decade_str')['id_num'].nunique()
valid_decades = decade_counts[decade_counts >= 10].index.tolist()

# Calculate average rating for valid decades
# Option 1: Average of all ratings
avg_ratings = merged[merged['decade_str'].isin(valid_decades)].groupby('decade_str')['rating'].mean()

# Option 2: Average of book averages (just to check)
book_avgs = merged.groupby(['decade_str', 'id_num'])['rating'].mean().reset_index()
avg_ratings_2 = book_avgs[book_avgs['decade_str'].isin(valid_decades)].groupby('decade_str')['rating'].mean()

print("__RESULT__:")
print(json.dumps({
    "decade_counts": decade_counts.to_dict(),
    "valid_decades": valid_decades,
    "avg_ratings_all_reviews": avg_ratings.to_dict(),
    "avg_ratings_book_means": avg_ratings_2.to_dict(),
    "highest_decade": avg_ratings.idxmax() if not avg_ratings.empty else None
}))"""

env_args = {'var_function-call-4625821707826321376': ['books_info'], 'var_function-call-14689115865615028949': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-2558492674629928494': [{'count': '200'}], 'var_function-call-239960103970687564': [{'COUNT(*)': '1833'}], 'var_function-call-6606013291303918156': [{'purchase_id': 'purchaseid_186'}, {'purchase_id': 'purchaseid_191'}, {'purchase_id': 'purchaseid_190'}, {'purchase_id': 'purchaseid_8'}, {'purchase_id': 'purchaseid_178'}], 'var_function-call-14460880874959676585': 'file_storage/function-call-14460880874959676585.json', 'var_function-call-2388459642956064486': 'file_storage/function-call-2388459642956064486.json'}

exec(code, env_args)
