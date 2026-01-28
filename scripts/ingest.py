import duckdb
import os
import glob

# Find all .txt files in the incoming folder
incoming_files = glob.glob('incoming/*.txt')

if not incoming_files:
    print("No new leaks found in /incoming.")
    exit(0)

con = duckdb.connect()

for file_path in incoming_files:
    file_name = os.path.basename(file_path).replace('.txt', '')
    output_path = f'leaks/{file_name}.parquet'
    
    print(f"Processing {file_name}...")
    
    # Ingesting raw text. This assumes common formats like email:pass or email,pass
    # It auto-detects delimiters and compresses using ZSTD (the best for leaks)
    con.execute(f"""
        COPY (SELECT * FROM read_csv('{file_path}', 
            header=False, 
            columns={{'email': 'VARCHAR', 'password': 'VARCHAR'}}, 
            auto_detect=True)) 
        TO '{output_path}' (FORMAT 'PARQUET', CODEC 'ZSTD');
    """)
    
    # Remove raw file after successful conversion
    os.remove(file_path)
    print(f"Successfully converted to {output_path}")
