code = """import json, re, pandas as pd

def load_result(var):
    if isinstance(var, str):
        with open(var, 'r', encoding='utf-8') as f:
            return json.load(f)
    return var

books = load_result(var_call_m9vGMguVk4UFHghf1KFvNHe0)
reviews = load_result(var_call_FC8zlhbN2qjSJYbYVQDju2Wx)

# Extract publication year from details text
pat = re.compile(r'\b(19\d{2}|20\d{2})\b')
book_year = {}
for r in books:
    bid = r.get('book_id')
    det = r.get('details') or ''
    m = pat.findall(det)
    if not m:
        continue
    # choose earliest plausible year as publication year
    years = [int(x) for x in m]
    y = min(years)
    if 1500 <= y <= 2026:
        book_year[bid] = y

# ratings per book from reviews. Need fuzzy join purchaseid_X -> bookid_X
rat_sum = {}
rat_cnt = {}
for rr in reviews:
    pid = rr.get('purchase_id')
    if not pid:
        continue
    # map purchaseid_123 -> bookid_123
    mapped = pid.replace('purchaseid_', 'bookid_')
    if mapped not in book_year:
        continue
    try:
        rating = float(rr.get('rating'))
    except Exception:
        continue
    rat_sum[mapped] = rat_sum.get(mapped, 0.0) + rating
    rat_cnt[mapped] = rat_cnt.get(mapped, 0) + 1

# compute average rating per distinct book
book_avg = []
for bid, cnt in rat_cnt.items():
    if cnt > 0:
        book_avg.append({'book_id': bid, 'year': book_year[bid], 'avg_rating': rat_sum[bid]/cnt})

if not book_avg:
    out = None
else:
    df = pd.DataFrame(book_avg)
    df['decade_start'] = (df['year']//10)*10
    # decades with at least 10 distinct rated books
    grp = df.groupby('decade_start').agg(n_books=('book_id','nunique'), avg_rating=('avg_rating','mean')).reset_index()
    grp = grp[grp['n_books']>=10]
    if grp.empty:
        out = None
    else:
        best = grp.sort_values(['avg_rating','n_books'], ascending=[False,False]).iloc[0]
        decade_label = f"{int(best['decade_start'])}s"
        out = {'decade': decade_label, 'average_rating': float(best['avg_rating']), 'distinct_rated_books': int(best['n_books'])}

print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_m9vGMguVk4UFHghf1KFvNHe0': 'file_storage/call_m9vGMguVk4UFHghf1KFvNHe0.json', 'var_call_FC8zlhbN2qjSJYbYVQDju2Wx': 'file_storage/call_FC8zlhbN2qjSJYbYVQDju2Wx.json'}

exec(code, env_args)
