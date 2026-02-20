code = """import pandas as pd
import json
import re

# Load data
file_path_books = locals()['var_function-call-5338804074318671779']
file_path_reviews = locals()['var_function-call-5338804074318669420']

with open(file_path_books, 'r') as f:
    books_data = json.load(f)
with open(file_path_reviews, 'r') as f:
    reviews_data = json.load(f)

df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

# ID Extraction
df_books['id_num'] = df_books['book_id'].str.extract(r'(\d+)').astype(float)
df_reviews['id_num'] = df_reviews['purchase_id'].str.extract(r'(\d+)').astype(float)

# Robust Year Extraction
def extract_year_robust(text):
    if not isinstance(text, str):
        return None
    
    # Priority 1: Date format (Month DD, YYYY)
    match = re.search(r'(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2},?\s+(\d{4})', text, re.IGNORECASE)
    if match:
        y = int(match.group(1))
        if 1900 <= y <= 2024:
            return y

    # Priority 2: "published/released ... YYYY"
    # Look for year within 50 chars of "published"
    match = re.search(r'(?:published|released).{0,50}?(\d{4})', text, re.IGNORECASE)
    if match:
        y = int(match.group(1))
        if 1900 <= y <= 2024:
            return y

    # Priority 3: Any valid year
    matches = re.findall(r'\d{4}', text)
    valid_years = [int(y) for y in matches if 1900 <= int(y) <= 2024]
    if valid_years:
        return valid_years[0] # Pick the first valid year found

    return None

df_books['year'] = df_books['details'].apply(extract_year_robust)

# Filter out books with no year
df_books_clean = df_books.dropna(subset=['year'])

# Calculate average rating per book
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
book_ratings = df_reviews.groupby('id_num')['rating'].mean().reset_index()
book_ratings.columns = ['id_num', 'avg_rating']

# Merge
merged = pd.merge(df_books_clean, book_ratings, on='id_num', how='inner')
merged['year'] = merged['year'].astype(int)

# Assign Decade
merged['decade'] = (merged['year'] // 10) * 10
merged['decade_str'] = merged['decade'].astype(str) + 's'

# Group by Decade
decade_stats = merged.groupby('decade_str').agg(
    book_count=('id_num', 'nunique'),
    decade_avg_rating=('avg_rating', 'mean')
).reset_index()

# Filter
filtered = decade_stats[decade_stats['book_count'] >= 10].copy()

# Find best
best_decade = filtered.sort_values(by='decade_avg_rating', ascending=False).head(1)

print("__RESULT__:")
if not best_decade.empty:
    res = best_decade.iloc[0].to_dict()
    # Ensure JSON serializable
    res['book_count'] = int(res['book_count'])
    print(json.dumps(res))
else:
    print(json.dumps({"error": "No decades found", "stats": decade_stats.to_dict(orient='records')}))"""

env_args = {'var_function-call-7216776813414452879': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-7216776813414449292': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-5360091024620676715': [{'book_id': 'bookid_186'}], 'var_function-call-5360091024620677050': [{'count': '200'}], 'var_function-call-5360091024620677385': [{'count(*)': '1833'}], 'var_function-call-5338804074318671779': 'file_storage/function-call-5338804074318671779.json', 'var_function-call-5338804074318669420': 'file_storage/function-call-5338804074318669420.json', 'var_function-call-9132499516586371892': [{'decade': '1980s', 'average_rating': 4.5481993851559075, 'book_count': 11}], 'var_function-call-4965347378229887521': {'status': 'debug complete'}, 'var_function-call-2448011590975388297': {'books_count': 200, 'reviews_count': 1833, 'overlap_count': 200, 'books_with_year': 0, 'merged_rows': 1833, 'decade_counts': {}, 'decade_avg_rating': {}}, 'var_function-call-3343962849344017994': {'sample': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'count': 0}, 'var_function-call-1535795940893581888': {'matches': ['1', '2004', '196', '10', '0701169850', '13', '978', '0701169855', '10', '1', '5', '39', '0', '71', '7', '48']}}

exec(code, env_args)
