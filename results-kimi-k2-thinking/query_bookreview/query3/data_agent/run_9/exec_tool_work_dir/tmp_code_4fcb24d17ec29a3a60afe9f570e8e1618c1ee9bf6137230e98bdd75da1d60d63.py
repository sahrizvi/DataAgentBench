code = """import json
import pandas as pd
import re

# Load children's books data
children_books_data = var_functions.query_db:12

# Load reviews from 2020 onwards (this is the file path)
reviews_file_path = var_functions.query_db:14

print("Loading reviews from file...")
with open(reviews_file_path, 'r') as f:
    reviews_2020 = json.load(f)

print(f"Number of children's books: {len(children_books_data)}")
print(f"Number of reviews from 2020 onwards: {len(reviews_2020)}")

# Convert to DataFrames
df_books = pd.DataFrame(children_books_data)
df_reviews = pd.DataFrame(reviews_2020)

# Extract numeric IDs for joining
# book_id format: 'bookid_X', purchase_id format: 'purchaseid_X'
def extract_numeric_id(id_str):
    match = re.search(r'\d+$', id_str)
    return int(match.group()) if match else None

df_books['numeric_id'] = df_books['book_id'].apply(extract_numeric_id)
df_reviews['numeric_id'] = df_reviews['purchase_id'].apply(extract_numeric_id)

# Join on numeric_id
merged_df = pd.merge(df_books, df_reviews, on='numeric_id', how='inner')

# Calculate average rating per book (book_id from books)
book_ratings = merged_df.groupby('book_id_x').agg({
    'title': 'first',
    'rating': 'mean'
}).reset_index()

book_ratings.columns = ['book_id', 'title', 'avg_rating']

# Filter books with avg rating >= 4.5
highly_rated_books = book_ratings[book_ratings['avg_rating'] >= 4.5]

print(f"Number of highly rated children's books: {len(highly_rated_books)}")
print("\nHighly rated books:")
for _, row in highly_rated_books.iterrows():
    print(f"- {row['title']}: {row['avg_rating']:.2f}")
    
# Prepare result in the required format
result_data = highly_rated_books.to_dict('records')

result_json = json.dumps(result_data, indent=2)

print("__RESULT__:")
print(result_json)"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:5': [{'book_id': 'bookid_1', 'title': 'Chaucer', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]'}, {'book_id': 'bookid_2', 'title': 'Notes from a Kidwatcher', 'categories': '["Books", "Reference", "Words, Language & Grammar"]'}, {'book_id': 'bookid_3', 'title': 'Service: A Navy SEAL at War', 'categories': '["Books", "Biographies & Memoirs", "Leaders & Notable People"]'}, {'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_5', 'title': 'Parker & Knight', 'categories': '["Books", "Mystery, Thriller & Suspense", "Thrillers & Suspense"]'}], 'var_functions.query_db:6': [{'purchase_id': 'purchaseid_186', 'rating': '4', 'review_time': '2012-11-24 18:52:00'}, {'purchase_id': 'purchaseid_191', 'rating': '4', 'review_time': '2015-12-31 13:35:00'}, {'purchase_id': 'purchaseid_190', 'rating': '4', 'review_time': '2013-05-05 10:47:00'}, {'purchase_id': 'purchaseid_8', 'rating': '5', 'review_time': '2020-08-12 11:06:00'}, {'purchase_id': 'purchaseid_178', 'rating': '4', 'review_time': '2014-11-13 18:55:00'}], 'var_functions.query_db:10': [{'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess'}, {'book_id': 'bookid_32', 'title': 'The Very Hungry Caterpillar (English and Arabic Edition)'}, {'book_id': 'bookid_40', 'title': 'Egypt (Enchantment of the World)'}, {'book_id': 'bookid_48', 'title': 'Clark the Shark: Tooth Trouble, No. 1'}, {'book_id': 'bookid_52', 'title': "I Hadn't Meant to Tell You This"}, {'book_id': 'bookid_54', 'title': 'Favorite Thorton W. Burgess Stories: 6 Books'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)'}, {'book_id': 'bookid_57', 'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)"}, {'book_id': 'bookid_96', 'title': 'Cheer Up, Ben Franklin! (Young Historians)'}], 'var_functions.query_db:12': [{'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_32', 'title': 'The Very Hungry Caterpillar (English and Arabic Edition)', 'categories': '["Books", "Children\'s Books", "Early Learning"]'}, {'book_id': 'bookid_40', 'title': 'Egypt (Enchantment of the World)', 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_48', 'title': 'Clark the Shark: Tooth Trouble, No. 1', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_52', 'title': "I Hadn't Meant to Tell You This", 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_54', 'title': 'Favorite Thorton W. Burgess Stories: 6 Books', 'categories': '["Books", "Children\'s Books", "Animals"]'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_57', 'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_96', 'title': 'Cheer Up, Ben Franklin! (Young Historians)', 'categories': '["Books", "Children\'s Books", "History"]'}, {'book_id': 'bookid_99', 'title': 'Buddy the Soldier Bear', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_108', 'title': 'The Library Book', 'categories': '["Books", "Children\'s Books", "Education & Reference"]'}, {'book_id': 'bookid_111', 'title': 'Can You Buy Me The Wind?', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_116', 'title': 'From the Earth to the Moon by Jules Verne, Fiction, Fantasy & Magic', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_120', 'title': "Caroline's Color Dreams: Los Sueños Coloridos De Carolina : Babl Children's Books in Spanish and English", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_124', 'title': 'Skeleton Play: A Fun, Rhyming Halloween Book for Kids! (1)', 'categories': '["Books", "Children\'s Books", "Holidays & Celebrations"]'}, {'book_id': 'bookid_130', 'title': "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_132', 'title': 'Mae and Jane in the Rain', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_145', 'title': 'Kirsten: An American Girl : 1854 (The American Girls Collection/Boxed Set)', 'categories': '["Books", "Boxed Sets", "Children\'s Books"]'}, {'book_id': 'bookid_146', 'title': 'LunaLu the Llamacorn', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_149', 'title': 'Trouble in the CTC!: The Terra Prime Adventures Book 2', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_152', 'title': 'Around the World Mazes', 'categories': '["Books", "Children\'s Books", "Activities, Crafts & Games"]'}, {'book_id': 'bookid_158', 'title': 'Cleo Porter and the Body Electric', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_163', 'title': 'Monster Kisses', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_170', 'title': 'Pokémon: Sun & Moon, Vol. 8 (8)', 'categories': '["Books", "Children\'s Books", "Comics & Graphic Novels"]'}], 'var_functions.query_db:14': 'file_storage/functions.query_db:14.json'}

exec(code, env_args)
