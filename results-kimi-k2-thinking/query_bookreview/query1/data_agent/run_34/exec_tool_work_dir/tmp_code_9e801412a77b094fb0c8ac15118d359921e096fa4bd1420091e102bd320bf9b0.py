code = """import pandas as pd
import json
import re

# Get the book data
file_path = locals()['var_functions.query_db:8']
with open(file_path, 'r') as f:
    books_data = json.load(f)

# Create a more robust year extraction function
def extract_year_robust(details_text):
    if not details_text or pd.isna(details_text):
        return None
    
    # Try multiple patterns in order of likelihood
    patterns = [
        # Pattern for dates like "May 20, 1996" or "January 1, 2004"
        r'(?:January|February|March|April|May|June|July|August|September|October|November|December)[^\d]*(\d{1,2})[^\d]*(\d{4})',
        # Pattern for "published on 2012"
        r'published[^\d]*(\d{4})',
        # Pattern for "released on 2012"
        r'released[^\d]*(\d{4})',
        # Pattern for "edition on 2012"
        r'edition[^\d]*(\d{4})',
        # Any 4-digit year from 1900-2023
        r'\b(19\d{2}|20[0-2]\d)\b'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, details_text, re.IGNORECASE)
        if matches:
            # For the first pattern, we get month and year, so take the year (second group)
            if 'month' in pattern:
                for match in matches:
                    if isinstance(match, tuple) and len(match) == 2:
                        year = int(match[1])
                        if 1900 <= year <= 2023:
                            return year
            else:
                # For other patterns, we get just the year
                for match in matches:
                    if isinstance(match, str):
                        year = int(match)
                        if 1900 <= year <= 2023:
                            return year
                    elif isinstance(match, tuple):
                        year_str = match[0] if match[0] else match[1] if len(match) > 1 else match[0]
                        year = int(year_str)
                        if 1900 <= year <= 2023:
                            return year
    
    return None

# Apply extraction
df_books = pd.DataFrame(books_data)
df_books['publication_year'] = df_books['details'].apply(extract_year_robust)

# Look at some examples that failed before
failed_before = df_books[df_books['publication_year'].isna()].head(10)
print("Examples of books without extracted year:")
for idx, row in failed_before.head(5).iterrows():
    print(f"\nBook ID: {row['book_id']}")
    print(f"Details: {row['details'][:200]}...")

# Also check successful ones
successful = df_books[df_books['publication_year'].notna()]
print(f"\n\nSuccessfully extracted years for {len(successful)} books:")
for idx, row in successful.head(10).iterrows():
    print(f"Book ID: {row['book_id']}, Year: {row['publication_year']}")"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review'], 'var_functions.query_db:6': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}, {'book_id': 'bookid_6', 'details': 'This book, published independently on December 30, 2021, is written in English and consists of 24 pages. It has an ISBN 13 of 979-8528537702 and weighs 3.2 ounces. The dimensions of the book are 7 x 0.06 x 9 inches.'}, {'book_id': 'bookid_7', 'details': 'The book, published by Guilford in its second edition in January 2004, is also noted as the 8082nd edition from January 1, 1994. It has a remarkably light item weight of just 0.01 ounces.'}, {'book_id': 'bookid_8', 'details': 'This book, published by Make Community, LLC, in its second edition on September 22, 2015, is available in English and spans 352 pages in paperback format. It has an ISBN of 9781680450262 for the 10-digit version and 978-1680450262 for the 13-digit version. The content is suitable for readers aged 11 to 17 years. The book weighs 2.91 pounds and its dimensions are 8 inches in width, 0.5 inches in thickness, and 10 inches in height.'}, {'book_id': 'bookid_9', 'details': 'This book, published independently on September 25, 2019, is written in English and spans 367 pages. It is available in paperback format and has an ISBN-10 of 1694621731 and an ISBN-13 of 978-1694621733. The item weighs 1.38 pounds and measures 6 x 0.92 x 9 inches.'}, {'book_id': 'bookid_10', 'details': 'This book, published by WallBuilder Press in its first edition on November 8, 2004, is available in English and comprises 51 pages in paperback format. It has an ISBN-10 of 1932225323 and an ISBN-13 of 978-1932225327, with a total item weight of 3.52 ounces.'}], 'var_functions.query_db:8': 'file_storage/functions.query_db:8.json', 'var_functions.execute_python:16': {'total_books': 200, 'books_with_year': 3, 'sample_books': [{'book_id': 'bookid_1', 'publication_year': nan, 'decade': None}, {'book_id': 'bookid_2', 'publication_year': nan, 'decade': None}, {'book_id': 'bookid_3', 'publication_year': nan, 'decade': None}, {'book_id': 'bookid_4', 'publication_year': nan, 'decade': None}, {'book_id': 'bookid_5', 'publication_year': nan, 'decade': None}, {'book_id': 'bookid_6', 'publication_year': nan, 'decade': None}, {'book_id': 'bookid_7', 'publication_year': 2004.0, 'decade': '2000s'}, {'book_id': 'bookid_8', 'publication_year': nan, 'decade': None}, {'book_id': 'bookid_9', 'publication_year': nan, 'decade': None}, {'book_id': 'bookid_10', 'publication_year': nan, 'decade': None}]}}

exec(code, env_args)
