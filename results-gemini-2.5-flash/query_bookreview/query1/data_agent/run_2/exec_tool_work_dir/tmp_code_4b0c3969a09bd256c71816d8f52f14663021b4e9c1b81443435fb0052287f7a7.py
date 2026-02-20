code = """import json
import pandas as pd

df_books_decades = pd.DataFrame(locals()['var_function-call-8141567747385715695'])

reviews_path = locals()['var_function-call-2861002454760239851']
with open(reviews_path, 'r') as f:
    reviews_data = json.load(f)
df_reviews = pd.DataFrame(reviews_data)

df_reviews['rating'] = df_reviews['rating'].astype(float)

df_merged = pd.merge(df_books_decades, df_reviews, left_on='book_id', right_on='purchase_id', how='inner')


book_count_per_decade = df_merged.groupby('publication_decade')['book_id'].nunique().reset_index()
book_count_per_decade.columns = ['publication_decade', 'distinct_book_count']

decades_with_at_least_10_books = book_count_per_decade[book_count_per_decade['distinct_book_count'] >= 10]

df_filtered = df_merged[df_merged['publication_decade'].isin(decades_with_at_least_10_books['publication_decade'])]


average_rating_per_decade = df_filtered.groupby('publication_decade')['rating'].mean().reset_index()

highest_avg_rating_decade = average_rating_per_decade.loc[average_rating_per_decade['rating'].idxmax()]

result = highest_avg_rating_decade.to_json()
print('__RESULT__:')
print(result)"""

env_args = {'var_function-call-2890100811406089170': ['books_info'], 'var_function-call-15840768285559180515': 'file_storage/function-call-15840768285559180515.json', 'var_function-call-8141567747385715695': [{'book_id': 'bookid_2', 'publication_decade': 1990}, {'book_id': 'bookid_3', 'publication_decade': 2010}, {'book_id': 'bookid_4', 'publication_decade': 2010}, {'book_id': 'bookid_5', 'publication_decade': 2010}, {'book_id': 'bookid_8', 'publication_decade': 2010}, {'book_id': 'bookid_10', 'publication_decade': 2000}, {'book_id': 'bookid_19', 'publication_decade': 2010}, {'book_id': 'bookid_20', 'publication_decade': 2000}, {'book_id': 'bookid_21', 'publication_decade': 1940}, {'book_id': 'bookid_24', 'publication_decade': 1930}, {'book_id': 'bookid_29', 'publication_decade': 2010}, {'book_id': 'bookid_33', 'publication_decade': 2010}, {'book_id': 'bookid_35', 'publication_decade': 2000}, {'book_id': 'bookid_40', 'publication_decade': 2010}, {'book_id': 'bookid_43', 'publication_decade': 2010}, {'book_id': 'bookid_44', 'publication_decade': 2010}, {'book_id': 'bookid_45', 'publication_decade': 2010}, {'book_id': 'bookid_46', 'publication_decade': 2010}, {'book_id': 'bookid_47', 'publication_decade': 1980}, {'book_id': 'bookid_49', 'publication_decade': 2010}, {'book_id': 'bookid_51', 'publication_decade': 2010}, {'book_id': 'bookid_60', 'publication_decade': 1980}, {'book_id': 'bookid_63', 'publication_decade': 2000}, {'book_id': 'bookid_64', 'publication_decade': 2000}, {'book_id': 'bookid_66', 'publication_decade': 2000}, {'book_id': 'bookid_67', 'publication_decade': 2000}, {'book_id': 'bookid_68', 'publication_decade': 1990}, {'book_id': 'bookid_71', 'publication_decade': 1990}, {'book_id': 'bookid_73', 'publication_decade': 2010}, {'book_id': 'bookid_76', 'publication_decade': 2010}, {'book_id': 'bookid_80', 'publication_decade': 1980}, {'book_id': 'bookid_86', 'publication_decade': 2000}, {'book_id': 'bookid_88', 'publication_decade': 2000}, {'book_id': 'bookid_89', 'publication_decade': 2010}, {'book_id': 'bookid_96', 'publication_decade': 2010}, {'book_id': 'bookid_99', 'publication_decade': 2010}, {'book_id': 'bookid_101', 'publication_decade': 2010}, {'book_id': 'bookid_105', 'publication_decade': 1980}, {'book_id': 'bookid_106', 'publication_decade': 2000}, {'book_id': 'bookid_107', 'publication_decade': 2020}, {'book_id': 'bookid_109', 'publication_decade': 1990}, {'book_id': 'bookid_113', 'publication_decade': 2010}, {'book_id': 'bookid_117', 'publication_decade': 2000}, {'book_id': 'bookid_119', 'publication_decade': 2010}, {'book_id': 'bookid_125', 'publication_decade': 2000}, {'book_id': 'bookid_126', 'publication_decade': 1980}, {'book_id': 'bookid_128', 'publication_decade': 2010}, {'book_id': 'bookid_129', 'publication_decade': 1970}, {'book_id': 'bookid_130', 'publication_decade': 2020}, {'book_id': 'bookid_131', 'publication_decade': 1990}, {'book_id': 'bookid_135', 'publication_decade': 2010}, {'book_id': 'bookid_136', 'publication_decade': 2010}, {'book_id': 'bookid_137', 'publication_decade': 2010}, {'book_id': 'bookid_138', 'publication_decade': 2000}, {'book_id': 'bookid_139', 'publication_decade': 2010}, {'book_id': 'bookid_143', 'publication_decade': 2000}, {'book_id': 'bookid_145', 'publication_decade': 1980}, {'book_id': 'bookid_150', 'publication_decade': 2010}, {'book_id': 'bookid_158', 'publication_decade': 2020}, {'book_id': 'bookid_159', 'publication_decade': 2010}, {'book_id': 'bookid_162', 'publication_decade': 2010}, {'book_id': 'bookid_163', 'publication_decade': 2010}, {'book_id': 'bookid_165', 'publication_decade': 2000}, {'book_id': 'bookid_168', 'publication_decade': 2000}, {'book_id': 'bookid_169', 'publication_decade': 1990}, {'book_id': 'bookid_171', 'publication_decade': 2010}, {'book_id': 'bookid_175', 'publication_decade': 2000}, {'book_id': 'bookid_178', 'publication_decade': 2010}, {'book_id': 'bookid_180', 'publication_decade': 2010}, {'book_id': 'bookid_188', 'publication_decade': 2000}, {'book_id': 'bookid_194', 'publication_decade': 2010}, {'book_id': 'bookid_195', 'publication_decade': 2010}, {'book_id': 'bookid_196', 'publication_decade': 2010}, {'book_id': 'bookid_197', 'publication_decade': 2010}, {'book_id': 'bookid_200', 'publication_decade': 2000}], 'var_function-call-2861002454760239851': 'file_storage/function-call-2861002454760239851.json'}

exec(code, env_args)
