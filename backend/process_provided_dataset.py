"""
Process the provided Gen_AI_Dataset.xlsx file
This contains the actual training and test data from SHL
"""
import pandas as pd
import json
import os

def process_dataset(excel_file="data/Gen_AI_Dataset.xlsx"):
    """Process the provided Excel dataset"""
    
    print("Loading Excel file...")
    
    # Read all sheets
    excel_data = pd.ExcelFile(excel_file)
    print(f"Found sheets: {excel_data.sheet_names}")
    
    # Process each sheet
    for sheet_name in excel_data.sheet_names:
        print(f"\n{'='*60}")
        print(f"Processing sheet: {sheet_name}")
        print(f"{'='*60}")
        
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"\nFirst few rows:")
        print(df.head())
        
        # Save as JSON for easier processing
        output_file = f"data/{sheet_name.lower().replace(' ', '_')}.json"
        
        # Convert to appropriate format based on sheet content
        if 'query' in df.columns.str.lower().tolist():
            # This is likely the queries sheet
            data = df.to_dict('records')
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"\n✓ Saved queries to {output_file}")
            
        elif 'url' in df.columns.str.lower().tolist() or 'assessment' in df.columns.str.lower().tolist():
            # This is likely the catalog sheet
            data = df.to_dict('records')
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"\n✓ Saved catalog to {output_file}")
        else:
            # Unknown format, save as is
            data = df.to_dict('records')
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"\n✓ Saved data to {output_file}")
    
    print(f"\n{'='*60}")
    print("Dataset processing complete!")
    print(f"{'='*60}")
    
    # Provide guidance on next steps
    print("\n📋 Next Steps:")
    print("1. Review the generated JSON files in backend/data/")
    print("2. Update embeddings.py to use the new catalog")
    print("3. Update evaluate.py to use the new queries")
    print("4. Rebuild the vector index: python embeddings.py")
    print("5. Run evaluation: python evaluate.py")


if __name__ == "__main__":
    if not os.path.exists("data/Gen_AI_Dataset.xlsx"):
        print("❌ Error: Gen_AI_Dataset.xlsx not found in data/ directory")
        print("Please download it first from the provided link")
        exit(1)
    
    process_dataset()
