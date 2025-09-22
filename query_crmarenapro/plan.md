# CRMArenaPro Multi-Database Benchmark Plan

## Overview
Create a challenging multi-database benchmark using real Salesforce CRMArenaPro queries. The benchmark tests agents' ability to perform complex CRM analysis across corrupted databases that require data cleaning and cross-database joins.

## Key Requirements
- Use actual CRMArenaPro queries with `reward_metric = exact_match`
- Multi-database architecture with corrupted join keys
- Real CRM data from Salesforce CRMArena repository
- Diverse query types covering all major CRM workflows
- 14 unique task types for comprehensive coverage

## Dataset Selection Process

### Source Data
1. **CRM Data**: Downloaded from Salesforce CRMArena GitHub repository
   - `crmarenapro_b2b_data.db` - Most complete schema with 27 tables
   - Real enterprise CRM data with 26,000+ total records

2. **Query Selection**: Filtered from HuggingFace CRMArenaPro dataset
   - Started with 4,280 queries from `b2b` and `b2c` task types
   - Applied comprehensive filtering and deduplication

### Query Filtering Pipeline
1. **Initial Filter**: `reward_metric = "exact_match"` → 3,400 queries
2. **Content Filter**: Removed "display" queries → 3,197 queries
3. **Metadata Deduplication**: Unique contexts → 2,608 queries
4. **Answer Deduplication**: Unique expected results → 449 queries
5. **Task Deduplication**: One query per task type → 16 queries
6. **ID Limitation**: Max 5 queries with "00" prefix answers → 14 final queries

## Multi-Database Architecture

### Database Distribution (6 databases across 3 database types)

1. **core_crm.db** (SQLite)
   - User: Sales team information (212 rows)
   - Account: Company/customer data (101 rows)
   - Contact: Individual contacts (886 rows)

2. **sales_pipeline.duckdb** (DuckDB)
   - Opportunity: Sales deals (1,170 rows)
   - OpportunityLineItem: Deal line items (4,926 rows)
   - Quote: Price quotes (704 rows)
   - QuoteLineItem: Quote details (2,966 rows)
   - Contract: Signed contracts (163 rows)
   - Lead: Sales leads (1,465 rows)

3. **support.sql** (PostgreSQL)
   - Case: Support cases (153 rows)
   - Knowledge__kav: Knowledge articles (194 rows)
   - Issue__c: Custom issues (15 rows)
   - CaseHistory__c: Case history (393 rows)
   - EmailMessage: Email communications (5,686 rows)
   - LiveChatTranscript: Chat logs (58 rows)

4. **products_orders.db** (SQLite)
   - ProductCategory: Product categories (10 rows)
   - Product2: Product catalog (51 rows)
   - Order: Customer orders (163 rows)
   - OrderItem: Order details (689 rows)
   - Plus pricing and mapping tables

5. **activities.duckdb** (DuckDB)
   - Task: Activities and tasks (4,783 rows)
   - Event: Calendar events (54 rows)
   - VoiceCallTranscript__c: Call records (4,033 rows)

6. **territory.db** (SQLite)
   - Territory2: Sales territories (10 rows)
   - UserTerritory2Association: Territory assignments (184 rows)

### Data Corruption Strategy
To increase difficulty and test data cleaning capabilities:

**Corrupted Join Keys** (applied to main databases):
- **ID Fields**: ~25% have `#` prefix added (e.g., `#001Wt00000PFj4zIAD`)
- **Text Fields**: ~20% have trailing spaces (e.g., `"Company Name "`)
- **Affected Fields**: Id, AccountId, ContactId, Name, FirstName, LastName, Email, Subject, Status

**Clean Reference Data**:
- Stored in `query_dataset/hidden/` folder
- Same structure but without corruption
- Used for ground truth verification

## Query Coverage

### 14 Unique Task Types Selected:
1. **lead_qualification** - BANT factor analysis
2. **quote_approval** - Policy compliance validation
3. **wrong_stage_rectification** - Opportunity stage correction
4. **monthly_trend_analysis** - Time-based case patterns
5. **top_issue_identification** - Product issue tracking
6. **invalid_config** - Configuration validation
7. **policy_violation_identification** - Compliance checking
8. **best_region_identification** - Regional performance
9. **transfer_count** - Agent transfer analysis
10. **handle_time** - Case resolution metrics
11. **named_entity_disambiguation** - Product identification
12. **sales_cycle_understanding** - Timing analysis
13. **sales_amount_understanding** - Revenue tracking
14. **activity_priority** - Task prioritization

### Query Complexity Features:
- **Length Range**: 123-300 characters
- **Multi-Database Requirements**: All queries require joins across 2-4 databases
- **Data Cleaning Required**: Corruption handling needed for joins
- **Business Logic**: Domain-specific CRM knowledge required
- **Exact Match Evaluation**: Precise answers expected

## Technical Implementation

### Setup Process:
1. **setup_databases.py**: Downloads CRM data and creates corrupted multi-database structure
2. **download_and_filter.py**: Filters and selects optimal queries from HuggingFace dataset
3. **db_config.yaml**: Configures 6 databases across SQLite, DuckDB, and PostgreSQL

### Benchmark Challenges:
- **Data Corruption**: Agents must clean join keys before cross-database operations
- **Schema Knowledge**: Understanding CRM relationships without foreign keys
- **Business Context**: Applying domain-specific rules (BANT, sales stages, etc.)
- **Multi-Database Joins**: Complex queries spanning multiple database types
- **Exact Matching**: Precise answers required for all 14 task types

## Success Metrics
- Tests both SQL proficiency and data cleaning skills
- Covers comprehensive CRM workflow scenarios
- Evaluates cross-database query capabilities
- Measures understanding of business domain logic
- Provides realistic enterprise data challenges