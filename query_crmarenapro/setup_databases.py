#!/usr/bin/env python3
"""
Download CRM databases from CRMArena and split across multiple database types with corrupted join keys
"""

import os
import requests
import sqlite3
import duckdb
import pandas as pd
import random
import re
from urllib.parse import urljoin

def download_file(url, filename):
    """Download a file from URL"""
    print(f"📥 Downloading {filename}...")
    
    response = requests.get(url)
    response.raise_for_status()
    
    with open(filename, 'wb') as f:
        f.write(response.content)
    
    print(f"✅ Downloaded {filename}")

def download_crm_databases():
    """Download CRM databases from CRMArena repository"""
    
    base_url = "https://github.com/SalesforceAIResearch/CRMArena/raw/main/local_data/"
    
    # List of database files to download
    db_files = [
        "crmarenapro_b2b_data.db"  # We only need B2B for the most complete schema
    ]
    
    print("🚀 Downloading CRM databases from CRMArena...")
    print("=" * 50)
    
    os.makedirs("query_dataset", exist_ok=True)
    
    for db_file in db_files:
        url = urljoin(base_url, db_file)
        local_path = os.path.join("query_dataset", db_file)
        
        try:
            download_file(url, local_path)
        except Exception as e:
            print(f"❌ Error downloading {db_file}: {e}")
            raise

def create_sqlite_db(tables_data, db_name):
    """Create SQLite database with specified tables"""
    print(f"🔄 Creating SQLite database: {db_name}")
    
    conn = sqlite3.connect(f"query_dataset/{db_name}")
    
    for table_name, df in tables_data.items():
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"  ✅ Added table {table_name} ({len(df)} rows)")
    
    conn.close()

def create_duckdb_db(tables_data, db_name):
    """Create DuckDB database with specified tables"""
    print(f"🔄 Creating DuckDB database: {db_name}")
    
    conn = duckdb.connect(f"query_dataset/{db_name}")
    
    for table_name, df in tables_data.items():
        conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
        print(f"  ✅ Added table {table_name} ({len(df)} rows)")
    
    conn.close()

def create_postgres_sql(tables_data, sql_filename):
    """Create PostgreSQL SQL file with table definitions and data"""
    print(f"🔄 Creating PostgreSQL SQL file: {sql_filename}")
    
    sql_content = []
    
    for table_name, df in tables_data.items():
        # Create table definition
        columns = []
        for col in df.columns:
            dtype = df[col].dtype
            if dtype == 'object':
                col_type = 'TEXT'
            elif dtype == 'int64':
                col_type = 'INTEGER'
            elif dtype == 'float64':
                col_type = 'REAL'
            else:
                col_type = 'TEXT'
            columns.append(f"    {col} {col_type}")
        
        create_sql = f"CREATE TABLE {table_name} (\n" + ",\n".join(columns) + "\n);"
        sql_content.append(create_sql)
        
        # Insert data
        for _, row in df.iterrows():
            values = []
            for val in row:
                if pd.isna(val):
                    values.append('NULL')
                elif isinstance(val, str):
                    # Escape single quotes
                    escaped_val = val.replace("'", "''")
                    values.append(f"'{escaped_val}'")
                else:
                    values.append(str(val))
            
            insert_sql = f"INSERT INTO {table_name} VALUES ({', '.join(values)});"
            sql_content.append(insert_sql)
        
        print(f"  ✅ Added table {table_name} ({len(df)} rows)")
    
    with open(f"query_dataset/{sql_filename}", 'w') as f:
        f.write('\n'.join(sql_content))

def corrupt_id_field(value, corruption_rate=0.3):
    """Add corruption to ID fields (add # prefix randomly)"""
    if pd.isna(value) or not isinstance(value, str):
        return value
    
    if random.random() < corruption_rate:
        return f"#{value}"
    return value

def corrupt_text_field(value, corruption_rate=0.3):
    """Add corruption to text fields (add trailing spaces)"""
    if pd.isna(value) or not isinstance(value, str):
        return value
    
    if random.random() < corruption_rate:
        # Add 1-3 trailing spaces
        return value + " " * random.randint(1, 3)
    return value

def corrupt_dataframe(df, table_name):
    """Apply corruption to join keys in a dataframe"""
    df_corrupted = df.copy()
    
    # Define which fields to corrupt for each table type
    corruption_rules = {
        # ID fields get # prefix sometimes
        'id_fields': ['Id', 'AccountId', 'ContactId', 'OpportunityId', 'Product2Id', 'OwnerId', 
                     'QuoteId', 'OrderId', 'UserId', 'Territory2Id', 'WhatId', 'WhoId', 
                     'CaseId', 'Case__c', 'RelatedTo__c', 'Pricebook2Id', 'ProductCategoryId'],
        
        # Text fields get trailing spaces sometimes  
        'text_fields': ['Name', 'FirstName', 'LastName', 'Company', 'Email', 'Subject', 
                       'Title', 'Username', 'Status', 'StageName', 'LeadSource']
    }
    
    print(f"  🔧 Applying corruption to {table_name}...")
    
    for col in df_corrupted.columns:
        if col in corruption_rules['id_fields']:
            df_corrupted[col] = df_corrupted[col].apply(lambda x: corrupt_id_field(x, 0.25))
        elif col in corruption_rules['text_fields']:
            df_corrupted[col] = df_corrupted[col].apply(lambda x: corrupt_text_field(x, 0.20))
    
    return df_corrupted

def split_crm_tables():
    """Split CRM tables across different database types with corruption"""

    print("\n🔄 Splitting CRM tables across multiple database types with corrupted join keys")
    print("=" * 80)

    # Create hidden folder for clean data
    os.makedirs("query_dataset/hidden", exist_ok=True)

    # Load source database (use B2B as it has the most complete schema)
    source_db = "query_dataset/crmarenapro_b2b_data.db"
    source_conn = sqlite3.connect(source_db)

    # Get all tables
    cursor = source_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    all_tables = [t[0] for t in cursor.fetchall()]

    print(f"📊 Found {len(all_tables)} tables in source database")

    # Create single clean SQLite database in hidden folder with ALL tables
    print("🔄 Creating clean reference database with all tables...")
    clean_all_tables = {}

    for table_name in all_tables:
        try:
            df = pd.read_sql(f"SELECT * FROM `{table_name}`", source_conn)
            clean_all_tables[table_name] = df
            print(f"  ✅ Loaded table {table_name} ({len(df)} rows)")
        except Exception as e:
            print(f"⚠️  Warning: Could not load table {table_name}: {e}")

    # Create the clean reference database
    create_sqlite_db(clean_all_tables, "hidden/crm_clean.db")

    # Define how to split tables across databases
    database_splits = {
        # SQLite: User management and core entities
        'core_crm.db': ['User', 'Account', 'Contact'],

        # DuckDB: Sales pipeline and transactions
        'sales_pipeline.duckdb': ['Opportunity', 'OpportunityLineItem', 'Quote', 'QuoteLineItem', 'Contract', 'Lead'],

        # PostgreSQL: Customer service and support
        'support.sql': ['Case', 'Knowledge__kav', 'Issue__c', 'CaseHistory__c', 'EmailMessage', 'LiveChatTranscript'],

        # SQLite: Products and orders
        'products_orders.db': ['ProductCategory', 'Product2', 'ProductCategoryProduct', 'Pricebook2', 'PricebookEntry', 'Order', 'OrderItem'],

        # DuckDB: Activities and communications
        'activities.duckdb': ['Task', 'Event', 'VoiceCallTranscript__c'],

        # SQLite: Territory management
        'territory.db': ['Territory2', 'UserTerritory2Association']
    }

    # Load and split tables for corrupted versions
    for db_name, table_list in database_splits.items():
        clean_tables_data = {}
        corrupted_tables_data = {}

        for table_name in table_list:
            if table_name in all_tables:
                try:
                    df = pd.read_sql(f"SELECT * FROM `{table_name}`", source_conn)
                    clean_tables_data[table_name] = df
                    corrupted_tables_data[table_name] = corrupt_dataframe(df, table_name)
                except Exception as e:
                    print(f"⚠️  Warning: Could not load table {table_name}: {e}")

        if corrupted_tables_data:
            # Create corrupted versions for the main challenge
            if db_name.endswith('.db'):
                create_sqlite_db(corrupted_tables_data, db_name)
            elif db_name.endswith('.duckdb'):
                create_duckdb_db(corrupted_tables_data, db_name)
            elif db_name.endswith('.sql'):
                create_postgres_sql(corrupted_tables_data, db_name)

    source_conn.close()

    # Clean up source database
    os.remove(source_db)
    
    print(f"\n✅ Database splitting completed!")
    print(f"📊 Summary:")
    print(f"  Main databases (with corrupted join keys):")
    print(f"  - core_crm.db: User management (SQLite)")
    print(f"  - sales_pipeline.duckdb: Sales data (DuckDB)")
    print(f"  - support.sql: Customer support (PostgreSQL)")
    print(f"  - products_orders.db: Product catalog (SQLite)")
    print(f"  - activities.duckdb: Activities & communications (DuckDB)")
    print(f"  - territory.db: Territory management (SQLite)")
    print(f"")
    print(f"  Clean reference data:")
    print(f"  - query_dataset/hidden/crm_clean.db: Single SQLite DB with ALL tables (uncorrupted)")
    print(f"  - This clean database can be used for ground truth validation")
    print(f"")
    print(f"🔧 Corruption applied:")
    print(f"  - ID fields: ~25% have '#' prefix added")
    print(f"  - Text fields: ~20% have trailing spaces added")
    print(f"  - Affects join keys like Id, AccountId, Name, etc.")

def update_db_config():
    """Update database configuration file"""
    print(f"\n🔄 Updating database configuration...")
    
    config = """db_clients:
  core_crm:
    db_type: sqlite
    db_path: query_dataset/core_crm.db
  sales_pipeline:
    db_type: duckdb
    db_path: query_dataset/sales_pipeline.duckdb
  support:
    db_type: postgres
    db_name: crm_support
    sql_file: query_dataset/support.sql
  products_orders:
    db_type: sqlite
    db_path: query_dataset/products_orders.db
  activities:
    db_type: duckdb
    db_path: query_dataset/activities.duckdb
  territory:
    db_type: sqlite
    db_path: query_dataset/territory.db
"""
    
    with open("db_config.yaml", "w") as f:
        f.write(config)
    
    print("✅ Updated db_config.yaml")

def main():
    """Main setup function"""
    print("🚀 Setting up CRMArenaPro Multi-Database Benchmark")
    print("=" * 60)
    
    download_crm_databases()
    split_crm_tables()
    update_db_config()
    
    print(f"\n🎉 Setup completed successfully!")
    print(f"Ready to create CRMArenaPro benchmark queries.")

if __name__ == "__main__":
    main()