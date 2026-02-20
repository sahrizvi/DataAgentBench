code = """import pandas as pd
import json

books_info_raw = locals()["var_function-call-8389686745309844594"]["results"]
review_raw_file = locals()["var_function-call-17902193751762410625"]

# Read the full review data from the JSON file
with open(review_raw_file, 'r') as f:
    review_data = json.load(f)

df_books = pd.DataFrame(books_info_raw)
df_reviews = pd.DataFrame(review_data)

# Convert rating to numeric, handling potential errors
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

# Convert review_time to datetime
df_reviews['review_time'] = pd.to_datetime(df_reviews['review_time'])

# Filter reviews from 2020 onwards
df_reviews_filtered = df_reviews[df_reviews['review_time'].dt.year >= 2020]

# Merge dataframes
df_merged = pd.merge(df_books, df_reviews_filtered, left_on='book_id', right_on='purchase_id')

# Calculate average rating for each book
average_ratings = df_merged.groupby('title')['rating'].mean().reset_index()

# Filter for books with average rating >= 4.5
high_rated_books = average_ratings[average_ratings['rating'] >= 4.5]

# Get the titles of these books
result_titles = high_rated_books['title'].tolist()

print("__RESULT__:")
print(json.dumps(result_titles))"""

env_args = {'var_function-call-8389686745309844594': [{'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess'}, {'book_id': 'bookid_32', 'title': 'The Very Hungry Caterpillar (English and Arabic Edition)'}, {'book_id': 'bookid_40', 'title': 'Egypt (Enchantment of the World)'}, {'book_id': 'bookid_48', 'title': 'Clark the Shark: Tooth Trouble, No. 1'}, {'book_id': 'bookid_52', 'title': "I Hadn't Meant to Tell You This"}, {'book_id': 'bookid_54', 'title': 'Favorite Thorton W. Burgess Stories: 6 Books'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)'}, {'book_id': 'bookid_57', 'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)"}, {'book_id': 'bookid_96', 'title': 'Cheer Up, Ben Franklin! (Young Historians)'}, {'book_id': 'bookid_99', 'title': 'Buddy the Soldier Bear'}, {'book_id': 'bookid_108', 'title': 'The Library Book'}, {'book_id': 'bookid_111', 'title': 'Can You Buy Me The Wind?'}, {'book_id': 'bookid_116', 'title': 'From the Earth to the Moon by Jules Verne, Fiction, Fantasy & Magic'}, {'book_id': 'bookid_120', 'title': "Caroline's Color Dreams: Los Sueños Coloridos De Carolina : Babl Children's Books in Spanish and English"}, {'book_id': 'bookid_124', 'title': 'Skeleton Play: A Fun, Rhyming Halloween Book for Kids! (1)'}, {'book_id': 'bookid_130', 'title': "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)"}, {'book_id': 'bookid_132', 'title': 'Mae and Jane in the Rain'}, {'book_id': 'bookid_145', 'title': 'Kirsten: An American Girl : 1854 (The American Girls Collection/Boxed Set)'}, {'book_id': 'bookid_146', 'title': 'LunaLu the Llamacorn'}, {'book_id': 'bookid_149', 'title': 'Trouble in the CTC!: The Terra Prime Adventures Book 2'}, {'book_id': 'bookid_152', 'title': 'Around the World Mazes'}, {'book_id': 'bookid_158', 'title': 'Cleo Porter and the Body Electric'}, {'book_id': 'bookid_163', 'title': 'Monster Kisses'}, {'book_id': 'bookid_170', 'title': 'Pokémon: Sun & Moon, Vol. 8 (8)'}], 'var_function-call-17902193751762410625': 'file_storage/function-call-17902193751762410625.json'}

exec(code, env_args)
