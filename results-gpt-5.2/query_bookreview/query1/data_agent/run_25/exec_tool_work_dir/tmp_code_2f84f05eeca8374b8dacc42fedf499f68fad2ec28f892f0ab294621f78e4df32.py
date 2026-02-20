code = """import json, re
import pandas as pd

def load_records(var):
    if isinstance(var, str):
        with open(var, 'r', encoding='utf-8') as f:
            return json.load(f)
    return var

books = load_records(var_call_36znDMBtOkeNr9riqxGiO73s)
bdf = pd.DataFrame(books)

year_pat = re.compile(r'\b(\d{4})\b')

def extract_year(text):
    if not isinstance(text, str):
        return None
    years = [int(y) for y in year_pat.findall(text)]
    years = [y for y in years if 1500 <= y <= 2026]
    return years[0] if years else None

# debug first row
first = bdf.loc[0,'details']
first_matches = year_pat.findall(first) if isinstance(first,str) else None
first_year = extract_year(first)

bdf['year'] = bdf['details'].apply(extract_year)

print('__RESULT__:')
print(json.dumps({
    'first_details': first,
    'first_matches': first_matches,
    'first_year': first_year,
    'non_null_count': int(bdf['year'].notna().sum())
}))"""

env_args = {'var_call_nuWYADeHCSdr0FMNeOqFkvJt': 'file_storage/call_nuWYADeHCSdr0FMNeOqFkvJt.json', 'var_call_5EZpQJjRpjY83aPPrihDAjyi': 'file_storage/call_5EZpQJjRpjY83aPPrihDAjyi.json', 'var_call_jWREfBZxjbuos3PeCJPKppLu': {'decade': None}, 'var_call_36znDMBtOkeNr9riqxGiO73s': 'file_storage/call_36znDMBtOkeNr9riqxGiO73s.json', 'var_call_MdIxdtORht2besMrBcKvlTvN': {'top': {'decade': None, 'note': 'No decade has >=10 distinct rated books after join.'}, 'eligible': [], 'all': []}, 'var_call_dWRS7wISMJWAQLGKvcYeJ24k': [{'purchase_id': 'purchaseid_196', 'n_reviews': '194'}, {'purchase_id': 'purchaseid_8', 'n_reviews': '190'}, {'purchase_id': 'purchaseid_3', 'n_reviews': '146'}, {'purchase_id': 'purchaseid_178', 'n_reviews': '118'}, {'purchase_id': 'purchaseid_186', 'n_reviews': '80'}, {'purchase_id': 'purchaseid_20', 'n_reviews': '42'}, {'purchase_id': 'purchaseid_10', 'n_reviews': '40'}, {'purchase_id': 'purchaseid_145', 'n_reviews': '36'}, {'purchase_id': 'purchaseid_190', 'n_reviews': '34'}, {'purchase_id': 'purchaseid_154', 'n_reviews': '29'}, {'purchase_id': 'purchaseid_148', 'n_reviews': '29'}, {'purchase_id': 'purchaseid_48', 'n_reviews': '27'}, {'purchase_id': 'purchaseid_5', 'n_reviews': '25'}, {'purchase_id': 'purchaseid_158', 'n_reviews': '24'}, {'purchase_id': 'purchaseid_95', 'n_reviews': '23'}, {'purchase_id': 'purchaseid_62', 'n_reviews': '22'}, {'purchase_id': 'purchaseid_165', 'n_reviews': '22'}, {'purchase_id': 'purchaseid_99', 'n_reviews': '20'}, {'purchase_id': 'purchaseid_72', 'n_reviews': '19'}, {'purchase_id': 'purchaseid_89', 'n_reviews': '18'}], 'var_call_RCgwe3hhFIJ5aFFmBaK6XQtj': [{'n_books': '200', 'max_suffix': '200'}], 'var_call_P1N1svu6qyTQb0d4advLfo9C': {'books_total': 200, 'books_with_year': 0, 'review_distinct_books': 200, 'joined_distinct_books': 0, 'joined_rows': 0}, 'var_call_vmFj8qvcZP5TPeEzhrPPj4vy': {'non_null_count': 0, 'sample_non_null': [], 'sample_details': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}]}, 'var_call_7nCdMJLuwyQmtgPXO9RFZ4c9': {'matches': ['2004']}}

exec(code, env_args)
