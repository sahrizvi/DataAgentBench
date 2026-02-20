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
        
        # specific string pattern
        if isinstance(bid, str) and 'bookid_' in bid:
            try:
                book_num = int(bid.split('_')[1])
                
                # Extract year
                years = re.findall(r'\b(19\d{2}|20\d{2})\b', str(details))
                if years:
                    year = int(years[0])
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
    if not df_reviews.empty and 'id' in df_reviews.columns:
        book_ratings = df_reviews.groupby('id')['rating'].mean().reset_index()
        book_ratings.rename(columns={'rating': 'avg_rating'}, inplace=True)
    else:
        book_ratings = pd.DataFrame(columns=['id', 'avg_rating'])

    # Merge
    if not df_books.empty and not book_ratings.empty:
        df_merged = pd.merge(df_books, book_ratings, on='id', how='inner')
    else:
        df_merged = pd.DataFrame()

    if df_merged.empty:
        result = "None"
    else:
        # Decade logic
        df_merged['decade'] = (df_merged['year'] // 10) * 10
        decade_stats = df_merged.groupby('decade').agg(
            num_books=('id', 'nunique'),
            avg_rating=('avg_rating', 'mean')
        ).reset_index()
        
        qualified = decade_stats[decade_stats['num_books'] >= 10].copy()
        qualified.sort_values(by='avg_rating', ascending=False, inplace=True)
        
        if not qualified.empty:
            best_decade = qualified.iloc[0]
            result = f"{int(best_decade['decade'])}s"
        else:
            result = "None"

    print("__RESULT__:")
    print(json.dumps(result))

except Exception as e:
    print("__RESULT__:")
    print(json.dumps(str(e)))"""

env_args = {'var_function-call-5130076193332532434': 'file_storage/function-call-5130076193332532434.json', 'var_function-call-15092950807577421772': [{'count': '200'}], 'var_function-call-9184208097909862798': [{'count(*)': '1833'}], 'var_function-call-4771381072856053893': 'file_storage/function-call-4771381072856053893.json', 'var_function-call-13869118034911199914': 'file_storage/function-call-13869118034911199914.json', 'var_function-call-1497323203245629920': 'Done'}

exec(code, env_args)
