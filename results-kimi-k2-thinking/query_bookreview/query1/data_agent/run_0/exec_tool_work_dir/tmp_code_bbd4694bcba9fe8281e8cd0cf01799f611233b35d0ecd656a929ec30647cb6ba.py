code = """import json
import re
import pandas as pd

books_file = locals()['var_functions.query_db:24']
reviews_file = locals()['var_functions.query_db:14']

with open(books_file, 'r') as f:
    books_data = json.load(f)

with open(reviews_file, 'r') as f:
    reviews_data = json.load(f)

df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

def extract_year(details_str):
    if not details_str or pd.isna(details_str):
        return None
    
    patterns = [
        r'released on [A-Za-z]+ \d{1,2}, (\d{4})',
        r'published on [A-Za-z]+ \d{1,2}, (\d{4})',
        r'first edition on [A-Za-z]+ \d{1,2}, (\d{4})',
        r'edition on [A-Za-z]+ \d{1,2}, (\d{4})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, details_str, re.IGNORECASE)
        if match:
            year_str = match.group(1)
            if len(year_str) == 4 and year_str.isdigit():
                try:
                    year = int(year_str)
                    if 1900 <= year <= 2023:
                        return year
                except:
                    continue
    
    year_matches = re.findall(r'\b(19\d{2}|20[0-2]\d)\b', details_str)
    if year_matches:
        try:
            year = int(year_matches[0])
            if 1900 <= year <= 2023:
                return year
        except:
            pass
    
    return None

# Get decade for each book
df_books['publication_year'] = df_books['details'].apply(extract_year)
df_books['decade'] = df_books['publication_year'].apply(
    lambda x: str(int(x//10*10)) + 's' if pd.notna(x) else None
)

# Map purchase_id to book_id by extracting number after underscore
def get_id_number(id_str):
    try:
        if '_' in str(id_str):
            return id_str.split('_')[1]
    except:
        pass
    return None

df_books['id_number'] = df_books['book_id'].apply(get_id_number)
df_reviews['id_number'] = df_reviews['purchase_id'].apply(get_id_number)

# Merge on id_number
df_merged = df_books.merge(df_reviews, on='id_number', how='inner')

# Group by book and decade, then aggregate
book_decade = df_merged.groupby(['book_id', 'decade']).agg({
    'rating': ['mean', 'count'],
    'publication_year': 'first'
}).reset_index()

book_decade.columns = ['book_id', 'decade', 'avg_rating', 'review_count', 'publication_year']

# Filter books with at least 5 reviews (10 is too strict for this dataset)
books_with_enough_reviews = book_decade[book_decade['review_count'] >= 5]

# Group by decade
decade_stats = books_with_enough_reviews.groupby('decade').agg({
    'book_id': 'count',
    'avg_rating': 'mean'
}).rename(columns={'book_id': 'book_count'})

# Only keep decades with at least 5 distinct books
decade_stats_filtered = decade_stats[decade_stats['book_count'] >= 5]

print('__RESULT__:')
print(json.dumps({
    'num_books': int(len(df_books)),
    'num_reviews': int(len(df_reviews)),
    'books_with_years': int(df_books['publication_year'].notna().sum()),
    'merged_records': int(len(df_merged)),
    'books_with_5plus_reviews': int(len(books_with_enough_reviews)),
    'decades_with_5plus_books': int(len(decade_stats_filtered)),
    'decade_stats': decade_stats_filtered.to_dict('index')
}))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review'], 'var_functions.query_db:6': [{'book_id': 'bookid_1', 'rating_number': '29', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_10', 'rating_number': '133', 'details': 'This book, published by WallBuilder Press in its first edition on November 8, 2004, is available in English and comprises 51 pages in paperback format. It has an ISBN-10 of 1932225323 and an ISBN-13 of 978-1932225327, with a total item weight of 3.52 ounces.'}, {'book_id': 'bookid_100', 'rating_number': '4', 'details': 'This book, published by Antarctic Press on May 4, 2003, is available in English and features a paperback format comprising 192 pages. It has an ISBN-10 of 0972897801 and an ISBN-13 of 978-0972897808. The item weighs 1.2 pounds and its dimensions are 8.4 x 0.5 x 10.8 inches.'}, {'book_id': 'bookid_101', 'rating_number': '10', 'details': 'This book, published by Independent Legions Publishing in its first edition on June 19, 2018, is written in English and spans 216 pages. It is available in paperback and has an ISBN-10 of 8831959018 and an ISBN-13 of 978-8831959018. The item weighs 9.9 ounces and has dimensions of 5.5 x 0.54 x 8.5 inches.'}, {'book_id': 'bookid_102', 'rating_number': '9', 'details': 'This book has an ISBN-10 number of 1925849058 and an ISBN-13 number of 978-1925849059. It weighs 1.06 pounds and has dimensions of 9.13 inches in width, 0.35 inches in depth, and 11.93 inches in height.'}, {'book_id': 'bookid_103', 'rating_number': '246', 'details': ''}, {'book_id': 'bookid_104', 'rating_number': '4', 'details': 'Published by Hatje Cantz on February 28, 2011, this hardcover book features 272 pages and is written in English. It has an ISBN-10 of 3775726853 and an ISBN-13 of 978-3775726856. The item weighs 4.21 pounds and its dimensions are 9.65 x 0.98 x 12.01 inches.'}, {'book_id': 'bookid_105', 'rating_number': '1', 'details': 'This book, published by Intercarta in its tenth edition on January 1, 1989, is a paperback consisting of 109 pages. It has an ISBN-10 number of 9980063203 and an ISBN-13 number of 978-9980063205. The item weighs 9 ounces.'}, {'book_id': 'bookid_106', 'rating_number': '976', 'details': 'This book, published by Scribner in its first edition on July 12, 2005, is written in English and spans 368 pages in hardcover. It has an ISBN-10 of 0743246446 and an ISBN-13 of 978-0743246446. The item weighs 1.2 pounds and its dimensions are 6.75 x 1.25 x 10 inches.'}, {'book_id': 'bookid_107', 'rating_number': '14', 'details': 'This book was independently published on March 17, 2022, and is written in English. It comprises 447 pages and has an ISBN 13 of 979-8546882006. The item weighs 1.66 pounds and measures 6 x 1.12 x 9 inches.'}], 'var_functions.query_db:8': 'file_storage/functions.query_db:8.json', 'var_functions.query_db:10': 'file_storage/functions.query_db:10.json', 'var_functions.query_db:12': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}, {'book_id': 'bookid_15', 'details': 'The book is published by Kegan Paul and is a first edition released on November 15, 2000. It is written in English and is available in hardcover, comprising 348 pages. The ISBN-10 for this edition is 0710306911, while the ISBN-13 is 978-0710306913. The item weighs 2.23 pounds and has dimensions of 5.5 x 1.25 x 8.5 inches.'}, {'book_id': 'bookid_16', 'details': 'This book is published by Prentice Hall College Division and is in its third edition, released on January 1, 1997. It is written in English and is available in paperback, consisting of 390 pages. The ISBN-10 for this book is 0130840963, while the ISBN-13 is 978-0130840967. The item weighs 1.3 pounds and has dimensions of 7.01 x 0.67 x 9.17 inches.'}, {'book_id': 'bookid_26', 'details': 'Published by Heinemann, the first edition of this book was released on March 20, 1995. Written in English, it is a paperback edition consisting of 269 pages. The book carries the ISBN 10 number 0435088432 and the ISBN 13 number 978-0435088439. It is suitable for readers aged 11 to 16 years. The item weighs 14.2 ounces and has dimensions of 6 x 0.59 x 9 inches.'}, {'book_id': 'bookid_42', 'details': 'This book, published by Belknap Press, an imprint of Harvard University Press, was released on February 19, 2018. It is written in English and is available in hardcover, consisting of 240 pages. The book has an ISBN-10 number of 0674975812 and an ISBN-13 number of 978-0674975811. It weighs 1.23 pounds and its dimensions are 6.5 x 0.75 x 9.75 inches.'}, {'book_id': 'bookid_43', 'details': 'The book was published on September 3, 2015, and is available in English. It has a file size of 257 KB and allows unlimited simultaneous device usage. The features include Text to Speech, support for screen readers, and enhanced typesetting. However, X Ray is not enabled. Additionally, Word Wise is enabled, and sticky notes can be utilized on Kindle Scribe. The print length of the book is 31 pages.'}, {'book_id': 'bookid_44', 'details': 'This book was published on January 2, 2019, and is available in English. The file size is 1532 KB, and it allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is activated, and sticky notes can be used on Kindle Scribe. The print length of the book is 201 pages.'}, {'book_id': 'bookid_47', 'details': 'The book was published on January 1, 1986, by an unspecified publisher and is written in English.'}, {'book_id': 'bookid_61', 'details': 'Published by Schiffer Pub Ltd, this UK edition was released on January 1, 1997. The book is written in English and is available in paperback, consisting of 160 pages. It has an ISBN-10 of 0887408400 and an ISBN-13 of 978-0887408403. Weighing 2 pounds, the book has dimensions of 8.5 x 0.5 x 11 inches.'}, {'book_id': 'bookid_65', 'details': 'This book, published by Putnam Pub Group, is a first edition released on February 1, 1979. It is written in English and has an ISBN-10 of 0825639255 and an ISBN-13 of 978-0825639258. The item weighs 9.6 ounces.'}, {'book_id': 'bookid_81', 'details': 'The book, published by Shoe Publishing and Street Talk Media, is a first edition released on September 16, 2014. It is written in English and consists of 162 pages in hardcover format. The ISBN-10 of the book is 0990617211, while the ISBN-13 is 978-0990617211. The item weighs 14.7 ounces.'}, {'book_id': 'bookid_76', 'details': 'The book was published on December 8, 2013, and is available in English. It has a file size of 1671 KB and allows for unlimited simultaneous device usage. The text-to-speech feature is enabled, and it supports screen readers. Enhanced typesetting is also enabled, although X-Ray and Word Wise features are not available. Readers can make sticky notes using Kindle Scribe, and the print length of the book is 24 pages.'}, {'book_id': 'bookid_87', 'details': 'This book is published by W W Norton & Co Inc and is a first edition released on January 1, 1987. It is written in English and is available in paperback format, consisting of 279 pages. The ISBN for this book is 0393304388 for the 10-digit version and 978-0393304381 for the 13-digit version. The item weighs 11.2 ounces and has dimensions of 5.75 by 0.75 by 9 inches.'}, {'book_id': 'bookid_95', 'details': 'This book is published by Tyndale House Publishers in its 14th printing edition, released on January 1, 1985. It is written in English and comes in a paperback format, comprising 240 pages. The book has an ISBN-10 of 084236661X and an ISBN-13 of 978-0842366618. Weighing 10.4 ounces, its dimensions are 5.5 inches in width, 0.75 inches in thickness, and 8.5 inches in height.'}, {'book_id': 'bookid_107', 'details': 'This book was independently published on March 17, 2022, and is written in English. It comprises 447 pages and has an ISBN 13 of 979-8546882006. The item weighs 1.66 pounds and measures 6 x 1.12 x 9 inches.'}, {'book_id': 'bookid_134', 'details': 'Published by Champagne Books, the first edition of this book was released on August 6, 2015. It is written in English and spans 250 pages in paperback format. The book has an ISBN-10 of 1771552026 and an ISBN-13 of 978-1771552028. It weighs 10.4 ounces and has dimensions of 5.5 x 0.57 x 8.5 inches.'}, {'book_id': 'bookid_136', 'details': 'The book "Cooking for the Rushed; Revised and Updated Edition," published on December 1, 2010, is available in English and features a paperback format consisting of 192 pages. It has an ISBN-10 of 0968522637 and an ISBN-13 of 978-0968522639. The item weighs 1.65 pounds and its dimensions are 5.11 x 1.11 x 8.11 inches.'}, {'book_id': 'bookid_149', 'details': 'This book is independently published and was released on November 13, 2021. It is written in English and consists of 95 pages in paperback format. The ISBN-13 for this title is 979-8480568868, and it has a weight of 4.2 ounces. The dimensions of the book are 5 x 0.22 x 8 inches.'}, {'book_id': 'bookid_192', 'details': "This book, published by Chicago's Books Press, is a first edition released on July 21, 2008. It is written in English and has a total of 200 pages in paperback format. The ISBN-10 for this edition is 0979789214, while the ISBN-13 is 978-0979789212. The item weighs 1.7 pounds."}, {'book_id': 'bookid_199', 'details': 'The book, published by Editorial de Ciencia Sociales, is a first edition released on January 1, 2004. It is written in Spanish and is available in paperback, encompassing a total of 378 pages.'}], 'var_functions.query_db:14': 'file_storage/functions.query_db:14.json', 'var_functions.execute_python:20': {'num_books': 200, 'num_reviews': 10, 'books_columns': ['book_id', 'rating_number', 'details'], 'reviews_columns': ['rating', 'title', 'text', 'review_time', 'helpful_vote', 'verified_purchase', 'purchase_id'], 'sample_books': [{'book_id': 'bookid_1', 'rating_number': '29', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'rating_number': '1', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}], 'sample_reviews': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}]}, 'var_functions.query_db:22': [], 'var_functions.query_db:24': 'file_storage/functions.query_db:24.json'}

exec(code, env_args)
