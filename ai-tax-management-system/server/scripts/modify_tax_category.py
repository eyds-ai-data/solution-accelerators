import json
import os
from pathlib import Path
from azure.cosmos import CosmosClient, exceptions
from typing import List, Dict, Any
from dotenv import load_dotenv


def convert_pph_to_article(pph_pasal: str) -> str:
    """
    Convert PPH Pasal code to Article format.
    E.g., PPH23 -> Art 23, PPH4-2 -> Art 4.2, PPH22 -> Art 22
    """
    if not pph_pasal:
        return ""
    
    # Remove 'PPH' prefix
    pph_pasal = pph_pasal.replace("PPH", "").strip()
    
    # Handle special cases
    if pph_pasal == "4-2":
        return "Art 4.2"
    
    return f"Art {pph_pasal}"


def create_type_of_tax(pph_pasal: str, category: str) -> str:
    """
    Create typeOfTax string in format: "Art 23 - Services"
    """
    article = convert_pph_to_article(pph_pasal)
    
    if not article:
        return ""
    
    if not category or category == "" or category == 0:
        return article
    
    return f"{article} - {category}"


def load_json_file(file_path: Path) -> list:
    """Load JSON file and return data."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json_file(file_path: Path, data: list):
    """Save data to JSON file with proper formatting."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def modify_tax_container_data(
    moi_file_path: str,
    tax_container_file_path: str,
    output_file_path: str = None
):
    """
    Modify tax_container_data.json by adding category and typeOfTax fields
    based on MOI tax object data.
    
    Args:
        moi_file_path: Path to MOI tax object JSON file
        tax_container_file_path: Path to tax_container_data.json file
        output_file_path: Optional path for output file. If None, overwrites input file.
    """
    # Load both JSON files
    print(f"Loading MOI tax object data from: {moi_file_path}")
    moi_data = load_json_file(Path(moi_file_path))
    
    print(f"Loading tax container data from: {tax_container_file_path}")
    tax_container_data = load_json_file(Path(tax_container_file_path))
    
    # Create mapping from taxObjectCode to category (from MOI file)
    # Category comes from "Remarks BP Code for WHT Calculation" field
    moi_mapping = {}
    for item in moi_data:
        tax_code = item.get("taxObjectCode", "")
        category = item.get("Remarks BP Code for W\r\nHT Calculation", "")
        
        # Handle numeric 0 as empty string
        if category == 0 or category is None:
            category = ""
        
        moi_mapping[tax_code] = category
    
    print(f"\nCreated mapping for {len(moi_mapping)} tax object codes")
    
    # Update tax_container_data
    updated_count = 0
    not_found_count = 0
    
    for item in tax_container_data:
        tax_code = item.get("taxObjectCode", "")
        pph_pasal = item.get("pphPasal", "")
        
        # Get category from MOI mapping
        if tax_code in moi_mapping:
            category = moi_mapping[tax_code]
            item["category"] = category
            
            # Create typeOfTax
            type_of_tax = create_type_of_tax(pph_pasal, category)
            item["typeOfTax"] = type_of_tax
            
            updated_count += 1
        else:
            # If not found in mapping, set empty values
            item["category"] = ""
            item["typeOfTax"] = create_type_of_tax(pph_pasal, "")
            not_found_count += 1
    
    # Save updated data
    if output_file_path is None:
        output_file_path = tax_container_file_path
    
    print(f"\nUpdated {updated_count} items")
    print(f"Not found in MOI mapping: {not_found_count} items")
    print(f"\nSaving updated data to: {output_file_path}")
    
    save_json_file(Path(output_file_path), tax_container_data)
    
    print("✓ Successfully updated tax_container_data.json")
    
    # Show some examples
    print("\n--- Example updates ---")
    for i, item in enumerate(tax_container_data[:3]):
        print(f"\nTax Object Code: {item.get('taxObjectCode')}")
        print(f"  PPH Pasal: {item.get('pphPasal')}")
        print(f"  Category: {item.get('category')}")
        print(f"  Type of Tax: {item.get('typeOfTax')}")
    
    return tax_container_data


def insert_to_cosmos_db(
    data: List[Dict[str, Any]],
    connection_string: str,
    database_name: str,
    container_name: str = "tax"
):
    """
    Insert tax data to Cosmos DB container.
    
    Args:
        data: List of tax data items to insert
        connection_string: Cosmos DB connection string
        database_name: Database name
        container_name: Container name (default: "tax")
    """
    try:
        print(f"\n=== Inserting to Cosmos DB ===")
        print(f"Database: {database_name}")
        print(f"Container: {container_name}")
        
        # Connect to Cosmos DB
        client = CosmosClient.from_connection_string(connection_string)
        database = client.get_database_client(database_name)
        container = database.get_container_client(container_name)
        
        print(f"✓ Connected to Cosmos DB")
        
        # Insert items
        success_count = 0
        error_count = 0
        updated_count = 0
        
        for item in data:
            try:
                # Use taxId as the document id if it exists
                if "taxId" in item and "id" not in item:
                    item["id"] = str(item["taxId"])
                elif "id" not in item:
                    # Generate id from taxObjectCode if no id exists
                    item["id"] = item.get("taxObjectCode", "").replace("-", "_")
                
                # Try to upsert (update if exists, insert if not)
                container.upsert_item(body=item)
                success_count += 1
                
                if success_count % 50 == 0:
                    print(f"  Processed {success_count} items...")
                    
            except exceptions.CosmosHttpResponseError as e:
                error_count += 1
                print(f"  Error inserting item {item.get('taxObjectCode', 'unknown')}: {e.message}")
            except Exception as e:
                error_count += 1
                print(f"  Unexpected error inserting item {item.get('taxObjectCode', 'unknown')}: {str(e)}")
        
        print(f"\n✓ Insertion complete!")
        print(f"  Successfully inserted/updated: {success_count}")
        print(f"  Errors: {error_count}")
        
        return success_count, error_count
        
    except exceptions.CosmosHttpResponseError as e:
        print(f"\n✗ Cosmos DB Error: {e.message}")
        raise
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        raise


if __name__ == "__main__":
    # Load environment variables from .env file
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)
    print(f"Loaded environment from: {env_path}\n")
    
    # Define file paths
    base_dir = Path(__file__).parent.parent
    
    moi_file = r"C:\Users\AF341XK\Downloads\MOI - Tax Object and Tax Rates (Update 13.01.2026).json"
    tax_container_file = base_dir / "tax_container_data.json"
    
    # Optional: specify output file path if you want to keep original
    # output_file = base_dir / "tax_container_data_updated.json"
    output_file = None  # This will overwrite the original file
    
    print("=== Tax Container Data Modification ===\n")
    
    updated_data = modify_tax_container_data(
        moi_file_path=moi_file,
        tax_container_file_path=str(tax_container_file),
        output_file_path=output_file
    )
    
    # Insert to Cosmos DB
    cosmos_connection_string = os.getenv("COSMOSDB_CONNECTION_STRING")
    cosmos_database_name = os.getenv("COSMOSDB_DATABASE", "TaxManagement")
    
    if cosmos_connection_string:
        try:
            insert_to_cosmos_db(
                data=updated_data,
                connection_string=cosmos_connection_string,
                database_name=cosmos_database_name,
                container_name="tax"
            )
        except Exception as e:
            print(f"\n⚠ Warning: Failed to insert to Cosmos DB. Data has been saved to JSON file.")
            print(f"  Error: {str(e)}")
    else:
        print("\n⚠ COSMOS_CONNECTION_STRING not found in environment variables.")
        print("  Skipping Cosmos DB insertion. Data has been saved to JSON file only.")

