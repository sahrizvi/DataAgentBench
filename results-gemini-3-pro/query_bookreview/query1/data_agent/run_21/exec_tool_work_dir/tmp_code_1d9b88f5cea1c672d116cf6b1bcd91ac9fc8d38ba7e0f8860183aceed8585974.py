code = """import json
import re
import pandas as pd

books_path = locals()['var_function-call-17597170398027844549']
with open(books_path, 'r') as f:
    books = json.load(f)

df_books = pd.DataFrame(books)

def extract_year(text):
    if not isinstance(text, str): return None
    matches = list(re.finditer(r'\b(19\d{2}|20[0-2]\d)\b', text))
    candidates = []
    for m in matches:
        year = int(m.group(1))
        end = m.end()
        # Look ahead a bit
        suffix = text[end:end+2].lower() if end + 2 <= len(text) else ""
        if suffix in ['st', 'nd', 'rd', 'th']:
            continue
        candidates.append(year)
    return candidates[0] if candidates else None

df_books['year'] = df_books['details'].apply(extract_year)
df_books['decade'] = (df_books['year'] // 10) * 10

# Count books per decade
decade_counts = df_books['decade'].value_counts()

print("__RESULT__:")
print(json.dumps({
    "decade_counts": decade_counts.to_dict(),
    "sample_years": df_books[['book_id', 'year']].head(20).to_dict(orient='records')
}))"""

env_args = {'var_function-call-6975577752223171344': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-11336959198502457448': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-15446129666109339953': [{'count': '200'}], 'var_function-call-2982058341310667547': [{'count(*)': '1833'}], 'var_function-call-17597170398027844549': 'file_storage/function-call-17597170398027844549.json', 'var_function-call-5746103583818394624': 'file_storage/function-call-5746103583818394624.json', 'var_function-call-7658024777571508570': [], 'var_function-call-7229365823781150716': {'books_count': 200, 'reviews_count': 1833, 'books_sample_ids': [1, 2, 3, 4, 5], 'reviews_sample_ids': [186, 191, 190, 8, 178], 'merged_count': 1833}}

exec(code, env_args)
