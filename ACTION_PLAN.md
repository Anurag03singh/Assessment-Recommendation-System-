# 🎯 Action Plan - Complete the Assignment

## Current Status

✅ **System Built and Running**
- Backend API: http://localhost:8000
- Frontend App: http://localhost:3000
- GitHub: https://github.com/Anurag03singh/Assessment-Recommendation-System-

✅ **Core Requirements Met**
- Accepts natural language query, JD text, JD URL
- Returns 5-10 recommendations
- Displays in tabular format
- Filters individual test solutions only

## What's Left to Do

### 🔴 Critical Tasks (Must Complete)

#### 1. Download and Process Dataset ⏳
**Time**: 5 minutes

```bash
cd backend
python process_dataset.py
```

**If automatic download fails**:
1. Manually download: https://rnd.aspiringminds.in/voiceRater/samples/files/Gen_AI%20Dataset.xlsx
2. Save to: `backend/data/Gen_AI_Dataset.xlsx`
3. Run: `python process_dataset.py`

**Expected Output**:
- `data/labeled_queries.json` with 10 train + 9 test queries

---

#### 2. Scrape 377+ Assessments ⏳
**Time**: 10-30 minutes

```bash
# Try basic scraping first
python scraper.py

# If < 377 assessments, use Selenium
python scraper.py --selenium
```

**Expected Output**:
- `data/shl_catalog.json` with 377+ assessments
- All are individual test solutions (no pre-packaged)

**Verification**:
```bash
python -c "import json; data=json.load(open('data/shl_catalog.json')); print(f'Scraped: {len(data)} assessments')"
```

---

#### 3. Rebuild Vector Index ⏳
**Time**: 5-10 minutes

```bash
# Delete old index (built with sample data)
rm -rf chroma_db/

# Build new index with 377+ assessments
python embeddings.py
```

**Expected Output**:
- `chroma_db/` directory with vector index
- 377+ embeddings stored

---

#### 4. Evaluate on Train Set ⏳
**Time**: 2 minutes

```bash
python evaluate.py
```

**Expected Output**:
- Mean Recall@10 score
- Individual query results
- `data/evaluation_results.json`

**Target**: Recall@10 > 0.70

---

#### 5. Generate Test Predictions ⏳
**Time**: 1 minute

```bash
python export_csv.py
```

**Expected Output**:
- `data/submission.csv`
- 90 rows (9 queries × 10 recommendations)
- Format: Query, Assessment_url

---

### 🟡 Optional Tasks (Improve Performance)

#### 6. Iterate to Improve Recall@10 (If Needed)
**Time**: 1-2 hours

**If Recall@10 < 0.70**, try these improvements:

**A. Better Embeddings**
```python
# In embeddings.py, line 13
model = SentenceTransformer('all-mpnet-base-v2')  # Larger, better model
```

**B. Increase Retrieval Size**
```python
# In recommender.py, line 67
candidates = self.em.search(query, k=30)  # Instead of k=20
```

**C. Tune K/P Weights**
```python
# In recommender.py, analyze_query method
# Adjust the weight calculation based on train data
```

**D. Query Enhancement**
```python
# Add preprocessing to extract key terms
# Expand with synonyms
# Add domain context
```

After each change:
```bash
python embeddings.py  # If model changed
python evaluate.py    # Check new Recall@10
```

---

## Step-by-Step Execution Plan

### Phase 1: Data Preparation (15-40 minutes)

```bash
cd backend

# Step 1: Download dataset
python process_dataset.py

# Step 2: Scrape SHL catalog
python scraper.py --selenium

# Step 3: Verify data
python -c "import json; print(f'Assessments: {len(json.load(open(\"data/shl_catalog.json\")))}')"
python -c "import json; data=json.load(open('data/labeled_queries.json')); print(f'Train: {len(data[\"train_queries\"])}, Test: {len(data[\"test_queries\"])}')"
```

**Checkpoint**: 
- ✅ 377+ assessments scraped
- ✅ 10 train queries loaded
- ✅ 9 test queries loaded

---

### Phase 2: Build & Evaluate (10-15 minutes)

```bash
# Step 4: Build vector index
rm -rf chroma_db/
python embeddings.py

# Step 5: Evaluate on train set
python evaluate.py

# Check results
cat data/evaluation_results.json
```

**Checkpoint**:
- ✅ Vector index built
- ✅ Recall@10 calculated
- ✅ Results documented

---

### Phase 3: Iterate (If Needed) (0-2 hours)

**If Recall@10 < 0.70**:

```bash
# Try improvement 1: Better model
# Edit embeddings.py, change model
python embeddings.py
python evaluate.py

# Try improvement 2: More candidates
# Edit recommender.py, increase k
python evaluate.py

# Continue until Recall@10 > 0.70
```

---

### Phase 4: Generate Predictions (2 minutes)

```bash
# Step 6: Generate test predictions
python export_csv.py

# Verify output
wc -l data/submission.csv  # Should be 91 (90 + header)
head data/submission.csv
```

**Checkpoint**:
- ✅ submission.csv generated
- ✅ 90 predictions (9 × 10)
- ✅ All URLs valid

---

## Verification Checklist

Before submission, verify:

### Data
- [ ] Downloaded Gen_AI_Dataset.xlsx
- [ ] Processed to labeled_queries.json
- [ ] 10 train queries present
- [ ] 9 test queries present
- [ ] Scraped 377+ assessments
- [ ] All are individual test solutions
- [ ] No pre-packaged solutions

### System
- [ ] Vector index built with 377+ assessments
- [ ] Evaluation run on train set
- [ ] Recall@10 calculated and documented
- [ ] Recall@10 > 0.70 (target)

### Output
- [ ] submission.csv generated
- [ ] 90 rows (9 queries × 10 recommendations)
- [ ] Format: Query, Assessment_url
- [ ] All URLs are valid SHL links
- [ ] URLs match scraped catalog

### Documentation
- [ ] TECHNICAL_DOCUMENT.md updated with results
- [ ] Evaluation metrics documented
- [ ] Improvements documented (if any)

---

## Quick Commands Reference

```bash
# Process dataset
python process_dataset.py

# Scrape catalog
python scraper.py --selenium

# Build index
rm -rf chroma_db/ && python embeddings.py

# Evaluate
python evaluate.py

# Generate predictions
python export_csv.py

# Verify counts
python -c "import json; print(f'Assessments: {len(json.load(open(\"data/shl_catalog.json\")))}')"
python -c "import json; data=json.load(open('data/labeled_queries.json')); print(f'Train: {len(data[\"train_queries\"])}, Test: {len(data[\"test_queries\"])}')"
wc -l data/submission.csv
```

---

## Troubleshooting

### Dataset Download Fails
**Solution**: Download manually and save to `backend/data/Gen_AI_Dataset.xlsx`

### Scraper Gets < 377 Assessments
**Solutions**:
1. Use Selenium: `python scraper.py --selenium`
2. Check website structure
3. Update CSS selectors
4. Add delays between requests

### Low Recall@10
**Solutions**:
1. Use better embedding model
2. Increase retrieval size
3. Tune K/P weights
4. Add query enhancement
5. Check data quality

### CSV Export Fails
**Solution**: Ensure test queries are loaded in `data/labeled_queries.json`

---

## Timeline

| Phase | Tasks | Time | Status |
|-------|-------|------|--------|
| 1 | Data Preparation | 15-40 min | ⏳ |
| 2 | Build & Evaluate | 10-15 min | ⏳ |
| 3 | Iterate (optional) | 0-2 hours | ⏳ |
| 4 | Generate Predictions | 2 min | ⏳ |
| **Total** | **30 min - 3 hours** | ⏳ |

**Minimum Time**: 30 minutes (if everything works first try)  
**Maximum Time**: 3 hours (if iteration needed)  
**Expected Time**: 1-2 hours

---

## Success Criteria

✅ **Data**
- 377+ assessments scraped
- 10 train queries processed
- 9 test queries processed

✅ **Performance**
- Recall@10 > 0.70 on train set
- Documented in evaluation_results.json

✅ **Output**
- submission.csv with 90 predictions
- All URLs valid and from SHL catalog

✅ **Documentation**
- Technical document updated
- Evaluation metrics included
- Process documented

---

## Final Deliverables

1. **submission.csv** - 90 predictions for test set
2. **TECHNICAL_DOCUMENT.md** - Updated with evaluation results
3. **GitHub Repository** - All code and documentation
4. **Deployed System** (optional) - Live demo

---

## Next Immediate Steps

1. **Run**: `cd backend && python process_dataset.py`
2. **Run**: `python scraper.py --selenium`
3. **Verify**: Check if 377+ assessments scraped
4. **Continue**: Follow Phase 2 if successful

---

**Status**: Ready to execute  
**Priority**: Complete Phase 1 (Data Preparation)  
**Target**: 377+ assessments, Recall@10 > 0.70, 90 predictions
