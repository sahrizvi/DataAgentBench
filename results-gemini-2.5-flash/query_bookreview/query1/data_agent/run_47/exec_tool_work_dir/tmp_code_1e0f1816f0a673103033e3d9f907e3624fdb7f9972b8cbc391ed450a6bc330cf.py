code = """import pandas as pd
import re
import json

# Load data from storage
books_info_path = locals()['var_function-call-13907616134218864720']
review_data_path = locals()['var_function-call-7810034097219618210']

with open(books_info_path, 'r') as f:
    books_info = json.load(f)

with open(review_data_path, 'r') as f:
    review_data = json.load(f)

df_books = pd.DataFrame(books_info)
df_reviews = pd.DataFrame(review_data)

# Extract publication year and calculate decade
def get_publication_year(details):
    year_match = re.search(r'(?:published|released|edition on) (?:January|February|March|April|May|June|July|August|September|October|November|December)?\s*\d{1,2},? (\d{4})', details)
    if year_match:
        return int(year_match.group(1))
    return None

df_books['publication_year'] = df_books['details'].apply(get_publication_year)
df_books = df_books.dropna(subset=['publication_year'])
df_books['decade'] = (df_books['publication_year'] // 10 * 10).astype(int)

# Rename purchase_id to book_id in df_reviews for merging
df_reviews = df_reviews.rename(columns={'purchase_id': 'book_id'})
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'])

# Merge the dataframes
df_merged = pd.merge(df_books, df_reviews, on='book_id')

# Calculate the number of distinct books and average rating per decade
decade_stats = df_merged.groupby('decade').agg(
    distinct_books=('book_id', 'nunique'),
    average_rating=('rating', 'mean')
).reset_index()

# Filter decades with at least 10 distinct books
filtered_decades = decade_stats[decade_stats['distinct_books'] >= 10]

# Find the decade with the highest average rating
if not filtered_decades.empty:
    highest_rated_decade = filtered_decades.loc[filtered_decades['average_rating'].idxmax()]
    result = f'{highest_rated_decade["decade"]}s'
else:
    result = "No decade found with at least 10 distinct books that have been rated."

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_function-call-13907616134218864720': 'file_storage/function-call-13907616134218864720.json', 'var_function-call-7810034097219618210': 'file_storage/function-call-7810034097219618210.json'}

exec(code, env_args)
