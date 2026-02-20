code = """import json
import pandas as pd

# Load data
books_df = pd.read_json('file_storage/functions.query_db:20.json')
reviews_df = pd.read_json('file_storage/functions.query_db:16.json')

# Convert rating to numeric and review_time to datetime
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'])
reviews_df['review_time'] = pd.to_datetime(reviews_df['review_time'])

# Filter reviews from 2020 onwards
reviews_2020_df = reviews_df[reviews_df['review_time'] >= '2020-01-01'].copy()

# Extract numeric IDs
books_df['numeric_id'] = books_df['book_id'].str.extract('(\d+)').astype(int)
reviews_2020_df['numeric_id'] = reviews_2020_df['purchase_id'].str.extract('(\d+)').astype(int)

# Filter for children's books
children_books_df = books_df[books_df['categories'].str.contains("Children's Books", na=False)].copy()

# Merge children books with reviews on numeric_id
merged_df = children_books_df.merge(
    reviews_2020_df,
    on='numeric_id',
    how='inner'
)

# Get column names
print("Merged columns:", merged_df.columns.tolist())

# Group by book_id and title from the original books table
if len(merged_df) > 0:
    grouped = merged_df.groupby(['book_id', 'title']).agg({
        'rating': ['mean', 'count']
    }).round(3)
    
    grouped.columns = ['avg_rating', 'review_count']
    grouped = grouped.reset_index()
    
    # Filter books with average rating >= 4.5
    high_rated_books = grouped[grouped['avg_rating'] >= 4.5].copy()
    high_rated_books = high_rated_books.sort_values('avg_rating', ascending=False)
    
    print(f"Books with avg rating >= 4.5: {len(high_rated_books)}")
    print("High rated books details:")
    for _, row in high_rated_books.iterrows():
        print(f"  {row['title']}: avg={row['avg_rating']}, reviews={row['review_count']}")
    
else:
    print("No merged records found")

# Also check overall merge stats
print(f"Children books: {len(children_books_df)}")
print(f"Reviews 2020+: {len(reviews_2020_df)}")
print(f"Merged: {len(merged_df)}")

result_list = []
if len(merged_df) > 0 and len(high_rated_books) > 0:
    for _, row in high_rated_books.iterrows():
        result_list.append({
            'book_id': row['book_id'],
            'title': row['title'],
            'avg_rating': str(row['avg_rating']),
            'review_count': int(row['review_count'])
        })

print('__RESULT__:')
print(json.dumps(result_list))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review'], 'var_functions.query_db:6': [{'rating': '4', 'title': 'Ha! On me!  I thought this was a cookbook!', 'text': 'Lucky for me it\'s more than a cookbook.<br /><br />The story of a modern Daniel Boone, growing up in Michigan, one of three sons of a hunter.  Beginning at age eight when he shot a squirrel, to age 13 his first deer, then hunting his way through college, a career as a fur trapper, hunting sheep in Alaska, canoeing the Missouri River for deer and ending in Brooklyn age 37. Brooklyn?<br /><br />I especially liked that I share his disgust at catch & release fishing - if you fish it, you have to eat it - anything else is sadism (my words).<br /><br />My brother in law is the cook in the family and I wanted to see if this would be a good gift for him and I struck pay dirt following each chapter are "Tasting Notes" where the author speaks of cooking wild game.<br /><br />I also enjoyed it for the history of the land he has hunted as well as the history of the hunt (I too was a big Daniel Boone fan growing up!).<br /><br />I think more pictures (everything but dead things) would have made this a keeper.', 'review_time': '2012-11-24 18:52:00', 'helpful_vote': '0', 'verified_purchase': '0', 'purchase_id': 'purchaseid_186'}, {'rating': '4', 'title': 'Four Stars', 'text': 'Not as developed as Stephanie but I like the characters so far.', 'review_time': '2015-12-31 13:35:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_191'}, {'rating': '4', 'title': 'A wonderful adventure in France', 'text': "I loved this book all the way until the end. I have recently discovered that the author is intending to release another book, and from what I understand it will continue where this one left off. I am thankful for this, as the way this book ended was definitely a negative for me. I wanted to know more! What happened to the author, did she learn what she came to learn? Did she get the job she was hoping for? So many questions.<br /><br />From the beginning of Linda's book, it is easy to love her. She is open, honest and definitely has the type of personality you want your heroine to have, whether the book is fiction or reality. I couldn't help but root for Linda throughout her trials with her host family, even when I thought she acted as a bit of a brat herself. Listening to her internal thoughts about what she went through and her desire to achieve her goals made this book feel close to my heart.<br /><br />I applaud the adventurous spirit of the author and her decision to keep journal entries from that chapter of her life. What great material to have later to inspire a book! While I enjoyed the entire memoir, my favourite part of this book would have to be the author's descriptions of the many places she visited and the people she met along the way. While I think she could definitely have made a better impression on the family she worked for if she had been honest about her lack of French language skills from the beginning, she is a pioneer. Her drive and desire to learn the language from those in the actual country was inspiring. Not many people would have been gutsy enough to do what Linda did.<br /><br />I also particularly enjoyed the relationship between Linda and Antoine. The Kind heart of the author was apparent in her actions toward the children, even when she struggled with them.<br /><br />There is some romance, and I appreciated the way the author handled it. While sex scenes are not necessarily automatically offensive, there is something about memoirs that makes me uncomfortable if they are filled with them. This author manages to hint at her experiences without going into too much detail, leaving the reader to decide exactly what happened. Great writing.<br /><br />When you step into reading this book, you learn a lot about French customs, French cuisine and wine. You also get the opportunity to brush up on your French skills a bit and get to step outside yourself and live an adventure through the eyes of the author. I read this book in one sitting with very few breaks in between and found myself enthralled in the sights, sounds and atmosphere of this memoir.<br /><br />In the end, I was disappointed that the book ended. I could have kept reading about Linda's experiences without stopping anytime in the foreseeable future. The end of the book leaves many unanswered questions, that I am assuming the author will be answering in her next book. Were this a standalone, I would be very disappointed with the way the book ended, but with the knowledge that she is writing another book to continue with her story, I can't fault this one. One thing is for sure, if you read this book, you will be anxiously awaiting the next.<br /><br />I would recommend this to anyone who likes books about travel, memoirs or just a good story that came from the recollections and heart of the author. Read it, you will be glad you did. Overall, this was a VERY enjoyable read that gave me many reasons to wish I could drop everything and head off to France!", 'review_time': '2013-05-05 10:47:00', 'helpful_vote': '1', 'verified_purchase': '0', 'purchase_id': 'purchaseid_190'}, {'rating': '5', 'title': 'Best beginner book.  Been looking for something like this for a long time.', 'text': "Looked online for years for something like this.  It's the best I've seen.", 'review_time': '2020-08-12 11:06:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_8'}, {'rating': '4', 'title': 'Referance Guide', 'text': 'Good reference guide for the basics', 'review_time': '2014-11-13 18:55:00', 'helpful_vote': '0', 'verified_purchase': '1', 'purchase_id': 'purchaseid_178'}], 'var_functions.query_db:10': 'file_storage/functions.query_db:10.json', 'var_functions.query_db:14': [{'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess'}, {'book_id': 'bookid_32', 'title': 'The Very Hungry Caterpillar (English and Arabic Edition)'}, {'book_id': 'bookid_40', 'title': 'Egypt (Enchantment of the World)'}, {'book_id': 'bookid_48', 'title': 'Clark the Shark: Tooth Trouble, No. 1'}, {'book_id': 'bookid_52', 'title': "I Hadn't Meant to Tell You This"}, {'book_id': 'bookid_54', 'title': 'Favorite Thorton W. Burgess Stories: 6 Books'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)'}, {'book_id': 'bookid_57', 'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)"}, {'book_id': 'bookid_96', 'title': 'Cheer Up, Ben Franklin! (Young Historians)'}, {'book_id': 'bookid_99', 'title': 'Buddy the Soldier Bear'}, {'book_id': 'bookid_108', 'title': 'The Library Book'}, {'book_id': 'bookid_111', 'title': 'Can You Buy Me The Wind?'}, {'book_id': 'bookid_116', 'title': 'From the Earth to the Moon by Jules Verne, Fiction, Fantasy & Magic'}, {'book_id': 'bookid_120', 'title': "Caroline's Color Dreams: Los Sueños Coloridos De Carolina : Babl Children's Books in Spanish and English"}, {'book_id': 'bookid_124', 'title': 'Skeleton Play: A Fun, Rhyming Halloween Book for Kids! (1)'}, {'book_id': 'bookid_130', 'title': "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)"}, {'book_id': 'bookid_132', 'title': 'Mae and Jane in the Rain'}, {'book_id': 'bookid_145', 'title': 'Kirsten: An American Girl : 1854 (The American Girls Collection/Boxed Set)'}, {'book_id': 'bookid_146', 'title': 'LunaLu the Llamacorn'}, {'book_id': 'bookid_149', 'title': 'Trouble in the CTC!: The Terra Prime Adventures Book 2'}, {'book_id': 'bookid_152', 'title': 'Around the World Mazes'}, {'book_id': 'bookid_158', 'title': 'Cleo Porter and the Body Electric'}, {'book_id': 'bookid_163', 'title': 'Monster Kisses'}, {'book_id': 'bookid_170', 'title': 'Pokémon: Sun & Moon, Vol. 8 (8)'}], 'var_functions.query_db:16': 'file_storage/functions.query_db:16.json', 'var_functions.query_db:20': 'file_storage/functions.query_db:20.json', 'var_functions.execute_python:30': {'books_path': 'file_storage/functions.query_db:20.json', 'reviews_path': 'file_storage/functions.query_db:16.json'}, 'var_functions.execute_python:34': [], 'var_functions.execute_python:36': {'count': 25, 'sample_titles': ['Monstrous Stories #4: The Day the Mice Stood Still', 'The Old Man and the Pirate Princess', 'The Very Hungry Caterpillar (English and Arabic Edition)', 'Egypt (Enchantment of the World)', 'Clark the Shark: Tooth Trouble, No. 1']}, 'var_functions.execute_python:40': {'total_books': 200, 'total_reviews': 329, 'children_books': 25, 'sample_book_ids': ['bookid_1', 'bookid_2', 'bookid_3'], 'sample_purchase_ids': ['purchaseid_8', 'purchaseid_76', 'purchaseid_167']}, 'var_functions.execute_python:42': {'books_with_numeric_id': 200, 'reviews_with_numeric_id': 329, 'overlapping_ids': 80, 'children_books_count': 25}}

exec(code, env_args)
