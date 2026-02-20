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

# Helper to extract year
def get_year(text):
    if not isinstance(text, str):
        return None
    candidates = re.findall(r'\d{4}', text)
    for c in candidates:
        y = int(c)
        if 1900 <= y <= 2023:
            return y
    return None

df_books['year'] = df_books['details'].apply(get_year)
df_books = df_books.dropna(subset=['year'])
df_books['decade'] = (df_books['year'] // 10) * 10
df_books['decade_str'] = df_books['decade'].astype(int).astype(str) + 's'

# Extract IDs
df_books['id_num'] = df_books['book_id'].str.extract(r'(\d+)').astype(int)
df_reviews['id_num'] = df_reviews['purchase_id'].str.extract(r'(\d+)').astype(int)
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

# Merge
merged = pd.merge(df_books, df_reviews, on='id_num', how='inner')

# Decade stats (All reviews)
decade_stats_reviews = merged.groupby('decade_str').agg(
    book_count=('id_num', 'nunique'),
    avg_rating_all=('rating', 'mean')
).reset_index()

filtered_reviews = decade_stats_reviews[decade_stats_reviews['book_count'] >= 10].sort_values(by='avg_rating_all', ascending=False)

print("__RESULT__:")
print(filtered_reviews.to_json(orient='records'))"""

env_args = {'var_function-call-6301180231551585539': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'rating_number': '29'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.', 'rating_number': '1'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.', 'rating_number': '3421'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.', 'rating_number': '40'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.', 'rating_number': '381'}], 'var_function-call-12516702256767511157': [{'count': '200'}], 'var_function-call-9335063315366319309': [{'count(*)': '1833'}], 'var_function-call-8084733100585816512': 'file_storage/function-call-8084733100585816512.json', 'var_function-call-14244121816731322471': 'file_storage/function-call-14244121816731322471.json', 'var_function-call-14551566676066817473': [], 'var_function-call-12612281021804131457': {'years_sample': [], 'book_ids_sample': [1, 2, 3, 4, 5], 'review_ids_sample': [186, 191, 190, 8, 178], 'merged_count': 1833, 'decade_stats': []}, 'var_function-call-15625594643125533329': 'Done', 'var_function-call-17778720171066895683': {'details_sample': ['Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.', 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.', 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.', 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'], 'years_found_sample': [None, None, None, None, None], 'valid_years_count': 0}, 'var_function-call-14007325087895377574': [['2004'], ['1996']], 'var_function-call-9905755838196075254': {'columns': ['book_id', 'details'], 'first_row_details_type': "<class 'str'>", 'first_row_details_val': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'years_found_sample': [['2004', '0701', '1698', '0701', '1698'], ['1996', '0435', '0886', '0435', '0886'], ['2012', '9780', '3161', '8536', '0316', '1853'], ['2013', '0545', '4255', '0545', '4255'], ['2014', '1542']]}, 'var_function-call-13182557863983094728': [{'decade_str': '1980s', 'book_count': 11, 'decade_avg_rating': 4.5481993852}, {'decade_str': '2020s', 'book_count': 21, 'decade_avg_rating': 4.5253052503}, {'decade_str': '2010s', 'book_count': 88, 'decade_avg_rating': 4.4051393366}, {'decade_str': '2000s', 'book_count': 47, 'decade_avg_rating': 4.3575175138}, {'decade_str': '1990s', 'book_count': 16, 'decade_avg_rating': 4.124937996}]}

exec(code, env_args)
