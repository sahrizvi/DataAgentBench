code = """import json
import pandas as pd
import re

# Load data
with open(locals()['var_function-call-15001058247278832755'], 'r') as f:
    books_data = json.load(f)

with open(locals()['var_function-call-15001058247278830752'], 'r') as f:
    reviews_data = json.load(f)

# Process books
book_records = []
date_pattern = re.compile(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+(?:[0-9]{1,2},?\s+)?([12][0-9]{3})')

for b in books_data:
    b_id_str = b.get('book_id', '')
    details = b.get('details', '')
    
    # Extract ID number
    # Assumes format "bookid_123"
    m_id = re.search(r'(\d+)', b_id_str)
    if not m_id:
        continue
    b_id = int(m_id.group(1))
    
    # Extract Year
    # Find all matches, take the first one?
    # Or strict "published...on/in..."?
    # Let's try searching the whole string with the date pattern.
    # The samples show the publication date is usually the first date mentioned.
    m_date = date_pattern.search(details)
    if m_date:
        year = int(m_date.group(1))
        book_records.append({'id': b_id, 'year': year})

df_books = pd.DataFrame(book_records)

# Process reviews
review_records = []
for r in reviews_data:
    p_id_str = r.get('purchase_id', '')
    rating_str = r.get('rating', '0')
    
    # Extract ID number
    m_id = re.search(r'(\d+)', p_id_str)
    if not m_id:
        continue
    p_id = int(m_id.group(1))
    
    try:
        rating = float(rating_str)
    except:
        rating = 0.0
        
    review_records.append({'id': p_id, 'rating': rating})

df_reviews = pd.DataFrame(review_records)

# Merge
df_merged = pd.merge(df_books, df_reviews, on='id')

# Calculate Decade
df_merged['decade'] = (df_merged['year'] // 10) * 10

# Group by Decade
# We need:
# 1. Count distinct books
# 2. Average rating
decade_stats = df_merged.groupby('decade').agg(
    distinct_books=('id', 'nunique'),
    avg_rating=('rating', 'mean')
).reset_index()

# Filter
filtered_decades = decade_stats[decade_stats['distinct_books'] >= 10]

# Find max
if not filtered_decades.empty:
    best_decade_row = filtered_decades.loc[filtered_decades['avg_rating'].idxmax()]
    best_decade = int(best_decade_row['decade'])
    avg_rating = best_decade_row['avg_rating']
    result = f"{best_decade}s"
else:
    result = "No decade meets criteria"

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_function-call-4227400311736665891': ['books_info'], 'var_function-call-4227400311736666654': ['review'], 'var_function-call-2295154817108503268': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-5028099617338922932': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-12684071134095455968': [{'cnt': '200'}], 'var_function-call-12684071134095457069': [{'cnt': '1833'}], 'var_function-call-15001058247278832755': 'file_storage/function-call-15001058247278832755.json', 'var_function-call-15001058247278830752': 'file_storage/function-call-15001058247278830752.json'}

exec(code, env_args)
