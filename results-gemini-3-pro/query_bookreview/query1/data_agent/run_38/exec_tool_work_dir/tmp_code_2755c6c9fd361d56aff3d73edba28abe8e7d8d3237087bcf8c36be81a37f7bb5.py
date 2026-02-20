code = """import json
import re
import pandas as pd

# Load books
with open('var_function-call-853803685077092385.json', 'r') as f:
    books = json.load(f)

# Load reviews
with open('var_function-call-12742188632596164832.json', 'r') as f:
    reviews = json.load(f)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'])

# Function to extract year
def extract_year(row):
    details = row.get('details', '')
    subtitle = row.get('subtitle', '')
    
    # Pattern 1: Month Day, Year in details
    # e.g. "released on January 1, 2004", "published ... on May 20, 1996"
    match = re.search(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+(\d{4})', details)
    if match:
        return int(match.group(1))
    
    # Pattern 2: Year in subtitle (e.g. "Hardcover – May 8, 2012")
    match = re.search(r'–\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+(\d{4})', subtitle)
    if match:
        return int(match.group(1))
        
    # Pattern 3: Simple year finding in details context?
    # "published on May 18, 2014" -> handled by 1
    # "published independently on December 30, 2021" -> handled by 1
    
    return None

df_books['year'] = df_books.apply(extract_year, axis=1)

# Check how many missing years
missing_years = df_books[df_books['year'].isnull()]
print(f"Missing years count: {len(missing_years)}")
if len(missing_years) > 0:
    print(missing_years[['details', 'subtitle']].head().to_dict(orient='records'))

# Create decade
df_books = df_books.dropna(subset=['year'])
df_books['decade'] = (df_books['year'] // 10) * 10
df_books['decade_str'] = df_books['decade'].astype(int).astype(str) + 's'

# Join with reviews
# Fuzzy join: book_id == purchase_id
# The prompt says "book_id" in books_info and "purchase_id" in review refer to the same book entities
merged = pd.merge(df_reviews, df_books, left_on='purchase_id', right_on='book_id', how='inner')

# Aggregation
# 1. Count distinct books per decade
# 2. Avg rating per decade
decade_stats = merged.groupby('decade_str').agg(
    distinct_books=('book_id', 'nunique'),
    avg_rating=('rating', 'mean')
).reset_index()

# Filter
filtered_stats = decade_stats[decade_stats['distinct_books'] >= 10].sort_values('avg_rating', ascending=False)

print("__RESULT__:")
print(filtered_stats.to_json(orient='records'))"""

env_args = {'var_function-call-111364020003070762': ['books_info'], 'var_function-call-3794927622158743902': [{'title': 'Chaucer', 'subtitle': 'Hardcover – Import, January 1, 2004', 'author': '{"avatar": "https://m.media-amazon.com/images/I/21Je2zja9pL._SY600_.jpg", "name": "Peter Ackroyd", "about": ["Peter Ackroyd, (born 5 October 1949) is an English biographer, novelist and critic with a particular interest in the history and culture of London. For his novels about English history and culture and his biographies of, among others, William Blake, Charles Dickens, T. S. Eliot and Sir Thomas More, he won the Somerset Maugham Award and two Whitbread Awards. He is noted for the volume of work he has produced, the range of styles therein, his skill at assuming different voices and the depth of his research.", "He was elected a fellow of the Royal Society of Literature in 1984 and appointed a Commander of the Order of the British Empire in 2003.", "Bio from Wikipedia, the free encyclopedia."]}', 'rating_number': '29', 'features': '[]', 'description': '[]', 'price': '8.23', 'store': 'Peter Ackroyd (Author)', 'categories': '["Books", "Literature & Fiction", "History & Criticism"]', 'details': 'Published by Chatto & Windus, the first edition of this book was released on January 1, 2004. It is written in English and comes in a hardcover format, comprising 196 pages. The book has an ISBN-10 of 0701169850 and an ISBN-13 of 978-0701169855. Weighing 10.1 ounces, its dimensions are 5.39 x 0.71 x 7.48 inches.', 'book_id': 'bookid_1'}, {'title': 'Notes from a Kidwatcher', 'subtitle': 'First Edition', 'author': '{"avatar": "https://m.media-amazon.com/images/I/01Kv-W2ysOL._SY600_.png", "name": "Yetta M. Goodman", "about": ["Discover more of the author’s books, see similar authors, read author blogs and more"]}', 'rating_number': '1', 'features': '["Contains 23 selected articles by this influential writer, researcher, educator, and speaker. They\'re grouped around six major themes inherent in teacher education: culture and community; miscue analysis, reading strategies and comprehension; print awareness and the roots of literacy; the writing process; kidwatching; and whole language theory. No index. Annotation c. by Book News, Inc., Portland, Or."]', 'description': '["About the Author", "SANDRA WILDE, Ph.D., is widely recognized for her expertise in developmental spelling and her advocacy of holistic approaches to spelling and phonics. She is Professor of Curriculum and Instruction at Portland State University in Oregon. She is best known for her work in invented spelling, phonics and miscue analysis. She specializes in showing teachers how kids\' invented spellings and miscues can help us work with them in more sophisticated and learner-centered ways. Looking at what kids do as they read and write is at the heart of Sandra\'s presentations and workshops. She can do lively keynote presentations that highlight the interesting things that we can learn by paying close attention to students\' invented spellings and miscues, as well as workshops of varying lengths that focus on student-centered teaching of spelling and phonics. She has recently begun offering workshops that focus on understanding students\' miscues as a guide to appropriate instruction, p"]', 'price': '3.52', 'store': 'Sandra Wilde (Editor)', 'categories': '["Books", "Reference", "Words, Language & Grammar"]', 'details': 'This book, published by Heinemann in its first edition on May 20, 1996, is written in English and is available in paperback format, consisting of 316 pages. It has an ISBN-10 of 0435088688 and an ISBN-13 of 978-0435088682. The item weighs 1.05 pounds and its dimensions are 6.03 x 0.67 x 8.95 inches.', 'book_id': 'bookid_2'}, {'title': 'Service: A Navy SEAL at War', 'subtitle': 'Hardcover – May 8, 2012', 'author': '{"avatar": "https://m.media-amazon.com/images/I/31rBoNEHiFL._SY600_.jpg", "name": "Marcus Luttrell", "about": ["Petty Officer First Class Marcus Luttrell was born in Huntsville, Texas in 1975."]}', 'rating_number': '3421', 'features': '["Marcus Luttrell, author of the #1 bestseller", "Lone Survivor", ", share war stories about true American heroism from himself and other soldiers who bravely fought alongside him.", "Navy SEAL Marcus Luttrell returned from his star-crossed mission in Afghanistan with his bones shattered and his heart broken. So many had given their lives to save him -- and he would have readily done the same for them. As he recuperated, he wondered why he and others, from America\'s founding to today, had been willing to sacrifice everything-including themselves-for the sake of family, nation, and freedom.  In", "Service", ", we follow Marcus Luttrell to Iraq, where he returns to the battlefield as a member of SEAL Team 5 to help take on the most dangerous city in the world: Ramadi, the capital of war-torn Al Anbar Province. There, in six months of high-intensity urban combat, he would be part of what has been called the greatest victory in the history of U.S. Special Operations forces. We also return to Afghanistan and Operation Redwing, where Luttrell offers powerful new details about his miraculous rescue. Throughout, he reflects on what it really means to take on a higher calling, about the men he\'s seen lose their lives for their country, and the legacy of those who came and bled before.  A thrilling war story,", "Service", "is also a profoundly moving tribute to the warrior brotherhood, to the belief that nobody goes it alone, and no one will be left behind."]', 'description': '["Review", "Praise for SERVICE\\"An action-packed...reflective saga of contemporary military service.\\"―", "Kirkus Reviews", "\\"Marcus Luttrell, with James D. Hornfischer, has written another emotional story that the reader will not want to put down.\\"―", "American Thinker", "About the Author", "Marcus Luttrell", "became a combat-trained Navy SEAL in 2002 and served in many dangerous Special Operations assignments around the world. He is the author of the", "New York Times", "bestseller", "Lone Survivor", ", and is a popular corporate and organizational speaker. He lives near Houston, Texas.\xa0James D. Hornfischer\xa0is the author of four bestselling books on the U.S. Navy in World War II,", "The Fleet at Flood", "Tide", ",", "Neptune\'s", "Inferno, Ship of Ghosts,", "and", "The Last Stand of the Tin Can Sailors,", "winner of the Samuel Eliot Morison Award. He lives in Austin, Texas."]', 'price': '17.17', 'store': 'Marcus Luttrell (Author),  James D. Hornfischer', 'categories': '["Books", "Biographies & Memoirs", "Leaders & Notable People"]', 'details': 'This book, published by Little, Brown and Company in its first edition on May 8, 2012, is available in English and is bound as a hardcover with a total of 384 pages. It has an ISBN-10 of 9780316185363 and an ISBN-13 of 978-0316185363. The item weighs 1.4 pounds and its dimensions are 6.25 inches in width, 1.55 inches in depth, and 9.55 inches in height.', 'book_id': 'bookid_3'}], 'var_function-call-15580473518099249470': [{'count': '200'}], 'var_function-call-674724490891876978': [{'COUNT(*)': '1833'}], 'var_function-call-853803685077092385': 'file_storage/function-call-853803685077092385.json', 'var_function-call-12742188632596164832': 'file_storage/function-call-12742188632596164832.json'}

exec(code, env_args)
