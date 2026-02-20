code = """import json
import re
import pandas as pd

# Load data from storage file paths
with open(var_call_TaVbWojF1K4ti0UmPdPayB35, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(var_call_SVajvW0ONUkTJipN3Gjf3rA1, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# Clean reviews ratings
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')
# Map purchase_id -> book_id by replacing prefix
reviews_df['book_id'] = reviews_df['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_', regex=False)

# Merge reviews with books on book_id
merged = reviews_df.merge(books_df[['book_id', 'details']], on='book_id', how='left')

# Function to extract first plausible year from details
def extract_year(detail):
    if not isinstance(detail, str):
        return None
    # find all 4-digit numbers
    years = re.findall(r'\b(1[0-9]{3}|20[0-2][0-9]|2023)\b', detail)
    if not years:
        return None
    # return first as int
    try:
        return int(years[0])
    except:
        return None

merged['year'] = merged['details'].apply(extract_year)

# Drop rows without year or rating
merged = merged.dropna(subset=['year', 'rating'])
merged['year'] = merged['year'].astype(int)

# Compute per-book average rating (across its reviews)
book_avg = merged.groupby('book_id', as_index=False).agg({'rating':'mean','year':'first'})
book_avg.rename(columns={'rating':'avg_rating'}, inplace=True)

# Compute decade label
book_avg['decade_start'] = (book_avg['year'] // 10) * 10
book_avg['decade'] = book_avg['decade_start'].astype(int).astype(str) + 's'

# For each decade, compute count of distinct books and average of per-book averages
decade_stats = book_avg.groupby('decade').agg(book_count=('book_id','nunique'), decade_avg_rating=('avg_rating','mean')).reset_index()

# Filter decades with at least 10 distinct books
eligible = decade_stats[decade_stats['book_count'] >= 10]

result_decade = None
if not eligible.empty:
    # find decade with highest average rating
    best = eligible.loc[eligible['decade_avg_rating'].idxmax()]
    result_decade = best['decade']

# Print according to required format
print("__RESULT__:")
print(json.dumps(result_decade))"""

env_args = {'var_call_D4wz8M4eWTZ4Gbz4SLgnwqBm': ['books_info'], 'var_call_TaVbWojF1K4ti0UmPdPayB35': 'file_storage/call_TaVbWojF1K4ti0UmPdPayB35.json', 'var_call_SVajvW0ONUkTJipN3Gjf3rA1': 'file_storage/call_SVajvW0ONUkTJipN3Gjf3rA1.json'}

exec(code, env_args)
