code = """import json
import re
import pandas as pd
import traceback

debug = {}

try:
    with open(locals()['var_function-call-12676996466119317051'], 'r') as f:
        books = json.load(f)
    with open(locals()['var_function-call-9741256298441356484'], 'r') as f:
        reviews = json.load(f)

    # Test regex on first book
    b1 = books[0]
    details = b1.get('details', '')
    debug['first_book_details'] = details
    
    # regex 1: \b(19\d{2}|20\d{2})\b
    r1 = re.findall(r'\b(19\d{2}|20\d{2})\b', details)
    debug['regex1_matches'] = r1
    
    # regex 2: \d{4}
    r2 = re.findall(r'\d{4}', details)
    debug['regex2_matches'] = r2
    
    # Process all books
    book_years = {}
    for book in books:
        b_id = book['book_id']
        det = book.get('details', '')
        if not det: continue
        
        # Use regex 2 and filter
        candidates = re.findall(r'\d{4}', det)
        # Filter for years 1900-2024
        valid = [int(y) for y in candidates if 1900 <= int(y) <= 2024]
        if valid:
            book_years[b_id] = valid[0] # taking first valid year
            
    debug['books_with_years_count'] = len(book_years)
    
    # Map reviews
    df_reviews = pd.DataFrame(reviews)
    df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
    
    # direct replace purchaseid -> bookid
    df_reviews['book_id'] = df_reviews['purchase_id'].str.replace('purchaseid', 'bookid')
    
    # merge
    df_reviews['year'] = df_reviews['book_id'].map(book_years)
    
    df_merged = df_reviews.dropna(subset=['year']).copy()
    debug['merged_count'] = len(df_merged)
    
    if len(df_merged) > 0:
        df_merged['year'] = df_merged['year'].astype(int)
        df_merged['decade'] = (df_merged['year'] // 10) * 10
        df_merged['decade_str'] = df_merged['decade'].astype(str) + 's'
        
        stats = df_merged.groupby('decade_str').agg(
            distinct_books=('book_id', 'nunique'),
            avg_rating=('rating', 'mean')
        ).reset_index()
        
        debug['stats'] = stats.to_dict(orient='records')
        
        qualified = stats[stats['distinct_books'] >= 10]
        if not qualified.empty:
            best = qualified.sort_values('avg_rating', ascending=False).iloc[0]
            result = best['decade_str']
        else:
            result = "No qualified decade"
    else:
        result = "No merged data"

except Exception as e:
    result = "Error"
    debug['error'] = str(e)
    debug['traceback'] = traceback.format_exc()

print("__RESULT__:")
print(json.dumps({"result": result, "debug": debug}))"""

env_args = {'var_function-call-14391079220039824156': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-12032611119589619147': [{'count': '200'}], 'var_function-call-14893637540441165934': [{'COUNT(*)': '1833'}], 'var_function-call-12676996466119317051': 'file_storage/function-call-12676996466119317051.json', 'var_function-call-9741256298441356484': 'file_storage/function-call-9741256298441356484.json', 'var_function-call-4533316282141004050': [], 'var_function-call-586999647154881006': {'result': 'No merged data', 'debug': {'sample_books': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}], 'books_with_years': 0, 'sample_years': [], 'sample_reviews': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}], 'common_ids_count': 0, 'merged_rows': 0}}}

exec(code, env_args)
