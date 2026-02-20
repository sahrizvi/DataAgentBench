code = """import pandas as pd
import json
import re

# Load data
with open(locals()['var_function-call-17584423273886338862'], 'r') as f:
    books_data = json.load(f)
with open(locals()['var_function-call-9381740438124898103'], 'r') as f:
    reviews_data = json.load(f)

df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

def extract_year(details):
    if not isinstance(details, str):
        return None
    match = re.search(r'(?:published|released).*?(\d{4})', details, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None

df_books['year'] = df_books['details'].apply(extract_year)
df_books = df_books.dropna(subset=['year'])
df_books['year'] = df_books['year'].astype(int)

df_books['decade'] = (df_books['year'] // 10) * 10
df_books['decade_str'] = df_books['decade'].astype(str) + "s"

# Parse IDs
df_books['id_num'] = df_books['book_id'].str.extract(r'(\d+)').astype(int)
df_reviews['id_num'] = df_reviews['purchase_id'].str.extract(r'(\d+)').astype(int)
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

# Join
merged = pd.merge(df_reviews, df_books, on='id_num', how='inner')

stats = merged.groupby('decade_str').agg(
    distinct_books=('id_num', 'nunique'),
    avg_rating=('rating', 'mean')
).reset_index()

print("__RESULT__:")
print(stats.to_json(orient='records'))"""

env_args = {'var_function-call-7846935078876793979': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-4565000254805596521': [{'count': '200'}], 'var_function-call-6157774012479870483': [{'COUNT(*)': '1833'}], 'var_function-call-17584423273886338862': 'file_storage/function-call-17584423273886338862.json', 'var_function-call-9381740438124898103': 'file_storage/function-call-9381740438124898103.json', 'var_function-call-9833549063634245984': {'decade': '2020s', 'average_rating': 4.663636363636364, 'distinct_books': 21}, 'var_function-call-10930039483587244939': [{'decade_str': '1980s', 'avg_rating': 4.2083333333, 'distinct_books': 11, 'count_reviews': 72}, {'decade_str': '1990s', 'avg_rating': 3.8208955224, 'distinct_books': 16, 'count_reviews': 67}, {'decade_str': '2000s', 'avg_rating': 4.2762237762, 'distinct_books': 47, 'count_reviews': 286}, {'decade_str': '2010s', 'avg_rating': 4.6085918854, 'distinct_books': 88, 'count_reviews': 1257}, {'decade_str': '2020s', 'avg_rating': 4.6636363636, 'distinct_books': 21, 'count_reviews': 110}], 'var_function-call-4893490894625765291': ['This book is written in English and is available in a paperback format consisting of 8 pages. It has an ISBN 10 number of 0780274164 and an ISBN 13 number of 978-0780274167. The item weighs 1.01 pounds.', 'This book is written in English and has an ISBN-10 of 0553819399 and an ISBN-13 of 978-0553819397. It weighs 1.06 pounds and has dimensions of 5 inches in width, 1.65 inches in depth, and 7.8 inches in height.', '', 'This book is written in English and has an ISBN 10 of 1938923391 and an ISBN 13 of 978-1938923395. It weighs 14.4 ounces.', 'This book has an ISBN-10 number of 1925849058 and an ISBN-13 number of 978-1925849059. It weighs 1.06 pounds and has dimensions of 9.13 inches in width, 0.35 inches in depth, and 11.93 inches in height.', '', '', '', 'The book has a weight of 4 ounces.', 'The book has a weight of 9.6 ounces.']}

exec(code, env_args)
