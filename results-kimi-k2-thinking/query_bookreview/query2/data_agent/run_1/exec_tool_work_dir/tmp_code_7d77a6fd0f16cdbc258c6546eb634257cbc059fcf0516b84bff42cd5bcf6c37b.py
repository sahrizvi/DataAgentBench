code = """import json
import pandas as pd
import ast
import os

# Find all JSON files in /tmp
json_files = []
for root, dirs, files in os.walk('/tmp'):
    for file in files:
        if file.endswith('.json'):
            json_files.append(os.path.join(root, file))

print('Found files:', len(json_files))

# Load data from files
books_data = []
reviews_data = []

for file_path in json_files:
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        if isinstance(data, list) and len(data) > 0:
            first_item = data[0]
            if isinstance(first_item, dict):
                keys = list(first_item.keys())
                if 'book_id' in keys and 'title' in keys and 'categories' in keys:
                    books_data = data
                    print('Loaded books data:', len(books_data))
                elif 'purchase_id' in keys and ('avg_rating' in keys or 'rating' in keys):
                    reviews_data = data
                    print('Loaded reviews data:', len(reviews_data))
    except Exception as e:
        print('Error loading file:', e)

# Process the data
result = []

if books_data and reviews_data:
    df_books = pd.DataFrame(books_data)
    df_reviews = pd.DataFrame(reviews_data)
    
    # Parse categories
    def parse_categories(cat_str):
        if pd.isna(cat_str) or cat_str == '[]':
            return []
        try:
            return ast.literal_eval(cat_str)
        except:
            return []
    
    # Filter books: Literature & Fiction category and English language
    df_books['categories_list'] = df_books['categories'].apply(parse_categories)
    df_books_filtered = df_books[
        df_books['categories_list'].apply(lambda x: 'Literature & Fiction' in x if x else False)
    ]
    
    # Check if details column exists for English language filter
    if 'details' in df_books_filtered.columns and not df_books_filtered.empty:
        df_books_filtered = df_books_filtered[
            df_books_filtered['details'].str.contains('English', case=False, na=False)
        ]
    
    print('\nFiltered books count:', len(df_books_filtered))
    
    # If avg_rating already in reviews, use it directly
    if 'avg_rating' in df_reviews.columns:
        df_perfect_ratings = df_reviews[df_reviews['avg_rating'].astype(float) == 5.0]
        df_reviews['book_num'] = df_perfect_ratings['purchase_id'].str.replace('purchaseid_', '')
    else:
        # Group reviews by purchase_id and calculate average
        df_reviews['rating'] = pd.to_numeric(df_reviews['rating'])
        df_review_agg = df_reviews.groupby('purchase_id').agg({
            'rating': ['mean', 'count']
        }).reset_index()
        
        df_review_agg.columns = ['purchase_id', 'avg_rating', 'review_count']
        df_perfect_ratings = df_review_agg[df_review_agg['avg_rating'] == 5.0]
        df_perfect_ratings['book_num'] = df_perfect_ratings['purchase_id'].str.replace('purchaseid_', '')
    
    print('Perfect rating reviews count:', len(df_perfect_ratings))
    
    # Match books with perfect ratings
    if not df_books_filtered.empty and not df_perfect_ratings.empty:
        df_books_filtered['book_num'] = df_books_filtered['book_id'].str.replace('bookid_', '')
        
        matched = df_books_filtered.merge(
            df_perfect_ratings[['book_num', 'avg_rating', 'review_count']], 
            left_on='book_num', 
            right_on='book_num', 
            how='inner'
        )
        
        print('Matched books count:', len(matched))
        
        if not matched.empty:
            result = matched[['book_id', 'title', 'categories', 'avg_rating', 'review_count']].to_dict('records')

print('\n__RESULT__:')
print(json.dumps(result, indent=2))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.execute_python:10': [], 'var_functions.query_db:16': 'file_storage/functions.query_db:16.json', 'var_functions.execute_python:22': [], 'var_functions.execute_python:26': [], 'var_functions.execute_python:30': [], 'var_functions.query_db:32': 'file_storage/functions.query_db:32.json', 'var_functions.query_db:36': [{'purchase_id': 'purchaseid_101', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_105', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_108', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_110', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_114', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_116', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_117', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_118', 'avg_rating': '5.0', 'review_count': '6'}, {'purchase_id': 'purchaseid_12', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_121', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_122', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_123', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_124', 'avg_rating': '5.0', 'review_count': '4'}, {'purchase_id': 'purchaseid_126', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_127', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_128', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_130', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_132', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_133', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_134', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_14', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_143', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_144', 'avg_rating': '5.0', 'review_count': '6'}, {'purchase_id': 'purchaseid_146', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_150', 'avg_rating': '5.0', 'review_count': '11'}, {'purchase_id': 'purchaseid_151', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_152', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_153', 'avg_rating': '5.0', 'review_count': '15'}, {'purchase_id': 'purchaseid_156', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_16', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_160', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_163', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_166', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_168', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_170', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_171', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_172', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_174', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_177', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_180', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_181', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_182', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_184', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_192', 'avg_rating': '5.0', 'review_count': '6'}, {'purchase_id': 'purchaseid_195', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_197', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_2', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_21', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_24', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_26', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_28', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_29', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_33', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_34', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_38', 'avg_rating': '5.0', 'review_count': '4'}, {'purchase_id': 'purchaseid_39', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_40', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_41', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_42', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_47', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_54', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_56', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_57', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_59', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_6', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_60', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_64', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_7', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_71', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_73', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_74', 'avg_rating': '5.0', 'review_count': '8'}, {'purchase_id': 'purchaseid_75', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_79', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_80', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_82', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_83', 'avg_rating': '5.0', 'review_count': '14'}, {'purchase_id': 'purchaseid_84', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_88', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_9', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_90', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_91', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_97', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_98', 'avg_rating': '5.0', 'review_count': '1'}], 'var_functions.query_db:42': [{'book_id': 'bookid_1', 'title': 'Chaucer', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]'}, {'book_id': 'bookid_9', 'title': 'Reunion: The Children of Lauderdale Park', 'categories': '["Books", "Literature & Fiction", "Genre Fiction"]'}, {'book_id': 'bookid_13', 'title': 'Girl Made of Glass', 'categories': '["Books", "Literature & Fiction", "Poetry"]'}, {'book_id': 'bookid_30', 'title': 'Sugary Sweets (A Taste of Love Series)', 'categories': '["Books", "Literature & Fiction", "Humor & Satire"]'}, {'book_id': 'bookid_36', 'title': 'Therapy Mammals', 'categories': '["Books", "Literature & Fiction", "Genre Fiction"]'}, {'book_id': 'bookid_37', 'title': "A Most Dangerous Book: Tacitus's Germania from the Roman Empire to the Third Reich", 'categories': '["Books", "Literature & Fiction", "History & Criticism"]'}, {'book_id': 'bookid_38', 'title': 'The Prophet: With Original 1923 Illustrations by the Author', 'categories': '["Books", "Literature & Fiction", "Poetry"]'}, {'book_id': 'bookid_39', 'title': 'The Melancholy Strumpet Master', 'categories': '["Books", "Literature & Fiction", "Humor & Satire"]'}, {'book_id': 'bookid_44', 'title': 'Reptilian', 'categories': '["Books", "Literature & Fiction", "Genre Fiction"]'}, {'book_id': 'bookid_49', 'title': 'Primeval: A Journal of the Uncanny - Issue #1', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_69', 'title': 'Out of Sheer Rage: Wrestling with D. H. Lawrence', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]'}, {'book_id': 'bookid_70', 'title': 'Polly and the Shadow Goblin: Book 2, Mother of Witches', 'categories': '["Books", "Literature & Fiction", "Mythology & Folk Tales"]'}, {'book_id': 'bookid_74', 'title': 'Child Of The King A Journey of Hope Book 1: Earthly Story With A Heavenly Message', 'categories': '["Books", "Literature & Fiction"]'}, {'book_id': 'bookid_77', 'title': 'One September Morning', 'categories': '["Books", "Literature & Fiction", "Genre Fiction"]'}, {'book_id': 'bookid_82', 'title': 'Fire Cracker', 'categories': '["Books", "Literature & Fiction", "United States"]'}, {'book_id': 'bookid_84', 'title': 'Local Honey', 'categories': '["Books", "Literature & Fiction"]'}, {'book_id': 'bookid_89', 'title': "I'll Ride For My Hood: A Salty Love Story", 'categories': '["Books", "Literature & Fiction", "Dramas & Plays"]'}, {'book_id': 'bookid_92', 'title': 'Outage', 'categories': '["Books", "Literature & Fiction", "Genre Fiction"]'}, {'book_id': 'bookid_93', 'title': 'Simantov', 'categories': '["Books", "Literature & Fiction", "Genre Fiction"]'}, {'book_id': 'bookid_98', 'title': 'Hollywood Confessions: Hollywood Headlines Book #3 (Hollywood Headlines Mysteries)', 'categories': '["Books", "Literature & Fiction", "Genre Fiction"]'}, {'book_id': 'bookid_99', 'title': 'Buddy the Soldier Bear', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_101', 'title': 'Knowing When To Die: Uncollected Stories', 'categories': '["Books", "Literature & Fiction", "Genre Fiction"]'}, {'book_id': 'bookid_106', 'title': 'Looking for Peyton Place: A Novel', 'categories': '["Books", "Literature & Fiction", "Contemporary"]'}, {'book_id': 'bookid_109', 'title': 'All the Way to the Gallows', 'categories': '["Books", "Literature & Fiction", "Short Stories & Anthologies"]'}, {'book_id': 'bookid_111', 'title': 'Can You Buy Me The Wind?', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_122', 'title': 'Childe Harold of Dysna', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]'}, {'book_id': 'bookid_137', 'title': 'Oligarchy', 'categories': '["Books", "Literature & Fiction", "Genre Fiction"]'}, {'book_id': 'bookid_142', 'title': 'The Jordan Tracks', 'categories': '["Books", "Literature & Fiction", "Contemporary"]'}, {'book_id': 'bookid_144', 'title': 'Forged in Blood (Freehold)', 'categories': '["Books", "Literature & Fiction", "Short Stories & Anthologies"]'}, {'book_id': 'bookid_161', 'title': "Time's Demon: BOOK II OF THE ISLEVALE CYCLE", 'categories': '["Books", "Literature & Fiction", "Genre Fiction"]'}, {'book_id': 'bookid_167', 'title': 'Dead Silence', 'categories': '["Books", "Christian Books & Bibles", "Literature & Fiction"]'}, {'book_id': 'bookid_171', 'title': 'Exits, Desires, & Slow Fires', 'categories': '["Books", "Literature & Fiction", "Poetry"]'}, {'book_id': 'bookid_177', 'title': 'Kennebago Moments', 'categories': '["Books", "Literature & Fiction", "Poetry"]'}, {'book_id': 'bookid_179', 'title': 'A Cherry Cola Christmas (A Cherry Cola Book Club Novel)', 'categories': '["Books", "Literature & Fiction", "Genre Fiction"]'}, {'book_id': 'bookid_180', 'title': 'The Sludge', 'categories': '["Books", "Literature & Fiction", "Genre Fiction"]'}, {'book_id': 'bookid_182', 'title': 'Liza of Lambeth', 'categories': '["Books", "Literature & Fiction", "Classics"]'}, {'book_id': 'bookid_187', 'title': 'Consort (A Dark(ish) Faerie Tale Book 3)', 'categories': '["Books", "Literature & Fiction", "Genre Fiction"]'}, {'book_id': 'bookid_188', 'title': "The Vampyre and Other Tales of the Macabre (Oxford World's Classics)", 'categories': '["Books", "Literature & Fiction", "Genre Fiction"]'}, {'book_id': 'bookid_195', 'title': 'Something That Feels Like Truth (Switchgrass Books)', 'categories': '["Books", "Literature & Fiction", "Short Stories & Anthologies"]'}], 'var_functions.execute_python:48': []}

exec(code, env_args)
