code = """import json
import pandas as pd
import re

with open(locals()['var_function-call-4581168591792627923'], 'r') as f:
    books_data = json.load(f)

with open(locals()['var_function-call-18354388691561664074'], 'r') as f:
    reviews_data = json.load(f)

df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

def extract_id(s, prefix):
    if pd.isna(s): return -1
    m = re.search(r'\d+', s)
    return int(m.group(0)) if m else -1

df_books['id_num'] = df_books['book_id'].apply(lambda x: extract_id(x, 'bookid_'))
df_reviews['id_num'] = df_reviews['purchase_id'].apply(lambda x: extract_id(x, 'purchaseid_'))

def extract_year(details):
    if not isinstance(details, str): return None
    # Check for "on [Month] [Day], [Year]" first
    m = re.search(r'on\s+[A-Za-z]+\s+\d{1,2},?\s+(\d{4})', details)
    if m: return int(m.group(1))
    m = re.search(r'in\s+[A-Za-z]+\s+(\d{4})', details)
    if m: return int(m.group(1))
    m = re.search(r'\b(19\d{2}|20[0-2]\d)\b', details)
    if m: return int(m.group(1))
    return None

df_books['year'] = df_books['details'].apply(extract_year)
df_books = df_books.dropna(subset=['year'])

merged = pd.merge(df_reviews, df_books, on='id_num', how='inner')
merged['rating'] = pd.to_numeric(merged['rating'], errors='coerce')
merged = merged.dropna(subset=['rating'])
merged['decade'] = (merged['year'] // 10 * 10).astype(int).astype(str) + 's'

books_2020s = merged[merged['decade'] == '2020s']
stats_2020s = books_2020s.groupby('id_num').agg(
    details=('details', 'first'),
    count=('rating', 'count'),
    avg=('rating', 'mean')
).reset_index()

print("__RESULT__:")
print(json.dumps(stats_2020s.to_dict(orient='records')))"""

env_args = {'var_function-call-2276679140674115627': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-8286769825331596695': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-3347946993610182413': [{'count': '200'}], 'var_function-call-7069546728401593342': [{'COUNT(*)': '1833'}], 'var_function-call-4581168591792627923': 'file_storage/function-call-4581168591792627923.json', 'var_function-call-18354388691561664074': 'file_storage/function-call-18354388691561664074.json', 'var_function-call-11422821532862554489': [{'decade': '2020s', 'distinct_books': 21, 'avg_rating': 4.663636363636364}, {'decade': '2010s', 'distinct_books': 87, 'avg_rating': 4.606714628297362}, {'decade': '2000s', 'distinct_books': 47, 'avg_rating': 4.276223776223776}, {'decade': '1980s', 'distinct_books': 10, 'avg_rating': 4.225352112676056}, {'decade': '1990s', 'distinct_books': 16, 'avg_rating': 3.8208955223880596}], 'var_function-call-7319985649673822824': [{'decade': '1980s', 'distinct_books': 10, 'avg_rating_of_books': 4.703019323671498}, {'decade': '2020s', 'distinct_books': 21, 'avg_rating_of_books': 4.52530525030525}, {'decade': '2010s', 'distinct_books': 87, 'avg_rating_of_books': 4.398301857678168}, {'decade': '2000s', 'distinct_books': 47, 'avg_rating_of_books': 4.357517513775337}, {'decade': '1990s', 'distinct_books': 16, 'avg_rating_of_books': 4.124937996031746}], 'var_function-call-9073760332540805772': [{'id_num': 34, 'details': 'Published by Henry Holt & Co on January 1, 1983, this book is written in English and has an ISBN-10 of 0805005277 and an ISBN-13 of 978-0805005271. Weighing 15.2 ounces, it has dimensions of 5.75 inches in width, 0.75 inches in depth, and 8.75 inches in height.', 'count': 2, 'avg': 5.0}, {'id_num': 47, 'details': 'The book was published on January 1, 1986, by an unspecified publisher and is written in English.', 'count': 1, 'avg': 5.0}, {'id_num': 60, 'details': 'This book, published by Signet in its fourth printing edition on March 1, 1983, is available in English and consists of 184 pages. It has an ISBN 10 of 0451120639 and an ISBN 13 of 978-0451120632. The item weighs 4 ounces and its dimensions are 7 x 1 x 5 inches.', 'count': 1, 'avg': 5.0}, {'id_num': 75, 'details': 'The book was published by Gick Publishing on January 1, 1983.', 'count': 1, 'avg': 5.0}, {'id_num': 80, 'details': 'This book, published by Random House as a first edition on November 12, 1987, is written in English and features a hardcover format with a total of 322 pages. It has an ISBN-10 of 0394559312 and an ISBN-13 of 978-0394559315, and it weighs 1 pound.', 'count': 2, 'avg': 5.0}, {'id_num': 87, 'details': 'This book is published by W W Norton & Co Inc and is a first edition released on January 1, 1987. It is written in English and is available in paperback format, consisting of 279 pages. The ISBN for this book is 0393304388 for the 10-digit version and 978-0393304381 for the 13-digit version. The item weighs 11.2 ounces and has dimensions of 5.75 by 0.75 by 9 inches.', 'count': 3, 'avg': 3.6666666666666665}, {'id_num': 95, 'details': 'This book is published by Tyndale House Publishers in its 14th printing edition, released on January 1, 1985. It is written in English and comes in a paperback format, comprising 240 pages. The book has an ISBN-10 of 084236661X and an ISBN-13 of 978-0842366618. Weighing 10.4 ounces, its dimensions are 5.5 inches in width, 0.75 inches in thickness, and 8.5 inches in height.', 'count': 23, 'avg': 4.391304347826087}, {'id_num': 105, 'details': 'This book, published by Intercarta in its tenth edition on January 1, 1989, is a paperback consisting of 109 pages. It has an ISBN-10 number of 9980063203 and an ISBN-13 number of 978-9980063205. The item weighs 9 ounces.', 'count': 1, 'avg': 5.0}, {'id_num': 126, 'details': 'This book, published by Palgrave Macmillan in a revised edition on November 1, 1987, is available in English. It has an ISBN-10 of 0283995327 and an ISBN-13 of 978-0283995323. Weighing 1.76 pounds, the book measures 6.5 inches in width, 1 inch in thickness, and 9.75 inches in height.', 'count': 1, 'avg': 5.0}, {'id_num': 145, 'details': "This book, published by Amer Girl Pub in a box edition on January 1, 1982, is written in English and is suitable for readers aged 8 to 10 years old, specifically those in grades 3 to 4. It has a weight of 2.4 pounds and its dimensions measure 1.5 by 6.5 by 9 inches. The book's ISBN-10 is 0937295760, and the ISBN-13 is 978-0937295762.", 'count': 36, 'avg': 3.9722222222222223}]}

exec(code, env_args)
