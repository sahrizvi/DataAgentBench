code = """import pandas as pd
import json

# Load books data
books_list = locals()['var_function-call-15218803090803203069']
books_df = pd.DataFrame(books_list)

# Load reviews data
reviews_file_path = locals()['var_function-call-15218803090803201690']
with open(reviews_file_path, 'r') as f:
    reviews_list = json.load(f)
reviews_df = pd.DataFrame(reviews_list)

# Extract numeric ID
# book_id format: "bookid_4"
# purchase_id format: "purchaseid_8"

def extract_id(val):
    try:
        if '_' in val:
            return int(val.split('_')[1])
        return None
    except:
        return None

books_df['id_num'] = books_df['book_id'].apply(extract_id)
reviews_df['id_num'] = reviews_df['purchase_id'].apply(extract_id)

# Filter out None IDs if any
books_df = books_df.dropna(subset=['id_num'])
reviews_df = reviews_df.dropna(subset=['id_num'])

# Convert rating to float
reviews_df['rating'] = reviews_df['rating'].astype(float)

# Merge
merged_df = pd.merge(books_df, reviews_df, on='id_num', how='inner')

# Calculate average rating per book
# We group by book_id and title to keep the title in the result
avg_ratings = merged_df.groupby(['book_id', 'title'])['rating'].mean().reset_index()

# Filter for >= 4.5
result_df = avg_ratings[avg_ratings['rating'] >= 4.5]

# Get titles
titles = result_df['title'].tolist()

print("__RESULT__:")
print(json.dumps(titles))"""

env_args = {'var_function-call-6929168918928619672': ['review'], 'var_function-call-6929168918928618509': ['books_info'], 'var_function-call-4263382293114797369': [{'review_time': '2012-11-24 18:52:00'}, {'review_time': '2015-12-31 13:35:00'}, {'review_time': '2013-05-05 10:47:00'}, {'review_time': '2020-08-12 11:06:00'}, {'review_time': '2014-11-13 18:55:00'}], 'var_function-call-4263382293114795578': [{'categories': '["Books", "Literature & Fiction", "History & Criticism"]'}, {'categories': '["Books", "Reference", "Words, Language & Grammar"]'}, {'categories': '["Books", "Biographies & Memoirs", "Leaders & Notable People"]'}, {'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'categories': '["Books", "Mystery, Thriller & Suspense", "Thrillers & Suspense"]'}], 'var_function-call-15218803090803203069': [{'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess'}, {'book_id': 'bookid_32', 'title': 'The Very Hungry Caterpillar (English and Arabic Edition)'}, {'book_id': 'bookid_40', 'title': 'Egypt (Enchantment of the World)'}, {'book_id': 'bookid_48', 'title': 'Clark the Shark: Tooth Trouble, No. 1'}, {'book_id': 'bookid_52', 'title': "I Hadn't Meant to Tell You This"}, {'book_id': 'bookid_54', 'title': 'Favorite Thorton W. Burgess Stories: 6 Books'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)'}, {'book_id': 'bookid_57', 'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)"}, {'book_id': 'bookid_96', 'title': 'Cheer Up, Ben Franklin! (Young Historians)'}, {'book_id': 'bookid_99', 'title': 'Buddy the Soldier Bear'}, {'book_id': 'bookid_108', 'title': 'The Library Book'}, {'book_id': 'bookid_111', 'title': 'Can You Buy Me The Wind?'}, {'book_id': 'bookid_116', 'title': 'From the Earth to the Moon by Jules Verne, Fiction, Fantasy & Magic'}, {'book_id': 'bookid_120', 'title': "Caroline's Color Dreams: Los Sueños Coloridos De Carolina : Babl Children's Books in Spanish and English"}, {'book_id': 'bookid_124', 'title': 'Skeleton Play: A Fun, Rhyming Halloween Book for Kids! (1)'}, {'book_id': 'bookid_130', 'title': "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)"}, {'book_id': 'bookid_132', 'title': 'Mae and Jane in the Rain'}, {'book_id': 'bookid_145', 'title': 'Kirsten: An American Girl : 1854 (The American Girls Collection/Boxed Set)'}, {'book_id': 'bookid_146', 'title': 'LunaLu the Llamacorn'}, {'book_id': 'bookid_149', 'title': 'Trouble in the CTC!: The Terra Prime Adventures Book 2'}, {'book_id': 'bookid_152', 'title': 'Around the World Mazes'}, {'book_id': 'bookid_158', 'title': 'Cleo Porter and the Body Electric'}, {'book_id': 'bookid_163', 'title': 'Monster Kisses'}, {'book_id': 'bookid_170', 'title': 'Pokémon: Sun & Moon, Vol. 8 (8)'}], 'var_function-call-15218803090803201690': 'file_storage/function-call-15218803090803201690.json'}

exec(code, env_args)
