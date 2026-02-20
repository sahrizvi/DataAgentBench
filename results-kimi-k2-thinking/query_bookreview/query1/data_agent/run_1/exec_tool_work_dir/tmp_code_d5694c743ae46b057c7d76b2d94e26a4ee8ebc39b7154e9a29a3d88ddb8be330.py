code = """import json, pandas as pd, re

# Load the books data (with year extracted) from query result
books_path = locals().get('var_functions.query_db:70')
if isinstance(books_path, str) and books_path.endswith('.json'):
    with open(books_path) as f:
        books = json.load(f)
else:
    books = books_path

# Load the reviews data
reviews_path = locals().get('var_functions.query_db:72')
if isinstance(reviews_path, str) and reviews_path.endswith('.json'):
    with open(reviews_path) as f:
        reviews = json.load(f)
else:
    reviews = reviews_path

print('Books with year extracted count:', len(books))
print('Reviews count:', len(reviews))

# Build books DataFrame with numeric ID and year and decade (as int)
books_df = []
for b in books:
    # num_id is already extracted as string e.g. "1"
    num_id = int(b.get('num_id')) if b.get('num_id') else None
    # year_str is e.g. "2004"
    year_str = b.get('year_str')
    year = int(year_str) if year_str else None
    decade = (year // 10) * 10 if year else None
    books_df.append({'book_id_full': b.get('book_id'), 'num_id': num_id, 'year': year, 'decade': decade})

books_df = pd.DataFrame(books_df)
# Ensure no missing values
books_df = books_df.dropna(subset=['num_id','year']).astype({'num_id':'int','year':'int'})
print('Books DataFrame rows after cleaning:', len(books_df))

# Build reviews DataFrame: extract numeric id from purchase_id and rating as float
reviews_df = []
for r in reviews:
    purchase_id = r.get('purchase_id')
    # Extract numeric ID after underscore
    m = re.search(r'_([0-9]+)$', purchase_id)
    if m:
        num_id = int(m.group(1))
        rating = float(r.get('rating'))
        reviews_df.append({'num_id': num_id, 'rating': rating})

reviews_df = pd.DataFrame(reviews_df)
print('Reviews DataFrame rows after cleaning:', len(reviews_df))

# Merge reviews and books on numeric ID
merged = pd.merge(reviews_df, books_df, on='num_id', how='inner')
print('Merged rows (review+book):', len(merged))

# Compute per-decade stats: distinct book count, average rating, total reviews count
# Group by decade
per_decade = merged.groupby('decade').agg(
    book_count=('book_id_full','nunique'),
    avg_rating=('rating','mean'),
    total_reviews=('rating','count')
).reset_index()

# Filter decades with at least 10 distinct books
decade_qualified = per_decade[per_decade['book_count'] >= 10]
print('Qualified decades (>=10 distinct books):', len(decade_qualified))
print(decade_qualified)

# Determine decade with highest average rating
if not decade_qualified.empty:
    best_idx = decade_qualified['avg_rating'].idxmax()
    best = decade_qualified.loc[best_idx]
    result = {
        'decade_str': f"{int(best['decade'])}s",
        'avg_rating': round(best['avg_rating'], 2),
        'book_count': int(best['book_count']),
        'total_reviews': int(best['total_reviews'])
    }
else:
    result = {'decade_str': None, 'avg_rating': None}

print('Best decade result:', result)
print('__RESULT__:')
print(json.dumps(result))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review'], 'var_functions.query_db:6': [{'rating': '4', 'title': 'Ha! On me!  I thought this was a cookbook!', 'text': 'Lucky for me it\'s more than a cookbook.<br /><br />The story of a modern Daniel Boone, growing up in Michigan, one of three sons of a hunter.  Beginning at age eight when he shot a squirrel, to age 13 his first deer, then hunting his way through college, a career as a fur trapper, hunting sheep in Alaska, canoeing the Missouri River for deer and ending in Brooklyn age 37. Brooklyn?<br /><br />I especially liked that I share his disgust at catch & release fishing - if you fish it, you have to eat it - anything else is sadism (my words).<br /><br />My brother in law is the cook in the family and I wanted to see if this would be a good gift for him and I struck pay dirt following each chapter are "Tasting Notes" where the author speaks of cooking wild game.<br /><br />I also enjoyed it for the history of the land he has hunted as well as the history of the hunt (I too was a big Daniel Boone fan growing up!).<br /><br />I think more pictures (everything but dead things) would have made this a keeper.', 'review_time': '2012-11-24 18:52:00', 'helpful_vote': '0', 'verified_purchase': '0', 'purchase_id': 'purchaseid_186'}, {'rating': '4', 'title': 'Four Stars', 'text': 'Not as developed as Stephanie but I like the characters so far.', 'review_time': '2015-12-31 13:35:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_191'}, {'rating': '4', 'title': 'A wonderful adventure in France', 'text': "I loved this book all the way until the end. I have recently discovered that the author is intending to release another book, and from what I understand it will continue where this one left off. I am thankful for this, as the way this book ended was definitely a negative for me. I wanted to know more! What happened to the author, did she learn what she came to learn? Did she get the job she was hoping for? So many questions.<br /><br />From the beginning of Linda's book, it is easy to love her. She is open, honest and definitely has the type of personality you want your heroine to have, whether the book is fiction or reality. I couldn't help but root for Linda throughout her trials with her host family, even when I thought she acted as a bit of a brat herself. Listening to her internal thoughts about what she went through and her desire to achieve her goals made this book feel close to my heart.<br /><br />I applaud the adventurous spirit of the author and her decision to keep journal entries from that chapter of her life. What great material to have later to inspire a book! While I enjoyed the entire memoir, my favourite part of this book would have to be the author's descriptions of the many places she visited and the people she met along the way. While I think she could definitely have made a better impression on the family she worked for if she had been honest about her lack of French language skills from the beginning, she is a pioneer. Her drive and desire to learn the language from those in the actual country was inspiring. Not many people would have been gutsy enough to do what Linda did.<br /><br />I also particularly enjoyed the relationship between Linda and Antoine. The Kind heart of the author was apparent in her actions toward the children, even when she struggled with them.<br /><br />There is some romance, and I appreciated the way the author handled it. While sex scenes are not necessarily automatically offensive, there is something about memoirs that makes me uncomfortable if they are filled with them. This author manages to hint at her experiences without going into too much detail, leaving the reader to decide exactly what happened. Great writing.<br /><br />When you step into reading this book, you learn a lot about French customs, French cuisine and wine. You also get the opportunity to brush up on your French skills a bit and get to step outside yourself and live an adventure through the eyes of the author. I read this book in one sitting with very few breaks in between and found myself enthralled in the sights, sounds and atmosphere of this memoir.<br /><br />In the end, I was disappointed that the book ended. I could have kept reading about Linda's experiences without stopping anytime in the foreseeable future. The end of the book leaves many unanswered questions, that I am assuming the author will be answering in her next book. Were this a standalone, I would be very disappointed with the way the book ended, but with the knowledge that she is writing another book to continue with her story, I can't fault this one. One thing is for sure, if you read this book, you will be anxiously awaiting the next.<br /><br />I would recommend this to anyone who likes books about travel, memoirs or just a good story that came from the recollections and heart of the author. Read it, you will be glad you did. Overall, this was a VERY enjoyable read that gave me many reasons to wish I could drop everything and head off to France!", 'review_time': '2013-05-05 10:47:00', 'helpful_vote': '1', 'verified_purchase': '0', 'purchase_id': 'purchaseid_190'}, {'rating': '5', 'title': 'Best beginner book.  Been looking for something like this for a long time.', 'text': "Looked online for years for something like this.  It's the best I've seen.", 'review_time': '2020-08-12 11:06:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_8'}, {'rating': '4', 'title': 'Referance Guide', 'text': 'Good reference guide for the basics', 'review_time': '2014-11-13 18:55:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_178'}], 'var_functions.query_db:8': 'file_storage/functions.query_db:8.json', 'var_functions.execute_python:16': {'reviews_count': 5, 'books_count': 200}, 'var_functions.execute_python:18': {'decade_str': None, 'avg_rating': None, 'book_count': 0}, 'var_functions.execute_python:22': {'decade': None, 'avg_rating': None, 'book_count': 0, 'total_reviews': 0}, 'var_functions.query_db:24': 'file_storage/functions.query_db:24.json', 'var_functions.query_db:26': [{'count': '200'}], 'var_functions.query_db:28': [{'total_reviews': '1833'}], 'var_functions.execute_python:30': {'decade': None, 'avg_rating': None, 'book_count': 0, 'total_reviews': 0, 'overlap': 200}, 'var_functions.execute_python:32': {'samples': [{'bid': 'bookid_1', 'details_sample': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of', 'years_found': [], 'year_from_date': 2004}, {'bid': 'bookid_2', 'details_sample': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN', 'years_found': [], 'year_from_date': 1996}, {'bid': 'bookid_3', 'details_sample': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363', 'years_found': [], 'year_from_date': 2012}, {'bid': 'bookid_4', 'details_sample': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575', 'years_found': [], 'year_from_date': 2013}, {'bid': 'bookid_5', 'details_sample': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it s', 'years_found': [], 'year_from_date': 2014}]}, 'var_functions.execute_python:34': {'book_sample': ['bookid_1', 'bookid_2', 'bookid_3', 'bookid_4', 'bookid_5', 'bookid_6', 'bookid_7', 'bookid_8', 'bookid_9', 'bookid_10'], 'purchase_sample': ['purchaseid_186', 'purchaseid_191', 'purchaseid_190', 'purchaseid_8', 'purchaseid_178', 'purchaseid_186', 'purchaseid_76', 'purchaseid_186', 'purchaseid_115', 'purchaseid_167'], 'common_all_size': 200, 'common_all_first_10': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}, 'var_functions.execute_python:36': {'decade': None, 'avg_rating': None, 'book_count': 0, 'total_reviews': 0}, 'var_functions.execute_python:38': {'books_with_year': 0, 'reviews_total': 200, 'common_total': 0, 'common_sample': []}, 'var_functions.execute_python:40': {'total_samples': 30, 'successes': 0}, 'var_functions.execute_python:42': {'done': True}, 'var_functions.execute_python:44': {'status': 'done'}, 'var_functions.execute_python:46': {'done': True}, 'var_functions.execute_python:50': {'success_count': 0, 'samples': []}, 'var_functions.execute_python:58': {'decade': None, 'avg_rating': None}, 'var_functions.query_db:64': [{'book_id': 'bookid_1', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'rating_number': '29'}, {'book_id': 'bookid_2', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.', 'rating_number': '1'}, {'book_id': 'bookid_3', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.', 'rating_number': '3421'}, {'book_id': 'bookid_4', 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575. The reading age is suitable for children between 7 and 10 years old, and it corresponds to a Lexile measure of 590L. The book is appropriate for students in grades 2 through 5. Weighing 1.92 ounces, its dimensions are 5.25 x 0.2 x 7.5 inches.', 'rating_number': '40'}, {'book_id': 'bookid_5', 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it supports screen readers, enhancing accessibility for readers. Enhanced typesetting is also enabled, while the X-Ray feature is not available. Word Wise is enabled to assist with comprehension, and sticky notes can be used on Kindle Scribe. The print length of the book is 233 pages.', 'rating_number': '381'}], 'var_functions.query_db:70': 'file_storage/functions.query_db:70.json', 'var_functions.query_db:72': 'file_storage/functions.query_db:72.json'}

exec(code, env_args)
