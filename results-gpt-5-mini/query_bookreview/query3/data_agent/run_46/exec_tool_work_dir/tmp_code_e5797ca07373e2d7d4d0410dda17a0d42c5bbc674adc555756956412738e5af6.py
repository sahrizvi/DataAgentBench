code = """import pandas as pd
import json
import re
from datetime import datetime

# Load data from storage variables
books = var_call_2XWP1rBamsgMpPI32nnpFlKt
# var_call_6... contains a file path to the full JSON of reviews
reviews_path = var_call_6lP32KgU3mNjKeAFcrMcUUgQ
with open(reviews_path, 'r') as f:
    reviews = json.load(f)

# Create DataFrames
df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Clean and convert types
# Ensure rating is float
if 'rating' in df_reviews.columns:
    df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
# Parse review_time to datetime
if 'review_time' in df_reviews.columns:
    df_reviews['review_time'] = pd.to_datetime(df_reviews['review_time'], errors='coerce')

# Filter reviews from 2020-01-01 onwards
df_reviews_2020 = df_reviews[df_reviews['review_time'] >= pd.Timestamp('2020-01-01')].copy()

# Extract numeric id from book_id and purchase_id to perform fuzzy join
def extract_num(s):
    if pd.isna(s):
        return None
    m = re.search(r"_(\d+)", str(s))
    return int(m.group(1)) if m else None

if 'book_id' in df_books.columns:
    df_books['id_num'] = df_books['book_id'].apply(extract_num)
else:
    df_books['id_num'] = None

if 'purchase_id' in df_reviews_2020.columns:
    df_reviews_2020['id_num'] = df_reviews_2020['purchase_id'].apply(extract_num)
else:
    df_reviews_2020['id_num'] = None

# Drop rows without numeric id
df_books = df_books.dropna(subset=['id_num']).copy()
df_books['id_num'] = df_books['id_num'].astype(int)

df_reviews_2020 = df_reviews_2020.dropna(subset=['id_num','rating']).copy()
df_reviews_2020['id_num'] = df_reviews_2020['id_num'].astype(int)

# Merge reviews with books (only children books present in df_books)
merged = pd.merge(df_reviews_2020, df_books, on='id_num', how='inner', suffixes=('_rev','_book'))

# Compute average rating and count per book
grouped = merged.groupby(['book_id','title']).agg(
    average_rating=('rating','mean'),
    review_count=('rating','count')
).reset_index()

# Filter for average_rating >= 4.5
result_df = grouped[grouped['average_rating'] >= 4.5].copy()

# Format average_rating to 3 decimal places
result_df['average_rating'] = result_df['average_rating'].round(3)

# Prepare output list
results = []
for _, row in result_df.sort_values(['average_rating','review_count'], ascending=[False,False]).iterrows():
    results.append({
        'book_id': row['book_id'],
        'title': row['title'],
        'average_rating': float(row['average_rating']),
        'review_count_2020_onwards': int(row['review_count'])
    })

# Print results in required format as JSON string
print("__RESULT__:")
print(json.dumps(results))"""

env_args = {'var_call_2XWP1rBamsgMpPI32nnpFlKt': [{'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_32', 'title': 'The Very Hungry Caterpillar (English and Arabic Edition)', 'categories': '["Books", "Children\'s Books", "Early Learning"]'}, {'book_id': 'bookid_40', 'title': 'Egypt (Enchantment of the World)', 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_48', 'title': 'Clark the Shark: Tooth Trouble, No. 1', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_52', 'title': "I Hadn't Meant to Tell You This", 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_54', 'title': 'Favorite Thorton W. Burgess Stories: 6 Books', 'categories': '["Books", "Children\'s Books", "Animals"]'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_57', 'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_96', 'title': 'Cheer Up, Ben Franklin! (Young Historians)', 'categories': '["Books", "Children\'s Books", "History"]'}, {'book_id': 'bookid_99', 'title': 'Buddy the Soldier Bear', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_108', 'title': 'The Library Book', 'categories': '["Books", "Children\'s Books", "Education & Reference"]'}, {'book_id': 'bookid_111', 'title': 'Can You Buy Me The Wind?', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_116', 'title': 'From the Earth to the Moon by Jules Verne, Fiction, Fantasy & Magic', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_120', 'title': "Caroline's Color Dreams: Los Sueños Coloridos De Carolina : Babl Children's Books in Spanish and English", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_124', 'title': 'Skeleton Play: A Fun, Rhyming Halloween Book for Kids! (1)', 'categories': '["Books", "Children\'s Books", "Holidays & Celebrations"]'}, {'book_id': 'bookid_130', 'title': "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_132', 'title': 'Mae and Jane in the Rain', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_145', 'title': 'Kirsten: An American Girl : 1854 (The American Girls Collection/Boxed Set)', 'categories': '["Books", "Boxed Sets", "Children\'s Books"]'}, {'book_id': 'bookid_146', 'title': 'LunaLu the Llamacorn', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_149', 'title': 'Trouble in the CTC!: The Terra Prime Adventures Book 2', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_152', 'title': 'Around the World Mazes', 'categories': '["Books", "Children\'s Books", "Activities, Crafts & Games"]'}, {'book_id': 'bookid_158', 'title': 'Cleo Porter and the Body Electric', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_163', 'title': 'Monster Kisses', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_170', 'title': 'Pokémon: Sun & Moon, Vol. 8 (8)', 'categories': '["Books", "Children\'s Books", "Comics & Graphic Novels"]'}], 'var_call_6lP32KgU3mNjKeAFcrMcUUgQ': 'file_storage/call_6lP32KgU3mNjKeAFcrMcUUgQ.json'}

exec(code, env_args)
