code = """import json
import pandas as pd
import re

# 1. Extract Book ID and Details from books_database
books_data_path = locals()['var_function-call-10435748601911513721']
with open(books_data_path, 'r') as f:
    books_data = json.load(f)

df_books = pd.DataFrame(books_data)

# 2. Extract Year from details
def extract_publication_year(details):
    if not isinstance(details, str): # Handle potential non-string details
        return None

    # Try to find dates with month and day first
    date_patterns = [
        r'(?:published on |on |in )?(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+(\d{4})',
        r'\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})'
    ]
    for pattern in date_patterns:
        match = re.search(pattern, details, re.IGNORECASE)
        if match:
            year = int(match.group(1))
            if 1900 <= year <= 2023:
                return year

    # Try to find year associated with keywords like 'published', 'edition', 'release'
    keyword_patterns = [
        r'published(?: by)?.*?(\d{4})',
        r'edition.*?(\d{4})',
        r'release(?:d)?.*?(\d{4})'
    ]
    for pattern in keyword_patterns:
        match = re.search(pattern, details, re.IGNORECASE)
        if match:
            year = int(match.group(1))
            if 1900 <= year <= 2023:
                return year

    # Fallback: find any 4-digit number that looks like a year within the range
    four_digit_numbers = [int(y) for y in re.findall(r'\b(\d{4})\b', details) if 1900 <= int(y) <= 2023]
    if four_digit_numbers:
        # Return the earliest valid year, as it's most likely the publication year
        return min(four_digit_numbers)

    return None

df_books['publication_year'] = df_books['details'].apply(extract_publication_year)
df_books_filtered = df_books.dropna(subset=['publication_year'])
df_books_filtered['publication_decade'] = (df_books_filtered['publication_year'] // 10 * 10).astype(int)

# 3. Process Review Data
df_reviews_path = locals()['var_function-call-17165447958828876928']
with open(df_reviews_path, 'r') as f:
    df_reviews = pd.DataFrame(json.load(f))

# 4. Standardize IDs for Joining (removing prefixes to allow fuzzy matching on the numeric part)
df_books_filtered['numeric_book_id'] = df_books_filtered['book_id'].str.replace('bookid_', '', regex=False).astype(int, errors='ignore')
df_reviews['numeric_book_id'] = df_reviews['purchase_id'].str.replace('purchaseid_', '', regex=False).astype(int, errors='ignore')
df_reviews['rating'] = df_reviews['rating'].astype(float)

# Filter out rows where numeric_book_id could not be converted to int
df_books_filtered = df_books_filtered[pd.to_numeric(df_books_filtered['numeric_book_id'], errors='coerce').notna()]
df_reviews = df_reviews[pd.to_numeric(df_reviews['numeric_book_id'], errors='coerce').notna()]

df_books_filtered['numeric_book_id'] = df_books_filtered['numeric_book_id'].astype(int)
df_reviews['numeric_book_id'] = df_reviews['numeric_book_id'].astype(int)

# 5. Merge DataFrames
merged_df = pd.merge(df_books_filtered, df_reviews, on='numeric_book_id', how='inner')

# 6. Calculate Decade Statistics
decade_stats = merged_df.groupby('publication_decade').agg(
    distinct_books=('book_id', 'nunique'), # Count distinct original book_ids
    average_rating=('rating', 'mean')
).reset_index()

# 7. Filter and Find Max
filtered_decades = decade_stats[decade_stats['distinct_books'] >= 10]

if not filtered_decades.empty:
    highest_avg_rating_decade = filtered_decades.loc[filtered_decades['average_rating'].idxmax()]
    result = int(highest_avg_rating_decade['publication_decade'])
else:
    result = "No decade found with at least 10 distinct books that have been rated."

print('__RESULT__:')
print(json.dumps(result))"""

env_args = {'var_function-call-11446481285406606755': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-8136443882673903768': 'file_storage/function-call-8136443882673903768.json', 'var_function-call-3760083664171841404': [], 'var_function-call-5826590712248697770': [{'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}, {'details': 'This book, published independently on December 30, 2021, is written in English and consists of 24 pages. It has an ISBN 13 of 979-8528537702 and weighs 3.2 ounces. The dimensions of the book are 7 x 0.06 x 9 inches.'}, {'details': 'The book, published by Guilford in its second edition in January 2004, is also noted as the 8082nd edition from January 1, 1994. It has a remarkably light item weight of just 0.01 ounces.'}, {'details': 'This book, published by Make Community, LLC, in its second edition on September 22, 2015, is available in English and spans 352 pages in paperback format. It has an ISBN of 9781680450262 for the 10-digit version and 978-1680450262 for the 13-digit version. The content is suitable for readers aged 11 to 17 years. The book weighs 2.91 pounds and its dimensions are 8 inches in width, 0.5 inches in thickness, and 10 inches in height.'}, {'details': 'This book, published independently on September 25, 2019, is written in English and spans 367 pages. It is available in paperback format and has an ISBN-10 of 1694621731 and an ISBN-13 of 978-1694621733. The item weighs 1.38 pounds and measures 6 x 0.92 x 9 inches.'}, {'details': 'This book, published by WallBuilder Press in its first edition on November 8, 2004, is available in English and comprises 51 pages in paperback format. It has an ISBN-10 of 1932225323 and an ISBN-13 of 978-1932225327, with a total item weight of 3.52 ounces.'}, {'details': 'Published by Caxton Press on January 1, 1993, this book is available in English and spans 407 pages. It has an ISBN-10 of 0893011673 and an ISBN-13 of 978-0893011673. Weighing 1.51 pounds, the book measures 6.05 inches in width, 1.14 inches in depth, and 9.03 inches in height.'}, {'details': 'This book, published by Lisette Marshall on May 29, 2022, is written in English and is available in paperback, comprising 215 pages. It has an ISBN 10 number of 9083256898 and an ISBN 13 number of 978-9083256894. The item weighs 11.4 ounces and has dimensions of 6 x 0.54 x 9 inches.'}, {'details': 'The book, published by Central Avenue Publishing on January 24, 2023, is available in English and comes in paperback format, consisting of 144 pages. It has an ISBN-10 number of 1771682760 and an ISBN-13 number of 978-1771682763. The item weighs 5.1 ounces and has dimensions of 5.25 x 0.4 x 8 inches.'}, {'details': 'The book, published by Jessica Mathews, LLC on November 13, 2019, is written in English and features a paperback format comprising 26 pages. It has an ISBN-10 of 1087848539 and an ISBN-13 of 978-1087848532. Suitable for readers aged 3 to 8 years, it is appropriate for students in Kindergarten through 3rd grade. The item weighs 3.03 ounces and has dimensions of 8.5 x 0.05 x 11 inches.'}, {'details': 'The book is published by Kegan Paul and is a first edition released on November 15, 2000. It is written in English and is available in hardcover, comprising 348 pages. The ISBN-10 for this edition is 0710306911, while the ISBN-13 is 978-0710306913. The item weighs 2.23 pounds and has dimensions of 5.5 x 1.25 x 8.5 inches.'}, {'details': 'This book is published by Prentice Hall College Division and is in its third edition, released on January 1, 1997. It is written in English and is available in paperback, consisting of 390 pages. The ISBN-10 for this book is 0130840963, while the ISBN-13 is 978-0130840967. The item weighs 1.3 pounds and has dimensions of 7.01 x 0.67 x 9.17 inches.'}, {'details': 'This book, published by Edelsa Grupo Didascalia in a September 1, 1987 edition, is written in Spanish and consists of 44 pages. It has an ISBN-10 number of 8477110190 and an ISBN-13 number of 978-8477110194. The item weighs 2.05 ounces and has dimensions of 5.12 x 0.16 x 7.48 inches.'}, {'details': 'The book, published by Gale, Sabin Americana on February 21, 2012, is written in English and is available in paperback format, comprising 26 pages. It has an ISBN-10 of 1275627234 and an ISBN-13 of 978-1275627239. The item weighs 2.4 ounces and has dimensions of 7.44 x 0.05 x 9.69 inches.'}, {'details': "The book, published by Foundation Press in its 2013th edition on March 22, 2013, is available in English and spans 355 pages. It has an ISBN-10 number of 1609303687 and an ISBN-13 number of 978-1609303686. Weighing 1.5 pounds, the book's dimensions are 7 inches in width, 0.5 inches in thickness, and 9.75 inches in height."}, {'details': 'The book, published by Soho Crime in a revised edition on July 1, 2003, is available in English and has a total print length of 372 pages. It has a file size of 2295 KB and supports various features such as Text to Speech, a screen reader, enhanced typesetting, X-Ray, Word Wise, and sticky notes on Kindle Scribe.'}], 'var_function-call-559093424399049919': 'file_storage/function-call-559093424399049919.json', 'var_function-call-17165447958828876928': 'file_storage/function-call-17165447958828876928.json', 'var_function-call-4613237622315317940': 'file_storage/function-call-4613237622315317940.json', 'var_function-call-14034248153056592047': [], 'var_function-call-17315950758566490134': 'file_storage/function-call-17315950758566490134.json', 'var_function-call-16508958372109162646': 'No decade found with at least 10 distinct books that have been rated.', 'var_function-call-10435748601911513721': 'file_storage/function-call-10435748601911513721.json', 'var_function-call-6336090291617165853': 'No decade found with at least 10 distinct books that have been rated.', 'var_function-call-17542477029274551302': 'file_storage/function-call-17542477029274551302.json', 'var_function-call-5304526122785629036': 'No decade found with at least 10 distinct books that have been rated.', 'var_function-call-4741443844843567138': 'No decade found with at least 10 distinct books that have been rated.'}

exec(code, env_args)
