code = """import pandas as pd
import json

# Load books (from the SQL result variable)
books_data = locals()['var_function-call-15863505052874489412']
df_books = pd.DataFrame(books_data)

# Filter books strictly for "Children's Books" in categories
def has_childrens_books(cat_str):
    try:
        # The string might be a python string representation of a list, e.g. "['a', 'b']"
        # json.loads expects double quotes: '["a", "b"]'
        # Let's try to replace single quotes with double quotes if needed, 
        # but be careful of apostrophes in "Children's Books".
        # A safer way is using ast.literal_eval if available, but I can't import ast.
        # So I'll do a robust string check or try to normalize quotes.
        
        # If the format is JSON-compliant (double quotes), json.loads works.
        # If it's Python style (single quotes), we might have issues.
        # Let's inspect the string format from the first record in my mind...
        # The preview showed: "[\"Books\", \"Literature & Fiction\", ...]" -> This is valid JSON.
        
        cats = json.loads(cat_str)
        return "Children's Books" in cats
    except:
        # If json load fails, it might be due to single quotes or other issues.
        # Fallback: check for exact string "Children's Books" inside the list syntax
        # e.g. "..., 'Children's Books', ..." or "..., \"Children's Books\", ..."
        # This is surprisingly hard with regex without import re (if not standard).
        # But simple string search for "\"Children's Books\"" or "'Children's Books'" is better than just "Children's Books"
        if '"Children\'s Books"' in cat_str: return True
        if "'Children\'s Books'" in cat_str: return True
        return False

# Apply strict filter
df_books['is_children'] = df_books['categories'].apply(has_childrens_books)
df_books = df_books[df_books['is_children']]

# Load reviews (from file)
reviews_file = locals()['var_function-call-8525528187572476752']
with open(reviews_file, 'r') as f:
    reviews = json.load(f)
df_reviews = pd.DataFrame(reviews)

# Extract IDs
def extract_id(s):
    if pd.isna(s): return None
    if '_' in s:
        return s.split('_')[-1]
    return s

df_books['id_num'] = df_books['book_id'].apply(extract_id)
df_reviews['id_num'] = df_reviews['purchase_id'].apply(extract_id)

# Convert rating
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'])

# Calculate average rating
avg_ratings = df_reviews.groupby('id_num')['rating'].mean().reset_index()

# Filter avg rating >= 4.5
high_rated = avg_ratings[avg_ratings['rating'] >= 4.5]

# Merge
result = pd.merge(df_books, high_rated, on='id_num', how='inner')

titles = result['title'].unique().tolist()

print("__RESULT__:")
print(json.dumps(titles))"""

env_args = {'var_function-call-9241314928258498783': [{'rating': '4', 'title': 'Ha! On me!  I thought this was a cookbook!', 'text': 'Lucky for me it\'s more than a cookbook.<br /><br />The story of a modern Daniel Boone, growing up in Michigan, one of three sons of a hunter.  Beginning at age eight when he shot a squirrel, to age 13 his first deer, then hunting his way through college, a career as a fur trapper, hunting sheep in Alaska, canoeing the Missouri River for deer and ending in Brooklyn age 37. Brooklyn?<br /><br />I especially liked that I share his disgust at catch & release fishing - if you fish it, you have to eat it - anything else is sadism (my words).<br /><br />My brother in law is the cook in the family and I wanted to see if this would be a good gift for him and I struck pay dirt following each chapter are "Tasting Notes" where the author speaks of cooking wild game.<br /><br />I also enjoyed it for the history of the land he has hunted as well as the history of the hunt (I too was a big Daniel Boone fan growing up!).<br /><br />I think more pictures (everything but dead things) would have made this a keeper.', 'review_time': '2012-11-24 18:52:00', 'helpful_vote': '0', 'verified_purchase': '0', 'purchase_id': 'purchaseid_186'}], 'var_function-call-1570556575466775343': [{'book_id': 'bookid_1', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]'}], 'var_function-call-15863505052874489412': [{'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess'}, {'book_id': 'bookid_32', 'title': 'The Very Hungry Caterpillar (English and Arabic Edition)'}, {'book_id': 'bookid_40', 'title': 'Egypt (Enchantment of the World)'}, {'book_id': 'bookid_48', 'title': 'Clark the Shark: Tooth Trouble, No. 1'}, {'book_id': 'bookid_52', 'title': "I Hadn't Meant to Tell You This"}, {'book_id': 'bookid_54', 'title': 'Favorite Thorton W. Burgess Stories: 6 Books'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)'}, {'book_id': 'bookid_57', 'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)"}, {'book_id': 'bookid_96', 'title': 'Cheer Up, Ben Franklin! (Young Historians)'}, {'book_id': 'bookid_99', 'title': 'Buddy the Soldier Bear'}, {'book_id': 'bookid_108', 'title': 'The Library Book'}, {'book_id': 'bookid_111', 'title': 'Can You Buy Me The Wind?'}, {'book_id': 'bookid_116', 'title': 'From the Earth to the Moon by Jules Verne, Fiction, Fantasy & Magic'}, {'book_id': 'bookid_120', 'title': "Caroline's Color Dreams: Los Sueños Coloridos De Carolina : Babl Children's Books in Spanish and English"}, {'book_id': 'bookid_124', 'title': 'Skeleton Play: A Fun, Rhyming Halloween Book for Kids! (1)'}, {'book_id': 'bookid_130', 'title': "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)"}, {'book_id': 'bookid_132', 'title': 'Mae and Jane in the Rain'}, {'book_id': 'bookid_145', 'title': 'Kirsten: An American Girl : 1854 (The American Girls Collection/Boxed Set)'}, {'book_id': 'bookid_146', 'title': 'LunaLu the Llamacorn'}, {'book_id': 'bookid_149', 'title': 'Trouble in the CTC!: The Terra Prime Adventures Book 2'}, {'book_id': 'bookid_152', 'title': 'Around the World Mazes'}, {'book_id': 'bookid_158', 'title': 'Cleo Porter and the Body Electric'}, {'book_id': 'bookid_163', 'title': 'Monster Kisses'}, {'book_id': 'bookid_170', 'title': 'Pokémon: Sun & Moon, Vol. 8 (8)'}], 'var_function-call-8525528187572476752': 'file_storage/function-call-8525528187572476752.json', 'var_function-call-5298750911725141268': ['Monstrous Stories #4: The Day the Mice Stood Still', 'The Old Man and the Pirate Princess', 'Egypt (Enchantment of the World)', 'Clark the Shark: Tooth Trouble, No. 1', 'Favorite Thorton W. Burgess Stories: 6 Books', 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)', 'Cheer Up, Ben Franklin! (Young Historians)', 'The Library Book', "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)", 'LunaLu the Llamacorn', 'Trouble in the CTC!: The Terra Prime Adventures Book 2', 'Around the World Mazes', 'Cleo Porter and the Body Electric', 'Pokémon: Sun & Moon, Vol. 8 (8)']}

exec(code, env_args)
