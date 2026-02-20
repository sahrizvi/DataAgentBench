code = """import pandas as pd
import json

# Correctly load english_literature_fiction_books from the JSON string.
# The result from the previous execute_python call (var_function-call-13024910977936607495) is a dictionary with a 'results' key,
# which contains a list with the JSON string as its first element.
english_literature_fiction_books_json_string = locals()['var_function-call-13024910977936607495']['results'][0]
english_literature_fiction_books = pd.DataFrame(json.loads(english_literature_fiction_books_json_string))

# Correctly load all_reviews from the file path.
# The result from the query_db call (var_function-call-1168265253559725348) directly stores the file path string.
all_reviews_filepath = locals()['var_function-call-1168265253559725348']
all_reviews = pd.read_json(all_reviews_filepath)

# Convert rating to numeric, coercing errors to NaN
all_reviews['rating'] = pd.to_numeric(all_reviews['rating'], errors='coerce')

# Drop rows where rating is NaN after conversion
all_reviews.dropna(subset=['rating'], inplace=True)

# Merge the two dataframes on book_id and purchase_id
merged_data = pd.merge(english_literature_fiction_books, all_reviews, left_on='book_id', right_on='purchase_id', how='inner')

# Calculate the average rating for each book
average_ratings = merged_data.groupby('book_id')['rating'].mean().reset_index()

# Filter for books with a perfect average rating of 5.0
perfect_rating_books = average_ratings[average_ratings['rating'] == 5.0]

# Get the titles of these books by merging back with the original book titles
final_books = pd.merge(perfect_rating_books, english_literature_fiction_books, on='book_id', how='inner')

print("__RESULT__:")
print(final_books['title'].to_json(orient='records'))"""

env_args = {'var_function-call-16511819307130799169': ['books_info'], 'var_function-call-382231788195853622': ['review'], 'var_function-call-11272966320864587591': 'file_storage/function-call-11272966320864587591.json', 'var_function-call-13024910977936607495': [{'book_id': 'bookid_1', 'title': 'Chaucer'}, {'book_id': 'bookid_9', 'title': 'Reunion: The Children of Lauderdale Park'}, {'book_id': 'bookid_13', 'title': 'Girl Made of Glass'}, {'book_id': 'bookid_30', 'title': 'Sugary Sweets (A Taste of Love Series)'}, {'book_id': 'bookid_36', 'title': 'Therapy Mammals'}, {'book_id': 'bookid_37', 'title': "A Most Dangerous Book: Tacitus's Germania from the Roman Empire to the Third Reich"}, {'book_id': 'bookid_38', 'title': 'The Prophet: With Original 1923 Illustrations by the Author'}, {'book_id': 'bookid_39', 'title': 'The Melancholy Strumpet Master'}, {'book_id': 'bookid_44', 'title': 'Reptilian'}, {'book_id': 'bookid_49', 'title': 'Primeval: A Journal of the Uncanny - Issue #1'}, {'book_id': 'bookid_55', 'title': 'Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)'}, {'book_id': 'bookid_69', 'title': 'Out of Sheer Rage: Wrestling with D. H. Lawrence'}, {'book_id': 'bookid_70', 'title': 'Polly and the Shadow Goblin: Book 2, Mother of Witches'}, {'book_id': 'bookid_74', 'title': 'Child Of The King A Journey of Hope Book 1: Earthly Story With A Heavenly Message'}, {'book_id': 'bookid_77', 'title': 'One September Morning'}, {'book_id': 'bookid_82', 'title': 'Fire Cracker'}, {'book_id': 'bookid_84', 'title': 'Local Honey'}, {'book_id': 'bookid_89', 'title': "I'll Ride For My Hood: A Salty Love Story"}, {'book_id': 'bookid_92', 'title': 'Outage'}, {'book_id': 'bookid_93', 'title': 'Simantov'}, {'book_id': 'bookid_98', 'title': 'Hollywood Confessions: Hollywood Headlines Book #3 (Hollywood Headlines Mysteries)'}, {'book_id': 'bookid_99', 'title': 'Buddy the Soldier Bear'}, {'book_id': 'bookid_101', 'title': 'Knowing When To Die: Uncollected Stories'}, {'book_id': 'bookid_106', 'title': 'Looking for Peyton Place: A Novel'}, {'book_id': 'bookid_109', 'title': 'All the Way to the Gallows'}, {'book_id': 'bookid_111', 'title': 'Can You Buy Me The Wind?'}, {'book_id': 'bookid_122', 'title': 'Childe Harold of Dysna'}, {'book_id': 'bookid_137', 'title': 'Oligarchy'}, {'book_id': 'bookid_142', 'title': 'The Jordan Tracks'}, {'book_id': 'bookid_144', 'title': 'Forged in Blood (Freehold)'}, {'book_id': 'bookid_161', 'title': "Time's Demon: BOOK II OF THE ISLEVALE CYCLE"}, {'book_id': 'bookid_167', 'title': 'Dead Silence'}, {'book_id': 'bookid_171', 'title': 'Exits, Desires, & Slow Fires'}, {'book_id': 'bookid_177', 'title': 'Kennebago Moments'}, {'book_id': 'bookid_179', 'title': 'A Cherry Cola Christmas (A Cherry Cola Book Club Novel)'}, {'book_id': 'bookid_180', 'title': 'The Sludge'}, {'book_id': 'bookid_182', 'title': 'Liza of Lambeth'}, {'book_id': 'bookid_187', 'title': 'Consort (A Dark(ish) Faerie Tale Book 3)'}, {'book_id': 'bookid_188', 'title': "The Vampyre and Other Tales of the Macabre (Oxford World's Classics)"}, {'book_id': 'bookid_195', 'title': 'Something That Feels Like Truth (Switchgrass Books)'}], 'var_function-call-1168265253559725348': 'file_storage/function-call-1168265253559725348.json'}

exec(code, env_args)
