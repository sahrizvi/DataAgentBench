code = """import json
import pandas as pd
import re

# Data from previous tool calls
books = var_call_HGhKzkjoKNH13XoQo7jYen6B
reviews_filepath = var_call_6LJgjG5ta6yGfRB1t6hw8Qpa

# Load full reviews JSON from file
with open(reviews_filepath, 'r') as f:
    reviews = json.load(f)

# Create DataFrame
df = pd.DataFrame(reviews)
# Ensure proper types
if 'rating' in df.columns:
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
if 'review_time' in df.columns:
    df['review_time'] = pd.to_datetime(df['review_time'], errors='coerce')

# Filter reviews from 2020 onwards
df = df[df['review_time'] >= pd.Timestamp('2020-01-01')]

# Extract numeric id suffix from purchase_id
def extract_num(s):
    if not isinstance(s, str):
        return None
    m = re.search(r'(\d+)$', s)
    return int(m.group(1)) if m else None

if 'purchase_id' in df.columns:
    df['pid_num'] = df['purchase_id'].apply(extract_num)
else:
    df['pid_num'] = None

# Build mapping from numeric id to ratings
grouped = df.groupby('pid_num')['rating'].agg(['mean','count']).reset_index()
pid_map = {int(row['pid_num']): {'avg': float(row['mean']), 'n': int(row['count'])} for _, row in grouped.iterrows() if pd.notna(row['pid_num'])}

# Process books, extract book numeric id and join
results = []
for b in books:
    bid = b.get('book_id')
    title = b.get('title')
    num = extract_num(bid)
    if num is None:
        continue
    info = pid_map.get(num)
    if info and info['avg'] >= 4.5:
        results.append({'book_id': bid, 'title': title, 'avg_rating': round(info['avg'], 3), 'n_reviews': info['n']})

# Sort by avg_rating desc, then n_reviews desc
results.sort(key=lambda x: (-x['avg_rating'], -x['n_reviews'], x['title']))

out = json.dumps(results)
print("__RESULT__:")
print(out)"""

env_args = {'var_call_YtiQX40UIrEnlDOJT0uf6L9n': ['books_info'], 'var_call_HGhKzkjoKNH13XoQo7jYen6B': [{'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_32', 'title': 'The Very Hungry Caterpillar (English and Arabic Edition)', 'categories': '["Books", "Children\'s Books", "Early Learning"]'}, {'book_id': 'bookid_40', 'title': 'Egypt (Enchantment of the World)', 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_48', 'title': 'Clark the Shark: Tooth Trouble, No. 1', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_52', 'title': "I Hadn't Meant to Tell You This", 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_54', 'title': 'Favorite Thorton W. Burgess Stories: 6 Books', 'categories': '["Books", "Children\'s Books", "Animals"]'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_57', 'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_96', 'title': 'Cheer Up, Ben Franklin! (Young Historians)', 'categories': '["Books", "Children\'s Books", "History"]'}, {'book_id': 'bookid_99', 'title': 'Buddy the Soldier Bear', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_108', 'title': 'The Library Book', 'categories': '["Books", "Children\'s Books", "Education & Reference"]'}, {'book_id': 'bookid_111', 'title': 'Can You Buy Me The Wind?', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_116', 'title': 'From the Earth to the Moon by Jules Verne, Fiction, Fantasy & Magic', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_120', 'title': "Caroline's Color Dreams: Los Sueños Coloridos De Carolina : Babl Children's Books in Spanish and English", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_124', 'title': 'Skeleton Play: A Fun, Rhyming Halloween Book for Kids! (1)', 'categories': '["Books", "Children\'s Books", "Holidays & Celebrations"]'}, {'book_id': 'bookid_130', 'title': "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_132', 'title': 'Mae and Jane in the Rain', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_145', 'title': 'Kirsten: An American Girl : 1854 (The American Girls Collection/Boxed Set)', 'categories': '["Books", "Boxed Sets", "Children\'s Books"]'}, {'book_id': 'bookid_146', 'title': 'LunaLu the Llamacorn', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_149', 'title': 'Trouble in the CTC!: The Terra Prime Adventures Book 2', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_152', 'title': 'Around the World Mazes', 'categories': '["Books", "Children\'s Books", "Activities, Crafts & Games"]'}, {'book_id': 'bookid_158', 'title': 'Cleo Porter and the Body Electric', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_163', 'title': 'Monster Kisses', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_170', 'title': 'Pokémon: Sun & Moon, Vol. 8 (8)', 'categories': '["Books", "Children\'s Books", "Comics & Graphic Novels"]'}], 'var_call_pl9vKGZQ93liXXd50TQOrYAN': [], 'var_call_6LJgjG5ta6yGfRB1t6hw8Qpa': 'file_storage/call_6LJgjG5ta6yGfRB1t6hw8Qpa.json'}

exec(code, env_args)
