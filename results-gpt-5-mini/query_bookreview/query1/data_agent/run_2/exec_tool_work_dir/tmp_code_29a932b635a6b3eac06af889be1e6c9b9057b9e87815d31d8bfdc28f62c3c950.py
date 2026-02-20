code = """import json
import re
import pandas as pd

# Load the query results from the provided storage file paths
books_path = var_call_pJMGKMAM0uO6MWj8hwBVhYxe
reviews_path = var_call_4tzooUmPjgZPvUh76KZQSzTi

with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(reviews_path, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Normalize ratings
# Some ratings may be strings; convert to numeric
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

# Map purchase_id like 'purchaseid_186' -> book_id 'bookid_186'
def purchase_to_book(purchase_id):
    if not isinstance(purchase_id, str):
        return None
    m = re.search(r'(\d+)$', purchase_id)
    if m:
        return f"bookid_{m.group(1)}"
    return None

df_reviews['book_id'] = df_reviews['purchase_id'].apply(purchase_to_book)

# Compute per-book average rating
book_avg = df_reviews.dropna(subset=['book_id']).groupby('book_id', as_index=False)['rating'].mean().rename(columns={'rating':'book_avg_rating'})

# Extract publication year from books.details using regex for years 1700-2029
year_re = re.compile(r'\b(17\d{2}|18\d{2}|19\d{2}|20\d{2})\b')

def extract_year(details):
    if not isinstance(details, str):
        return None
    m = year_re.search(details)
    if m:
        try:
            y = int(m.group(0))
            return y
        except:
            return None
    return None

# Ensure details column exists
if 'details' not in df_books.columns:
    df_books['details'] = None

df_books['pub_year'] = df_books['details'].apply(extract_year)

# Merge book_avg with books to get publication year
df = pd.merge(book_avg, df_books[['book_id','title','pub_year']], on='book_id', how='left')

# Drop books without pub_year
df = df.dropna(subset=['pub_year'])

# Compute decade label
df['pub_year'] = df['pub_year'].astype(int)

def year_to_decade_label(year):
    decade = (year // 10) * 10
    return f"{decade}s"

df['decade'] = df['pub_year'].apply(year_to_decade_label)

# Group by decade: count distinct books and average of book_avg_rating
decade_stats = df.groupby('decade').agg(num_books=('book_id','nunique'), avg_rating=('book_avg_rating','mean')).reset_index()

# Filter decades with at least 10 distinct books
decade_stats_filtered = decade_stats[decade_stats['num_books'] >= 10]

# If no decade meets threshold, prepare a message
if decade_stats_filtered.empty:
    result = {"decade": None, "average_rating": None, "num_books": 0}
else:
    # Find decade with highest avg_rating
    best = decade_stats_filtered.sort_values(['avg_rating','decade'], ascending=[False, True]).iloc[0]
    result = {
        "decade": best['decade'],
        "average_rating": round(float(best['avg_rating']), 4),
        "num_books": int(best['num_books'])
    }

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_QBrgVNBPSNfetWFUNw5xwdES': ['books_info'], 'var_call_pJMGKMAM0uO6MWj8hwBVhYxe': 'file_storage/call_pJMGKMAM0uO6MWj8hwBVhYxe.json', 'var_call_PEWtYxJoP3K9OvaUdBpAry8O': ['review'], 'var_call_4tzooUmPjgZPvUh76KZQSzTi': 'file_storage/call_4tzooUmPjgZPvUh76KZQSzTi.json'}

exec(code, env_args)
