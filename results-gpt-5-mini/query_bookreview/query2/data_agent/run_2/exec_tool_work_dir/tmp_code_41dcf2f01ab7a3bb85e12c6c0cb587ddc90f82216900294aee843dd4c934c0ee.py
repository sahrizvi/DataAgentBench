code = """import json, re
# Load the review aggregates (already a Python list in storage)
reviews = var_call_j9e6mjOQ50932YI73jcEldhF

# Load the books_info result from the JSON file path stored in var_call_V3ecZJ1jjLrqdLg2iLn5I9zn
books_file_path = var_call_V3ecZJ1jjLrqdLg2iLn5I9zn
with open(books_file_path, 'r', encoding='utf-8') as f:
    books = json.load(f)

# Build a dict of books by book_id for quick lookup
books_by_id = {b.get('book_id'): b for b in books}

results = []
for r in reviews:
    pid = r.get('purchase_id')
    m = re.search(r"(\d+)$", pid or "")
    if not m:
        continue
    num = m.group(1)
    mapped_bid = f'bookid_{num}'
    book = books_by_id.get(mapped_bid)
    if not book:
        # try other possible mappings (no leading zeros expected)
        continue
    categories = book.get('categories') or ''
    details = book.get('details') or ''
    # Check if categories include Literature & Fiction (case-insensitive)
    if 'literature & fiction' in categories.lower():
        # Check if details mention English language
        if 'english' in details.lower():
            # Prepare output record
            out = {
                'purchase_id': pid,
                'mapped_book_id': mapped_bid,
                'title': book.get('title'),
                'author': book.get('author'),
                'categories': categories,
                'details': details,
                'avg_rating': float(r.get('avg_rating')) if r.get('avg_rating') is not None else None,
                'review_count': int(r.get('cnt')) if r.get('cnt') is not None else None
            }
            results.append(out)

# Deduplicate by mapped_book_id
unique = {}
for rec in results:
    unique[rec['mapped_book_id']] = rec
final = list(unique.values())

print('__RESULT__:')
print(json.dumps(final))"""

env_args = {'var_call_Gx7SD7lUL0Fo9dM89LiYseaM': ['books_info'], 'var_call_j9e6mjOQ50932YI73jcEldhF': [{'purchase_id': 'purchaseid_101', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_105', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_108', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_110', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_114', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_116', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_117', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_118', 'avg_rating': '5.0', 'cnt': '6'}, {'purchase_id': 'purchaseid_12', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_121', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_122', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_123', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_124', 'avg_rating': '5.0', 'cnt': '4'}, {'purchase_id': 'purchaseid_126', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_127', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_128', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_130', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_132', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_133', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_134', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_14', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_143', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_144', 'avg_rating': '5.0', 'cnt': '6'}, {'purchase_id': 'purchaseid_146', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_150', 'avg_rating': '5.0', 'cnt': '11'}, {'purchase_id': 'purchaseid_151', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_152', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_153', 'avg_rating': '5.0', 'cnt': '15'}, {'purchase_id': 'purchaseid_156', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_16', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_160', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_163', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_166', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_168', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_170', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_171', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_172', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_174', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_177', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_180', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_181', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_182', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_184', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_192', 'avg_rating': '5.0', 'cnt': '6'}, {'purchase_id': 'purchaseid_195', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_197', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_2', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_21', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_24', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_26', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_28', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_29', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_33', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_34', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_38', 'avg_rating': '5.0', 'cnt': '4'}, {'purchase_id': 'purchaseid_39', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_40', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_41', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_42', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_47', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_54', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_56', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_57', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_59', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_6', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_60', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_64', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_7', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_71', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_73', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_74', 'avg_rating': '5.0', 'cnt': '8'}, {'purchase_id': 'purchaseid_75', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_79', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_80', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_82', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_83', 'avg_rating': '5.0', 'cnt': '14'}, {'purchase_id': 'purchaseid_84', 'avg_rating': '5.0', 'cnt': '2'}, {'purchase_id': 'purchaseid_88', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_9', 'avg_rating': '5.0', 'cnt': '3'}, {'purchase_id': 'purchaseid_90', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_91', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_97', 'avg_rating': '5.0', 'cnt': '1'}, {'purchase_id': 'purchaseid_98', 'avg_rating': '5.0', 'cnt': '1'}], 'var_call_V3ecZJ1jjLrqdLg2iLn5I9zn': 'file_storage/call_V3ecZJ1jjLrqdLg2iLn5I9zn.json'}

exec(code, env_args)
