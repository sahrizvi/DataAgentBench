code = """import json
with open(var_call_0K4vCMKr1SXV0J6AA7PpNF53, 'r') as f:
    data = json.load(f)

if not data:
    out_str = "No matching books found."
else:
    lines = []
    for b in data:
        title = b.get('title') or ''
        bid = b.get('book_id') or ''
        avg = b.get('average_rating')
        cnt = b.get('review_count')
        lines.append('- {} (book_id: {}) - average_rating: {}, review_count: {}'.format(title, bid, avg, cnt))
    out_str = "\n".join(lines)

print("__RESULT__:")
print(json.dumps(out_str))"""

env_args = {'var_call_pjCtQvecYsH4jHPnp1Li6D7Y': ['books_info'], 'var_call_vhPkybGtfIBe6ysQofGklOYQ': 'file_storage/call_vhPkybGtfIBe6ysQofGklOYQ.json', 'var_call_jWLnIzcvOYNihhGirovQ0cAi': 'file_storage/call_jWLnIzcvOYNihhGirovQ0cAi.json', 'var_call_0K4vCMKr1SXV0J6AA7PpNF53': 'file_storage/call_0K4vCMKr1SXV0J6AA7PpNF53.json'}

exec(code, env_args)
