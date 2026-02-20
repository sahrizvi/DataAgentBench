code = """import json
import pandas as pd

# Get children's books from storage
storage_key_books = 'var_functions.query_db:7'
books_list = locals()[storage_key_books]
df_books = pd.DataFrame(books_list)

# Get reviews file path from storage
storage_key_reviews = 'var_functions.query_db:8'
review_file_path = locals()[storage_key_reviews]

# Read the reviews from file
with open(review_file_path, 'r') as f:
    reviews_data = json.load(f)

df_reviews = pd.DataFrame(reviews_data)

# Extract book_id number from book_id (e.g., 'bookid_4' -> '4')
df_books['book_num'] = df_books['book_id'].str.extract('bookid_(\\d+)')

# Extract the same from purchase_id (e.g., 'purchaseid_4' -> '4')
df_reviews['book_num'] = df_reviews['purchase_id'].str.extract('purchaseid_(\\d+)')

# Merge on extracted book number
df_merged = pd.merge(df_books, df_reviews, on='book_num', how='inner')

# Group by book and calculate average rating
result = df_merged.groupby(['book_id', 'title']).agg({
    'rating': ['mean', 'count']
}).reset_index()

result.columns = ['book_id', 'title', 'avg_rating', 'review_count']

# Filter books with average rating >= 4.5
filtered_books = result[result['avg_rating'] >= 4.5]

# Sort by average rating descending
filtered_books = filtered_books.sort_values('avg_rating', ascending=False)

# Convert to JSON for output
result_json = filtered_books.to_json(orient='records')

print('__RESULT__:')
print(result_json)"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:7': [{'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'book_id': 'bookid_4', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'title': 'The Old Man and the Pirate Princess', 'book_id': 'bookid_14', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'title': 'The Very Hungry Caterpillar (English and Arabic Edition)', 'book_id': 'bookid_32', 'categories': '["Books", "Children\'s Books", "Early Learning"]'}, {'title': 'Egypt (Enchantment of the World)', 'book_id': 'bookid_40', 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'title': 'Clark the Shark: Tooth Trouble, No. 1', 'book_id': 'bookid_48', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'title': "I Hadn't Meant to Tell You This", 'book_id': 'bookid_52', 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'title': 'Favorite Thorton W. Burgess Stories: 6 Books', 'book_id': 'bookid_54', 'categories': '["Books", "Children\'s Books", "Animals"]'}, {'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)', 'book_id': 'bookid_55', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)", 'book_id': 'bookid_57', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'title': 'Cheer Up, Ben Franklin! (Young Historians)', 'book_id': 'bookid_96', 'categories': '["Books", "Children\'s Books", "History"]'}, {'title': 'Buddy the Soldier Bear', 'book_id': 'bookid_99', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'title': 'The Library Book', 'book_id': 'bookid_108', 'categories': '["Books", "Children\'s Books", "Education & Reference"]'}, {'title': 'Can You Buy Me The Wind?', 'book_id': 'bookid_111', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'title': 'From the Earth to the Moon by Jules Verne, Fiction, Fantasy & Magic', 'book_id': 'bookid_116', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'title': "Caroline's Color Dreams: Los Sueños Coloridos De Carolina : Babl Children's Books in Spanish and English", 'book_id': 'bookid_120', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'title': 'Skeleton Play: A Fun, Rhyming Halloween Book for Kids! (1)', 'book_id': 'bookid_124', 'categories': '["Books", "Children\'s Books", "Holidays & Celebrations"]'}, {'title': "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)", 'book_id': 'bookid_130', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'title': 'Mae and Jane in the Rain', 'book_id': 'bookid_132', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'title': 'Kirsten: An American Girl : 1854 (The American Girls Collection/Boxed Set)', 'book_id': 'bookid_145', 'categories': '["Books", "Boxed Sets", "Children\'s Books"]'}, {'title': 'LunaLu the Llamacorn', 'book_id': 'bookid_146', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'title': 'Trouble in the CTC!: The Terra Prime Adventures Book 2', 'book_id': 'bookid_149', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'title': 'Around the World Mazes', 'book_id': 'bookid_152', 'categories': '["Books", "Children\'s Books", "Activities, Crafts & Games"]'}, {'title': 'Cleo Porter and the Body Electric', 'book_id': 'bookid_158', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'title': 'Monster Kisses', 'book_id': 'bookid_163', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'title': 'Pokémon: Sun & Moon, Vol. 8 (8)', 'book_id': 'bookid_170', 'categories': '["Books", "Children\'s Books", "Comics & Graphic Novels"]'}], 'var_functions.query_db:8': 'file_storage/functions.query_db:8.json'}

exec(code, env_args)
