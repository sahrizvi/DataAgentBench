code = """import json
import pandas as pd

# Load the data
children_books = json.loads(json.dumps(var_functions.query_db__8))
reviews_file_path = var_functions.query_db__14

print("Step 1: Data loading complete")
print(f"Children's books count: {len(children_books)}")
print(f"Reviews file path: {reviews_file_path}")

# Load reviews from file
with open(reviews_file_path, 'r') as f:
    reviews_2020 = json.load(f)

print(f"Successfully loaded {len(reviews_2020)} reviews from file")

# Create DataFrames
df_books = pd.DataFrame(children_books)
df_reviews = pd.DataFrame(reviews_2020)

# Extract numeric IDs for joining - handle different ID formats
df_reviews['book_id_num'] = df_reviews['purchase_id'].str.extract('(\d+)')
df_books['book_id_num'] = df_books['book_id'].str.extract('(\d+)')

# Merge datasets
merged_df = pd.merge(df_books, df_reviews, on='book_id_num', how='inner')

print(f"Successfully merged {len(merged_df)} records")

# Calculate average rating for each book
df_avg = merged_df.groupby(['book_id_x', 'title'])['rating'].agg(['mean', 'count']).reset_index()
df_avg.columns = ['book_id', 'title', 'avg_rating', 'review_count']

# Filter books with average rating >= 4.5
high_rated_books = df_avg[df_avg['avg_rating'] >= 4.5]

print(f"Found {len(high_rated_books)} books with average rating >= 4.5")

# Sort by avg rating descending, then review count descending
result_df = high_rated_books.sort_values(['avg_rating', 'review_count'], ascending=[False, False])

# Prepare result
result = result_df.head(20).to_dict('records')

print("__RESULT__:")
print(json.dumps(result, indent=2))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': [{'book_id': 'bookid_1', 'title': 'Chaucer', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]'}, {'book_id': 'bookid_2', 'title': 'Notes from a Kidwatcher', 'categories': '["Books", "Reference", "Words, Language & Grammar"]'}, {'book_id': 'bookid_3', 'title': 'Service: A Navy SEAL at War', 'categories': '["Books", "Biographies & Memoirs", "Leaders & Notable People"]'}, {'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_5', 'title': 'Parker & Knight', 'categories': '["Books", "Mystery, Thriller & Suspense", "Thrillers & Suspense"]'}, {'book_id': 'bookid_6', 'title': 'Writings from a Black Woman Living in the Land of the "Free": Strength, Power, Resilience', 'categories': '["Books", "Arts & Photography", "History & Criticism"]'}, {'book_id': 'bookid_7', 'title': "Child Development: A Practitioner's Guide:2nd (Second) edition", 'categories': '["Books", "Parenting & Relationships", "Parenting"]'}, {'book_id': 'bookid_8', 'title': 'Make: Electronics: Learning Through Discovery', 'categories': '["Books", "Engineering & Transportation", "Engineering"]'}, {'book_id': 'bookid_9', 'title': 'Reunion: The Children of Lauderdale Park', 'categories': '["Books", "Literature & Fiction", "Genre Fiction"]'}, {'book_id': 'bookid_10', 'title': 'Four Centuries of American Education', 'categories': '["Books", "Education & Teaching", "Schools & Teaching"]'}], 'var_functions.query_db:8': [{'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_32', 'title': 'The Very Hungry Caterpillar (English and Arabic Edition)', 'categories': '["Books", "Children\'s Books", "Early Learning"]'}, {'book_id': 'bookid_40', 'title': 'Egypt (Enchantment of the World)', 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_48', 'title': 'Clark the Shark: Tooth Trouble, No. 1', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_52', 'title': "I Hadn't Meant to Tell You This", 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_54', 'title': 'Favorite Thorton W. Burgess Stories: 6 Books', 'categories': '["Books", "Children\'s Books", "Animals"]'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_57', 'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_96', 'title': 'Cheer Up, Ben Franklin! (Young Historians)', 'categories': '["Books", "Children\'s Books", "History"]'}, {'book_id': 'bookid_99', 'title': 'Buddy the Soldier Bear', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_108', 'title': 'The Library Book', 'categories': '["Books", "Children\'s Books", "Education & Reference"]'}, {'book_id': 'bookid_111', 'title': 'Can You Buy Me The Wind?', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_116', 'title': 'From the Earth to the Moon by Jules Verne, Fiction, Fantasy & Magic', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_120', 'title': "Caroline's Color Dreams: Los Sueños Coloridos De Carolina : Babl Children's Books in Spanish and English", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_124', 'title': 'Skeleton Play: A Fun, Rhyming Halloween Book for Kids! (1)', 'categories': '["Books", "Children\'s Books", "Holidays & Celebrations"]'}, {'book_id': 'bookid_130', 'title': "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_132', 'title': 'Mae and Jane in the Rain', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_145', 'title': 'Kirsten: An American Girl : 1854 (The American Girls Collection/Boxed Set)', 'categories': '["Books", "Boxed Sets", "Children\'s Books"]'}, {'book_id': 'bookid_146', 'title': 'LunaLu the Llamacorn', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_149', 'title': 'Trouble in the CTC!: The Terra Prime Adventures Book 2', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_152', 'title': 'Around the World Mazes', 'categories': '["Books", "Children\'s Books", "Activities, Crafts & Games"]'}, {'book_id': 'bookid_158', 'title': 'Cleo Porter and the Body Electric', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_163', 'title': 'Monster Kisses', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_170', 'title': 'Pokémon: Sun & Moon, Vol. 8 (8)', 'categories': '["Books", "Children\'s Books", "Comics & Graphic Novels"]'}], 'var_functions.list_db:10': ['review'], 'var_functions.query_db:12': [{'purchase_id': 'purchaseid_186', 'rating': '4', 'review_time': '2012-11-24 18:52:00'}, {'purchase_id': 'purchaseid_191', 'rating': '4', 'review_time': '2015-12-31 13:35:00'}, {'purchase_id': 'purchaseid_190', 'rating': '4', 'review_time': '2013-05-05 10:47:00'}, {'purchase_id': 'purchaseid_8', 'rating': '5', 'review_time': '2020-08-12 11:06:00'}, {'purchase_id': 'purchaseid_178', 'rating': '4', 'review_time': '2014-11-13 18:55:00'}, {'purchase_id': 'purchaseid_186', 'rating': '4', 'review_time': '2013-02-20 16:09:00'}, {'purchase_id': 'purchaseid_76', 'rating': '5', 'review_time': '2020-02-27 05:11:00'}, {'purchase_id': 'purchaseid_186', 'rating': '4', 'review_time': '2013-01-06 07:52:00'}, {'purchase_id': 'purchaseid_115', 'rating': '5', 'review_time': '2019-07-24 13:29:00'}, {'purchase_id': 'purchaseid_167', 'rating': '2', 'review_time': '2020-06-01 07:33:00'}], 'var_functions.query_db:14': 'file_storage/functions.query_db:14.json'}

exec(code, env_args)
