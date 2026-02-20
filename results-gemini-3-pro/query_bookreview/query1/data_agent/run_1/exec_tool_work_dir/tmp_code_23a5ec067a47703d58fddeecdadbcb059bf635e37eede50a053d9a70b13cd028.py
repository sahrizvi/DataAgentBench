code = """import json
import re
import pandas as pd

# Load books data
with open(locals()['var_function-call-17578456053743105324'], 'r') as f:
    books_data = json.load(f)

# Load reviews data
with open(locals()['var_function-call-12400972779654688605'], 'r') as f:
    reviews_data = json.load(f)

# Helper to extract year
def extract_year(details):
    if not details:
        return None
    # Patterns to look for year associated with published/released
    # Try to find year (4 digits starting with 19 or 20)
    # The text usually says "published ... on ... YYYY" or "released on ... YYYY"
    matches = re.findall(r'(?:published|released).*?(\d{4})', details, re.IGNORECASE)
    if matches:
        # Take the first match as the publication year
        return int(matches[0])
    
    # Fallback: look for any valid year if explicit keyword not found close by?
    # But risky. Let's stick to strict context first.
    # Looking at data: "published ... in its second edition on September 22, 2015" -> 2015
    # "published ... in a September 1, 1987 edition" -> 1987
    # "published ... in January 2004" -> 2004
    
    # Sometimes just date at end: "released on January 1, 2004."
    
    return None

# Process books
book_years = {}
for book in books_data:
    bid = book['book_id']
    # Extract number from book_id "bookid_X"
    if '_' in bid:
        num_id = bid.split('_')[1]
    else:
        num_id = bid # fallback
        
    year = extract_year(book.get('details', ''))
    if year:
        book_years[num_id] = year

# Process reviews
# We need to map review -> book -> year -> decade
# And accumulate ratings

decade_stats = {} # decade -> {'ratings_sum': 0, 'ratings_count': 0, 'books': set()}

for review in reviews_data:
    pid = review['purchase_id']
    # Extract number from purchase_id "purchaseid_X"
    if '_' in pid:
        num_id = pid.split('_')[1]
    else:
        num_id = pid
    
    if num_id in book_years:
        year = book_years[num_id]
        decade_start = (year // 10) * 10
        decade_str = f"{decade_start}s"
        
        if decade_str not in decade_stats:
            decade_stats[decade_str] = {'ratings_sum': 0.0, 'ratings_count': 0, 'books': set()}
        
        try:
            r = float(review['rating'])
            decade_stats[decade_str]['ratings_sum'] += r
            decade_stats[decade_str]['ratings_count'] += 1
            decade_stats[decade_str]['books'].add(num_id)
        except:
            pass

# Filter and find max
valid_decades = []
for dec, stats in decade_stats.items():
    if len(stats['books']) >= 10:
        avg_rating = stats['ratings_sum'] / stats['ratings_count'] if stats['ratings_count'] > 0 else 0
        valid_decades.append({
            'decade': dec,
            'average_rating': avg_rating,
            'book_count': len(stats['books'])
        })

# Sort by average rating descending
valid_decades.sort(key=lambda x: x['average_rating'], reverse=True)

print("__RESULT__:")
print(json.dumps(valid_decades))"""

env_args = {'var_function-call-4960458581660214722': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-5604823520361681521': [{'count': '200'}], 'var_function-call-13013353557435363717': [{'COUNT(*)': '1833'}], 'var_function-call-17578456053743105324': 'file_storage/function-call-17578456053743105324.json', 'var_function-call-12400972779654688605': 'file_storage/function-call-12400972779654688605.json'}

exec(code, env_args)
