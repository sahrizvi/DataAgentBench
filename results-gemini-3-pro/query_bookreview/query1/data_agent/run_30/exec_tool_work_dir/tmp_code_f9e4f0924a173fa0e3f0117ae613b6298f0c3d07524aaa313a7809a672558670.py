code = """import json
import pandas as pd
import re

# Load data
with open(locals()['var_function-call-4837046250283943508'], 'r') as f:
    books_data = json.load(f)

with open(locals()['var_function-call-4837046250283945065'], 'r') as f:
    reviews_data = json.load(f)

# Process books
book_records = []
for b in books_data:
    bid_str = b['book_id']
    # Extract number from bookid_X
    m = re.search(r'bookid_(\d+)', bid_str)
    if not m:
        continue
    bid = int(m.group(1))
    
    details = b['details']
    # Extract year. Look for 4 digits 19xx or 20xx
    # Priority: "published ... 1999" or "released ... 2004"
    # Regex to capture year after published/released
    # Try to find date pattern first: Month Day, Year
    # Or just find the first valid year in the string
    
    # Simple robust finder: find all 19xx or 20xx
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', details)
    
    # Filter years to be <= 2023
    valid_years = [int(y) for y in years if int(y) <= 2023]
    
    # Heuristic: The publication year is likely the first one mentioned, or the one appearing in a date context.
    # Often details start with "Published by ... on [Date]"
    # Let's take the first valid year found.
    if valid_years:
        year = valid_years[0]
        book_records.append({'id': bid, 'year': year})

books_df = pd.DataFrame(book_records)

# Process reviews
review_records = []
for r in reviews_data:
    pid_str = r['purchase_id']
    m = re.search(r'purchaseid_(\d+)', pid_str)
    if not m:
        continue
    pid = int(m.group(1))
    rating = float(r['rating'])
    review_records.append({'id': pid, 'rating': rating})

reviews_df = pd.DataFrame(review_records)

# Calculate average rating per book
book_avg_ratings = reviews_df.groupby('id')['rating'].mean().reset_index()
book_avg_ratings.columns = ['id', 'avg_rating']

# Merge
merged = pd.merge(books_df, book_avg_ratings, on='id', how='inner')

# Assign decade
merged['decade'] = (merged['year'] // 10) * 10
merged['decade_str'] = merged['decade'].astype(str) + "s"

# Group by decade
decade_stats = merged.groupby('decade_str').agg(
    book_count=('id', 'count'), # This is distinct books because we aggregated by book first
    avg_rating=('avg_rating', 'mean')
).reset_index()

# Filter
filtered_decades = decade_stats[decade_stats['book_count'] >= 10].copy()

# Sort by avg_rating
result = filtered_decades.sort_values(by='avg_rating', ascending=False)

print("__RESULT__:")
print(json.dumps(result.to_dict(orient='records')))"""

env_args = {'var_function-call-7608015069099391471': ['books_info'], 'var_function-call-7608015069099390306': ['review'], 'var_function-call-9565206854667938728': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-9565206854667939563': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-6871574713258866780': [{'count': '200'}], 'var_function-call-6871574713258865367': [{'COUNT(*)': '1833'}], 'var_function-call-4837046250283943508': 'file_storage/function-call-4837046250283943508.json', 'var_function-call-4837046250283945065': 'file_storage/function-call-4837046250283945065.json'}

exec(code, env_args)
