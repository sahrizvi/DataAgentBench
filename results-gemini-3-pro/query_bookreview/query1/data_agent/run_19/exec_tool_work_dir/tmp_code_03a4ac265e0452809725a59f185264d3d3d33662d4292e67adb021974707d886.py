code = """import json
import re
import pandas as pd

# Load file paths
file_path_books = locals()['var_function-call-3096561497567485986']
file_path_reviews = locals()['var_function-call-5332796046984058542']

# Load data
with open(file_path_books, 'r') as f:
    books_data = json.load(f)

with open(file_path_reviews, 'r') as f:
    reviews_data = json.load(f)

books_df = pd.DataFrame(books_data)
reviews_df = pd.DataFrame(reviews_data)
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')

# Debug details
details_sample = books_df['details'].iloc[0]
subtitle_sample = books_df['subtitle'].iloc[0]

# Extract ID
def extract_id_num(s):
    if pd.isna(s): return None
    match = re.search(r'(\d+)$', str(s))
    if match:
        return int(match.group(1))
    return None

books_df['id_num'] = books_df['book_id'].apply(extract_id_num)
reviews_df['id_num'] = reviews_df['purchase_id'].apply(extract_id_num)

# Extract year
def extract_year(row):
    text = str(row.get('details', ''))
    # Look for 4 digits (19xx or 20xx)
    years = re.findall(r'(19\d{2}|20\d{2})', text)
    if years:
        return int(years[-1])
    
    text_sub = str(row.get('subtitle', ''))
    years = re.findall(r'(19\d{2}|20\d{2})', text_sub)
    if years:
        return int(years[-1])
    return None

books_df['year'] = books_df.apply(extract_year, axis=1)

# Debug years
valid_years = books_df['year'].dropna().tolist()
valid_years_count = len(valid_years)

# Merge
merged_df = pd.merge(reviews_df, books_df, on='id_num', how='inner')

# Filter valid year
merged_df = merged_df.dropna(subset=['year', 'rating'])
merged_df['year'] = merged_df['year'].astype(int)

# Calculate decade
merged_df['decade'] = (merged_df['year'] // 10) * 10

# Count unique books per decade
decade_counts = merged_df.groupby('decade')['book_id'].nunique().reset_index(name='unique_books')

# Filter decades with >= 10 unique books
qualified_decades = decade_counts[decade_counts['unique_books'] >= 10]['decade'].tolist()

# Filter merged_df for qualified decades
qualified_df = merged_df[merged_df['decade'].isin(qualified_decades)]

result = {}
if not qualified_df.empty:
    # Calculate average rating per decade
    decade_avg = qualified_df.groupby('decade')['rating'].mean().reset_index(name='avg_rating')
    
    # Find max
    best_decade_row = decade_avg.loc[decade_avg['avg_rating'].idxmax()]
    result = {
        "decade": int(best_decade_row['decade']),
        "avg_rating": float(best_decade_row['avg_rating']),
        "unique_books": int(decade_counts[decade_counts['decade'] == best_decade_row['decade']]['unique_books'].iloc[0])
    }
else:
    result = {
        "error": "No decade met the criteria.",
        "debug_valid_years_count": valid_years_count,
        "debug_details_sample": str(details_sample),
        "debug_subtitle_sample": str(subtitle_sample),
        "debug_years_sample": valid_years[:5]
    }

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_function-call-10944610125865916082': ['books_info'], 'var_function-call-7623816645255018684': 'file_storage/function-call-7623816645255018684.json', 'var_function-call-4621741179361575125': [{'count': '200'}], 'var_function-call-14482848130311299562': [{'COUNT(*)': '1833'}], 'var_function-call-8131521746694899491': [{'purchase_id': 'purchaseid_186'}, {'purchase_id': 'purchaseid_191'}, {'purchase_id': 'purchaseid_190'}, {'purchase_id': 'purchaseid_8'}, {'purchase_id': 'purchaseid_178'}], 'var_function-call-3096561497567485986': 'file_storage/function-call-3096561497567485986.json', 'var_function-call-5332796046984058542': 'file_storage/function-call-5332796046984058542.json', 'var_function-call-12575391759179135184': {'error': 'No decade met the criteria.'}, 'var_function-call-15019832477204085469': {'book_ids_count': 200, 'review_ids_count': 200, 'overlap_count': 200, 'sample_overlap': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}, 'var_function-call-11203936561784481049': {'valid_years_count': 0, 'sample_years': [{'title': 'Chaucer', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'year': None}, {'title': 'Notes from a Kidwatcher', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.', 'year': None}, {'title': 'Service: A Navy SEAL at War', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.', 'year': None}, {'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.', 'year': None}, {'title': 'Parker & Knight', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.', 'year': None}, {'title': 'Writings from a Black Woman Living in the Land of the "Free": Strength, Power, Resilience', 'details': 'This book, published independently on December 30, 2021, is written in English and consists of 24 pages. It has an ISBN 13 of 979-8528537702 and weighs 3.2 ounces. The dimensions of the book are 7 x 0.06 x 9 inches.', 'year': None}, {'title': "Child Development: A Practitioner's Guide:2nd (Second) edition", 'details': 'The book, published by Guilford in its second edition in January 2004, is also noted as the 8082nd edition from January 1, 1994. It has a remarkably light item weight of just 0.01 ounces.', 'year': None}, {'title': 'Make: Electronics: Learning Through Discovery', 'details': 'This book, published by Make Community, LLC, in its second edition on September 22, 2015, is available in English and spans 352 pages in paperback format. It has an ISBN of 9781680450262 for the 10-digit version and 978-1680450262 for the 13-digit version. The content is suitable for readers aged 11 to 17 years. The book weighs 2.91 pounds and its dimensions are 8 inches in width, 0.5 inches in thickness, and 10 inches in height.', 'year': None}, {'title': 'Reunion: The Children of Lauderdale Park', 'details': 'This book, published independently on September 25, 2019, is written in English and spans 367 pages. It is available in paperback format and has an ISBN-10 of 1694621731 and an ISBN-13 of 978-1694621733. The item weighs 1.38 pounds and measures 6 x 0.92 x 9 inches.', 'year': None}, {'title': 'Four Centuries of American Education', 'details': 'This book, published by WallBuilder Press in its first edition on November 8, 2004, is available in English and comprises 51 pages in paperback format. It has an ISBN-10 of 1932225323 and an ISBN-13 of 978-1932225327, with a total item weight of 3.52 ounces.', 'year': None}, {'title': 'Mining Engineers and the American West: The Lace-Boot Brigarde, 1849-1933', 'details': 'Published by Caxton Press on January 1, 1993, this book is available in English and spans 407 pages. It has an ISBN-10 of 0893011673 and an ISBN-13 of 978-0893011673. Weighing 1.51 pounds, the book measures 6.05 inches in width, 1.14 inches in depth, and 9.03 inches in height.', 'year': None}, {'title': 'Heart of Silk and Shadows: A Fae Fantasy Romance (Fae Isles)', 'details': 'This book, published by Lisette Marshall on May 29, 2022, is written in English and is available in paperback, comprising 215 pages. It has an ISBN 10 number of 9083256898 and an ISBN 13 number of 978-9083256894. The item weighs 11.4 ounces and has dimensions of 6 x 0.54 x 9 inches.', 'year': None}, {'title': 'Girl Made of Glass', 'details': 'The book, published by Central Avenue Publishing on January 24, 2023, is available in English and comes in paperback format, consisting of 144 pages. It has an ISBN-10 number of 1771682760 and an ISBN-13 number of 978-1771682763. The item weighs 5.1 ounces and has dimensions of 5.25 x 0.4 x 8 inches.', 'year': None}, {'title': 'The Old Man and the Pirate Princess', 'details': 'The book, published by Jessica Mathews, LLC on November 13, 2019, is written in English and features a paperback format comprising 26 pages. It has an ISBN-10 of 1087848539 and an ISBN-13 of 978-1087848532. Suitable for readers aged 3 to 8 years, it is appropriate for students in Kindergarten through 3rd grade. The item weighs 3.03 ounces and has dimensions of 8.5 x 0.05 x 11 inches.', 'year': None}, {'title': 'Japanese Girls and Women', 'details': 'The book is published by Kegan Paul and is a first edition released on November 15, 2000. It is written in English and is available in hardcover, comprising 348 pages. The ISBN-10 for this edition is 0710306911, while the ISBN-13 is 978-0710306913. The item weighs 2.23 pounds and has dimensions of 5.5 x 1.25 x 8.5 inches.', 'year': None}, {'title': 'Behavior Principles in Everyday Life', 'details': 'This book is published by Prentice Hall College Division and is in its third edition, released on January 1, 1997. It is written in English and is available in paperback, consisting of 390 pages. The ISBN-10 for this book is 0130840963, while the ISBN-13 is 978-0130840967. The item weighs 1.3 pounds and has dimensions of 7.01 x 0.67 x 9.17 inches.', 'year': None}, {'title': 'PQL 3 - Lola (Spanish Edition)', 'details': 'This book, published by Edelsa Grupo Didascalia in a September 1, 1987 edition, is written in Spanish and consists of 44 pages. It has an ISBN-10 number of 8477110190 and an ISBN-13 number of 978-8477110194. The item weighs 2.05 ounces and has dimensions of 5.12 x 0.16 x 7.48 inches.', 'year': None}, {'title': 'A sermon, preached at the execution of Moses Paul, an Indian: who was executed at New-Haven, on the 2d of September, 1772, for the murder of Mr. Moses ... 1771 : preached at the desire of said Paul.', 'details': 'The book, published by Gale, Sabin Americana on February 21, 2012, is written in English and is available in paperback format, comprising 26 pages. It has an ISBN-10 of 1275627234 and an ISBN-13 of 978-1275627239. The item weighs 2.4 ounces and has dimensions of 7.44 x 0.05 x 9.69 inches.', 'year': None}, {'title': 'Business Associations: Agency, Partnerships, LLCs, and Corporations- 2013 Statutes and Rules', 'details': "The book, published by Foundation Press in its 2013th edition on March 22, 2013, is available in English and spans 355 pages. It has an ISBN-10 number of 1609303687 and an ISBN-13 number of 978-1609303686. Weighing 1.5 pounds, the book's dimensions are 7 inches in width, 0.5 inches in thickness, and 9.75 inches in height.", 'year': None}, {'title': 'Inspector Imanishi Investigates (Soho Crime)', 'details': 'The book, published by Soho Crime in a revised edition on July 1, 2003, is available in English and has a total print length of 372 pages. It has a file size of 2295 KB and supports various features such as Text to Speech, a screen reader, enhanced typesetting, X-Ray, Word Wise, and sticky notes on Kindle Scribe.', 'year': None}]}}

exec(code, env_args)
