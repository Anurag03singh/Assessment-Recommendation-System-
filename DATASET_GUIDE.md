# Dataset Processing Guide

## Overview

This guide explains how to work with the Gen AI Dataset for training and testing the recommendation system.

## Dataset Information

**Source**: https://rnd.aspiringminds.in/voiceRater/samples/files/Gen_AI%20Dataset.xlsx

**Contents**:
- **Train Set**: 10 labeled queries with relevant assessments
- **Test Set**: 9 unlabeled queries for prediction

## Step-by-Step Process

### Step 1: Download the Dataset

**Option A: Automatic Download**
```bash
cd backend
python process_dataset.py
```

**Option B: Manual Download**
1. Download from: https://rnd.aspiringminds.in/voiceRater/samples/files/Gen_AI%20Dataset.xlsx
2. Save to: `backend/data/Gen_AI_Dataset.xlsx`
3. Run: `python process_dataset.py`

### Step 2: Scrape SHL Catalog (377+ Assessments)

**Basic Scraping** (using requests):
```bash
cd backend
python scraper.py
```

**Advanced Scraping** (using Selenium for dynamic content):
```bash
python scraper.py --selenium
```

**Expected Output**:
- File: `backend/data/shl_catalog.json`
- Count: 377+ individual test solutions
- Format: Structured JSON with all metadata

**Verification**:
```bash
python -c "import json; data=json.load(open('data/shl_catalog.json')); print(f'Scraped {len(data)} assessments')"
```

### Step 3: Build Vector Index

```bash
python embeddings.py
```

**What This Does**:
- Loads scraped assessments
- Generates embeddings for each assessment
- Stores in ChromaDB vector database
- Enables semantic search

**Expected Time**: 5-10 minutes for 377 assessments

### Step 4: Evaluate on Train Set

```bash
python evaluate.py
```

**What This Does**:
- Loads 10 labeled train queries
- Generates recommendations for each
- Compares with ground truth
- Calculates Recall@10 metric

**Expected Output**:
```
Mean Recall@10: 0.75+
Individual query results
Saved to: data/evaluation_results.json
```

### Step 5: Generate Predictions on Test Set

```bash
python export_csv.py
```

**What This Does**:
- Loads 9 test queries
- Generates top 10 recommendations for each
- Exports to CSV format

**Output File**: `backend/data/submission.csv`

**Format**:
```csv
Query,Assessment_url
"Leadership role requiring strategic thinking",https://www.shl.com/...
"Leadership role requiring strategic thinking",https://www.shl.com/...
...
```

**Expected Rows**: 9 queries × 10 recommendations = 90 rows

## Dataset Structure

### Train Data Format

```json
{
  "train_queries": [
    {
      "query": "Software developer with Java and Python skills",
      "relevant_assessments": [
        "https://www.shl.com/solutions/products/java-programming/",
        "https://www.shl.com/solutions/products/python-test/",
        "https://www.shl.com/solutions/products/coding-assessment/"
      ]
    }
    // ... 9 more queries
  ]
}
```

### Test Data Format

```json
{
  "test_queries": [
    {
      "query": "Leadership role requiring strategic thinking",
      "relevant_assessments": []  // Empty - we need to predict these
    }
    // ... 8 more queries
  ]
}
```

## Evaluation Metrics

### Recall@K

**Formula**:
```
Recall@K = |Predicted ∩ Actual| / |Actual|
```

**Example**:
- Actual relevant: 5 assessments
- Predicted top 10: Contains 4 of the 5
- Recall@10 = 4/5 = 0.80

### Mean Recall@10

Average Recall@10 across all train queries.

**Target**: > 0.70 (good performance)

## Iteration Process

### 1. Baseline Evaluation

```bash
python evaluate.py
```

Note the baseline Recall@10.

### 2. Improve the System

**Options to Try**:

A. **Better Embeddings**
```python
# In embeddings.py
model = SentenceTransformer('all-mpnet-base-v2')  # Larger model
```

B. **Adjust K/P Weights**
```python
# In recommender.py
def analyze_query(self, query: str):
    # Tune the weight calculation
    return {'K': 0.6, 'P': 0.4}  # Adjust ratios
```

C. **Increase Retrieval Size**
```python
# In recommender.py
candidates = self.em.search(query, k=30)  # Instead of k=20
```

D. **Query Enhancement**
```python
# Add query preprocessing
def enhance_query(self, query: str) -> str:
    # Extract key terms
    # Expand with synonyms
    # Add context
    return enhanced_query
```

### 3. Re-evaluate

```bash
python evaluate.py
```

Compare new Recall@10 with baseline.

### 4. Repeat

Continue iterating until Recall@10 is satisfactory.

## Troubleshooting

### Issue: Dataset Download Fails

**Solution**:
1. Download manually from the URL
2. Save to `backend/data/Gen_AI_Dataset.xlsx`
3. Run `python process_dataset.py`

### Issue: Scraper Gets < 377 Assessments

**Solutions**:

1. **Try Selenium**:
```bash
python scraper.py --selenium
```

2. **Check Website**:
- Visit: https://www.shl.com/solutions/products/product-catalog/
- Verify structure hasn't changed
- Check if JavaScript is required

3. **Update Selectors**:
- Inspect HTML in browser
- Update CSS selectors in `scraper.py`

4. **Add Delays**:
```python
time.sleep(2)  # Between requests
```

### Issue: Low Recall@10

**Solutions**:

1. **Check Data Quality**:
```bash
# Verify URLs match
python -c "import json; data=json.load(open('data/labeled_queries.json')); print(data['train_queries'][0])"
```

2. **Improve Embeddings**:
- Use larger model
- Better text enrichment
- More context

3. **Tune Parameters**:
- Adjust K/P weights
- Increase retrieval size
- Modify re-ranking

4. **Query Enhancement**:
- Extract key terms
- Add synonyms
- Expand context

### Issue: CSV Export Fails

**Solution**:
```bash
# Check test queries exist
python -c "import json; data=json.load(open('data/labeled_queries.json')); print(f'Test queries: {len(data[\"test_queries\"])}')"

# Run export
python export_csv.py
```

## Validation Checklist

Before submission, verify:

- [ ] Scraped 377+ assessments
- [ ] All assessments are individual test solutions (no pre-packaged)
- [ ] Train data loaded (10 queries)
- [ ] Test data loaded (9 queries)
- [ ] Vector index built
- [ ] Evaluation run on train set
- [ ] Recall@10 calculated
- [ ] CSV generated for test set
- [ ] CSV has 90 rows (9 × 10)
- [ ] All URLs are valid SHL links

## File Locations

```
backend/
├── data/
│   ├── Gen_AI_Dataset.xlsx          # Downloaded dataset
│   ├── labeled_queries.json         # Processed train/test data
│   ├── shl_catalog.json             # Scraped assessments (377+)
│   ├── evaluation_results.json      # Evaluation metrics
│   └── submission.csv               # Final predictions
├── process_dataset.py               # Dataset processor
├── scraper.py                       # SHL scraper
├── embeddings.py                    # Vector index builder
├── evaluate.py                      # Evaluation script
└── export_csv.py                    # CSV generator
```

## Commands Summary

```bash
# 1. Process dataset
python process_dataset.py

# 2. Scrape catalog
python scraper.py --selenium

# 3. Build index
python embeddings.py

# 4. Evaluate
python evaluate.py

# 5. Generate predictions
python export_csv.py

# 6. Verify
python -c "import json; print(len(json.load(open('data/shl_catalog.json'))))"
```

## Expected Timeline

| Task | Time | Status |
|------|------|--------|
| Download dataset | 2 min | ⏳ |
| Scrape 377+ assessments | 10-30 min | ⏳ |
| Build vector index | 5-10 min | ⏳ |
| Evaluate on train | 2 min | ⏳ |
| Iterate & improve | 1-2 hours | ⏳ |
| Generate predictions | 1 min | ⏳ |
| **Total** | **2-3 hours** | ⏳ |

## Success Criteria

✅ Scraped 377+ individual test solutions  
✅ Processed train data (10 queries)  
✅ Processed test data (9 queries)  
✅ Built vector index  
✅ Recall@10 > 0.70 on train set  
✅ Generated CSV with 90 predictions  
✅ All URLs are valid  

## Next Steps

1. Run `python process_dataset.py`
2. Run `python scraper.py --selenium`
3. Verify 377+ assessments scraped
4. Run `python embeddings.py`
5. Run `python evaluate.py`
6. Iterate to improve Recall@10
7. Run `python export_csv.py`
8. Submit `data/submission.csv`

---

**Status**: Ready to process dataset  
**Target**: 377+ assessments, Recall@10 > 0.70  
**Output**: submission.csv with 90 predictions
