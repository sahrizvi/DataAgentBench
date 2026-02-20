code = """import pandas as pd
import json
import re

# Load data from previous tool calls
books = var_call_nFuORyb0xzJEmNvfQanrs94a
reviews = var_call_hA9IHiLsBzjTmMEdXQX8zUG7

# Create DataFrames
df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Ensure columns present
# Extract numeric suffix from ids for fuzzy join
df_books['id_num'] = df_books['book_id'].astype(str).str.extract(r'(\d+)$')
df_reviews['id_num'] = df_reviews['purchase_id'].astype(str).str.extract(r'(\d+)$')

# Drop rows without numeric id
df_books = df_books[df_books['id_num'].notna()].copy()
df_reviews = df_reviews[df_reviews['id_num'].notna()].copy()

# Convert to int
df_books['id_num'] = df_books['id_num'].astype(int)
df_reviews['id_num'] = df_reviews['id_num'].astype(int)

# Convert avg_rating and review_count to numeric
df_reviews['avg_rating'] = pd.to_numeric(df_reviews['avg_rating'])
df_reviews['review_count'] = pd.to_numeric(df_reviews['review_count']).astype(int)

# Merge on numeric id
df_merged = pd.merge(df_books, df_reviews, on='id_num', how='inner', suffixes=('_book', '_review'))

# Filter books categorized as Children's Books (case-insensitive search for Children)
mask_children = df_merged['categories'].astype(str).str.contains("Children", case=False, na=False)
df_result = df_merged[mask_children].copy()

# Also ensure avg_rating >= 4.5 (though reviews were prefiltered, but be safe)
df_result = df_result[df_result['avg_rating'] >= 4.5]

# Prepare output
output = []
for _, row in df_result.iterrows():
    output.append({
        'title': row.get('title'),
        'book_id': row.get('book_id'),
        'purchase_id': row.get('purchase_id'),
        'avg_rating': float(row.get('avg_rating')),
        'review_count': int(row.get('review_count')),
        'categories': row.get('categories')
    })

# Sort by avg_rating desc then review_count desc
output = sorted(output, key=lambda x: (-x['avg_rating'], -x['review_count'], x['title']))

print("__RESULT__:")
print(json.dumps(output))"""

env_args = {'var_call_5SqN716IUN3iUg5EDSnda6dl': ['books_info'], 'var_call_nFuORyb0xzJEmNvfQanrs94a': [{'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_32', 'title': 'The Very Hungry Caterpillar (English and Arabic Edition)', 'categories': '["Books", "Children\'s Books", "Early Learning"]'}, {'book_id': 'bookid_40', 'title': 'Egypt (Enchantment of the World)', 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_48', 'title': 'Clark the Shark: Tooth Trouble, No. 1', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_52', 'title': "I Hadn't Meant to Tell You This", 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_54', 'title': 'Favorite Thorton W. Burgess Stories: 6 Books', 'categories': '["Books", "Children\'s Books", "Animals"]'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_57', 'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_96', 'title': 'Cheer Up, Ben Franklin! (Young Historians)', 'categories': '["Books", "Children\'s Books", "History"]'}, {'book_id': 'bookid_99', 'title': 'Buddy the Soldier Bear', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_108', 'title': 'The Library Book', 'categories': '["Books", "Children\'s Books", "Education & Reference"]'}, {'book_id': 'bookid_111', 'title': 'Can You Buy Me The Wind?', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_116', 'title': 'From the Earth to the Moon by Jules Verne, Fiction, Fantasy & Magic', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_120', 'title': "Caroline's Color Dreams: Los Sueños Coloridos De Carolina : Babl Children's Books in Spanish and English", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_124', 'title': 'Skeleton Play: A Fun, Rhyming Halloween Book for Kids! (1)', 'categories': '["Books", "Children\'s Books", "Holidays & Celebrations"]'}, {'book_id': 'bookid_130', 'title': "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_132', 'title': 'Mae and Jane in the Rain', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_145', 'title': 'Kirsten: An American Girl : 1854 (The American Girls Collection/Boxed Set)', 'categories': '["Books", "Boxed Sets", "Children\'s Books"]'}, {'book_id': 'bookid_146', 'title': 'LunaLu the Llamacorn', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_149', 'title': 'Trouble in the CTC!: The Terra Prime Adventures Book 2', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_152', 'title': 'Around the World Mazes', 'categories': '["Books", "Children\'s Books", "Activities, Crafts & Games"]'}, {'book_id': 'bookid_158', 'title': 'Cleo Porter and the Body Electric', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_163', 'title': 'Monster Kisses', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_170', 'title': 'Pokémon: Sun & Moon, Vol. 8 (8)', 'categories': '["Books", "Children\'s Books", "Comics & Graphic Novels"]'}], 'var_call_hA9IHiLsBzjTmMEdXQX8zUG7': [{'purchase_id': 'purchaseid_10', 'avg_rating': '5.0', 'review_count': '4'}, {'purchase_id': 'purchaseid_105', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_108', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_110', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_115', 'avg_rating': '4.75', 'review_count': '8'}, {'purchase_id': 'purchaseid_118', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_12', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_122', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_126', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_129', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_13', 'avg_rating': '4.923076923076923', 'review_count': '13'}, {'purchase_id': 'purchaseid_130', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_14', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_144', 'avg_rating': '5.0', 'review_count': '4'}, {'purchase_id': 'purchaseid_146', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_149', 'avg_rating': '4.9', 'review_count': '10'}, {'purchase_id': 'purchaseid_152', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_154', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_158', 'avg_rating': '4.708333333333333', 'review_count': '24'}, {'purchase_id': 'purchaseid_161', 'avg_rating': '4.5', 'review_count': '2'}, {'purchase_id': 'purchaseid_169', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_170', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_172', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_178', 'avg_rating': '4.795918367346939', 'review_count': '49'}, {'purchase_id': 'purchaseid_182', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_184', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_185', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_187', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_192', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_196', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_198', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_200', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_22', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_23', 'avg_rating': '4.5', 'review_count': '2'}, {'purchase_id': 'purchaseid_3', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_33', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_37', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_38', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_39', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_4', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_40', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_41', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_46', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_48', 'avg_rating': '4.75', 'review_count': '4'}, {'purchase_id': 'purchaseid_50', 'avg_rating': '4.5', 'review_count': '2'}, {'purchase_id': 'purchaseid_54', 'avg_rating': '5.0', 'review_count': '3'}, {'purchase_id': 'purchaseid_55', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_6', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_60', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_66', 'avg_rating': '5.0', 'review_count': '2'}, {'purchase_id': 'purchaseid_72', 'avg_rating': '4.5', 'review_count': '2'}, {'purchase_id': 'purchaseid_74', 'avg_rating': '5.0', 'review_count': '8'}, {'purchase_id': 'purchaseid_76', 'avg_rating': '4.75', 'review_count': '4'}, {'purchase_id': 'purchaseid_8', 'avg_rating': '4.709677419354839', 'review_count': '31'}, {'purchase_id': 'purchaseid_80', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_83', 'avg_rating': '5.0', 'review_count': '14'}, {'purchase_id': 'purchaseid_88', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_94', 'avg_rating': '5.0', 'review_count': '1'}, {'purchase_id': 'purchaseid_96', 'avg_rating': '5.0', 'review_count': '1'}]}

exec(code, env_args)
