code = """import pandas as pd
import json

# Correctly access and parse children_books data
children_books_response_dict = locals()['var_function-call-891945208824814073']
children_books_raw_string = children_books_response_dict['query_db_response']['results'][0]

# The string data contains extra info, extract only the JSON array part
json_start = children_books_raw_string.find('[')
json_end = children_books_raw_string.rfind(']')
children_books_json_string = children_books_raw_string[json_start:json_end+1]

children_books_data = json.loads(children_books_json_string)
df_children_books = pd.DataFrame(children_books_data)

# Correctly access reviews file path and load data
reviews_response_dict = locals()['var_function-call-13217426747881690336']
reviews_file_path = reviews_response_dict['query_db_response']['results'][0]

with open(reviews_file_path, 'r') as f:
    all_reviews = json.load(f)
df_reviews = pd.DataFrame(all_reviews)

# Process reviews data
df_reviews['review_time'] = pd.to_datetime(df_reviews['review_time'])
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'])
df_reviews_2020_onwards = df_reviews[df_reviews['review_time'].dt.year >= 2020]

# Merge and filter
merged_df = pd.merge(df_children_books, df_reviews_2020_onwards, left_on='book_id', right_on='purchase_id', how='inner')
average_ratings = merged_df.groupby('title')['rating'].mean().reset_index()
high_rated_children_books = average_ratings[average_ratings['rating'] >= 4.5]

# Get the list of titles
result = high_rated_children_books['title'].tolist()

print('__RESULT__:')
print(json.dumps(result))"""

env_args = {'var_function-call-3099652530996472062': ['books_info'], 'var_function-call-891945208824814073': [{'book_id': 'bookid_4', 'title': 'Monstrous Stories #4: The Day the Mice Stood Still'}, {'book_id': 'bookid_14', 'title': 'The Old Man and the Pirate Princess'}, {'book_id': 'bookid_32', 'title': 'The Very Hungry Caterpillar (English and Arabic Edition)'}, {'book_id': 'bookid_40', 'title': 'Egypt (Enchantment of the World)'}, {'book_id': 'bookid_48', 'title': 'Clark the Shark: Tooth Trouble, No. 1'}, {'book_id': 'bookid_52', 'title': "I Hadn't Meant to Tell You This"}, {'book_id': 'bookid_54', 'title': 'Favorite Thorton W. Burgess Stories: 6 Books'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)'}, {'book_id': 'bookid_57', 'title': "Goodnight Riley and the Moon, It's Almost Bedtime: Personalized Children’s Books, Personalized Gifts, and Bedtime Stories (A Magnificent Me! estorytime.com Series)"}, {'book_id': 'bookid_96', 'title': 'Cheer Up, Ben Franklin! (Young Historians)'}, {'book_id': 'bookid_99', 'title': 'Buddy the Soldier Bear'}, {'book_id': 'bookid_108', 'title': 'The Library Book'}, {'book_id': 'bookid_111', 'title': 'Can You Buy Me The Wind?'}, {'book_id': 'bookid_116', 'title': 'From the Earth to the Moon by Jules Verne, Fiction, Fantasy & Magic'}, {'book_id': 'bookid_120', 'title': "Caroline's Color Dreams: Los Sueños Coloridos De Carolina : Babl Children's Books in Spanish and English"}, {'book_id': 'bookid_124', 'title': 'Skeleton Play: A Fun, Rhyming Halloween Book for Kids! (1)'}, {'book_id': 'bookid_130', 'title': "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)"}, {'book_id': 'bookid_132', 'title': 'Mae and Jane in the Rain'}, {'book_id': 'bookid_145', 'title': 'Kirsten: An American Girl : 1854 (The American Girls Collection/Boxed Set)'}, {'book_id': 'bookid_146', 'title': 'LunaLu the Llamacorn'}, {'book_id': 'bookid_149', 'title': 'Trouble in the CTC!: The Terra Prime Adventures Book 2'}, {'book_id': 'bookid_152', 'title': 'Around the World Mazes'}, {'book_id': 'bookid_158', 'title': 'Cleo Porter and the Body Electric'}, {'book_id': 'bookid_163', 'title': 'Monster Kisses'}, {'book_id': 'bookid_170', 'title': 'Pokémon: Sun & Moon, Vol. 8 (8)'}], 'var_function-call-13217426747881690336': 'file_storage/function-call-13217426747881690336.json'}

exec(code, env_args)
