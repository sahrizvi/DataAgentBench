code = """import pandas as pd
import json
import re

# Load books_info data
with open(locals()['var_function-call-17427853686190860066'], 'r') as f:
    books_info_data = json.load(f)
df_books = pd.DataFrame(books_info_data)

# Extract publication year and calculate decade with an improved approach
def extract_year_improved(details_string):
    if isinstance(details_string, str):
        # Try to find a year explicitly mentioned after 'published on' or 'released on' or 'edition on'
        match_date = re.search(r'(?:published|released|edition) (?:on )?(?:January|February|March|April|May|June|July|August|September|October|November|December)?(?: \d{1,2},)?\s*(\d{4})', details_string)
        if match_date:
            year = int(match_date.group(1))
            if 1800 <= year <= 2023: # A wider range for publication years
                return year
        
        # If not found, try to find any 4-digit number that looks like a year
        years_found = re.findall(r'\b(\d{4})\b', details_string)
        # Prioritize the last occurring year as it is often the publication year
        if years_found:
            year = int(years_found[-1])
            if 1800 <= year <= 2023:
                return year
    return None

df_books['publication_year'] = df_books['details'].apply(extract_year_improved)
df_books['decade'] = (df_books['publication_year'] // 10) * 10

# Load reviews data
with open(locals()['var_function-call-10147937107887987371'], 'r') as f:
    reviews_data = json.load(f)
df_reviews = pd.DataFrame(reviews_data)

# Rename 'purchase_id' to 'book_id' for merging
df_reviews = df_reviews.rename(columns={'purchase_id': 'book_id'})

# Convert rating to numeric, coercing errors to NaN
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

# Merge the dataframes
merged_df = pd.merge(df_books[['book_id', 'decade']], df_reviews, on='book_id', how='inner')

# Drop rows where decade or rating is missing
merged_df.dropna(subset=['decade', 'rating'], inplace=True)

# Convert 'decade' to integer
merged_df['decade'] = merged_df['decade'].astype(int)

# Group by decade, count distinct books and calculate average rating
decade_stats = merged_df.groupby('decade').agg(
    distinct_books=('book_id', 'nunique'),
    average_rating=('rating', 'mean')
).reset_index()

# Filter for decades with at least 10 distinct books
filtered_decades = decade_stats[decade_stats['distinct_books'] >= 10]

# Find the decade with the highest average rating
if not filtered_decades.empty:
    highest_avg_rating_decade = filtered_decades.loc[filtered_decades['average_rating'].idxmax()]
    result = str(highest_avg_rating_decade['decade'])
else:
    result = "No decade meets the criteria of having at least 10 distinct books."

print('__RESULT__:')
print(json.dumps(result))"""

env_args = {'var_function-call-8221080890098848692': 'file_storage/function-call-8221080890098848692.json', 'var_function-call-11822431761995139965': [{'book_id': 'bookid_1', 'decade': None}, {'book_id': 'bookid_2', 'decade': 1990.0}, {'book_id': 'bookid_3', 'decade': None}, {'book_id': 'bookid_4', 'decade': 2010.0}, {'book_id': 'bookid_5', 'decade': 2010.0}, {'book_id': 'bookid_6', 'decade': None}, {'book_id': 'bookid_7', 'decade': None}, {'book_id': 'bookid_8', 'decade': None}, {'book_id': 'bookid_9', 'decade': None}, {'book_id': 'bookid_10', 'decade': 2000.0}, {'book_id': 'bookid_11', 'decade': None}, {'book_id': 'bookid_12', 'decade': 2020.0}, {'book_id': 'bookid_13', 'decade': 2020.0}, {'book_id': 'bookid_14', 'decade': None}, {'book_id': 'bookid_15', 'decade': 2000.0}, {'book_id': 'bookid_16', 'decade': None}, {'book_id': 'bookid_17', 'decade': 1980.0}, {'book_id': 'bookid_18', 'decade': None}, {'book_id': 'bookid_19', 'decade': 2010.0}, {'book_id': 'bookid_20', 'decade': 2000.0}, {'book_id': 'bookid_21', 'decade': 1940.0}, {'book_id': 'bookid_22', 'decade': 2000.0}, {'book_id': 'bookid_23', 'decade': None}, {'book_id': 'bookid_24', 'decade': 1930.0}, {'book_id': 'bookid_25', 'decade': None}, {'book_id': 'bookid_32', 'decade': 1990.0}, {'book_id': 'bookid_26', 'decade': None}, {'book_id': 'bookid_27', 'decade': None}, {'book_id': 'bookid_28', 'decade': 1990.0}, {'book_id': 'bookid_29', 'decade': 2010.0}, {'book_id': 'bookid_30', 'decade': 2010.0}, {'book_id': 'bookid_31', 'decade': 2010.0}, {'book_id': 'bookid_33', 'decade': 2010.0}, {'book_id': 'bookid_34', 'decade': None}, {'book_id': 'bookid_35', 'decade': 2000.0}, {'book_id': 'bookid_36', 'decade': 2010.0}, {'book_id': 'bookid_37', 'decade': 2010.0}, {'book_id': 'bookid_38', 'decade': 2010.0}, {'book_id': 'bookid_56', 'decade': 2010.0}, {'book_id': 'bookid_39', 'decade': None}, {'book_id': 'bookid_40', 'decade': None}, {'book_id': 'bookid_41', 'decade': 2010.0}, {'book_id': 'bookid_42', 'decade': None}, {'book_id': 'bookid_43', 'decade': 2010.0}, {'book_id': 'bookid_62', 'decade': 2010.0}, {'book_id': 'bookid_44', 'decade': 2010.0}, {'book_id': 'bookid_45', 'decade': 2010.0}, {'book_id': 'bookid_46', 'decade': 2010.0}, {'book_id': 'bookid_47', 'decade': 1980.0}, {'book_id': 'bookid_48', 'decade': 2010.0}, {'book_id': 'bookid_49', 'decade': 2010.0}, {'book_id': 'bookid_50', 'decade': None}, {'book_id': 'bookid_51', 'decade': 2010.0}, {'book_id': 'bookid_52', 'decade': None}, {'book_id': 'bookid_53', 'decade': 1990.0}, {'book_id': 'bookid_54', 'decade': 2000.0}, {'book_id': 'bookid_55', 'decade': 2010.0}, {'book_id': 'bookid_57', 'decade': 2010.0}, {'book_id': 'bookid_58', 'decade': None}, {'book_id': 'bookid_59', 'decade': 2000.0}, {'book_id': 'bookid_60', 'decade': 1980.0}, {'book_id': 'bookid_61', 'decade': None}, {'book_id': 'bookid_63', 'decade': 2000.0}, {'book_id': 'bookid_64', 'decade': 2000.0}, {'book_id': 'bookid_65', 'decade': None}, {'book_id': 'bookid_66', 'decade': 2000.0}, {'book_id': 'bookid_67', 'decade': None}, {'book_id': 'bookid_68', 'decade': 1990.0}, {'book_id': 'bookid_69', 'decade': 2000.0}, {'book_id': 'bookid_70', 'decade': 2010.0}, {'book_id': 'bookid_71', 'decade': 1990.0}, {'book_id': 'bookid_72', 'decade': 2010.0}, {'book_id': 'bookid_73', 'decade': 2010.0}, {'book_id': 'bookid_74', 'decade': 2020.0}, {'book_id': 'bookid_75', 'decade': 1980.0}, {'book_id': 'bookid_81', 'decade': None}, {'book_id': 'bookid_76', 'decade': 2010.0}, {'book_id': 'bookid_77', 'decade': 2000.0}, {'book_id': 'bookid_78', 'decade': 2010.0}, {'book_id': 'bookid_79', 'decade': 2010.0}, {'book_id': 'bookid_80', 'decade': 1980.0}, {'book_id': 'bookid_82', 'decade': 1990.0}, {'book_id': 'bookid_83', 'decade': 2020.0}, {'book_id': 'bookid_84', 'decade': 2010.0}, {'book_id': 'bookid_85', 'decade': None}, {'book_id': 'bookid_86', 'decade': 2000.0}, {'book_id': 'bookid_87', 'decade': 1980.0}, {'book_id': 'bookid_88', 'decade': 2000.0}, {'book_id': 'bookid_89', 'decade': 2010.0}, {'book_id': 'bookid_90', 'decade': None}, {'book_id': 'bookid_91', 'decade': 2010.0}, {'book_id': 'bookid_92', 'decade': 2010.0}, {'book_id': 'bookid_93', 'decade': None}, {'book_id': 'bookid_94', 'decade': 2000.0}, {'book_id': 'bookid_95', 'decade': None}, {'book_id': 'bookid_96', 'decade': 2010.0}, {'book_id': 'bookid_97', 'decade': None}, {'book_id': 'bookid_98', 'decade': 2010.0}, {'book_id': 'bookid_99', 'decade': 2010.0}, {'book_id': 'bookid_100', 'decade': 2000.0}, {'book_id': 'bookid_101', 'decade': 2010.0}, {'book_id': 'bookid_102', 'decade': None}, {'book_id': 'bookid_103', 'decade': None}, {'book_id': 'bookid_104', 'decade': None}, {'book_id': 'bookid_105', 'decade': 1980.0}, {'book_id': 'bookid_106', 'decade': 2000.0}, {'book_id': 'bookid_107', 'decade': 2020.0}, {'book_id': 'bookid_108', 'decade': 2020.0}, {'book_id': 'bookid_164', 'decade': 1880.0}, {'book_id': 'bookid_109', 'decade': 1990.0}, {'book_id': 'bookid_110', 'decade': None}, {'book_id': 'bookid_111', 'decade': None}, {'book_id': 'bookid_112', 'decade': None}, {'book_id': 'bookid_113', 'decade': 2010.0}, {'book_id': 'bookid_114', 'decade': 2000.0}, {'book_id': 'bookid_115', 'decade': None}, {'book_id': 'bookid_116', 'decade': 2000.0}, {'book_id': 'bookid_117', 'decade': 2000.0}, {'book_id': 'bookid_118', 'decade': 1990.0}, {'book_id': 'bookid_119', 'decade': 2010.0}, {'book_id': 'bookid_120', 'decade': 2010.0}, {'book_id': 'bookid_127', 'decade': 1930.0}, {'book_id': 'bookid_184', 'decade': None}, {'book_id': 'bookid_121', 'decade': 2000.0}, {'book_id': 'bookid_122', 'decade': 2020.0}, {'book_id': 'bookid_123', 'decade': 2010.0}, {'book_id': 'bookid_124', 'decade': 2010.0}, {'book_id': 'bookid_125', 'decade': 2000.0}, {'book_id': 'bookid_126', 'decade': 1980.0}, {'book_id': 'bookid_128', 'decade': 2010.0}, {'book_id': 'bookid_129', 'decade': 1970.0}, {'book_id': 'bookid_130', 'decade': 2020.0}, {'book_id': 'bookid_131', 'decade': 1990.0}, {'book_id': 'bookid_132', 'decade': 2010.0}, {'book_id': 'bookid_133', 'decade': 2000.0}, {'book_id': 'bookid_134', 'decade': None}, {'book_id': 'bookid_135', 'decade': 2010.0}, {'book_id': 'bookid_136', 'decade': 2010.0}, {'book_id': 'bookid_137', 'decade': 2010.0}, {'book_id': 'bookid_138', 'decade': 2000.0}, {'book_id': 'bookid_139', 'decade': 2010.0}, {'book_id': 'bookid_140', 'decade': 2020.0}, {'book_id': 'bookid_141', 'decade': 2010.0}, {'book_id': 'bookid_142', 'decade': None}, {'book_id': 'bookid_143', 'decade': 2000.0}, {'book_id': 'bookid_144', 'decade': 2010.0}, {'book_id': 'bookid_145', 'decade': 1980.0}, {'book_id': 'bookid_156', 'decade': 2000.0}, {'book_id': 'bookid_146', 'decade': 2020.0}, {'book_id': 'bookid_147', 'decade': None}, {'book_id': 'bookid_148', 'decade': 2010.0}, {'book_id': 'bookid_149', 'decade': None}, {'book_id': 'bookid_150', 'decade': 2010.0}, {'book_id': 'bookid_157', 'decade': 2000.0}, {'book_id': 'bookid_151', 'decade': 2000.0}, {'book_id': 'bookid_152', 'decade': 2010.0}, {'book_id': 'bookid_153', 'decade': 2010.0}, {'book_id': 'bookid_154', 'decade': 2010.0}, {'book_id': 'bookid_155', 'decade': None}, {'book_id': 'bookid_158', 'decade': 2020.0}, {'book_id': 'bookid_159', 'decade': 2010.0}, {'book_id': 'bookid_160', 'decade': 2000.0}, {'book_id': 'bookid_161', 'decade': 2010.0}, {'book_id': 'bookid_162', 'decade': 2010.0}, {'book_id': 'bookid_163', 'decade': None}, {'book_id': 'bookid_165', 'decade': 2000.0}, {'book_id': 'bookid_166', 'decade': None}, {'book_id': 'bookid_167', 'decade': None}, {'book_id': 'bookid_168', 'decade': 2000.0}, {'book_id': 'bookid_169', 'decade': 1990.0}, {'book_id': 'bookid_170', 'decade': 2020.0}, {'book_id': 'bookid_171', 'decade': 2010.0}, {'book_id': 'bookid_172', 'decade': 2000.0}, {'book_id': 'bookid_173', 'decade': 2000.0}, {'book_id': 'bookid_174', 'decade': None}, {'book_id': 'bookid_175', 'decade': 2000.0}, {'book_id': 'bookid_176', 'decade': 2010.0}, {'book_id': 'bookid_177', 'decade': 2010.0}, {'book_id': 'bookid_178', 'decade': 2010.0}, {'book_id': 'bookid_179', 'decade': 2010.0}, {'book_id': 'bookid_180', 'decade': 2010.0}, {'book_id': 'bookid_181', 'decade': None}, {'book_id': 'bookid_182', 'decade': None}, {'book_id': 'bookid_183', 'decade': None}, {'book_id': 'bookid_185', 'decade': 2010.0}, {'book_id': 'bookid_186', 'decade': None}, {'book_id': 'bookid_187', 'decade': 2010.0}, {'book_id': 'bookid_188', 'decade': 2000.0}, {'book_id': 'bookid_189', 'decade': 2000.0}, {'book_id': 'bookid_190', 'decade': None}, {'book_id': 'bookid_191', 'decade': 2010.0}, {'book_id': 'bookid_192', 'decade': None}, {'book_id': 'bookid_193', 'decade': 2000.0}, {'book_id': 'bookid_194', 'decade': 2010.0}, {'book_id': 'bookid_195', 'decade': 2010.0}, {'book_id': 'bookid_196', 'decade': 2010.0}, {'book_id': 'bookid_197', 'decade': 2010.0}, {'book_id': 'bookid_198', 'decade': None}, {'book_id': 'bookid_199', 'decade': None}, {'book_id': 'bookid_200', 'decade': 2000.0}], 'var_function-call-10147937107887987371': 'file_storage/function-call-10147937107887987371.json', 'var_function-call-13320251191390041984': 'No decade meets the criteria of having at least 10 distinct books.', 'var_function-call-12268144106694870139': 'No decade meets the criteria of having at least 10 distinct books.', 'var_function-call-11792275538222188280': 'No decade meets the criteria of having at least 10 distinct books.', 'var_function-call-7641392574650926716': 'No decade meets the criteria of having at least 10 distinct books.', 'var_function-call-17427853686190860066': 'file_storage/function-call-17427853686190860066.json', 'var_function-call-6811193924483894872': 'No decade meets the criteria of having at least 10 distinct books.', 'var_function-call-12712381218153775109': 'No decade meets the criteria of having at least 10 distinct books.', 'var_function-call-8558749293085381850': '[{"book_id":"bookid_1","publication_year":2004.0,"decade":2000.0},{"book_id":"bookid_2","publication_year":1996.0,"decade":1990.0},{"book_id":"bookid_3","publication_year":2012.0,"decade":2010.0},{"book_id":"bookid_4","publication_year":2013.0,"decade":2010.0},{"book_id":"bookid_5","publication_year":2014.0,"decade":2010.0},{"book_id":"bookid_8","publication_year":2015.0,"decade":2010.0},{"book_id":"bookid_10","publication_year":2004.0,"decade":2000.0},{"book_id":"bookid_15","publication_year":2000.0,"decade":2000.0},{"book_id":"bookid_16","publication_year":1997.0,"decade":1990.0},{"book_id":"bookid_19","publication_year":2013.0,"decade":2010.0},{"book_id":"bookid_20","publication_year":2003.0,"decade":2000.0},{"book_id":"bookid_21","publication_year":1945.0,"decade":1940.0},{"book_id":"bookid_24","publication_year":1939.0,"decade":1930.0},{"book_id":"bookid_26","publication_year":1995.0,"decade":1990.0},{"book_id":"bookid_29","publication_year":2017.0,"decade":2010.0},{"book_id":"bookid_33","publication_year":2016.0,"decade":2010.0},{"book_id":"bookid_35","publication_year":2006.0,"decade":2000.0},{"book_id":"bookid_40","publication_year":2012.0,"decade":2010.0},{"book_id":"bookid_42","publication_year":2018.0,"decade":2010.0},{"book_id":"bookid_43","publication_year":2015.0,"decade":2010.0}]'}

exec(code, env_args)
