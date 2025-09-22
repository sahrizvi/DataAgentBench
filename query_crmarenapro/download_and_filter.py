#!/usr/bin/env python3
"""
Download CRMArenaPro dataset and filter for longest exact_match queries
"""

from datasets import load_dataset
import pandas as pd
import json

def download_and_filter_queries():
    """Download CRMArenaPro and filter for longest exact_match queries"""
    
    print("📥 Downloading CRMArenaPro dataset from HuggingFace...")
    
    # Load the dataset
    dataset = load_dataset("Salesforce/CRMArenaPro", "CRMArenaPro")
    
    print(f"Dataset keys: {list(dataset.keys())}")
    
    # Combine both interactive datasets
    all_data = []
    
    for task_type in ['b2b', 'b2c']:
        if task_type in dataset:
            task_data = pd.DataFrame(dataset[task_type])
            task_data['task_type'] = task_type
            all_data.append(task_data)
            print(f"{task_type}: {len(task_data)} queries")
    
    # Combine all data
    df = pd.concat(all_data, ignore_index=True)
    
    print(f"Total combined dataset size: {len(df)} queries")
    print(f"Task types: {df['task_type'].value_counts().to_dict()}")
    
    # Check columns
    print(f"Available columns: {list(df.columns)}")
    
    # Filter for exact_match queries if reward_metric column exists
    if 'reward_metric' in df.columns:
        print(f"Reward metrics: {df['reward_metric'].value_counts().to_dict()}")
        filtered_df = df[df['reward_metric'] == 'exact_match'].copy()
    else:
        print("No reward_metric column found, using all queries")
        filtered_df = df.copy()
    
    # Filter out queries with "display" as they're not appropriate for data analysis
    print(f"Before filtering 'display' queries: {len(filtered_df)}")
    filtered_df = filtered_df[~filtered_df['query'].str.contains('display', case=False, na=False)]
    print(f"After filtering 'display' queries: {len(filtered_df)}")
    
    print(f"\n📊 After filtering:")
    print(f"Exact match interactive queries: {len(filtered_df)}")
    print(f"Task type breakdown: {filtered_df['task_type'].value_counts().to_dict()}")
    
    # Calculate query lengths
    filtered_df['query_length'] = filtered_df['query'].str.len()
    
    print(f"\nQuery length statistics:")
    print(f"Min: {filtered_df['query_length'].min()}")
    print(f"Max: {filtered_df['query_length'].max()}")
    print(f"Mean: {filtered_df['query_length'].mean():.1f}")
    print(f"Median: {filtered_df['query_length'].median():.1f}")
    
    # Convert metadata and answer columns to string for duplicate detection
    filtered_df['metadata_str'] = filtered_df['metadata'].astype(str)
    filtered_df['answer_str'] = filtered_df['answer'].astype(str)
    
    # Drop duplicates based on metadata column first
    print(f"\nBefore removing duplicates: {len(filtered_df)} queries")
    filtered_df = filtered_df.drop_duplicates(subset=['metadata_str'], keep='first')
    print(f"After removing metadata duplicates: {len(filtered_df)} queries")
    
    # Then drop duplicates based on answer column
    filtered_df = filtered_df.drop_duplicates(subset=['answer_str'], keep='first')
    print(f"After removing answer duplicates: {len(filtered_df)} queries")
    
    # Finally drop duplicates based on task column (to remove transfer_count duplicates)
    filtered_df = filtered_df.drop_duplicates(subset=['task'], keep='first')
    print(f"After removing task duplicates: {len(filtered_df)} queries")
    
    # Limit queries with answers starting with "00" to only 5
    def starts_with_00(answer):
        if isinstance(answer, list) and len(answer) > 0:
            first_item = str(answer[0])
            return first_item.startswith('0')
        return False
    
    # Separate queries by whether they start with "00"
    queries_with_00 = filtered_df[filtered_df['answer'].apply(starts_with_00)]
    queries_without_00 = filtered_df[~filtered_df['answer'].apply(starts_with_00)]
    
    print(f"Queries with answers starting with '00': {len(queries_with_00)}")
    print(f"Queries without answers starting with '00': {len(queries_without_00)}")
    
    # Take only 5 queries that start with "00" (longest ones)
    if len(queries_with_00) > 5:
        queries_with_00 = queries_with_00.nlargest(5, 'query_length')
        print(f"Limited '00' queries to top 5 longest")
    
    # Combine back
    filtered_df = pd.concat([queries_with_00, queries_without_00], ignore_index=True)
    print(f"Final dataset size: {len(filtered_df)} queries")
    
    # Sort by query length and take top 50
    top_queries = filtered_df.nlargest(50, 'query_length')
    
    print(f"\n🎯 Selected top 50 longest queries:")
    print(f"Length range: {top_queries['query_length'].min()} - {top_queries['query_length'].max()}")
    
    # Save the selected queries
    selected_queries = []
    for idx, row in top_queries.iterrows():
        query_data = {
            'idx': row['idx'],
            'query': row['query'],
            'answer': row['answer'],
            'task': row['task'],
            'task_type': row['task_type'],
            'reward_metric': row['reward_metric'],
            'query_length': row['query_length']
        }
        
        # Add metadata if available
        if 'metadata' in row and pd.notna(row['metadata']):
            query_data['metadata'] = row['metadata']
            
        # Add persona if available
        if 'persona' in row and pd.notna(row['persona']):
            query_data['persona'] = row['persona']
            
        selected_queries.append(query_data)
    
    # Save to file
    with open('selected_queries.json', 'w') as f:
        json.dump(selected_queries, f, indent=2)
    
    print(f"\n💾 Saved {len(selected_queries)} queries to selected_queries.json")
    
    # Show sample queries
    print(f"\n📝 Sample queries:")
    for i, query in enumerate(selected_queries[:3]):
        print(f"\nQuery {i+1} (length: {query['query_length']}):")
        print(f"Task: {query['task_type']}")
        print(f"Query: {query['query'][:200]}...")
        print(f"Answer: {query['answer']}")
    
    return selected_queries

if __name__ == "__main__":
    download_and_filter_queries()