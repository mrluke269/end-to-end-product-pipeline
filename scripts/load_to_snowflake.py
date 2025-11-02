import json # For handling JSON files
import snowflake.connector # Snowflake connector for Python
from config import snowflake_config, snowflake_table # Importing configuration details
from pathlib import Path # For handling file paths
import time # For timestamping temp files

def load_products_to_snowflake():
    
    failure_count = 0
    conn = None # Initialize connection variable
    cursor = None # Initialize cursor variable
    results = None  
    
    try:
        # 1. Connect to Snowflake
        conn = snowflake.connector.connect(**snowflake_config) # Establish connection
        cursor = conn.cursor() # Create a cursor object

        # 2. Define the file path
        file_path = Path(__file__).parent.parent / 'data' / 'product_details' / 'combined_products.json' # Path to JSON file

        # 3. Read JSON file
        try:
            with open(file_path, 'r') as file:
                products = json.load(file) # Load JSON data
        except Exception as e:
            print(f"Error reading JSON file: {e}")

        # 4. Extract ASINs from products
        try:
            incoming_asins = []
            for product in products:
                asin = product.get('data', {}).get('asin')
                incoming_asins.append(asin)
            print(f"Extracted {len(incoming_asins)} ASINs from JSON file.")
        except Exception as e:
            print(f"Error extracting ASINs: {e}")

        # 5. Check existing ASINs in Snowflake
        try:
            check_asin_query = f"""
        SELECT details_raw:asin FROM {snowflake_config['database']}.{snowflake_config['schema']}.{snowflake_table}
        """
            cursor.execute(check_asin_query)
            existing_asins = []
            for row in cursor.fetchall():
                existing_asins.append(row[0])
            print(f"Existing ASINs fetched from Snowflake: {len(existing_asins)}")
        except Exception as e:
            print(f"Error fetching existing ASINs: {e}")

        # 6. Identify new ASINs
        try:
            new_asins = set(incoming_asins) - set(existing_asins)
            if not new_asins:
                print("No new ASINs to load. Exiting.")
                return
            print(f"New ASINs to be inserted: {len(new_asins)}")
        except Exception as e:
            print(f"Error identifying new ASINs: {e}")

        # 7. Filter products to only include new ASINs
        try:
            new_products = []
            for product in products:
                asin = product.get('data', {}).get('asin')
                if asin in new_asins:
                    new_products.append(product)
            print(f"Products to be loaded: {len(new_products)}")
        except Exception as e:
            print(f"Error filtering new products: {e}")
            return
        

        # 8. Create temp directory and write new products to file
        temp_dir = Path(__file__).parent.parent / 'data' / 'temp' # Define temp directory path
        try:
            temp_dir.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist
        except Exception as e:
            print(f"Error creating temp directory: {e}")
            return
        temp_file_path = temp_dir / f'new_products_{int(time.time())}.json'  # Define the temp file path
        try:
            with open(temp_file_path, 'w') as temp_file:
                json.dump(new_products, temp_file)  # Write new_products to the temp JSON file
        except Exception as e:
            print(f"Error writing temp file: {e}")
            return

        # 9. Execute Put Command to upload file to Snowflake stage
        str_path = temp_file_path.as_posix() # Convert Path to string
        try:
            put_command = f"PUT file://{str_path} @~ AUTO_COMPRESS=false OVERWRITE=true" # Command to upload file to user stage

            cursor.execute(put_command) # Execute the PUT command
            print(cursor.fetchall()) # Print the result of the PUT command
        except Exception as e:
            print(f"Error during PUT command: {e}")
            return

        # 10. Execute Copy Command to load data into Snowflake table
        try:
            copy_command = f"""
            COPY INTO {snowflake_config['database']}.{snowflake_config['schema']}.{snowflake_table}(details_raw, request_id, load_at)
            FROM (
                SELECT $1:data, $1:request_id, current_timestamp() as load_at
                FROM @~/{temp_file_path.name}
                    )   
            FILE_FORMAT = (TYPE = 'JSON' STRIP_OUTER_ARRAY = TRUE);
            """ # Command to copy data from stage to table

            cursor.execute(copy_command) # Execute the COPY command
            results = cursor.fetchall() # Fetch results
            print(f"COPY command: successfully loaded {results} from stage.")
        except Exception as e:
            failure_count += 1
            print(f"Error during COPY command: {e}")
        

        # 11. Execute Remove Command to delete file from Snowflake stage
        try:
            remove_command = f"REMOVE @~/{temp_file_path.name}" # Command to remove file from user stage

            cursor.execute(remove_command) # Execute the REMOVE command
            print(f"REMOVE successful: {cursor.fetchall()}")
        except Exception as e:
            print(f"Error during REMOVE command: {e}")
    
    except Exception as e:
        print(f"A connection error occurred: {e}")
        return

    # 6. Close resources
    finally:
        # 4. Always close resources
        if cursor: # Close the cursor
            cursor.close()
        if conn: # Close the connection
            conn.close()

    print(f"Finished loading products. Success loaded: {file_path.name}, Failures: {failure_count}")

if __name__ == "__main__":
    load_products_to_snowflake()