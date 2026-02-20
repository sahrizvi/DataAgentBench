code = """import json
import pandas as pd

# Get the file path from the storage key
file_path = '/tmp/tmpv5v2q0s7.json'
print(f"Reading review data from file path: {file_path}")

# Read the reviews data
with open(file_path, 'r') as f:
    reviews_data = json.load(f)

print(f"Total reviews from 2020 onwards: {len(reviews_data)}")

# Convert to DataFrame
reviews_df = pd.DataFrame(reviews_data)
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')

# Create children's book list
children_book_ids = {
    'bookid_4', 'bookid_14', 'bookid_32', 'bookid_40', 'bookid_48', 'bookid_52',
    'bookid_54', 'bookid_55', 'bookid_57', 'bookid_96', 'bookid_99', 'bookid_108',
    'bookid_111', 'bookid_116', 'bookid_120', 'bookid_124', 'bookid_130', 'bookid_132',
    'bookid_145', 'bookid_146', 'bookid_149', 'bookid_152', 'bookid_158', 'bookid_163',
    'bookid_170'
}

print(f"Total children's books: {len(children_book_ids)}")

# Map purchase_id to book_id (purchaseid_XX -> bookid_XX)
def map_purchase_to_book(purchase_id):
    if isinstance(purchase_id, str) and '_' in purchase_id:
        parts = purchase_id.split('_')
        if len(parts) > 1:
            return f"bookid_{parts[1]}"
    return None

reviews_df['book_id'] = reviews_df['purchase_id'].apply(map_purchase_to_book)

# Filter for children's books
children_reviews = reviews_df[reviews_df['book_id'].isin(children_book_ids)]
print(f"Reviews for children's books: {len(children_reviews)}")

# Calculate average rating per book
book_ratings = children_reviews.groupby('book_id')['rating'].agg(['mean', 'count']).reset_index()
book_ratings.columns = ['book_id', 'avg_rating', 'review_count']

# Filter books with avg rating >= 4.5
high_rated_books = book_ratings[book_ratings['avg_rating'] >= 4.5]
print(f"Books with rating >= 4.5: {len(high_rated_books)}")

# Create title mapping
book_titles = {
    'bookid_4': 'Monstrous Stories #4: The Day the Mice Stood Still',
    'bookid_14': 'The Old Man and the Pirate Princess',
    'bookid_32': 'The Very Hungry Caterpillar (English and Arabic Edition)',
    'bookid_40': 'Egypt (Enchantment of the World)',
    'bookid_48': 'Clark the Shark: Tooth Trouble, No. 1',
    'bookid_52': "I Hadn't Meant to Tell You This",
    'bookid_54': 'Favorite Thorton W. Burgess Stories: 6 Books',
    'bookid_55': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)',
    'bookid_57': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children's Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)",
    'bookid_96': 'Cheer Up, Ben Franklin! (Young Historians)',
    'bookid_99': 'Buddy the Soldier Bear',
    'bookid_108': 'The Library Book',
    'bookid_111': 'Can You Buy Me The Wind?',
    'bookid_116': 'From the Earth to the Moon by Jules Verne, Fiction, Fantasy & Magic',
    'bookid_120': "Caroline's Color Dreams: Los Sueños Coloridos De Carolina : Babl Children's Books in Spanish and English",
    'bookid_124': 'Skeleton Play: A Fun, Rhyming Halloween Book for Kids! (1)',
    'bookid_130': "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)",
    'bookid_132': 'Mae and Jane in the Rain',
    'bookid_145': 'Kirsten: An American Girl : 1854 (The American Girls Collection/Boxed Set)',
    'bookid_146': 'LunaLu the Llamacorn',
    'bookid_149': 'Trouble in the CTC!: The Terra Prime Adventures Book 2',
    'bookid_152': 'Around the World Mazes',
    'bookid_158': 'Cleo Porter and the Body Electric',
    'bookid_163': 'Monster Kisses',
    'bookid_170': 'Pokémon: Sun & Moon, Vol. 8 (8)'
}

# Add titles
high_rated_books['title'] = high_rated_books['book_id'].map(book_titles)

# Sort by avg_rating descending
high_rated_books = high_rated_books.sort_values('avg_rating', ascending=False)

# Prepare result
result = high_rated_books[['title', 'book_id', 'avg_rating', 'review_count']].to_dict('records')

print("__RESULT__:")
print(json.dumps(result, indent=2))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:5': [{'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_32', 'title': 'The Very Hungry Caterpillar (English and Arabic Edition)', 'categories': '["Books", "Children\'s Books", "Early Learning"]'}, {'book_id': 'bookid_40', 'title': 'Egypt (Enchantment of the World)', 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_48', 'title': 'Clark the Shark: Tooth Trouble, No. 1', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_52', 'title': "I Hadn't Meant to Tell You This", 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_54', 'title': 'Favorite Thorton W. Burgess Stories: 6 Books', 'categories': '["Books", "Children\'s Books", "Animals"]'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_57', 'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_96', 'title': 'Cheer Up, Ben Franklin! (Young Historians)', 'categories': '["Books", "Children\'s Books", "History"]'}], 'var_functions.query_db:8': [{'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_32', 'title': 'The Very Hungry Caterpillar (English and Arabic Edition)', 'categories': '["Books", "Children\'s Books", "Early Learning"]'}, {'book_id': 'bookid_40', 'title': 'Egypt (Enchantment of the World)', 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_48', 'title': 'Clark the Shark: Tooth Trouble, No. 1', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_52', 'title': "I Hadn't Meant to Tell You This", 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_54', 'title': 'Favorite Thorton W. Burgess Stories: 6 Books', 'categories': '["Books", "Children\'s Books", "Animals"]'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_57', 'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_96', 'title': 'Cheer Up, Ben Franklin! (Young Historians)', 'categories': '["Books", "Children\'s Books", "History"]'}, {'book_id': 'bookid_99', 'title': 'Buddy the Soldier Bear', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_108', 'title': 'The Library Book', 'categories': '["Books", "Children\'s Books", "Education & Reference"]'}, {'book_id': 'bookid_111', 'title': 'Can You Buy Me The Wind?', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_116', 'title': 'From the Earth to the Moon by Jules Verne, Fiction, Fantasy & Magic', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_120', 'title': "Caroline's Color Dreams: Los Sueños Coloridos De Carolina : Babl Children's Books in Spanish and English", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_124', 'title': 'Skeleton Play: A Fun, Rhyming Halloween Book for Kids! (1)', 'categories': '["Books", "Children\'s Books", "Holidays & Celebrations"]'}, {'book_id': 'bookid_130', 'title': "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_132', 'title': 'Mae and Jane in the Rain', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_145', 'title': 'Kirsten: An American Girl : 1854 (The American Girls Collection/Boxed Set)', 'categories': '["Books", "Boxed Sets", "Children\'s Books"]'}, {'book_id': 'bookid_146', 'title': 'LunaLu the Llamacorn', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_149', 'title': 'Trouble in the CTC!: The Terra Prime Adventures Book 2', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_152', 'title': 'Around the World Mazes', 'categories': '["Books", "Children\'s Books", "Activities, Crafts & Games"]'}, {'book_id': 'bookid_158', 'title': 'Cleo Porter and the Body Electric', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_163', 'title': 'Monster Kisses', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_170', 'title': 'Pokémon: Sun & Moon, Vol. 8 (8)', 'categories': '["Books", "Children\'s Books", "Comics & Graphic Novels"]'}], 'var_functions.query_db:10': [{'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_32', 'title': 'The Very Hungry Caterpillar (English and Arabic Edition)', 'categories': '["Books", "Children\'s Books", "Early Learning"]'}, {'book_id': 'bookid_40', 'title': 'Egypt (Enchantment of the World)', 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_48', 'title': 'Clark the Shark: Tooth Trouble, No. 1', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_52', 'title': "I Hadn't Meant to Tell You This", 'categories': '["Books", "Children\'s Books", "Geography & Cultures"]'}, {'book_id': 'bookid_54', 'title': 'Favorite Thorton W. Burgess Stories: 6 Books', 'categories': '["Books", "Children\'s Books", "Animals"]'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_57', 'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_96', 'title': 'Cheer Up, Ben Franklin! (Young Historians)', 'categories': '["Books", "Children\'s Books", "History"]'}, {'book_id': 'bookid_99', 'title': 'Buddy the Soldier Bear', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_108', 'title': 'The Library Book', 'categories': '["Books", "Children\'s Books", "Education & Reference"]'}, {'book_id': 'bookid_111', 'title': 'Can You Buy Me The Wind?', 'categories': '["Books", "Children\'s Books", "Literature & Fiction"]'}, {'book_id': 'bookid_116', 'title': 'From the Earth to the Moon by Jules Verne, Fiction, Fantasy & Magic', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_120', 'title': "Caroline's Color Dreams: Los Sueños Coloridos De Carolina : Babl Children's Books in Spanish and English", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_124', 'title': 'Skeleton Play: A Fun, Rhyming Halloween Book for Kids! (1)', 'categories': '["Books", "Children\'s Books", "Holidays & Celebrations"]'}, {'book_id': 'bookid_130', 'title': "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)", 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_132', 'title': 'Mae and Jane in the Rain', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_145', 'title': 'Kirsten: An American Girl : 1854 (The American Girls Collection/Boxed Set)', 'categories': '["Books", "Boxed Sets", "Children\'s Books"]'}, {'book_id': 'bookid_146', 'title': 'LunaLu the Llamacorn', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_149', 'title': 'Trouble in the CTC!: The Terra Prime Adventures Book 2', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_152', 'title': 'Around the World Mazes', 'categories': '["Books", "Children\'s Books", "Activities, Crafts & Games"]'}, {'book_id': 'bookid_158', 'title': 'Cleo Porter and the Body Electric', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'book_id': 'bookid_163', 'title': 'Monster Kisses', 'categories': '["Books", "Children\'s Books", "Growing Up & Facts of Life"]'}, {'book_id': 'bookid_170', 'title': 'Pokémon: Sun & Moon, Vol. 8 (8)', 'categories': '["Books", "Children\'s Books", "Comics & Graphic Novels"]'}], 'var_functions.query_db:14': [{'rating': '5', 'review_time': '2020-08-12 11:06:00', 'purchase_id': 'purchaseid_8'}, {'rating': '5', 'review_time': '2020-02-27 05:11:00', 'purchase_id': 'purchaseid_76'}, {'rating': '2', 'review_time': '2020-06-01 07:33:00', 'purchase_id': 'purchaseid_167'}, {'rating': '5', 'review_time': '2021-07-31 18:34:00', 'purchase_id': 'purchaseid_23'}, {'rating': '2', 'review_time': '2021-01-27 07:08:00', 'purchase_id': 'purchaseid_99'}, {'rating': '4', 'review_time': '2020-06-14 11:52:00', 'purchase_id': 'purchaseid_167'}, {'rating': '5', 'review_time': '2021-10-31 19:46:00', 'purchase_id': 'purchaseid_20'}, {'rating': '5', 'review_time': '2021-06-22 12:04:00', 'purchase_id': 'purchaseid_83'}, {'rating': '3', 'review_time': '2021-02-10 16:28:00', 'purchase_id': 'purchaseid_67'}, {'rating': '5', 'review_time': '2020-04-16 04:41:00', 'purchase_id': 'purchaseid_62'}], 'var_functions.query_db:18': 'file_storage/functions.query_db:18.json'}

exec(code, env_args)
