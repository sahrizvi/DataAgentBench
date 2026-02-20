code = """import json
import pandas as pd
import re

# Get the file paths from storage
books_file_path = locals()['var_functions.query_db:10']
reviews_file_path = locals()['var_functions.query_db:11']

# Load the data
with open(books_file_path, 'r') as f:
    books_data = json.load(f)

with open(reviews_file_path, 'r') as f:
    reviews_data = json.load(f)

# Convert to DataFrames
books_df = pd.DataFrame(books_data)
reviews_df = pd.DataFrame(reviews_data)

# Function to extract publication year from details text
def extract_year(details_text):
    if not details_text:
        return None
    
    # Look for patterns like "on January 1, 2004", "in 2004", "released on 2004", "published on 2004"
    # Year should be between 1900-2030 (reasonable publication years)
    patterns = [
        r'in\s+(\d{4})',
        r'on\s+[A-Za-z]*\s*\d*,\s+(\d{4})',
        r'released\s+(?:in\s+)?(\d{4})',
        r'published\s+(?:on\s+)?(\d{4})',
        r'edition\s+on\s+(\d{4})',
        r'\b(19\d{2}|20[0-2]\d)\b'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, details_text, re.IGNORECASE)
        if match:
            year = int(match.group(1))
            if 1900 <= year <= 2030:
                return year
    return None

# Extract year for each book
books_df['publication_year'] = books_df['details'].apply(extract_year)

# Calculate decade (e.g., 1996 -> 1990)
books_df['decade'] = (books_df['publication_year'] // 10) * 10

# Convert rating to numeric in reviews
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'])

# Add decade info to reviews by joining
# First, create mapping from purchase_id to book_id and decade
# Note: purchase_id format is like "purchaseid_186" and book_id is like "bookid_1"
# We need to extract the numeric part and match them

# Extract numeric parts
books_df['book_num'] = books_df['book_id'].str.extract('(\d+)').astype(int)
reviews_df['purchase_num'] = reviews_df['purchase_id'].str.extract('(\d+)').astype(int)

# Now join on these numeric IDs
joined_df = reviews_df.merge(
    books_df[['book_num', 'decade', 'publication_year']], 
    left_on='purchase_num', 
    right_on='book_num', 
    how='inner'
)

# Group by decade and calculate stats
decade_stats = joined_df.groupby('decade').agg({
    'rating': ['mean', 'count', 'std'],
    'purchase_num': 'nunique'  # number of distinct books
}).round(3)

# Flatten column names
decade_stats.columns = ['avg_rating', 'total_reviews', 'rating_std', 'distinct_books']
decade_stats = decade_stats.reset_index()

# Filter for decades with at least 10 distinct books
filtered_stats = decade_stats[decade_stats['distinct_books'] >= 10]

# Find decade with highest average rating
if not filtered_stats.empty:
    best_decade = filtered_stats.loc[filtered_stats['avg_rating'].idxmax()]
    result = {
        'best_decade': int(best_decade['decade']),
        'avg_rating': float(best_decade['avg_rating']),
        'distinct_books': int(best_decade['distinct_books']),
        'total_reviews': int(best_decade['total_reviews'])
    }
else:
    result = {'error': 'No decade found with at least 10 distinct books'}

# For debugging, also show all decades with their stats
all_decades = decade_stats.to_dict('records')

print('__RESULT__:')
print(json.dumps({
    'result': result,
    'all_decades_with_stats': all_decades,
    'total_books_with_year': int(books_df['publication_year'].notna().sum()),
    'total_reviews_joined': len(joined_df),
    'decades_with_10plus_books': len(filtered_stats)
}))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.query_db:6': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'rating_number': '29'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.', 'rating_number': '1'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.', 'rating_number': '3421'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.', 'rating_number': '40'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.', 'rating_number': '381'}, {'book_id': 'bookid_6', 'details': 'This book, published independently on December 30, 2021, is written in English and consists of 24 pages. It has an ISBN 13 of 979-8528537702 and weighs 3.2 ounces. The dimensions of the book are 7 x 0.06 x 9 inches.', 'rating_number': '5'}, {'book_id': 'bookid_7', 'details': 'The book, published by Guilford in its second edition in January 2004, is also noted as the 8082nd edition from January 1, 1994. It has a remarkably light item weight of just 0.01 ounces.', 'rating_number': '2'}, {'book_id': 'bookid_8', 'details': 'This book, published by Make Community, LLC, in its second edition on September 22, 2015, is available in English and spans 352 pages in paperback format. It has an ISBN of 9781680450262 for the 10-digit version and 978-1680450262 for the 13-digit version. The content is suitable for readers aged 11 to 17 years. The book weighs 2.91 pounds and its dimensions are 8 inches in width, 0.5 inches in thickness, and 10 inches in height.', 'rating_number': '1366'}, {'book_id': 'bookid_9', 'details': 'This book, published independently on September 25, 2019, is written in English and spans 367 pages. It is available in paperback format and has an ISBN-10 of 1694621731 and an ISBN-13 of 978-1694621733. The item weighs 1.38 pounds and measures 6 x 0.92 x 9 inches.', 'rating_number': '12'}, {'book_id': 'bookid_10', 'details': 'This book, published by WallBuilder Press in its first edition on November 8, 2004, is available in English and comprises 51 pages in paperback format. It has an ISBN-10 of 1932225323 and an ISBN-13 of 978-1932225327, with a total item weight of 3.52 ounces.', 'rating_number': '133'}], 'var_functions.query_db:7': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}, {'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_76', 'rating': '5'}, {'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_115', 'rating': '5'}, {'purchase_id': 'purchaseid_167', 'rating': '2'}], 'var_functions.query_db:10': 'file_storage/functions.query_db:10.json', 'var_functions.query_db:11': 'file_storage/functions.query_db:11.json', 'var_functions.execute_python:16': {'books_info': "Books data shape: (200, 3), Columns: ['book_id', 'details', 'rating_number']", 'reviews_info': "Reviews data shape: (1833, 2), Columns: ['purchase_id', 'rating']", 'books_preview': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'rating_number': '29'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.', 'rating_number': '1'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.', 'rating_number': '3421'}], 'reviews_preview': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}]}}

exec(code, env_args)
