code = """import json
import re
import pandas as pd

# Load data
with open(locals()['var_function-call-13546280856055606026'], 'r') as f:
    books = json.load(f)

with open(locals()['var_function-call-13546280856055603329'], 'r') as f:
    reviews = json.load(f)

# Helper to extract year
def get_year(details):
    # Pattern 1: Published ... on Month Day, Year
    # Pattern 2: released on ... Year
    # Pattern 3: Published ... in Year
    
    # Try looking for "published ... on ... year"
    # Matches: published ... on January 1, 2004
    match = re.search(r'published.*?on\s+(?:[a-zA-Z]+\s+\d{1,2},?\s+)?(\d{4})', details, re.IGNORECASE)
    if match:
        return int(match.group(1))
    
    # Try released on
    match = re.search(r'released.*?on\s+(?:[a-zA-Z]+\s+\d{1,2},?\s+)?(\d{4})', details, re.IGNORECASE)
    if match:
        return int(match.group(1))
        
    # Fallback: simple 4 digit year 19xx or 20xx
    # But be careful of ISBN.
    # details string usually starts with description.
    # Let's try to find 19xx or 20xx that is NOT part of ISBN?
    # Or just all 4 digit nums and pick one that looks like a year?
    # Given the previous patterns were good, let's see.
    # Let's try finding (19|20)\d{2}
    matches = re.findall(r'\b(19\d{2}|20\d{2})\b', details)
    # Filter out potential ISBN parts or numbers that are not years? 
    # Usually ISBNs are grouped.
    # If we have multiple, maybe the first one?
    if matches:
        return int(matches[0])
    return None

def get_id(s):
    # bookid_123 -> 123
    # purchaseid_123 -> 123
    match = re.search(r'(\d+)$', s)
    if match:
        return int(match.group(1))
    return None

# Process books
book_data = []
for b in books:
    bid_str = b.get('book_id')
    bid = get_id(bid_str)
    year = get_year(b.get('details', ''))
    if bid is not None and year is not None:
        book_data.append({'id': bid, 'year': year})

df_books = pd.DataFrame(book_data)

# Process reviews
review_data = []
for r in reviews:
    pid_str = r.get('purchase_id')
    pid = get_id(pid_str)
    rating = r.get('rating')
    try:
        rating = float(rating)
    except:
        continue
        
    if pid is not None:
        review_data.append({'id': pid, 'rating': rating})

df_reviews = pd.DataFrame(review_data)

# Join
# Filter books that have ratings
# Group reviews by book id to get avg rating per book
book_stats = df_reviews.groupby('id')['rating'].agg(['mean', 'count']).reset_index()
book_stats.columns = ['id', 'avg_rating', 'review_count']

# Merge with years
merged = pd.merge(df_books, book_stats, on='id', how='inner')

# Add decade
merged['decade'] = (merged['year'] // 10) * 10
merged['decade_str'] = merged['decade'].astype(str) + 's'

# Group by decade
decade_stats = merged.groupby('decade_str').agg(
    num_distinct_books=('id', 'count'), # since id is unique in df_books? No, check duplicates
    avg_rating_of_decade=('avg_rating', 'mean')
).reset_index()

# Check uniqueness of books in df_books
# df_books might have duplicates if book_id is not unique? 
# The SQL query returned unique rows? book_id is primary key usually.
# Let's assume book_id is unique.

# Filter decades with >= 10 distinct books
qualified_decades = decade_stats[decade_stats['num_distinct_books'] >= 10]

# Find highest avg rating
if not qualified_decades.empty:
    best_decade = qualified_decades.sort_values('avg_rating_of_decade', ascending=False).iloc[0]
    result = {
        "decade": best_decade['decade_str'],
        "average_rating": best_decade['avg_rating_of_decade'],
        "num_books": int(best_decade['num_distinct_books']),
        "all_stats": qualified_decades.to_dict(orient='records')
    }
else:
    result = "No decade met criteria"

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_function-call-14461102883439102455': ['books_info'], 'var_function-call-14461102883439100430': ['review'], 'var_function-call-5814846834777023767': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-5814846834777024656': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-4879635628562112594': [{'book_id': 'bookid_8'}, {'book_id': 'bookid_186'}], 'var_function-call-14240924787632698197': [{'count': '200'}], 'var_function-call-14240924787632698360': [{'COUNT(*)': '1833'}], 'var_function-call-13546280856055606026': 'file_storage/function-call-13546280856055606026.json', 'var_function-call-13546280856055603329': 'file_storage/function-call-13546280856055603329.json'}

exec(code, env_args)
