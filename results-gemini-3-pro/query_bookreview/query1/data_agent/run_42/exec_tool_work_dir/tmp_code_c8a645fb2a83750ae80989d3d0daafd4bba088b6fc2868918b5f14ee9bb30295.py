code = """import json
import re
import pandas as pd

# Load data again (or reuse if persistent, but safe to reload)
with open(locals()['var_function-call-13546280856055606026'], 'r') as f:
    books = json.load(f)

with open(locals()['var_function-call-13546280856055603329'], 'r') as f:
    reviews = json.load(f)

def get_year(details):
    # Same logic as before to verify
    match = re.search(r'published.*?on\s+(?:[a-zA-Z]+\s+\d{1,2},?\s+)?(\d{4})', details, re.IGNORECASE)
    if match:
        return int(match.group(1))
    match = re.search(r'released.*?on\s+(?:[a-zA-Z]+\s+\d{1,2},?\s+)?(\d{4})', details, re.IGNORECASE)
    if match:
        return int(match.group(1))
    matches = re.findall(r'\b(19\d{2}|20\d{2})\b', details)
    if matches:
        return int(matches[0])
    return None

def get_id(s):
    match = re.search(r'(\d+)$', s)
    if match:
        return int(match.group(1))
    return None

book_data = []
for b in books:
    bid_str = b.get('book_id')
    bid = get_id(bid_str)
    year = get_year(b.get('details', ''))
    if bid is not None and year is not None:
        book_data.append({'id': bid, 'year': year, 'details': b.get('details', '')[:50]})

df_books = pd.DataFrame(book_data)

review_data = []
for r in reviews:
    pid_str = r.get('purchase_id')
    pid = get_id(pid_str)
    try:
        rating = float(r.get('rating'))
    except:
        continue
    if pid is not None:
        review_data.append({'id': pid, 'rating': rating})

df_reviews = pd.DataFrame(review_data)
book_stats = df_reviews.groupby('id')['rating'].agg(['mean', 'count']).reset_index()
book_stats.columns = ['id', 'avg_rating', 'review_count']

merged = pd.merge(df_books, book_stats, on='id', how='inner')
merged['decade'] = (merged['year'] // 10) * 10
merged['decade_str'] = merged['decade'].astype(str) + 's'

# Check 1980s
df_1980s = merged[merged['decade_str'] == '1980s']
print("__RESULT__:")
print(df_1980s[['id', 'year', 'avg_rating', 'review_count']].to_json(orient='records'))"""

env_args = {'var_function-call-14461102883439102455': ['books_info'], 'var_function-call-14461102883439100430': ['review'], 'var_function-call-5814846834777023767': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-5814846834777024656': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-4879635628562112594': [{'book_id': 'bookid_8'}, {'book_id': 'bookid_186'}], 'var_function-call-14240924787632698197': [{'count': '200'}], 'var_function-call-14240924787632698360': [{'COUNT(*)': '1833'}], 'var_function-call-13546280856055606026': 'file_storage/function-call-13546280856055606026.json', 'var_function-call-13546280856055603329': 'file_storage/function-call-13546280856055603329.json', 'var_function-call-10799161636207356': {'decade': '1980s', 'average_rating': 4.703019323671498, 'num_books': 10, 'all_stats': [{'decade_str': '1980s', 'num_distinct_books': 10, 'avg_rating_of_decade': 4.703019323671498}, {'decade_str': '1990s', 'num_distinct_books': 16, 'avg_rating_of_decade': 4.124937996031746}, {'decade_str': '2000s', 'num_distinct_books': 46, 'avg_rating_of_decade': 4.343550503205235}, {'decade_str': '2010s', 'num_distinct_books': 87, 'avg_rating_of_decade': 4.398301857678168}, {'decade_str': '2020s', 'num_distinct_books': 21, 'avg_rating_of_decade': 4.52530525030525}]}}

exec(code, env_args)
