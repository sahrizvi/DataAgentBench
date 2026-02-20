code = """# Investigate year extraction issues
import json, re, pandas as pd

books_path = locals()['var_functions.query_db:2']
with open(books_path, 'r') as f:
    books = json.load(f)
books_df = pd.DataFrame(books)

# Check first few details values
top10 = books_df.head(10)['details'].tolist()

# Test the extraction function on actual data
def extract_year(text):
    try:
        if pd.isna(text):
            return None
        matches = re.findall(r'\b(19\d{2}|20[0-2]\d)\b', text)
        if matches:
            years = [int(y) for y in matches]
            return min(years)
    except Exception as e:
        return None

test_years = [extract_year(d) for d in top10]

# Get distribution of results for all books
books_df['year_test'] = books_df['details'].apply(extract_year)
year_counts = books_df['year_test'].value_counts().head(10)

result = {
    'first_10_details': top10,
    'first_10_years': test_years,
    'distinct_years_count': books_df['year_test'].nunique(),
    'sample_year_dist': year_counts.reset_index().head(10).to_dict('records')
}

print('__RESULT__:')
print(json.dumps(result, ensure_ascii=False, default=str))"""

env_args = {'var_functions.query_db:0': [{'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}, {'details': 'This book, published independently on December 30, 2021, is written in English and consists of 24 pages. It has an ISBN 13 of 979-8528537702 and weighs 3.2 ounces. The dimensions of the book are 7 x 0.06 x 9 inches.'}, {'details': 'The book, published by Guilford in its second edition in January 2004, is also noted as the 8082nd edition from January 1, 1994. It has a remarkably light item weight of just 0.01 ounces.'}, {'details': 'This book, published by Make Community, LLC, in its second edition on September 22, 2015, is available in English and spans 352 pages in paperback format. It has an ISBN of 9781680450262 for the 10-digit version and 978-1680450262 for the 13-digit version. The content is suitable for readers aged 11 to 17 years. The book weighs 2.91 pounds and its dimensions are 8 inches in width, 0.5 inches in thickness, and 10 inches in height.'}, {'details': 'This book, published independently on September 25, 2019, is written in English and spans 367 pages. It is available in paperback format and has an ISBN-10 of 1694621731 and an ISBN-13 of 978-1694621733. The item weighs 1.38 pounds and measures 6 x 0.92 x 9 inches.'}, {'details': 'This book, published by WallBuilder Press in its first edition on November 8, 2004, is available in English and comprises 51 pages in paperback format. It has an ISBN-10 of 1932225323 and an ISBN-13 of 978-1932225327, with a total item weight of 3.52 ounces.'}], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review'], 'var_functions.query_db:6': 'file_storage/functions.query_db:6.json', 'var_functions.execute_python:10': {'decade': None, 'avg_rating': None, 'distinct_books': 0}, 'var_functions.execute_python:12': {'books_top20_ids': ['bookid_1', 'bookid_2', 'bookid_3', 'bookid_4', 'bookid_5', 'bookid_6', 'bookid_7', 'bookid_8', 'bookid_9', 'bookid_10', 'bookid_11', 'bookid_12', 'bookid_13', 'bookid_14', 'bookid_15', 'bookid_16', 'bookid_17', 'bookid_18', 'bookid_19', 'bookid_20']}, 'var_functions.query_db:14': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_186', 'details': 'Published by Spiegel & Grau on September 4, 2012, this book is written in English and features a hardcover format with 256 pages. It has an ISBN-10 of 0385529813 and an ISBN-13 of 978-0385529815. The item weighs 1.15 pounds and has dimensions of 6.5 x 0.75 x 9.5 inches.'}, {'book_id': 'bookid_191', 'details': "This special edition of the book, published by St. Martin's Paperbacks on June 2, 2015, is available in English and comes in a mass market paperback format with a total of 352 pages. It has an ISBN-10 of 1250074274 and an ISBN-13 of 978-1250074270. The item weighs 6.4 ounces and measures 4.2 inches in width, 0.93 inches in depth, and 6.83 inches in height."}], 'var_functions.execute_python:16': {'total_books': 200, 'books_with_year': 0, 'total_reviews': 1833, 'matched_reviews': 1833, 'sample_matches': [{'book_id': 'bookid_1', 'year': None, 'book_num': 1, 'purchase_id': 'purchaseid_1', 'review_num': 1}, {'book_id': 'bookid_2', 'year': None, 'book_num': 2, 'purchase_id': 'purchaseid_2', 'review_num': 2}, {'book_id': 'bookid_3', 'year': None, 'book_num': 3, 'purchase_id': 'purchaseid_3', 'review_num': 3}, {'book_id': 'bookid_3', 'year': None, 'book_num': 3, 'purchase_id': 'purchaseid_3', 'review_num': 3}, {'book_id': 'bookid_3', 'year': None, 'book_num': 3, 'purchase_id': 'purchaseid_3', 'review_num': 3}, {'book_id': 'bookid_3', 'year': None, 'book_num': 3, 'purchase_id': 'purchaseid_3', 'review_num': 3}, {'book_id': 'bookid_3', 'year': None, 'book_num': 3, 'purchase_id': 'purchaseid_3', 'review_num': 3}, {'book_id': 'bookid_3', 'year': None, 'book_num': 3, 'purchase_id': 'purchaseid_3', 'review_num': 3}, {'book_id': 'bookid_3', 'year': None, 'book_num': 3, 'purchase_id': 'purchaseid_3', 'review_num': 3}, {'book_id': 'bookid_3', 'year': None, 'book_num': 3, 'purchase_id': 'purchaseid_3', 'review_num': 3}], 'decade_distribution': []}}

exec(code, env_args)
