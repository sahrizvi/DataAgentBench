code = """import json
import pandas as pd
import re

with open(locals()['var_function-call-17298644812689446293'], 'r') as f:
    books_data = json.load(f)

df_books = pd.DataFrame(books_data)

# Print first 5 details
print("Details Sample:")
for d in df_books['details'].head(5):
    print(d)

# Test regex manually
sample_text = "Published by Chatto & Windus, the first edition of this book was released on January 1, 2004."
regex_pattern = r'\b(19\d{2}|20[0-2]\d)\b'
matches = re.findall(regex_pattern, sample_text)
print("Regex Matches:", matches)

# Check extraction on dataframe
def get_year(details):
    if not isinstance(details, str):
        return None
    matches = re.findall(r'\b(19\d{2}|20[0-2]\d)\b', details)
    if matches:
        return int(matches[0])
    return None

df_books['extracted_year'] = df_books['details'].apply(get_year)
print("Extracted Years Sample:")
print(df_books['extracted_year'].head(5).tolist())

print('__RESULT__:')
print('"Debug complete"')"""

env_args = {'var_function-call-8065903626328758421': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-17298644812689446293': 'file_storage/function-call-17298644812689446293.json', 'var_function-call-9570983987664028606': 'file_storage/function-call-9570983987664028606.json', 'var_function-call-11296063608096238312': '2020s', 'var_function-call-5434364186148591045': [], 'var_function-call-12744497610901172679': 'End of debug', 'var_function-call-5212606854046506895': {'books_total': 200, 'books_with_year': 0, 'merged_rows': 0, 'stats': []}}

exec(code, env_args)
