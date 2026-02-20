code = """import json
import re
import pandas as pd

# Load data
with open(locals()['var_function-call-3610629538051826770'], 'r') as f:
    books_data = json.load(f)

with open(locals()['var_function-call-3610629538051828953'], 'r') as f:
    reviews_data = json.load(f)

# Process Books
book_list = []
for b in books_data:
    b_id_str = b.get('book_id', '')
    details = b.get('details', '')
    
    # Extract numeric ID
    # Assumes format "bookid_123"
    m_id = re.search(r'(\d+)', b_id_str)
    if m_id:
        b_id = int(m_id.group(1))
    else:
        continue

    # Extract Year
    # Look for patterns like "January 1, 2004"
    # The text usually says "published ... on <Date>" or "released on <Date>"
    # or "in a <Date> edition"
    
    year = None
    # Regex for "Month Day, Year"
    # Matches: January 1, 2004 | May 20, 1996 | etc.
    date_matches = re.findall(r'([A-Z][a-z]+\s+\d{1,2},\s+(\d{4}))', details)
    
    if date_matches:
        # Take the first match's year
        # In the example: "published by ... on May 8, 2012" -> ('May 8, 2012', '2012')
        # In the example with two dates: "published ... in January 2004 ... from January 1, 1994"
        # "January 2004" is not Month Day, Year.
        # Let's adjust regex to allow "Month Year" or "Month Day, Year"
        # But "Month Day, Year" is more specific.
        # Let's check the complex example: "published by Guilford in its second edition in January 2004..."
        # If I use `[A-Z][a-z]+ \d{4}` I might catch "January 2004".
        
        # Let's prioritize "published ... on/in ..."
        # Simple heuristic: Find all years (19xx or 20xx). 
        # The publication year is likely the first one mentioned in the context of "published" or "released".
        # Or just the first 4-digit number that looks like a year?
        # ISBNs are 10 or 13 digits.
        # Dimensions are small numbers.
        # Pages are hundreds.
        
        # Let's stick to the specific date format first.
        year = int(date_matches[0][1])
    else:
        # Fallback: look for just a year 19XX or 20XX that is NOT part of ISBN (usually ISBN starts with 0, 1, 9)
        # But ISBN-10 can look like a year? No, usually longer.
        # Let's look for "published ... (\d{4})"
        m_year = re.search(r'(?:published|released).*?(\d{4})', details, re.IGNORECASE)
        if m_year:
            year = int(m_year.group(1))
        
    if year:
        book_list.append({'id': b_id, 'year': year})

df_books = pd.DataFrame(book_list)

# Process Reviews
review_list = []
for r in reviews_data:
    p_id_str = r.get('purchase_id', '')
    rating = r.get('rating')
    
    try:
        rating = float(rating)
    except:
        continue
        
    m_id = re.search(r'(\d+)', p_id_str)
    if m_id:
        p_id = int(m_id.group(1))
        review_list.append({'id': p_id, 'rating': rating})

df_reviews = pd.DataFrame(review_list)

# Merge
if not df_books.empty and not df_reviews.empty:
    merged = pd.merge(df_reviews, df_books, on='id', how='inner')
    
    # Calculate Decade
    merged['decade'] = (merged['year'] // 10) * 10
    merged['decade_str'] = merged['decade'].astype(str) + 's'
    
    # Distinct books per decade
    # Count distinct 'id' in the merged set (books that have ratings)
    decade_stats = merged.groupby('decade_str').agg(
        avg_rating=('rating', 'mean'),
        distinct_books=('id', 'nunique')
    ).reset_index()
    
    # Filter >= 10 distinct books
    filtered = decade_stats[decade_stats['distinct_books'] >= 10]
    
    # Find highest average rating
    if not filtered.empty:
        best_decade = filtered.sort_values('avg_rating', ascending=False).iloc[0]
        result = {
            'decade': best_decade['decade_str'],
            'avg_rating': best_decade['avg_rating'],
            'distinct_books': int(best_decade['distinct_books'])
        }
    else:
        result = "No decade met criteria"
else:
    result = "Data empty or merge failed"

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_function-call-18101336634187803449': ['books_info'], 'var_function-call-18101336634187801202': ['review'], 'var_function-call-5580524011425732162': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'title': 'Chaucer'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.', 'title': 'Notes from a Kidwatcher'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.', 'title': 'Service: A Navy SEAL at War'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.', 'title': 'Parker & Knight'}], 'var_function-call-5580524011425734391': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-6209676167917198432': [{'count': '200'}], 'var_function-call-6209676167917195647': [{'count(*)': '1833'}], 'var_function-call-3610629538051826770': 'file_storage/function-call-3610629538051826770.json', 'var_function-call-3610629538051828953': 'file_storage/function-call-3610629538051828953.json'}

exec(code, env_args)
