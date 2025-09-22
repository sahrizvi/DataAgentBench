# CRMArenaPro Multi-Database Benchmark

## Overview

This benchmark implements complex CRM analysis queries that require semantic joins across multiple databases. Unlike traditional benchmarks with simple ID-based joins, every query requires semantic transformations and fuzzy matching to solve.

## Database Architecture

### 4-Database Design with Semantic Gaps

1. **company_profiles.db** (SQLite) - Company directory information
   - Company names: "NaviCorp Tech", "FusionTech Systems" 
   - Industries: "Software & Technology", "Aerospace Engineering & Services"
   - Size ranges: "500-1000", "1000+"
   - Geography: "North America - West Coast", "North America - Central"

2. **sales_interactions.db** (DuckDB) - Interaction history  
   - Organization IDs: "NAVICORP_TECH", "FUSIONTECH_SYSTEMS"
   - Business sectors: "Tech/SaaS", "TechMfg", "Aerospace"
   - Size tiers: "Enterprise", "Mid-Market" 
   - Territories: "Americas", "EMEA", "WEST01"

3. **product_catalog.db** (SQLite) - Product information
   - Target industries: "technology,software,saas,engineering"
   - Customer sizes: "100-1000 employees", "200-2000 employees" 
   - Geographic availability: "americas,emea", "global"

4. **opportunity_pipeline.db** (DuckDB) - Sales pipeline
   - Account references: "NaviCorp Tech", "FusionTech Systems"
   - Business verticals: "Tech/Software", "Aerospace/Defense"
   - Territory codes: "WEST01", "EAST02", "CENT01"

## Required Semantic Transformations

### 1. Company Name Fuzzy Matching
```
"NaviCorp Tech" ↔ "NAVICORP_TECH" ↔ "NaviCorp Tech"
```
- Normalization of corporate suffixes (Inc, Corp, Systems)
- Fuzzy matching with threshold-based word overlap
- Case-insensitive abbreviation handling

### 2. Industry Semantic Mapping  
```
"Software & Technology" → "Tech/SaaS" → "technology,software,saas"
```
- Domain knowledge translation between industry formats
- Keyword extraction and semantic matching
- Multi-format industry targeting

### 3. Company Size Translation
```
"500-1000" → "Enterprise" → "100-1000 employees" 
```
- Range overlap logic for size matching
- Business tier correlation
- Product fit analysis

### 4. Geographic Normalization
```
"North America - West Coast" → "Americas" → "WEST01"
```
- Hierarchical geographic mapping
- Territory code translation  
- Regional aggregation logic

## Sample Queries Implemented

### Query 1 (Level 1): Basic Semantic Joins
**Question**: "How many companies in the technology industry have had at least 3 successful interactions in 2023?"

**Complexity**: 
- Company-interaction fuzzy matching
- Industry semantic filtering
- Temporal aggregation

**Result**: Integer count of qualified companies

### Query 2 (Level 2): Complex Multi-Database Analysis  
**Question**: "What is the total pipeline value for Enterprise-sized companies in the Americas territory that have interacted with products matching their industry?"

**Complexity**:
- 4-database semantic joins
- Size/geography normalization  
- Industry-product fit analysis
- Pipeline value aggregation

**Result**: $3,484,201.12 total pipeline value

### Query 3 (Level 3): Advanced Time-Based Analysis
**Question**: "Calculate the average time-to-close for deals by industry vertical, but only include companies that had C-level stakeholder engagement and used products with high implementation complexity."

**Complexity**:
- Multi-stakeholder filtering
- Product complexity assessment
- Temporal calculations
- Industry vertical grouping

**Result**: Industry:days pairs (e.g., "Cybersecurity:180.0")

## Key Features

### ✅ Semantic Complexity
- **No direct ID joins possible** - all relationships require transformation
- **Multiple semantic mapping layers** - industry, geography, size, names
- **Fuzzy matching algorithms** - threshold-based company name matching
- **Business logic requirements** - domain knowledge for query solving

### ✅ Data Intensity  
- **101 companies** across diverse industries
- **401 interactions** with temporal patterns
- **204 opportunities** with complex pipeline stages
- **8 products** with detailed targeting criteria

### ✅ Exact Match Results
- **Deterministic outputs** despite semantic complexity
- **Validation scripts** for result verification
- **Ground truth implementations** with step-by-step logic
- **CSV result format** compatible with benchmark framework

## Technical Implementation

### Directory Structure
```
query_crmarenapro/
├── db_config.yaml              # Database connection config
├── db_description.txt          # Multi-database schema documentation
├── query_dataset/              # 4 database files
├── scripts/                    # Data processing and utilities
├── query1/                     # Sample query implementations
│   ├── query.json             # Natural language question
│   ├── ground_truth.py        # Semantic join implementation  
│   ├── ground_truth.csv       # Expected result
│   └── validate.py            # Result validation
├── query2/                     # Level 2 complexity query
└── query3/                     # Level 3 complexity query
```

### Semantic Transformation Engine
- **SemanticTransformer class** - handles all mapping logic
- **Enhanced fuzzy matching** - company name normalization
- **Industry mapping dictionaries** - multi-format translations  
- **Geographic hierarchies** - territory code mappings
- **Size correlation logic** - range overlap calculations

## Usage

### Running Individual Queries
```bash
cd query1
python ground_truth.py
python validate.py
```

### Expected Output Pattern
```
🔍 Query 1: Technology companies with 3+ successful interactions in 2023
📋 Step 1: Loading technology companies...
Found 46 technology companies
📞 Step 2: Loading successful interactions from 2023...  
Found 59 organization-sector combinations
🔗 Step 3: Performing semantic matching...
  ✓ Matched: 'NaviCorp Tech' → 'NAVICORP_TECH' (2 interactions)
🎯 Final Answer: 0 technology companies had 3+ successful interactions in 2023
```

## Benchmark Characteristics

### Difficulty Scaling
- **Level 1**: Basic semantic joins (2-3 databases)
- **Level 2**: Complex aggregations with mapping (3-4 databases)  
- **Level 3**: Time-based analysis with multiple filters (4 databases)
- **Level 4**: Advanced business intelligence (all databases, complex logic)

### Evaluation Criteria
- **Semantic join correctness** - proper fuzzy matching implementation
- **Business logic accuracy** - domain knowledge application
- **Result exactness** - deterministic outputs despite complexity
- **Performance efficiency** - handling of cross-database operations

## Expansion to 50 Queries

This implementation provides the foundation for expanding to 50 complex queries:

- **15 query templates designed** across all difficulty levels
- **Semantic transformation framework** ready for scaling
- **Data generation scripts** for additional scenarios
- **Validation infrastructure** for quality assurance

The benchmark successfully demonstrates that every query requires semantic understanding - no simple SQL joins can solve these problems without domain knowledge and fuzzy matching logic.