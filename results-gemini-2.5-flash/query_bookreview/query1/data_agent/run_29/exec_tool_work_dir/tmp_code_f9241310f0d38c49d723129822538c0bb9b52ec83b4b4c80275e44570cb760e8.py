code = """import pandas as pd
import json

df_books_processed = pd.DataFrame(json.loads(locals()['var_function-call-12854487615454820362']))

with open(locals()['var_function-call-12449172615242602580'], 'r') as f:
    reviews_data = json.load(f)

df_reviews = pd.DataFrame(reviews_data)

df_reviews = df_reviews.rename(columns={'purchase_id': 'book_id'})
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'])

merged_df = pd.merge(df_books_processed, df_reviews, on='book_id')

decade_stats = merged_df.groupby('publication_decade').agg(
    distinct_books=('book_id', 'nunique'),
    average_rating=('rating', 'mean')
).reset_index()

filtered_decades = decade_stats[decade_stats['distinct_books'] >= 10]

highest_avg_rating_decade = filtered_decades.loc[filtered_decades['average_rating'].idxmax()]

result = highest_avg_rating_decade['publication_decade']

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_function-call-6008838561389752942': 'file_storage/function-call-6008838561389752942.json', 'var_function-call-12854487615454820362': [{'book_id': 'bookid_1', 'publication_decade': '2000s'}, {'book_id': 'bookid_2', 'publication_decade': '1990s'}, {'book_id': 'bookid_3', 'publication_decade': '2010s'}, {'book_id': 'bookid_4', 'publication_decade': '2010s'}, {'book_id': 'bookid_5', 'publication_decade': '2010s'}, {'book_id': 'bookid_7', 'publication_decade': '2000s'}, {'book_id': 'bookid_8', 'publication_decade': '2010s'}, {'book_id': 'bookid_10', 'publication_decade': '2000s'}, {'book_id': 'bookid_15', 'publication_decade': '2000s'}, {'book_id': 'bookid_16', 'publication_decade': '1990s'}, {'book_id': 'bookid_19', 'publication_decade': '2010s'}, {'book_id': 'bookid_20', 'publication_decade': '2000s'}, {'book_id': 'bookid_21', 'publication_decade': '1940s'}, {'book_id': 'bookid_24', 'publication_decade': '1930s'}, {'book_id': 'bookid_26', 'publication_decade': '1990s'}, {'book_id': 'bookid_29', 'publication_decade': '2010s'}, {'book_id': 'bookid_33', 'publication_decade': '2010s'}, {'book_id': 'bookid_35', 'publication_decade': '2000s'}, {'book_id': 'bookid_40', 'publication_decade': '2010s'}, {'book_id': 'bookid_42', 'publication_decade': '2010s'}, {'book_id': 'bookid_43', 'publication_decade': '2010s'}, {'book_id': 'bookid_44', 'publication_decade': '2010s'}, {'book_id': 'bookid_45', 'publication_decade': '2010s'}, {'book_id': 'bookid_46', 'publication_decade': '2010s'}, {'book_id': 'bookid_47', 'publication_decade': '1980s'}, {'book_id': 'bookid_49', 'publication_decade': '2010s'}, {'book_id': 'bookid_51', 'publication_decade': '2010s'}, {'book_id': 'bookid_60', 'publication_decade': '1980s'}, {'book_id': 'bookid_61', 'publication_decade': '1990s'}, {'book_id': 'bookid_63', 'publication_decade': '2000s'}, {'book_id': 'bookid_64', 'publication_decade': '2000s'}, {'book_id': 'bookid_65', 'publication_decade': '1970s'}, {'book_id': 'bookid_66', 'publication_decade': '2000s'}, {'book_id': 'bookid_67', 'publication_decade': '2000s'}, {'book_id': 'bookid_68', 'publication_decade': '1990s'}, {'book_id': 'bookid_71', 'publication_decade': '1990s'}, {'book_id': 'bookid_73', 'publication_decade': '2010s'}, {'book_id': 'bookid_81', 'publication_decade': '2010s'}, {'book_id': 'bookid_76', 'publication_decade': '2010s'}, {'book_id': 'bookid_80', 'publication_decade': '1980s'}, {'book_id': 'bookid_86', 'publication_decade': '2000s'}, {'book_id': 'bookid_87', 'publication_decade': '1980s'}, {'book_id': 'bookid_88', 'publication_decade': '2000s'}, {'book_id': 'bookid_89', 'publication_decade': '2010s'}, {'book_id': 'bookid_95', 'publication_decade': '1980s'}, {'book_id': 'bookid_96', 'publication_decade': '2010s'}, {'book_id': 'bookid_99', 'publication_decade': '2010s'}, {'book_id': 'bookid_101', 'publication_decade': '2010s'}, {'book_id': 'bookid_105', 'publication_decade': '1980s'}, {'book_id': 'bookid_106', 'publication_decade': '2000s'}, {'book_id': 'bookid_107', 'publication_decade': '2020s'}, {'book_id': 'bookid_109', 'publication_decade': '1990s'}, {'book_id': 'bookid_113', 'publication_decade': '2010s'}, {'book_id': 'bookid_117', 'publication_decade': '2000s'}, {'book_id': 'bookid_119', 'publication_decade': '2010s'}, {'book_id': 'bookid_125', 'publication_decade': '2000s'}, {'book_id': 'bookid_126', 'publication_decade': '1980s'}, {'book_id': 'bookid_128', 'publication_decade': '2010s'}, {'book_id': 'bookid_129', 'publication_decade': '1970s'}, {'book_id': 'bookid_130', 'publication_decade': '2020s'}, {'book_id': 'bookid_131', 'publication_decade': '1990s'}, {'book_id': 'bookid_134', 'publication_decade': '2010s'}, {'book_id': 'bookid_135', 'publication_decade': '2010s'}, {'book_id': 'bookid_136', 'publication_decade': '2010s'}, {'book_id': 'bookid_137', 'publication_decade': '2010s'}, {'book_id': 'bookid_138', 'publication_decade': '2000s'}, {'book_id': 'bookid_139', 'publication_decade': '2010s'}, {'book_id': 'bookid_143', 'publication_decade': '2000s'}, {'book_id': 'bookid_145', 'publication_decade': '1980s'}, {'book_id': 'bookid_149', 'publication_decade': '2020s'}, {'book_id': 'bookid_150', 'publication_decade': '2010s'}, {'book_id': 'bookid_158', 'publication_decade': '2020s'}, {'book_id': 'bookid_159', 'publication_decade': '2010s'}, {'book_id': 'bookid_162', 'publication_decade': '2010s'}, {'book_id': 'bookid_163', 'publication_decade': '2010s'}, {'book_id': 'bookid_165', 'publication_decade': '2000s'}, {'book_id': 'bookid_168', 'publication_decade': '2000s'}, {'book_id': 'bookid_169', 'publication_decade': '1990s'}, {'book_id': 'bookid_171', 'publication_decade': '2010s'}, {'book_id': 'bookid_175', 'publication_decade': '2000s'}, {'book_id': 'bookid_178', 'publication_decade': '2010s'}, {'book_id': 'bookid_180', 'publication_decade': '2010s'}, {'book_id': 'bookid_188', 'publication_decade': '2000s'}, {'book_id': 'bookid_192', 'publication_decade': '2000s'}, {'book_id': 'bookid_194', 'publication_decade': '2010s'}, {'book_id': 'bookid_195', 'publication_decade': '2010s'}, {'book_id': 'bookid_196', 'publication_decade': '2010s'}, {'book_id': 'bookid_197', 'publication_decade': '2010s'}, {'book_id': 'bookid_199', 'publication_decade': '2000s'}, {'book_id': 'bookid_200', 'publication_decade': '2000s'}], 'var_function-call-12449172615242602580': 'file_storage/function-call-12449172615242602580.json'}

exec(code, env_args)
