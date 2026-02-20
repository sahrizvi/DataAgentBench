code = """import json
import pandas as pd
import re

# Load data
with open(locals()['var_function-call-8084733100585816512'], 'r') as f:
    books_data = json.load(f)
with open(locals()['var_function-call-14244121816731322471'], 'r') as f:
    reviews_data = json.load(f)

df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

debug_info = {}

# Extract year
def extract_year(text):
    if not isinstance(text, str):
        return None
    matches = re.findall(r'\b(19\d{2}|20[0-2]\d)\b', text)
    if matches:
        return int(matches[0])
    return None

df_books['year'] = df_books['details'].apply(extract_year)
debug_info['years_sample'] = df_books['year'].dropna().head().tolist()

# Extract IDs
df_books['id_num'] = df_books['book_id'].str.extract(r'(\d+)').fillna(-1).astype(int)
df_reviews['id_num'] = df_reviews['purchase_id'].str.extract(r'(\d+)').fillna(-1).astype(int)

debug_info['book_ids_sample'] = df_books['id_num'].head().tolist()
debug_info['review_ids_sample'] = df_reviews['id_num'].head().tolist()

# Join
merged = pd.merge(df_books, df_reviews, on='id_num', how='inner')
debug_info['merged_count'] = len(merged)

if len(merged) > 0:
    merged['rating'] = pd.to_numeric(merged['rating'], errors='coerce')
    
    # Calculate average rating per book first
    book_stats = merged.groupby(['id_num', 'year'])['rating'].mean().reset_index()
    book_stats['decade'] = (book_stats['year'] // 10) * 10
    
    # Group by decade
    decade_stats = book_stats.groupby('decade').agg(
        book_count=('id_num', 'nunique'),
        avg_rating=('rating', 'mean')
    ).reset_index()
    
    debug_info['decade_stats'] = decade_stats.to_dict(orient='records')
else:
    debug_info['decade_stats'] = []

print("__RESULT__:")
print(json.dumps(debug_info))"""

env_args = {'var_function-call-6301180231551585539': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'rating_number': '29'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.', 'rating_number': '1'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.', 'rating_number': '3421'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.', 'rating_number': '40'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.', 'rating_number': '381'}], 'var_function-call-12516702256767511157': [{'count': '200'}], 'var_function-call-9335063315366319309': [{'count(*)': '1833'}], 'var_function-call-8084733100585816512': 'file_storage/function-call-8084733100585816512.json', 'var_function-call-14244121816731322471': 'file_storage/function-call-14244121816731322471.json', 'var_function-call-14551566676066817473': []}

exec(code, env_args)
