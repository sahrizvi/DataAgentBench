code = """import json
import re
import pandas as pd

try:
    with open(locals()['var_function-call-4771381072856053893'], 'r') as f:
        books_data = json.load(f)

    with open(locals()['var_function-call-13869118034911199914'], 'r') as f:
        reviews_data = json.load(f)

    # Process Books
    book_records = []
    for b in books_data:
        bid = b.get('book_id', '')
        details = b.get('details', '')
        subtitle = b.get('subtitle', '')
        
        # Extract ID
        if isinstance(bid, str) and 'bookid_' in bid:
            try:
                book_num = int(bid.split('_')[1])
                
                # Combine text for year search
                text = f"{details} {subtitle}"
                
                # Find all 4-digit numbers
                candidates = re.findall(r'(\d{4})', text)
                
                year = None
                for c in candidates:
                    if c.startswith('19') or c.startswith('20'):
                        # Check if valid year range
                        y = int(c)
                        if 1900 <= y <= 2023:
                            year = y
                            break
                
                if year:
                    book_records.append({'id': book_num, 'year': year})
            except:
                pass

    df_books = pd.DataFrame(book_records)

    # Process Reviews
    review_records = []
    for r in reviews_data:
        pid = r.get('purchase_id', '')
        rating = r.get('rating')
        
        if isinstance(pid, str) and 'purchaseid_' in pid:
            try:
                book_num = int(pid.split('_')[1])
                val = float(rating)
                review_records.append({'id': book_num, 'rating': val})
            except:
                pass

    df_reviews = pd.DataFrame(review_records)

    # Aggregate
    if not df_reviews.empty and not df_books.empty:
        book_ratings = df_reviews.groupby('id')['rating'].mean().reset_index()
        book_ratings.rename(columns={'rating': 'avg_rating'}, inplace=True)
        
        # Merge
        df_merged = pd.merge(df_books, book_ratings, on='id', how='inner')
        
        if not df_merged.empty:
            df_merged['decade'] = (df_merged['year'] // 10) * 10
            
            decade_stats = df_merged.groupby('decade').agg(
                num_books=('id', 'nunique'),
                avg_rating=('avg_rating', 'mean')
            ).reset_index()
            
            # Filter
            qualified = decade_stats[decade_stats['num_books'] >= 10].copy()
            qualified.sort_values(by='avg_rating', ascending=False, inplace=True)
            
            if not qualified.empty:
                best_decade = int(qualified.iloc[0]['decade'])
                result = f"{best_decade}s"
            else:
                result = "None - No qualified decades"
        else:
            result = "None - No merged data"
    else:
        result = "None - Empty dataframes"

    print("__RESULT__:")
    print(json.dumps(result))

except Exception as e:
    print("__RESULT__:")
    print(json.dumps(str(e)))"""

env_args = {'var_function-call-5130076193332532434': 'file_storage/function-call-5130076193332532434.json', 'var_function-call-15092950807577421772': [{'count': '200'}], 'var_function-call-9184208097909862798': [{'count(*)': '1833'}], 'var_function-call-4771381072856053893': 'file_storage/function-call-4771381072856053893.json', 'var_function-call-13869118034911199914': 'file_storage/function-call-13869118034911199914.json', 'var_function-call-1497323203245629920': 'Done', 'var_function-call-11749323720662552993': 'None', 'var_function-call-11496871228647915128': 'Done', 'var_function-call-4914481013675661386': ['Num books: 200', "First book keys: ['book_id', 'details', 'subtitle']", 'First book ID: bookid_1', 'First book details: Published by Chatto & Windus, the first edition of...', 'Regex match: 1', 'Years found: []'], 'var_function-call-532188489042779544': ['Full details: Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'Regex 1 result: []', "Regex 2 result: ['2004', '0701', '1698', '0701', '1698']", 'Subtitle: Hardcover – Import, January 1, 2004', "Subtitle regex: ['2004']"]}

exec(code, env_args)
