code = """import pandas as pd
import json
import re

# Load data using the file paths from previous steps
# The variable name holds the file path string
file_path_books = locals()['var_function-call-5338804074318671779']
file_path_reviews = locals()['var_function-call-5338804074318669420']

with open(file_path_books, 'r') as f:
    books_data = json.load(f)
with open(file_path_reviews, 'r') as f:
    reviews_data = json.load(f)

df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

# Process IDs
# Extract numbers from IDs
df_books['id_num'] = df_books['book_id'].str.extract(r'(\d+)').astype(int)
df_reviews['id_num'] = df_reviews['purchase_id'].str.extract(r'(\d+)').astype(int)

# Extract Year from details
def extract_year(text):
    if not text:
        return None
    
    # Check for Month Day, Year pattern
    match = re.search(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+(\d{4})', text)
    if match:
        return int(match.group(1))

    # Check for 'published ... Year' pattern
    match = re.search(r'published.*?(\d{4})', text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    
    # Check for 'released ... Year' pattern
    match = re.search(r'released.*?(\d{4})', text, re.IGNORECASE)
    if match:
        return int(match.group(1))

    # Check for general 4-digit year if other patterns fail
    # Be careful not to pick up ISBNs or page counts
    # Look for '19xx' or '20xx'
    match = re.search(r'\b(19\d{2}|20\d{2})\b', text)
    if match:
        return int(match.group(1))
        
    return None

df_books['year'] = df_books['details'].apply(extract_year)

# Calculate average rating per book
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'])
# Average rating per book
book_avg_ratings = df_reviews.groupby('id_num')['rating'].mean().reset_index()
book_avg_ratings.columns = ['id_num', 'avg_rating']

# Merge
merged = pd.merge(df_books, book_avg_ratings, on='id_num', how='inner')
merged = merged.dropna(subset=['year'])
merged['year'] = merged['year'].astype(int)

# Assign Decade
merged['decade'] = (merged['year'] // 10) * 10

# Group by Decade
decade_stats = merged.groupby('decade').agg(
    book_count=('id_num', 'nunique'),
    avg_rating=('avg_rating', 'mean')
).reset_index()

# Filter
filtered = decade_stats[decade_stats['book_count'] >= 10].copy()

# Find best
best_decade = filtered.sort_values(by='avg_rating', ascending=False).head(1)

# Format result
result = []
if not best_decade.empty:
    decade_val = int(best_decade['decade'].iloc[0])
    avg_r = best_decade['avg_rating'].iloc[0]
    result.append({"decade": f"{decade_val}s", "average_rating": avg_r, "book_count": int(best_decade['book_count'].iloc[0])})

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_function-call-7216776813414452879': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-7216776813414449292': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-5360091024620676715': [{'book_id': 'bookid_186'}], 'var_function-call-5360091024620677050': [{'count': '200'}], 'var_function-call-5360091024620677385': [{'count(*)': '1833'}], 'var_function-call-5338804074318671779': 'file_storage/function-call-5338804074318671779.json', 'var_function-call-5338804074318669420': 'file_storage/function-call-5338804074318669420.json'}

exec(code, env_args)
