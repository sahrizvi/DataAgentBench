code = """import json, pandas as pd, re, glob, os

# Check what files exist
print('Temp directory contents:', os.listdir('/tmp')[:20])

# Find JSON files
json_files = glob.glob('/tmp/tmp*.json')
print('JSON files:', json_files)

books_data = None
reviews_data = None

# Load files
for f in json_files:
    try:
        file_size = os.path.getsize(f)
        if file_size > 1000:  # Only process larger files (skip small queries)
            with open(f, 'r') as file:
                data = json.load(file)
            if isinstance(data, list) and len(data) > 0:
                sample = str(data[0])
                if 'book_id' in sample:
                    books_data = data
                    print('Found books:', f, 'records:', len(books_data))
                elif 'purchase_id' in sample and 'rating' in sample:
                    reviews_data = data
                    print('Found reviews:', f, 'records:', len(reviews_data))
    except Exception as e:
        print('Error with', f, ':', e)

if books_data and reviews_data:
    df_books = pd.DataFrame(books_data)
    df_reviews = pd.DataFrame(reviews_data)
    
    print('Books columns:', df_books.columns.tolist())
    print('Books first record keys:', list(df_books.iloc[0].keys()) if len(df_books) > 0 else [])
    
    # Extract year properly
    def get_year(text):
        if pd.isna(text) or text is None:
            return None
        match = re.search(r'(19\d{2}|20[0-2]\d)', str(text))
        return int(match.group(1)) if match else None
    
    # Find which column contains publication info if details not in columns
    if 'details' in df_books.columns:
        df_books['year'] = df_books['details'].apply(get_year)
    else:
        # Try other columns
        for col in df_books.columns:
            if df_books[col].dtype == 'object':
                year_count = df_books[col].apply(get_year).notna().sum()
                if year_count > 0:
                    print(f'Found {year_count} years in column {col}')
                    df_books['year'] = df_books[col].apply(get_year)
                    break
    
    df_books['decade'] = (df_books['year'] // 10) * 10
    
    # Extract IDs
    def get_id(id_str):
        match = re.search(r'(\d+)', str(id_str))
        return int(match.group(1)) if match else None
    
    df_books['num_id'] = df_books['book_id'].apply(get_id)
    df_reviews['num_id'] = df_reviews['purchase_id'].apply(get_id)
    df_reviews['rating'] = pd.to_numeric(df_reviews['rating'])
    
    # Clean and merge
    books_clean = df_books.dropna(subset=['year', 'num_id', 'decade'])
    reviews_clean = df_reviews.dropna(subset=['num_id', 'rating'])
    
    common_ids = set(books_clean['num_id']) & set(reviews_clean['num_id'])
    
    print(f'Books clean: {len(books_clean)}, Reviews clean: {len(reviews_clean)}, Common: {len(common_ids)}')
    
    if len(common_ids) > 0:
        merged = pd.merge(
            books_clean[books_clean['num_id'].isin(common_ids)][['num_id', 'decade']],
            reviews_clean[reviews_clean['num_id'].isin(common_ids)][['num_id', 'rating']],
            on='num_id'
        )
        
        decade_stats = merged.groupby('decade').agg({
            'rating': ['mean', 'count'],
            'num_id': 'nunique'
        }).round(3)
        
        decade_stats.columns = ['avg_rating', 'total_ratings', 'distinct_books']
        decade_stats = decade_stats.reset_index()
        
        print('Decade stats:')
        print(decade_stats.to_string())
        
        eligible = decade_stats[decade_stats['distinct_books'] >= 10]
        
        if not eligible.empty:
            best_row = eligible.loc[eligible['avg_rating'].idxmax()]
            result = str(int(best_row['decade'])) + 's'
            print('Best decade:', result)
        else:
            print('No decades with >= 10 books')
            result = None
    else:
        result = None
else:
    result = None

print('__RESULT__:')
print(json.dumps(result))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:4': ['review'], 'var_functions.query_db:6': [{'rating': '4', 'title': 'Ha! On me!  I thought this was a cookbook!', 'text': 'Lucky for me it\'s more than a cookbook.<br /><br />The story of a modern Daniel Boone, growing up in Michigan, one of three sons of a hunter.  Beginning at age eight when he shot a squirrel, to age 13 his first deer, then hunting his way through college, a career as a fur trapper, hunting sheep in Alaska, canoeing the Missouri River for deer and ending in Brooklyn age 37. Brooklyn?<br /><br />I especially liked that I share his disgust at catch & release fishing - if you fish it, you have to eat it - anything else is sadism (my words).<br /><br />My brother in law is the cook in the family and I wanted to see if this would be a good gift for him and I struck pay dirt following each chapter are "Tasting Notes" where the author speaks of cooking wild game.<br /><br />I also enjoyed it for the history of the land he has hunted as well as the history of the hunt (I too was a big Daniel Boone fan growing up!).<br /><br />I think more pictures (everything but dead things) would have made this a keeper.', 'review_time': '2012-11-24 18:52:00', 'helpful_vote': '0', 'verified_purchase': '0', 'purchase_id': 'purchaseid_186'}, {'rating': '4', 'title': 'Four Stars', 'text': 'Not as developed as Stephanie but I like the characters so far.', 'review_time': '2015-12-31 13:35:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_191'}, {'rating': '4', 'title': 'A wonderful adventure in France', 'text': "I loved this book all the way until the end. I have recently discovered that the author is intending to release another book, and from what I understand it will continue where this one left off. I am thankful for this, as the way this book ended was definitely a negative for me. I wanted to know more! What happened to the author, did she learn what she came to learn? Did she get the job she was hoping for? So many questions.<br /><br />From the beginning of Linda's book, it is easy to love her. She is open, honest and definitely has the type of personality you want your heroine to have, whether the book is fiction or reality. I couldn't help but root for Linda throughout her trials with her host family, even when I thought she acted as a bit of a brat herself. Listening to her internal thoughts about what she went through and her desire to achieve her goals made this book feel close to my heart.<br /><br />I applaud the adventurous spirit of the author and her decision to keep journal entries from that chapter of her life. What great material to have later to inspire a book! While I enjoyed the entire memoir, my favourite part of this book would have to be the author's descriptions of the many places she visited and the people she met along the way. While I think she could definitely have made a better impression on the family she worked for if she had been honest about her lack of French language skills from the beginning, she is a pioneer. Her drive and desire to learn the language from those in the actual country was inspiring. Not many people would have been gutsy enough to do what Linda did.<br /><br />I also particularly enjoyed the relationship between Linda and Antoine. The Kind heart of the author was apparent in her actions toward the children, even when she struggled with them.<br /><br />There is some romance, and I appreciated the way the author handled it. While sex scenes are not necessarily automatically offensive, there is something about memoirs that makes me uncomfortable if they are filled with them. This author manages to hint at her experiences without going into too much detail, leaving the reader to decide exactly what happened. Great writing.<br /><br />When you step into reading this book, you learn a lot about French customs, French cuisine and wine. You also get the opportunity to brush up on your French skills a bit and get to step outside yourself and live an adventure through the eyes of the author. I read this book in one sitting with very few breaks in between and found myself enthralled in the sights, sounds and atmosphere of this memoir.<br /><br />In the end, I was disappointed that the book ended. I could have kept reading about Linda's experiences without stopping anytime in the foreseeable future. The end of the book leaves many unanswered questions, that I am assuming the author will be answering in her next book. Were this a standalone, I would be very disappointed with the way the book ended, but with the knowledge that she is writing another book to continue with her story, I can't fault this one. One thing is for sure, if you read this book, you will be anxiously awaiting the next.<br /><br />I would recommend this to anyone who likes books about travel, memoirs or just a good story that came from the recollections and heart of the author. Read it, you will be glad you did. Overall, this was a VERY enjoyable read that gave me many reasons to wish I could drop everything and head off to France!", 'review_time': '2013-05-05 10:47:00', 'helpful_vote': '1', 'verified_purchase': '0', 'purchase_id': 'purchaseid_190'}, {'rating': '5', 'title': 'Best beginner book.  Been looking for something like this for a long time.', 'text': "Looked online for years for something like this.  It's the best I've seen.", 'review_time': '2020-08-12 11:06:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_8'}, {'rating': '4', 'title': 'Referance Guide', 'text': 'Good reference guide for the basics', 'review_time': '2014-11-13 18:55:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_178'}], 'var_functions.query_db:8': [], 'var_functions.query_db:10': 'file_storage/functions.query_db:10.json', 'var_functions.query_db:12': 'file_storage/functions.query_db:12.json', 'var_functions.query_db:14': [{'purchase_id': 'purchaseid_186'}, {'purchase_id': 'purchaseid_191'}, {'purchase_id': 'purchaseid_190'}, {'purchase_id': 'purchaseid_8'}, {'purchase_id': 'purchaseid_178'}, {'purchase_id': 'purchaseid_186'}, {'purchase_id': 'purchaseid_76'}, {'purchase_id': 'purchaseid_186'}, {'purchase_id': 'purchaseid_115'}, {'purchase_id': 'purchaseid_167'}], 'var_functions.query_db:16': 'file_storage/functions.query_db:16.json', 'var_functions.query_db:26': 'file_storage/functions.query_db:26.json', 'var_functions.query_db:28': 'file_storage/functions.query_db:28.json', 'var_functions.execute_python:34': None, 'var_functions.query_db:40': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.'}], 'var_functions.query_db:44': [{'book_id': 'bookid_1', 'year_str': '2004'}, {'book_id': 'bookid_2', 'year_str': '1996'}, {'book_id': 'bookid_3', 'year_str': '2012'}, {'book_id': 'bookid_4', 'year_str': '2013'}, {'book_id': 'bookid_5', 'year_str': '2014'}, {'book_id': 'bookid_6', 'year_str': '2021'}, {'book_id': 'bookid_7', 'year_str': '1994'}, {'book_id': 'bookid_8', 'year_str': '2015'}, {'book_id': 'bookid_9', 'year_str': '2019'}, {'book_id': 'bookid_10', 'year_str': '1932'}], 'var_functions.execute_python:46': None, 'var_functions.query_db:48': [{'total_books': '200'}], 'var_functions.query_db:52': 'file_storage/functions.query_db:52.json', 'var_functions.query_db:56': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]'}], 'var_functions.execute_python:66': 'analysis_complete', 'var_functions.query_db:68': [], 'var_functions.execute_python:72': None}

exec(code, env_args)
