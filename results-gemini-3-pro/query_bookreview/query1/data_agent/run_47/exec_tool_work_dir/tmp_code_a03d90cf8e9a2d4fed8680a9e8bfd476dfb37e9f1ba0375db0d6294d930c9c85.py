code = """# List all decades
import json
import re
import pandas as pd

books_file = locals()['var_function-call-3066775094646459386']
reviews_file = locals()['var_function-call-5947289885956607296']

with open(books_file, 'r') as f:
    books_data = json.load(f)
with open(reviews_file, 'r') as f:
    reviews_data = json.load(f)

df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

def extract_id(s):
    if pd.isna(s): return None
    m = re.search(r'(\d+)$', s)
    if m:
        return int(m.group(1))
    return None

df_books['id'] = df_books['book_id'].apply(extract_id)
df_reviews['id'] = df_reviews['purchase_id'].apply(extract_id)

month_pattern = r'(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)'
date_pattern = re.compile(month_pattern + r'\s+(?:\d{1,2},?\s+)?(\d{4})', re.IGNORECASE)

def extract_year(s):
    if pd.isna(s): return None
    matches = date_pattern.findall(s)
    if matches:
        return int(matches[0])
    return None

df_books['year'] = df_books['details'].apply(extract_year)

# Filter valid
df_books = df_books.dropna(subset=['id', 'year'])
df_reviews = df_reviews.dropna(subset=['id', 'rating'])
df_reviews['rating'] = df_reviews['rating'].astype(float)

# Book Avg
book_ratings = df_reviews.groupby('id')['rating'].mean().reset_index()
book_ratings.columns = ['id', 'avg_rating']

# Merge
merged = pd.merge(book_ratings, df_books[['id', 'year']], on='id', how='inner')
merged['decade'] = (merged['year'] // 10) * 10
merged['decade_str'] = merged['decade'].astype(int).astype(str) + 's'

# Agg
decade_stats = merged.groupby('decade_str').agg(
    book_count=('id', 'count'),
    average_rating=('avg_rating', 'mean')
).reset_index().sort_values(by='average_rating', ascending=False)

print("__RESULT__:")
print(decade_stats.to_json(orient='records'))"""

env_args = {'var_function-call-1231660614224188337': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-12087562879080618544': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-17821108303418904348': [{'book_id': 'bookid_186'}], 'var_function-call-9768576688950840343': [{'count': '200'}], 'var_function-call-13324393016607837260': [{'count(*)': '1833'}], 'var_function-call-3066775094646459386': 'file_storage/function-call-3066775094646459386.json', 'var_function-call-5947289885956607296': 'file_storage/function-call-5947289885956607296.json', 'var_function-call-13821763643036164946': [{'decade_str': '1980.0s', 'book_count': 11, 'average_rating': 4.5481993852}, {'decade_str': '2020.0s', 'book_count': 21, 'average_rating': 4.5253052503}, {'decade_str': '2010.0s', 'book_count': 88, 'average_rating': 4.4051393366}, {'decade_str': '2000.0s', 'book_count': 47, 'average_rating': 4.3575175138}, {'decade_str': '1990.0s', 'book_count': 16, 'average_rating': 4.124937996}], 'var_function-call-12295038481939239344': ['This book is written in English and is available in a paperback format consisting of 8 pages. It has an ISBN 10 number of 0780274164 and an ISBN 13 number of 978-0780274167. The item weighs 1.01 pounds.', 'This book is written in English and has an ISBN-10 of 0553819399 and an ISBN-13 of 978-0553819397. It weighs 1.06 pounds and has dimensions of 5 inches in width, 1.65 inches in depth, and 7.8 inches in height.', '', 'This book is written in English and has an ISBN 10 of 1938923391 and an ISBN 13 of 978-1938923395. It weighs 14.4 ounces.', 'This book has an ISBN-10 number of 1925849058 and an ISBN-13 number of 978-1925849059. It weighs 1.06 pounds and has dimensions of 9.13 inches in width, 0.35 inches in depth, and 11.93 inches in height.', '', '', '', 'The book has a weight of 4 ounces.', 'The book has a weight of 9.6 ounces.', 'The book has a weight of 3.04 ounces and its dimensions measure 0.01 inches in thickness, 7.5 inches in height, and 5.6 inches in width.'], 'var_function-call-11410975913358396193': []}

exec(code, env_args)
