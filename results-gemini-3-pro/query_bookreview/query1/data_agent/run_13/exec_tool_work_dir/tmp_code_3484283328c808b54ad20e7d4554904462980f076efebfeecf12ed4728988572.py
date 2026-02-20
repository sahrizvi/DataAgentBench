code = """import pandas as pd
import re
import json

log = []
try:
    with open(locals()['var_function-call-9654581938833205007']) as f:
        books = json.load(f)
    
    log.append(f"Total books: {len(books)}")
    
    # Debug first book details
    b0 = books[0]
    log.append(f"Details 0: {b0.get('details')}")
    matches = re.findall(r'\d{4}', b0.get('details', ''))
    log.append(f"Matches 0: {matches}")
    
    book_data = []
    for b in books:
        bid_str = b.get('book_id', '')
        id_match = re.search(r'(\d+)', bid_str)
        if not id_match:
            continue
        bid = int(id_match.group(1))
        
        details = b.get('details', '')
        # Try finding any 4 digit number
        candidates = re.findall(r'\d{4}', details)
        year = None
        for c in candidates:
            y = int(c)
            if 1900 <= y <= 2024:
                year = y
                break # Take first valid year
        
        if year:
            decade = (year // 10) * 10
            book_data.append({'id': bid, 'year': year, 'decade': decade})
            
    log.append(f"Extracted {len(book_data)} valid books.")
    
    # Process reviews
    with open(locals()['var_function-call-9654581938833204166']) as f:
        reviews = json.load(f)
    
    review_data = []
    for r in reviews:
        pid_str = r.get('purchase_id', '')
        id_match = re.search(r'(\d+)', pid_str)
        if not id_match:
            continue
        pid = int(id_match.group(1))
        rating = float(r.get('rating', 0))
        review_data.append({'id': pid, 'rating': rating})
    
    log.append(f"Extracted {len(review_data)} reviews.")
    
    df_books = pd.DataFrame(book_data)
    df_reviews = pd.DataFrame(review_data)
    
    if df_books.empty:
        final_ans = "No books extracted"
    else:
        merged = pd.merge(df_reviews, df_books, on='id', how='inner')
        log.append(f"Merged rows: {len(merged)}")
        
        if not merged.empty:
            stats = merged.groupby('decade').agg(
                distinct_books=('id', 'nunique'),
                avg_rating=('rating', 'mean')
            ).reset_index()
            
            log.append(f"Decade stats: {stats.to_dict(orient='records')}")
            
            valid = stats[stats['distinct_books'] >= 10]
            if not valid.empty:
                 best = valid.loc[valid['avg_rating'].idxmax()]
                 result = {"decade": int(best['decade']), "avg_rating": best['avg_rating']}
                 final_ans = f"{int(best['decade'])}s"
            else:
                 final_ans = "No valid decade"
        else:
            final_ans = "Merge empty"

    print("__RESULT__:")
    print(json.dumps({"log": log, "final_answer": final_ans}))

except Exception as e:
    print("__RESULT__:")
    print(json.dumps({"error": str(e), "log": log}))"""

env_args = {'var_function-call-13366482996862838801': ['books_info'], 'var_function-call-13366482996862839796': ['review'], 'var_function-call-14784826910390619232': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.'}], 'var_function-call-14784826910390618829': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}], 'var_function-call-5735080624127152271': [{'book_id': 'bookid_186'}], 'var_function-call-17037478580475657313': [{'count': '200'}], 'var_function-call-17037478580475656736': [{'count(*)': '1833'}], 'var_function-call-9654581938833205007': 'file_storage/function-call-9654581938833205007.json', 'var_function-call-9654581938833204166': 'file_storage/function-call-9654581938833204166.json', 'var_function-call-15725907390585084504': 'DEBUG_DONE', 'var_function-call-1712801689761789523': {'error': 'No books extracted', 'sample_book': {'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}}, 'var_function-call-14763423390235687455': 'DEBUG_TRACING_DONE', 'var_function-call-3226559586249020779': {'error': "'id'", 'log': ['Total books: 200', "Book 0: ID='bookid_1'", '  ID Match: 1', '  Years Found: []', "Book 1: ID='bookid_2'", '  ID Match: 2', '  Years Found: []', "Book 2: ID='bookid_3'", '  ID Match: 3', '  Years Found: []', "Book 3: ID='bookid_4'", '  ID Match: 4', '  Years Found: []', "Book 4: ID='bookid_5'", '  ID Match: 5', '  Years Found: []', 'Extracted 0 valid books.', 'Extracted 1833 reviews.']}}

exec(code, env_args)
