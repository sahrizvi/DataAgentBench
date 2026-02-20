code = """import pandas as pd
import json
import re

# Load data
with open('var_function-call-5338804074318671779.json', 'r') as f:
    books_data = json.load(f)
with open('var_function-call-5338804074318669420.json', 'r') as f:
    reviews_data = json.load(f)

df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

# Process IDs
df_books['id_num'] = df_books['book_id'].str.extract(r'(\d+)').astype(int)
df_reviews['id_num'] = df_reviews['purchase_id'].str.extract(r'(\d+)').astype(int)

# Extract Year from details
def extract_year(text):
    if not text:
        return None
    # Pattern 1: Month Day, Year (e.g., January 1, 2004)
    match = re.search(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+(\d{4})', text)
    if match:
        return int(match.group(1))
    
    # Pattern 2: published ... Year (fallback)
    match = re.search(r'published.*?(\d{4})', text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    
    # Pattern 3: released ... Year
    match = re.search(r'released.*?(\d{4})', text, re.IGNORECASE)
    if match:
        return int(match.group(1))
        
    return None

df_books['year'] = df_books['details'].apply(extract_year)

# Check for missing years
missing_years = df_books[df_books['year'].isnull()]
# print(f"Missing years count: {len(missing_years)}")
# if len(missing_years) > 0:
#     print(missing_years['details'].head().tolist())

# Calculate average rating per book
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'])
book_ratings = df_reviews.groupby('id_num')['rating'].agg(['mean', 'count']).reset_index()
book_ratings.rename(columns={'mean': 'avg_rating', 'count': 'review_count'}, inplace=True)

# Merge
merged = pd.merge(df_books, book_ratings, on='id_num', how='inner')

# Assign Decade
merged = merged.dropna(subset=['year']) # Drop books with unknown year
merged['year'] = merged['year'].astype(int)
merged['decade'] = (merged['year'] // 10) * 10
merged['decade_str'] = merged['decade'].astype(str) + 's'

# Group by Decade
decade_stats = merged.groupby('decade_str').agg(
    book_count=('id_num', 'nunique'),
    decade_avg_rating=('avg_rating', 'mean')
).reset_index()

# Filter for at least 10 distinct books
filtered_decades = decade_stats[decade_stats['book_count'] >= 10]

# Find best decade
best_decade = filtered_decades.sort_values(by='decade_avg_rating', ascending=False).head(1)

print("__RESULT__:")
print(json.dumps(best_decade.to_dict(orient='records')))"""

env_args = {'var_function-call-7216776813414452879': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-7216776813414449292': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-5360091024620676715': [{'book_id': 'bookid_186'}], 'var_function-call-5360091024620677050': [{'count': '200'}], 'var_function-call-5360091024620677385': [{'count(*)': '1833'}], 'var_function-call-5338804074318671779': 'file_storage/function-call-5338804074318671779.json', 'var_function-call-5338804074318669420': 'file_storage/function-call-5338804074318669420.json'}

exec(code, env_args)
