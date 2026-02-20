code = """import json
import re
import pandas as pd

# Load data
with open(locals()['var_function-call-3610629538051826770'], 'r') as f:
    books_data = json.load(f)

with open(locals()['var_function-call-3610629538051828953'], 'r') as f:
    reviews_data = json.load(f)

# 1. Parse Books
book_list = []
for b in books_data:
    b_id_str = b.get('book_id', '')
    details = b.get('details', '')
    
    # Extract numeric ID from "bookid_X"
    m = re.search(r'bookid_(\d+)', b_id_str)
    if m:
        bid = int(m.group(1))
    else:
        continue
        
    # Extract Year
    # Strategy: Find "published ... \d{4}"
    # or "released ... \d{4}"
    # or just any 4-digit year 19xx or 20xx?
    # Let's try to be specific first.
    
    # Clean details a bit
    details_clean = details.replace('\n', ' ')
    
    year = None
    
    # Pattern 1: "published ... on [Month] [Day], [Year]"
    # Pattern 2: "released on [Month] [Day], [Year]"
    # Pattern 3: "published ... in [Month] [Year]"
    # Pattern 4: "published ... [Year]"
    
    # Regex to find years 1900-2099
    years_found = re.findall(r'\b(19\d{2}|20\d{2})\b', details_clean)
    
    if years_found:
        # If multiple years, which one?
        # Usually the publication year is the first one mentioned in "published" context.
        # But simply taking the first year found in text is often correct for these descriptions.
        # Let's verify with "8082nd edition from January 1, 1994". 2004 appears before 1994 in that text?
        # Text: "The book, published by Guilford in its second edition in January 2004, is also noted as the 8082nd edition from January 1, 1994."
        # 2004 is first.
        # Text: "Published by Chatto & Windus... January 1, 2004." -> 2004.
        # Text: "published by Heinemann ... May 20, 1996" -> 1996.
        # Text: "published by Random House ... January 1, 1945" -> 1945.
        
        # So taking the first 4-digit year (19xx or 20xx) seems a good heuristic.
        year = int(years_found[0])
    
    if year:
        book_list.append({'id': bid, 'year': year})

df_books = pd.DataFrame(book_list)

# 2. Parse Reviews
review_list = []
for r in reviews_data:
    p_id_str = r.get('purchase_id', '')
    rating = r.get('rating')
    
    try:
        rating = float(rating)
    except:
        continue
    
    # Extract numeric ID from "purchaseid_X"
    m = re.search(r'purchaseid_(\d+)', p_id_str)
    if m:
        pid = int(m.group(1))
        review_list.append({'id': pid, 'rating': rating})

df_reviews = pd.DataFrame(review_list)

# 3. Merge
if not df_books.empty and not df_reviews.empty:
    # Inner join to keep only rated books
    merged = pd.merge(df_reviews, df_books, on='id', how='inner')
    
    # Calculate Decade
    merged['decade'] = (merged['year'] // 10) * 10
    
    # Group by Decade
    # We need:
    # - Decade
    # - Count of distinct books
    # - Average rating
    
    # Let's calculate average rating per book first
    book_stats = merged.groupby(['decade', 'id']).agg(
        avg_book_rating=('rating', 'mean')
    ).reset_index()
    
    # Now group by decade
    decade_stats = book_stats.groupby('decade').agg(
        distinct_books=('id', 'count'),
        avg_of_avg_ratings=('avg_book_rating', 'mean')
    ).reset_index()
    
    # Also calculate pooled average for comparison
    decade_pooled = merged.groupby('decade').agg(
        pooled_avg_rating=('rating', 'mean')
    ).reset_index()
    
    final_stats = pd.merge(decade_stats, decade_pooled, on='decade')
    
    # Filter >= 10 distinct books
    valid_decades = final_stats[final_stats['distinct_books'] >= 10].copy()
    
    valid_decades['decade_str'] = valid_decades['decade'].astype(str) + 's'
    
    # Sort by avg_of_avg_ratings
    result_avg_book = valid_decades.sort_values('avg_of_avg_ratings', ascending=False)
    
    # Sort by pooled_avg_rating
    result_pooled = valid_decades.sort_values('pooled_avg_rating', ascending=False)
    
    res = {
        'by_book_avg': result_avg_book.to_dict(orient='records'),
        'by_pooled_avg': result_pooled.to_dict(orient='records')
    }
else:
    res = "Empty"

print("__RESULT__:")
print(json.dumps(res))"""

env_args = {'var_function-call-18101336634187803449': ['books_info'], 'var_function-call-18101336634187801202': ['review'], 'var_function-call-5580524011425732162': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'title': 'Chaucer'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.', 'title': 'Notes from a Kidwatcher'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.', 'title': 'Service: A Navy SEAL at War'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.', 'title': 'Parker & Knight'}], 'var_function-call-5580524011425734391': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-6209676167917198432': [{'count': '200'}], 'var_function-call-6209676167917195647': [{'count(*)': '1833'}], 'var_function-call-3610629538051826770': 'file_storage/function-call-3610629538051826770.json', 'var_function-call-3610629538051828953': 'file_storage/function-call-3610629538051828953.json', 'var_function-call-18386140052340095889': {'decade': '2020s', 'avg_rating': 4.663636363636364, 'distinct_books': 21}}

exec(code, env_args)
