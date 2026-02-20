code = """import json
import pandas as pd
import re

# Load data
with open(locals()['var_function-call-11217342331341158317'], 'r') as f:
    books_data = json.load(f)

with open(locals()['var_function-call-18352100415714738754'], 'r') as f:
    reviews_data = json.load(f)

books_df = pd.DataFrame(books_data)
reviews_df = pd.DataFrame(reviews_data)

# Extract IDs
def extract_id(s):
    if not isinstance(s, str): return None
    m = re.search(r'(\d+)$', s)
    return int(m.group(1)) if m else None

books_df['book_num'] = books_df['book_id'].apply(extract_id)
reviews_df['purchase_num'] = reviews_df['purchase_id'].apply(extract_id)

# Extract Year
def extract_year(text):
    if not isinstance(text, str): return None
    matches = re.findall(r'(\d{4})', text)
    valid_years = []
    for m in matches:
        try:
            y = int(m)
            if 1900 <= y <= 2023:
                valid_years.append(y)
        except:
            pass
    if valid_years:
        return valid_years[0]
    return None

books_df['year'] = books_df['details'].apply(extract_year)
books_with_year = books_df.dropna(subset=['year']).copy()

# Calculate Decade
books_with_year['decade'] = (books_with_year['year'] // 10) * 10
books_with_year['decade_str'] = books_with_year['decade'].astype(int).astype(str) + "s"

# Merge
merged_df = pd.merge(reviews_df, books_with_year, left_on='purchase_num', right_on='book_num', how='inner')

# Convert rating
merged_df['rating'] = pd.to_numeric(merged_df['rating'], errors='coerce')
merged_df = merged_df.dropna(subset=['rating'])

# Method 2: Average of Book Averages
book_avgs = merged_df.groupby(['decade_str', 'book_num'])['rating'].mean().reset_index()
decade_avgs_method2 = book_avgs.groupby('decade_str')['rating'].mean().reset_index()

# Also count distinct books
decade_counts = merged_df.groupby('decade_str')['book_num'].nunique().reset_index(name='distinct_books')
decade_stats_method2 = pd.merge(decade_avgs_method2, decade_counts, on='decade_str')

qualified_method2 = decade_stats_method2[decade_stats_method2['distinct_books'] >= 10].copy()

print("__RESULT__:")
print(json.dumps(qualified_method2.to_dict(orient='records')))"""

env_args = {'var_function-call-1972179510569002468': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-4538444698924124667': [{'COUNT(*)': '1833'}], 'var_function-call-1245807085132264558': [{'count': '200'}], 'var_function-call-11217342331341158317': 'file_storage/function-call-11217342331341158317.json', 'var_function-call-18352100415714738754': 'file_storage/function-call-18352100415714738754.json', 'var_function-call-929890728202468694': {'error': 'No qualified decade found'}, 'var_function-call-4961246982507686762': {'error': 'No decade meets criteria', 'stats': []}, 'var_function-call-1585524080417120906': {'status': 'debug_printed'}, 'var_function-call-13012804703232327359': {'num_books': 200, 'num_reviews': 1833, 'num_common_ids': 200, 'num_books_with_year': 0, 'num_merged': 0, 'decade_stats': [], 'qualified': []}, 'var_function-call-6978184613435783773': {'samples': ['Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.', 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.', 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.', 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'], 'extracted': [['2004', '0701', '1698', '0701', '1698'], ['1996', '0435', '0886', '0435', '0886'], ['2012', '9780', '3161', '8536', '0316', '1853'], ['2013', '0545', '4255', '0545', '4255'], ['2014', '1542']]}, 'var_function-call-6647481913535504565': {'error': 'No qualified decade found', 'stats': [], 'num_merged': 0, 'num_books_with_year': 0}, 'var_function-call-3947115369630888563': {'best_decade': '2020s', 'avg_rating': 4.663636363636364, 'distinct_books': 21}, 'var_function-call-8097856520681872602': [{'decade_str': '1980s', 'distinct_books': 11, 'avg_rating': 4.208333333333333}, {'decade_str': '1990s', 'distinct_books': 16, 'avg_rating': 3.8208955223880596}, {'decade_str': '2000s', 'distinct_books': 47, 'avg_rating': 4.276223776223776}, {'decade_str': '2010s', 'distinct_books': 88, 'avg_rating': 4.608591885441528}, {'decade_str': '2020s', 'distinct_books': 21, 'avg_rating': 4.663636363636364}]}

exec(code, env_args)
