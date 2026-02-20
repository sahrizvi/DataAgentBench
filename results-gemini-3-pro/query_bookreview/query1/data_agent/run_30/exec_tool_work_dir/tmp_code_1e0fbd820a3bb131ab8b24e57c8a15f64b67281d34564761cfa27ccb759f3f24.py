code = """import json
import pandas as pd
import re
import numpy as np
import sys

# Load data
try:
    with open(locals()['var_function-call-4837046250283943508'], 'r') as f:
        books_data = json.load(f)
    print(f"Books loaded: {len(books_data)}")
except Exception as e:
    print(f"Error loading books: {e}")
    books_data = []

try:
    with open(locals()['var_function-call-4837046250283945065'], 'r') as f:
        reviews_data = json.load(f)
    print(f"Reviews loaded: {len(reviews_data)}")
except Exception as e:
    print(f"Error loading reviews: {e}")
    reviews_data = []

# Process books
book_records = []
for b in books_data:
    bid_str = b.get('book_id', '')
    m = re.search(r'bookid_(\d+)', bid_str)
    if m:
        bid = int(m.group(1))
        details = b.get('details', '')
        years = re.findall(r'\b(19\d{2}|20\d{2})\b', details)
        valid_years = [int(y) for y in years if 1900 <= int(y) <= 2023]
        if valid_years:
            book_records.append({'id': bid, 'year': valid_years[0]})

print(f"Books parsed: {len(book_records)}")

# Process reviews
review_records = []
for r in reviews_data:
    pid_str = r.get('purchase_id', '')
    m = re.search(r'purchaseid_(\d+)', pid_str)
    if m:
        pid = int(m.group(1))
        try:
            rating = float(r.get('rating', 0))
            review_records.append({'id': pid, 'rating': rating})
        except:
            pass

print(f"Reviews parsed: {len(review_records)}")

books_df = pd.DataFrame(book_records)
reviews_df = pd.DataFrame(review_records)

if not books_df.empty and not reviews_df.empty:
    # Average rating per book
    book_avg = reviews_df.groupby('id')['rating'].mean().reset_index()
    book_avg.columns = ['id', 'avg_rating']
    
    # Merge
    merged = pd.merge(books_df, book_avg, on='id', how='inner')
    print(f"Merged count: {len(merged)}")
    
    # Decade
    merged['decade'] = (merged['year'] // 10) * 10
    merged['decade_str'] = merged['decade'].astype(int).astype(str) + "s"
    
    # Group by decade
    decade_stats = merged.groupby('decade_str').agg(
        book_count=('id', 'count'),
        decade_avg_rating=('avg_rating', 'mean')
    ).reset_index()
    
    # Filter
    filtered = decade_stats[decade_stats['book_count'] >= 10].copy()
    
    if not filtered.empty:
        # Sort by rating descending
        filtered.sort_values(by='decade_avg_rating', ascending=False, inplace=True)
        
        best_decade = filtered.iloc[0]
        
        result = {
            "decade": str(best_decade['decade_str']),
            "average_rating": float(best_decade['decade_avg_rating']),
            "book_count": int(best_decade['book_count'])
        }
        print("__RESULT__:")
        print(json.dumps(result))
    else:
        print("__RESULT__:")
        print(json.dumps({"error": "No result found"}))
else:
    print("__RESULT__:")
    print(json.dumps({"error": "Data empty", "books_len": len(books_df), "reviews_len": len(reviews_df)}))"""

env_args = {'var_function-call-7608015069099391471': ['books_info'], 'var_function-call-7608015069099390306': ['review'], 'var_function-call-9565206854667938728': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-9565206854667939563': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-6871574713258866780': [{'count': '200'}], 'var_function-call-6871574713258865367': [{'COUNT(*)': '1833'}], 'var_function-call-4837046250283943508': 'file_storage/function-call-4837046250283943508.json', 'var_function-call-4837046250283945065': 'file_storage/function-call-4837046250283945065.json', 'var_function-call-6561548000523148282': {'error': 'Data empty.'}, 'var_function-call-2287585016991985716': {'error': 'Data empty'}}

exec(code, env_args)
