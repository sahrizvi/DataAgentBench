code = """import json
import pandas as pd

# Load books query result (small list of records)
books = var_call_3SzLxJ3if5wqsoi4NYa1rUFt

# Load reviews full result from file path provided
review_file_path = var_call_shaW6JdKEXETUtE8eRK0wSL2
with open(review_file_path, 'r') as f:
    reviews = json.load(f)

# Create DataFrames
df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Normalize review ratings and times
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
df_reviews['review_time'] = pd.to_datetime(df_reviews['review_time'], errors='coerce')

# Ensure reviews are from 2020-01-01 onwards
df_reviews = df_reviews[df_reviews['review_time'] >= pd.to_datetime('2020-01-01')]

# Compute average rating and count per purchase_id
grp = df_reviews.groupby('purchase_id')['rating'].agg(['mean','count']).reset_index().rename(columns={'mean':'avg_rating','count':'review_count'})

# Map purchase_id to book_id by replacing prefix
grp['book_id'] = grp['purchase_id'].str.replace('purchaseid_','bookid_')

# Identify children's books in df_books (categories stored as string)
# Use a case-insensitive check for the word "Children"
df_books['is_children'] = df_books['categories'].str.contains('Children', case=False, na=False)

# Merge on book_id
merged = pd.merge(grp, df_books, on='book_id', how='left')

# Filter for children's books with avg_rating >= 4.5
filtered = merged[(merged['is_children']==True) & (merged['avg_rating'] >= 4.5)]

# Prepare result list
result = []
for _, row in filtered.sort_values(['avg_rating','review_count'], ascending=[False, False]).iterrows():
    result.append({
        'book_id': row['book_id'],
        'title': row.get('title'),
        'avg_rating': round(float(row['avg_rating']), 3),
        'review_count': int(row['review_count'])
    })

# Print result in required format
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_3SzLxJ3if5wqsoi4NYa1rUFt': [{'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_32', 'title': 'The Very Hungry Caterpillar (English and Arabic Edition)', 'categories': '["Books", "Children\'s Books", "Early Learning"]'}, {'book_id': 'bookid_40', 'title': 'Egypt (Enchantment of the World)', 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_48', 'title': 'Clark the Shark: Tooth Trouble, No. 1', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_52', 'title': "I Hadn't Meant to Tell You This", 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_54', 'title': 'Favorite Thorton W. Burgess Stories: 6 Books', 'categories': '["Books", "Children\'s Books", "Animals"]'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_57', 'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_96', 'title': 'Cheer Up, Ben Franklin! (Young Historians)', 'categories': '["Books", "Children\'s Books", "History"]'}, {'book_id': 'bookid_99', 'title': 'Buddy the Soldier Bear', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_108', 'title': 'The Library Book', 'categories': '["Books", "Children\'s Books", "Education & Reference"]'}, {'book_id': 'bookid_111', 'title': 'Can You Buy Me The Wind?', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_116', 'title': 'From the Earth to the Moon by Jules Verne, Fiction, Fantasy & Magic', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_120', 'title': "Caroline's Color Dreams: Los Sueños Coloridos De Carolina : Babl Children's Books in Spanish and English", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_124', 'title': 'Skeleton Play: A Fun, Rhyming Halloween Book for Kids! (1)', 'categories': '["Books", "Children\'s Books", "Holidays & Celebrations"]'}, {'book_id': 'bookid_130', 'title': "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_132', 'title': 'Mae and Jane in the Rain', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_145', 'title': 'Kirsten: An American Girl : 1854 (The American Girls Collection/Boxed Set)', 'categories': '["Books", "Boxed Sets", "Children\'s Books"]'}, {'book_id': 'bookid_146', 'title': 'LunaLu the Llamacorn', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_149', 'title': 'Trouble in the CTC!: The Terra Prime Adventures Book 2', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_152', 'title': 'Around the World Mazes', 'categories': '["Books", "Children\'s Books", "Activities, Crafts & Games"]'}, {'book_id': 'bookid_158', 'title': 'Cleo Porter and the Body Electric', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_163', 'title': 'Monster Kisses', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_170', 'title': 'Pokémon: Sun & Moon, Vol. 8 (8)', 'categories': '["Books", "Children\'s Books", "Comics & Graphic Novels"]'}], 'var_call_shaW6JdKEXETUtE8eRK0wSL2': 'file_storage/call_shaW6JdKEXETUtE8eRK0wSL2.json'}

exec(code, env_args)
