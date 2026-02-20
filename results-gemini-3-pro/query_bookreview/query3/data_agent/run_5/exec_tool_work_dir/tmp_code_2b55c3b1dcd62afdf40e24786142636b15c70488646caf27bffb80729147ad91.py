code = """import json
import pandas as pd

# Load book data
books_data = locals()['var_function-call-1609308388430053231']
# Load review data from file
with open(locals()['var_function-call-4919421442614798599'], 'r') as f:
    reviews_data = json.load(f)

# Create DataFrame for books
df_books = pd.DataFrame(books_data)
# Extract numeric ID
df_books['id_num'] = df_books['book_id'].apply(lambda x: x.split('_')[1] if '_' in x else x)

# Create DataFrame for reviews
df_reviews = pd.DataFrame(reviews_data)
# Extract numeric ID
df_reviews['id_num'] = df_reviews['purchase_id'].apply(lambda x: x.split('_')[1] if '_' in x else x)
df_reviews['rating'] = df_reviews['rating'].astype(float)

# Aggregate reviews
review_stats = df_reviews.groupby('id_num')['rating'].mean().reset_index()
review_stats.rename(columns={'rating': 'avg_rating'}, inplace=True)

# Merge
merged = pd.merge(df_books, review_stats, on='id_num', how='inner')

# Filter for avg rating >= 4.5
result_df = merged[merged['avg_rating'] >= 4.5]

# Get titles
titles = result_df['title'].tolist()

print("__RESULT__:")
print(json.dumps(titles))"""

env_args = {'var_function-call-7233486359747502788': [{'book_id': 'bookid_1', 'title': 'Chaucer', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]'}, {'book_id': 'bookid_2', 'title': 'Notes from a Kidwatcher', 'categories': '["Books", "Reference", "Words, Language & Grammar"]'}, {'book_id': 'bookid_3', 'title': 'Service: A Navy SEAL at War', 'categories': '["Books", "Biographies & Memoirs", "Leaders & Notable People"]'}, {'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_5', 'title': 'Parker & Knight', 'categories': '["Books", "Mystery, Thriller & Suspense", "Thrillers & Suspense"]'}], 'var_function-call-7233486359747505299': [{'purchase_id': 'purchaseid_186', 'rating': '4', 'review_time': '2012-11-24 18:52:00'}, {'purchase_id': 'purchaseid_191', 'rating': '4', 'review_time': '2015-12-31 13:35:00'}, {'purchase_id': 'purchaseid_190', 'rating': '4', 'review_time': '2013-05-05 10:47:00'}, {'purchase_id': 'purchaseid_8', 'rating': '5', 'review_time': '2020-08-12 11:06:00'}, {'purchase_id': 'purchaseid_178', 'rating': '4', 'review_time': '2014-11-13 18:55:00'}], 'var_function-call-1609308388430053231': [{'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_32', 'title': 'The Very Hungry Caterpillar (English and Arabic Edition)', 'categories': '["Books", "Children\'s Books", "Early Learning"]'}, {'book_id': 'bookid_40', 'title': 'Egypt (Enchantment of the World)', 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_48', 'title': 'Clark the Shark: Tooth Trouble, No. 1', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_52', 'title': "I Hadn't Meant to Tell You This", 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_54', 'title': 'Favorite Thorton W. Burgess Stories: 6 Books', 'categories': '["Books", "Children\'s Books", "Animals"]'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_57', 'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_96', 'title': 'Cheer Up, Ben Franklin! (Young Historians)', 'categories': '["Books", "Children\'s Books", "History"]'}, {'book_id': 'bookid_99', 'title': 'Buddy the Soldier Bear', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_108', 'title': 'The Library Book', 'categories': '["Books", "Children\'s Books", "Education & Reference"]'}, {'book_id': 'bookid_111', 'title': 'Can You Buy Me The Wind?', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_116', 'title': 'From the Earth to the Moon by Jules Verne, Fiction, Fantasy & Magic', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_120', 'title': "Caroline's Color Dreams: Los Sueños Coloridos De Carolina : Babl Children's Books in Spanish and English", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_124', 'title': 'Skeleton Play: A Fun, Rhyming Halloween Book for Kids! (1)', 'categories': '["Books", "Children\'s Books", "Holidays & Celebrations"]'}, {'book_id': 'bookid_130', 'title': "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_132', 'title': 'Mae and Jane in the Rain', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_145', 'title': 'Kirsten: An American Girl : 1854 (The American Girls Collection/Boxed Set)', 'categories': '["Books", "Boxed Sets", "Children\'s Books"]'}, {'book_id': 'bookid_146', 'title': 'LunaLu the Llamacorn', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_149', 'title': 'Trouble in the CTC!: The Terra Prime Adventures Book 2', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_152', 'title': 'Around the World Mazes', 'categories': '["Books", "Children\'s Books", "Activities, Crafts & Games"]'}, {'book_id': 'bookid_158', 'title': 'Cleo Porter and the Body Electric', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_163', 'title': 'Monster Kisses', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_170', 'title': 'Pokémon: Sun & Moon, Vol. 8 (8)', 'categories': '["Books", "Children\'s Books", "Comics & Graphic Novels"]'}], 'var_function-call-4919421442614798599': 'file_storage/function-call-4919421442614798599.json'}

exec(code, env_args)
