import sqlite3
import duckdb
import pandas as pd
import numpy as np
from pathlib import Path

# -----------------------------
# Config
# -----------------------------
RAW_CSV = "/home/ruiying/DataAgentBench/query_music_brainz_20k/musicbrainz-20-A01.csv"
SQLITE_DB = "/home/ruiying/DataAgentBench/query_music_brainz_20k/query_dataset/catalog.db"
DUCKDB_DB = "/home/ruiying/DataAgentBench/query_music_brainz_20k/query_dataset/sales.duckdb"
RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)

# -----------------------------
# Load raw dataset
# -----------------------------
df = pd.read_csv(RAW_CSV)

# # Normalize column names (defensive)
# df.columns = [c.lower() for c in df.columns]

# -----------------------------
# Create SQLite DB: music_catalog
# -----------------------------
sqlite_conn = sqlite3.connect(SQLITE_DB)

tracks_raw = df[[
    "tid",
    "sourceid",
    "id",
    "title",
    "length",
    "artist",
    "album",
    "year",
    "language"
]].rename(columns={
    "sourceid": "source_id",
    "id": "source_track_id"
})

tracks_raw.to_sql(
    "tracks_raw",
    sqlite_conn,
    if_exists="replace",
    index=False
)

sqlite_conn.commit()
sqlite_conn.close()

print("SQLite database created: tracks_raw")

# -----------------------------
# Create DuckDB DB: music_sales
# -----------------------------
duck = duckdb.connect(DUCKDB_DB)

duck.execute("""
CREATE TABLE sales (
    sale_id INTEGER,
    sale_date DATE,
    country TEXT,
    store TEXT,
    track_title TEXT,
    artist_name TEXT,
    album_name TEXT,
    units_sold INTEGER,
    revenue_usd DOUBLE
)
""")

# -----------------------------
# Generate synthetic sales data
# -----------------------------
def perturb_string(s):
    if pd.isna(s):
        return s
    s = str(s)
    if len(s) > 8 and np.random.rand() < 0.4:
        return s[:np.random.randint(5, len(s))]
    if np.random.rand() < 0.3:
        return s.lower()
    return s

sales_rows = []
sale_id = 1

for _, row in df.iterrows():
    if np.random.rand() < 0.6:  # not every track gets sales
        continue

    num_sales = np.random.randint(1, 4)
    for _ in range(num_sales):
        sales_rows.append({
            "sale_id": sale_id,
            "sale_date": pd.Timestamp(
                year=np.random.randint(2000, 2024),
                month=np.random.randint(1, 13),
                day=np.random.randint(1, 28)
            ),
            "country": np.random.choice(["US", "FR", "DE", "UK"]),
            "store": np.random.choice(["iTunes", "Amazon", "Bandcamp"]),
            "track_title": perturb_string(row["title"]),
            "artist_name": perturb_string(row["artist"]),
            "album_name": perturb_string(row["album"]),
            "units_sold": np.random.randint(1, 20),
            "revenue_usd": round(np.random.uniform(0.99, 15.99), 2)
        })
        sale_id += 1

sales_df = pd.DataFrame(sales_rows)

duck.register("sales_df", sales_df)
duck.execute("INSERT INTO sales SELECT * FROM sales_df")

print("DuckDB database created: sales")

# -----------------------------
# GROUND TRUTH: Use CID as oracle
# -----------------------------
# Map every sale to its true song entity via CID
# This simulates PERFECT ER (not available to the system)

# Join sales to raw tracks via original (non-perturbed) record linkage
oracle_df = df.merge(
    sales_df,
    left_on=["title", "artist", "album"],
    right_on=["track_title", "artist_name", "album_name"],
    how="inner"
)

# -----------------------------
# Query 1: Total revenue per song (after ER)
# -----------------------------
gt_total_revenue_per_song = (
    oracle_df
    .groupby("cid")["revenue_usd"]
    .sum()
    .reset_index()
    .rename(columns={"cid": "song_entity_id", "revenue_usd": "total_revenue"})
)

# -----------------------------
# Query 2: Top artists by total revenue
# -----------------------------
gt_top_artists = (
    oracle_df
    .groupby("artist")["revenue_usd"]
    .sum()
    .reset_index()
    .sort_values("revenue_usd", ascending=False)
)

# -----------------------------
# Query 3: Revenue per language
# -----------------------------
gt_revenue_by_language = (
    oracle_df
    .groupby("language")["revenue_usd"]
    .sum()
    .reset_index()
)

# -----------------------------
# Query 4: Average revenue per album
# -----------------------------
album_revenue = (
    oracle_df
    .groupby(["cid", "album"])["revenue_usd"]
    .sum()
    .reset_index()
)

gt_avg_revenue_per_album = (
    album_revenue
    .groupby("album")["revenue_usd"]
    .mean()
    .reset_index()
)

# -----------------------------
# Save ground truth answers
# -----------------------------
Path("ground_truth").mkdir(exist_ok=True)

gt_total_revenue_per_song.to_csv(
    "ground_truth/q1_total_revenue_per_song.csv",
    index=False
)

gt_top_artists.to_csv(
    "ground_truth/q2_top_artists.csv",
    index=False
)

gt_revenue_by_language.to_csv(
    "ground_truth/q3_revenue_by_language.csv",
    index=False
)

gt_avg_revenue_per_album.to_csv(
    "ground_truth/q4_avg_revenue_per_album.csv",
    index=False
)

print("Ground truth queries generated and saved.")
