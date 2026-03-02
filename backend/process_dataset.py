"""
Process the Gen AI Dataset (Excel file)
Downloads and converts train/test data to JSON format
"""
import pandas as pd
import json
import os
import requests


def download_dataset(url: str, output_path: str):
    """Download the Excel dataset"""
    print(f"Downloading dataset from {url}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Dataset downloaded to {output_path}")
        return True
    except Exception as e:
        print(f"✗ Failed to download: {e}")
        return False


def process_excel_to_json(excel_path: str, output_path: str):
    """Convert Excel file to JSON format for evaluation"""
    print(f"\nProcessing {excel_path}...")
    
    try:
        # Read Excel file
        # Assuming it has sheets: 'Train' and 'Test'
        xls = pd.ExcelFile(excel_path)
        
        print(f"Sheets found: {xls.sheet_names}")
        
        # Process train data
        train_df = pd.read_excel(excel_path, sheet_name='Train' if 'Train' in xls.sheet_names else 0)
        print(f"\nTrain data: {len(train_df)} rows")
        print(f"Columns: {train_df.columns.tolist()}")
        
        # Process test data
        test_df = pd.read_excel(excel_path, sheet_name='Test' if 'Test' in xls.sheet_names else 1)
        print(f"\nTest data: {len(test_df)} rows")
        print(f"Columns: {test_df.columns.tolist()}")
        
        # Convert to JSON format
        labeled_data = {
            "train_queries": [],
            "test_queries": []
        }
        
        # Process train queries (10 labeled queries)
        for idx, row in train_df.iterrows():
            query_data = {
                "query": str(row.get('Query', row.get('query', ''))),
                "relevant_assessments": []
            }
            
            # Extract relevant assessment URLs
            # Assuming columns like 'Assessment_1', 'Assessment_2', etc.
            for col in train_df.columns:
                if 'assessment' in col.lower() or 'url' in col.lower():
                    url = str(row.get(col, '')).strip()
                    if url and url != 'nan' and url.startswith('http'):
                        query_data["relevant_assessments"].append(url)
            
            if query_data["query"]:
                labeled_data["train_queries"].append(query_data)
        
        # Process test queries (9 unlabeled queries)
        for idx, row in test_df.iterrows():
            query_data = {
                "query": str(row.get('Query', row.get('query', ''))),
                "relevant_assessments": []  # Empty for test set
            }
            
            if query_data["query"]:
                labeled_data["test_queries"].append(query_data)
        
        # Save to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(labeled_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Processed data saved to {output_path}")
        print(f"  Train queries: {len(labeled_data['train_queries'])}")
        print(f"  Test queries: {len(labeled_data['test_queries'])}")
        
        return labeled_data
        
    except Exception as e:
        print(f"✗ Error processing Excel: {e}")
        import traceback
        traceback.print_exc()
        return None


def create_sample_structure():
    """Create sample structure if download fails"""
    print("\nCreating sample data structure...")
    
    sample_data = {
        "train_queries": [
            {
                "query": "Software developer with Java and Python skills",
                "relevant_assessments": [
                    "https://www.shl.com/solutions/products/...",
                    "https://www.shl.com/solutions/products/..."
                ]
            }
            # Add 9 more...
        ],
        "test_queries": [
            {
                "query": "Leadership role requiring strategic thinking",
                "relevant_assessments": []
            }
            # Add 8 more...
        ]
    }
    
    output_path = "data/labeled_queries.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, indent=2)
    
    print(f"✓ Sample structure created at {output_path}")
    print("\n⚠️  Please download the dataset manually and run this script again:")
    print("   URL: https://rnd.aspiringminds.in/voiceRater/samples/files/Gen_AI%20Dataset.xlsx")
    print("   Save as: backend/data/Gen_AI_Dataset.xlsx")
    print("   Then run: python process_dataset.py")


def main():
    """Main processing function"""
    print("="*60)
    print("GEN AI DATASET PROCESSOR")
    print("="*60)
    
    dataset_url = "https://rnd.aspiringminds.in/voiceRater/samples/files/Gen_AI%20Dataset.xlsx"
    excel_path = "data/Gen_AI_Dataset.xlsx"
    json_path = "data/labeled_queries.json"
    
    # Try to download
    if not os.path.exists(excel_path):
        success = download_dataset(dataset_url, excel_path)
        if not success:
            print("\n⚠️  Could not download dataset automatically.")
            print("Please download manually from:")
            print(f"  {dataset_url}")
            print(f"Save to: {excel_path}")
            create_sample_structure()
            return
    
    # Process Excel to JSON
    result = process_excel_to_json(excel_path, json_path)
    
    if result:
        print("\n" + "="*60)
        print("DATASET PROCESSING COMPLETE")
        print("="*60)
        print(f"\nNext steps:")
        print(f"1. Review: {json_path}")
        print(f"2. Run scraper: python scraper.py")
        print(f"3. Build index: python embeddings.py")
        print(f"4. Run evaluation: python evaluate.py")
        print(f"5. Generate predictions: python export_csv.py")
    else:
        create_sample_structure()


if __name__ == "__main__":
    main()
