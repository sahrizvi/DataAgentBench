code = """import json, re
from pathlib import Path
import pandas as pd

books_path = Path(var_call_CUdkO2yEe1cPmTYus0qHCUgo)
reviews_path = Path(var_call_x83zbwbj5mEwvUZg0qHCUgo) if False else Path(var_call_x83zbwbj5mEwvUZg0hsrUepd)

books = json.load(books_path.open('r', encoding='utf-8'))
reviews = json.load(reviews_path.open('r', encoding='utf-8'))

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# extract numeric id
def extract_num(s):
    if not isinstance(s, str):
        return None
    m = re.search(r"(\d+)", s)
    return int(m.group(1)) if m else None

books_df['num'] = books_df['book_id'].apply(extract_num)
reviews_df['num'] = reviews_df['purchase_id'].apply(extract_num)

# robust year extraction
pattern_pub = re.compile(r"(?:published|published by|first edition|reprint edition|published independently|edition|published in|released on|released).*?(1[5-9]\d{2}|20\d{2})", re.IGNORECASE)
pattern_year = re.compile(r"\b(1[5-9]\d{2}|20\d{2})\b")

def extract_year(detail):
    if not isinstance(detail, str):
        return None
    # try published pattern
    m = pattern_pub.findall(detail)
    if m:
        # m is list of year strings; pick last
        for y in reversed(m):
            yi = int(y)
            if 1500 <= yi <= 2023:
                return yi
    # fallback: find all years, prefer >= 1800 then >=1500
    all_y = pattern_year.findall(detail)
    if not all_y:
        return None
    # convert to ints and filter
    ys = [int(y) for y in all_y if 1500 <= int(y) <= 2023]
    if not ys:
        return None
    # prefer years >= 1800
    ys1800 = [y for y in ys if y >= 1800]
    if ys1800:
        return ys1800[0]
    return ys[0]

books_df['year'] = books_df['details'].apply(extract_year)

# prepare reviews: convert rating to numeric
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')
reviews_df = reviews_df[reviews_df['rating'].notna()]

# merge on numeric id
merged = pd.merge(reviews_df, books_df[['num','book_id','title','year']], on='num', how='inner')
merged = merged[merged['year'].notna()]
merged['year'] = merged['year'].astype(int)
merged['decade'] = merged['year'].apply(lambda y: f"{(y//10)*10}s")

# per-book average rating
book_avg = merged.groupby('num').agg(book_id=('book_id','first'), title=('title','first'), year=('year','first'), decade=('decade','first'), avg_rating=('rating','mean'), n_reviews=('rating','count')).reset_index()

# per-decade stats
decade_stats = book_avg.groupby('decade').agg(book_count=('num','nunique'), decade_avg_rating=('avg_rating','mean')).reset_index()

# eligible decades with at least 10 distinct books
eligible = decade_stats[decade_stats['book_count'] >= 10].copy()

result = {'total_books': int(len(books_df)), 'total_reviews': int(len(reviews_df)), 'books_with_year': int(books_df['year'].notna().sum()), 'books_with_reviews_and_year': int(book_avg.shape[0]), 'eligible_decades': []}

for _, row in eligible.iterrows():
    result['eligible_decades'].append({'decade': row['decade'], 'book_count': int(row['book_count']), 'decade_avg_rating': round(float(row['decade_avg_rating']),4)})

if not eligible.empty:
    best = eligible.sort_values(by=['decade_avg_rating','book_count'], ascending=[False,False]).iloc[0]
    result['best_decade'] = {'decade': best['decade'], 'book_count': int(best['book_count']), 'average_rating': round(float(best['decade_avg_rating']),4)}
else:
    result['best_decade'] = None

print('__RESULT__:')
print(json.dumps(result))"""

env_args = {'var_call_t8ICoTdZa5hhfV8cD7hQJlQf': ['books_info'], 'var_call_CUdkO2yEe1cPmTYus0qHCUgo': 'file_storage/call_CUdkO2yEe1cPmTYus0qHCUgo.json', 'var_call_GRCXW9zYHtaqYli2lmJg1NBh': ['review'], 'var_call_x83zbwbj5mEwvUZg0hsrUepd': 'file_storage/call_x83zbwbj5mEwvUZg0hsrUepd.json', 'var_call_pWym9YvF1umLsL0l4XXJaoQ8': {'best_decade': None, 'average_rating': None, 'book_count': 0}, 'var_call_ZmhAUewJuPHzFH1v3EarTie1': {'num_books': 200, 'num_reviews': 1833, 'unique_book_nums': 200, 'unique_review_nums': 200, 'intersection_count': 200, 'intersection_sample': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50], 'full_string_intersection_count': 0, 'full_string_intersection_sample': []}, 'var_call_TWCmnCYiL3FCciTypj0C9tpF': {'total_books_in_books_table': 200, 'total_reviews_in_review_table': 1833, 'books_with_extracted_year': 0, 'books_with_reviews_and_year': 0, 'decade_stats_all': [], 'eligible_decades': [], 'best_decade': None}, 'var_call_8wZxvTpvXiCZV2BpsZZS2Nc4': 'file_storage/call_8wZxvTpvXiCZV2BpsZZS2Nc4.json', 'var_call_PlAwzN692QXrOojgNVfanzsd': {'count_matches': 192, 'examples': [{'book_id': 'bookid_1', 'matches': ['2004', '1698', '1698'], 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of'}, {'book_id': 'bookid_2', 'matches': ['1996'], 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN'}, {'book_id': 'bookid_3', 'matches': ['2012', '1618', '1618'], 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363'}, {'book_id': 'bookid_4', 'matches': ['2013'], 'details': 'This book, published by Scholastic Paperbacks in a reprint edition on October 29, 2013, is written in English and consists of 64 pages. It has an ISBN-10 of 0545425573 and an ISBN-13 of 978-0545425575'}, {'book_id': 'bookid_5', 'matches': ['2014', '1542'], 'details': 'The book was published on May 18, 2014, and is available in English. It has a file size of 1542 KB and allows for unlimited simultaneous device usage. Text-to-speech functionality is enabled, and it s'}, {'book_id': 'bookid_6', 'matches': ['2021'], 'details': 'This book, published independently on December 30, 2021, is written in English and consists of 24 pages. It has an ISBN 13 of 979-8528537702 and weighs 3.2 ounces. The dimensions of the book are 7 x 0'}, {'book_id': 'bookid_7', 'matches': ['2004', '1994'], 'details': 'The book, published by Guilford in its second edition in January 2004, is also noted as the 8082nd edition from January 1, 1994. It has a remarkably light item weight of just 0.01 ounces.'}, {'book_id': 'bookid_8', 'matches': ['2015', '1680', '1680'], 'details': 'This book, published by Make Community, LLC, in its second edition on September 22, 2015, is available in English and spans 352 pages in paperback format. It has an ISBN of 9781680450262 for the 10-di'}, {'book_id': 'bookid_9', 'matches': ['2019', '1694', '1731', '1694', '1733'], 'details': 'This book, published independently on September 25, 2019, is written in English and spans 367 pages. It is available in paperback format and has an ISBN-10 of 1694621731 and an ISBN-13 of 978-16946217'}, {'book_id': 'bookid_10', 'matches': ['2004', '1932', '1932'], 'details': 'This book, published by WallBuilder Press in its first edition on November 8, 2004, is available in English and comprises 51 pages in paperback format. It has an ISBN-10 of 1932225323 and an ISBN-13 o'}, {'book_id': 'bookid_11', 'matches': ['1993', '1673', '1673'], 'details': 'Published by Caxton Press on January 1, 1993, this book is available in English and spans 407 pages. It has an ISBN-10 of 0893011673 and an ISBN-13 of 978-0893011673. Weighing 1.51 pounds, the book me'}, {'book_id': 'bookid_12', 'matches': ['2022'], 'details': 'This book, published by Lisette Marshall on May 29, 2022, is written in English and is available in paperback, comprising 215 pages. It has an ISBN 10 number of 9083256898 and an ISBN 13 number of 978'}, {'book_id': 'bookid_13', 'matches': ['2023', '1771', '1771'], 'details': 'The book, published by Central Avenue Publishing on January 24, 2023, is available in English and comes in paperback format, consisting of 144 pages. It has an ISBN-10 number of 1771682760 and an ISBN'}, {'book_id': 'bookid_14', 'matches': ['2019'], 'details': 'The book, published by Jessica Mathews, LLC on November 13, 2019, is written in English and features a paperback format comprising 26 pages. It has an ISBN-10 of 1087848539 and an ISBN-13 of 978-10878'}, {'book_id': 'bookid_15', 'matches': ['2000'], 'details': 'The book is published by Kegan Paul and is a first edition released on November 15, 2000. It is written in English and is available in hardcover, comprising 348 pages. The ISBN-10 for this edition is '}, {'book_id': 'bookid_16', 'matches': ['1997'], 'details': 'This book is published by Prentice Hall College Division and is in its third edition, released on January 1, 1997. It is written in English and is available in paperback, consisting of 390 pages. The '}, {'book_id': 'bookid_17', 'matches': ['1987'], 'details': 'This book, published by Edelsa Grupo Didascalia in a September 1, 1987 edition, is written in Spanish and consists of 44 pages. It has an ISBN-10 number of 8477110190 and an ISBN-13 number of 978-8477'}, {'book_id': 'bookid_18', 'matches': ['2012'], 'details': 'The book, published by Gale, Sabin Americana on February 21, 2012, is written in English and is available in paperback format, comprising 26 pages. It has an ISBN-10 of 1275627234 and an ISBN-13 of 97'}, {'book_id': 'bookid_19', 'matches': ['2013', '2013', '1609', '1609'], 'details': 'The book, published by Foundation Press in its 2013th edition on March 22, 2013, is available in English and spans 355 pages. It has an ISBN-10 number of 1609303687 and an ISBN-13 number of 978-160930'}, {'book_id': 'bookid_20', 'matches': ['2003'], 'details': 'The book, published by Soho Crime in a revised edition on July 1, 2003, is available in English and has a total print length of 372 pages. It has a file size of 2295 KB and supports various features s'}], 'no_match_samples': []}}

exec(code, env_args)
