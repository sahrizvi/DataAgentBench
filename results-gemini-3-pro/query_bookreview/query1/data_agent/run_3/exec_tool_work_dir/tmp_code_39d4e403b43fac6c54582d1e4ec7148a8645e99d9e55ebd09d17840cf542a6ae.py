code = """import json
import pandas as pd
import re

# Load data
with open(locals()['var_function-call-8482854063102919039'], 'r') as f:
    books_data = json.load(f)

with open(locals()['var_function-call-1179657304216333277'], 'r') as f:
    reviews_data = json.load(f)

# Process Books
book_rows = []
months = r"(?:January|February|March|April|May|June|July|August|September|October|November|December)"
date_regex = re.compile(rf"{months}\s+(?:\d{{1,2}},?\s+)?(\d{{4}})")

for b in books_data:
    b_id = b.get('book_id')
    details = b.get('details', '')
    
    # Extract ID number
    # Assuming bookid_X
    if 'bookid_' in b_id:
        id_num = b_id.replace('bookid_', '')
    else:
        id_num = b_id # Fallback
    
    # Extract Year
    match = date_regex.search(details)
    year = None
    if match:
        year = int(match.group(1))
    
    if year:
        decade_val = (year // 10) * 10
        decade = f"{decade_val}s"
        book_rows.append({'id_num': id_num, 'decade': decade, 'year': year})

books_df = pd.DataFrame(book_rows)

# Process Reviews
review_rows = []
for r in reviews_data:
    p_id = r.get('purchase_id')
    rating = r.get('rating')
    
    if p_id and rating:
        # Extract ID number
        if 'purchaseid_' in p_id:
            id_num = p_id.replace('purchaseid_', '')
        else:
            id_num = p_id
            
        try:
            rating = float(rating)
            review_rows.append({'id_num': id_num, 'rating': rating})
        except ValueError:
            pass

reviews_df = pd.DataFrame(review_rows)

# Merge
# Ensure id_num is string in both
books_df['id_num'] = books_df['id_num'].astype(str)
reviews_df['id_num'] = reviews_df['id_num'].astype(str)

merged = pd.merge(reviews_df, books_df, on='id_num', how='inner')

# Group by Decade
decade_stats = merged.groupby('decade').agg(
    distinct_books=('id_num', 'nunique'),
    avg_rating=('rating', 'mean'),
    count_ratings=('rating', 'count')
).reset_index()

# Filter
filtered_decades = decade_stats[decade_stats['distinct_books'] >= 10]

# Find max
best_decade = filtered_decades.sort_values(by='avg_rating', ascending=False).head(1)

print("__RESULT__:")
print(json.dumps(best_decade.to_dict(orient='records')))"""

env_args = {'var_function-call-266154951765162905': [{'book_id': 'bookid_1', 'title': 'Chaucer', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'title': 'Notes from a Kidwatcher', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'title': 'Service: A Navy SEAL at War', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'title': 'Parker & Knight', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-8914348186361102579': [{'count': '1833'}], 'var_function-call-7554791131260371443': [{'count': '200'}], 'var_function-call-8482854063102919039': 'file_storage/function-call-8482854063102919039.json', 'var_function-call-1179657304216333277': 'file_storage/function-call-1179657304216333277.json'}

exec(code, env_args)
