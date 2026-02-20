code = """import json
import re
import pandas as pd
from datetime import datetime

books_path = locals()['var_function-call-13031625442222991424']
reviews_path = locals()['var_function-call-3241637180014007920']

with open(books_path, 'r') as f: books_data = json.load(f)
with open(reviews_path, 'r') as f: reviews_data = json.load(f)

books = pd.DataFrame(books_data)
reviews = pd.DataFrame(reviews_data)

def get_id_num(s):
    match = re.search(r'(\d+)', str(s))
    return int(match.group(1)) if match else None

books['id_num'] = books['book_id'].apply(get_id_num)
reviews['id_num'] = reviews['purchase_id'].apply(get_id_num)

def get_year(details):
    match = re.search(r'(?:on|released)\s+([A-Za-z]+)\s+(\d{1,2}),\s+(\d{4})', str(details))
    if match: return int(match.group(3))
    match2 = re.search(r'published.*?in\s+(\d{4})', str(details))
    if match2: return int(match2.group(1))
    return None

books['year'] = books['details'].apply(get_year)
books_valid = books.dropna(subset=['year']).copy()
books_valid['decade'] = (books_valid['year'].astype(int) // 10) * 10

merged = pd.merge(reviews, books_valid[['id_num', 'decade']], on='id_num', how='inner')
merged['rating'] = pd.to_numeric(merged['rating'], errors='coerce')
merged = merged.dropna(subset=['rating'])

# Metric 1: Global Average (already done)
# Metric 2: Average of Book Averages

# Group by book first
book_avgs = merged.groupby(['decade', 'id_num'])['rating'].mean().reset_index()

# Group by decade
decade_stats = book_avgs.groupby('decade').agg(
    avg_of_avgs=('rating', 'mean'),
    num_books=('id_num', 'count')
).reset_index()

result = decade_stats[decade_stats['num_books'] >= 10].sort_values(by='avg_of_avgs', ascending=False)

print("__RESULT__:")
print(result.to_json(orient='records'))"""

env_args = {'var_function-call-6240078878666439792': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-16420436372098634934': [{'count': '200'}], 'var_function-call-7158374868136901473': [{'COUNT(*)': '1833'}], 'var_function-call-13031625442222991424': 'file_storage/function-call-13031625442222991424.json', 'var_function-call-3241637180014007920': 'file_storage/function-call-3241637180014007920.json', 'var_function-call-4395434653014188405': [], 'var_function-call-10250256004433475987': [{'decade': 2020, 'avg_rating': 4.6636363636, 'num_books': 21}, {'decade': 2010, 'avg_rating': 4.6067146283, 'num_books': 87}, {'decade': 2000, 'avg_rating': 4.2736842105, 'num_books': 46}, {'decade': 1980, 'avg_rating': 4.2253521127, 'num_books': 10}, {'decade': 1990, 'avg_rating': 3.8208955224, 'num_books': 16}]}

exec(code, env_args)
