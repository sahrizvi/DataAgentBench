code = """import json
import pandas as pd

# Access the data from previous queries
df_children_books = pd.DataFrame(locals()['var_functions.query_db:8'])

# Read the review data from file
with open(locals()['var_functions.query_db:10'], 'r') as f:
    review_data = json.load(f)

df_reviews = pd.DataFrame(review_data)

# Convert rating to numeric
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

# Filter reviews from 2020 onwards
df_reviews_2020 = df_reviews[df_reviews['review_time'] >= '2020-01-01'].copy()

# Extract numeric part for joining
df_children_books['book_number'] = df_children_books['book_id'].str.extract('(\d+)')
df_reviews_2020['book_number'] = df_reviews_2020['purchase_id'].str.extract('(\d+)')

# Merge datasets
merged_data = pd.merge(df_children_books, df_reviews_2020, on='book_number', how='inner')

# Calculate average rating for each book
book_avg_ratings = merged_data.groupby(['book_id_x', 'title_x']).agg({'rating': 'mean', 'purchase_id': 'count'}).reset_index()
book_avg_ratings.columns = ['book_id', 'title', 'avg_rating', 'review_count']

# Filter books with average rating >= 4.5
high_rated_books = book_avg_ratings[book_avg_ratings['avg_rating'] >= 4.5]

# Sort by average rating descending
high_rated_books = high_rated_books.sort_values('avg_rating', ascending=False)

# Create result list
result_list = []
for idx, row in high_rated_books.iterrows():
    result_list.append({
        'title': row['title'],
        'avg_rating': round(row['avg_rating'], 2),
        'review_count': int(row['review_count'])
    })

print('__RESULT__:')
print(json.dumps(result_list))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:4': [{'title': 'Chaucer', 'book_id': 'bookid_1', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]'}, {'title': 'Notes from a Kidwatcher', 'book_id': 'bookid_2', 'categories': '["Books", "Reference", "Words, Language & Grammar"]'}, {'title': 'Service: A Navy SEAL at War', 'book_id': 'bookid_3', 'categories': '["Books", "Biographies & Memoirs", "Leaders & Notable People"]'}, {'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'book_id': 'bookid_4', 'categories': '["Books", "Children\'s Books", "Science Fiction & Fantasy"]'}, {'title': 'Parker & Knight', 'book_id': 'bookid_5', 'categories': '["Books", "Mystery, Thriller & Suspense", "Thrillers & Suspense"]'}, {'title': 'Writings from a Black Woman Living in the Land of the "Free": Strength, Power, Resilience', 'book_id': 'bookid_6', 'categories': '["Books", "Arts & Photography", "History & Criticism"]'}, {'title': "Child Development: A Practitioner's Guide:2nd (Second) edition", 'book_id': 'bookid_7', 'categories': '["Books", "Parenting & Relationships", "Parenting"]'}, {'title': 'Make: Electronics: Learning Through Discovery', 'book_id': 'bookid_8', 'categories': '["Books", "Engineering & Transportation", "Engineering"]'}, {'title': 'Reunion: The Children of Lauderdale Park', 'book_id': 'bookid_9', 'categories': '["Books", "Literature & Fiction", "Genre Fiction"]'}, {'title': 'Four Centuries of American Education', 'book_id': 'bookid_10', 'categories': '["Books", "Education & Teaching", "Schools & Teaching"]'}], 'var_functions.query_db:8': [{'title': 'Monstrous Stories #4: The Day the Mice Stood Still', 'book_id': 'bookid_4'}, {'title': 'The Old Man and the Pirate Princess', 'book_id': 'bookid_14'}, {'title': 'The Very Hungry Caterpillar (English and Arabic Edition)', 'book_id': 'bookid_32'}, {'title': 'Egypt (Enchantment of the World)', 'book_id': 'bookid_40'}, {'title': 'Clark the Shark: Tooth Trouble, No. 1', 'book_id': 'bookid_48'}, {'title': "I Hadn't Meant to Tell You This", 'book_id': 'bookid_52'}, {'title': 'Favorite Thorton W. Burgess Stories: 6 Books', 'book_id': 'bookid_54'}, {'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)', 'book_id': 'bookid_55'}, {'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)", 'book_id': 'bookid_57'}, {'title': 'Cheer Up, Ben Franklin! (Young Historians)', 'book_id': 'bookid_96'}, {'title': 'Buddy the Soldier Bear', 'book_id': 'bookid_99'}, {'title': 'The Library Book', 'book_id': 'bookid_108'}, {'title': 'Can You Buy Me The Wind?', 'book_id': 'bookid_111'}, {'title': 'From the Earth to the Moon by Jules Verne, Fiction, Fantasy & Magic', 'book_id': 'bookid_116'}, {'title': "Caroline's Color Dreams: Los Sueños Coloridos De Carolina : Babl Children's Books in Spanish and English", 'book_id': 'bookid_120'}, {'title': 'Skeleton Play: A Fun, Rhyming Halloween Book for Kids! (1)', 'book_id': 'bookid_124'}, {'title': "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)", 'book_id': 'bookid_130'}, {'title': 'Mae and Jane in the Rain', 'book_id': 'bookid_132'}, {'title': 'Kirsten: An American Girl : 1854 (The American Girls Collection/Boxed Set)', 'book_id': 'bookid_145'}, {'title': 'LunaLu the Llamacorn', 'book_id': 'bookid_146'}, {'title': 'Trouble in the CTC!: The Terra Prime Adventures Book 2', 'book_id': 'bookid_149'}, {'title': 'Around the World Mazes', 'book_id': 'bookid_152'}, {'title': 'Cleo Porter and the Body Electric', 'book_id': 'bookid_158'}, {'title': 'Monster Kisses', 'book_id': 'bookid_163'}, {'title': 'Pokémon: Sun & Moon, Vol. 8 (8)', 'book_id': 'bookid_170'}], 'var_functions.query_db:10': 'file_storage/functions.query_db:10.json'}

exec(code, env_args)
