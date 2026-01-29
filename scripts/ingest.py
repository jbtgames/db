import duckdb
import os
import glob
import hashlib

# Find all .txt files in the incoming folder
incoming_files = glob.glob('incoming/*.txt')

if not incoming_files:
    print("No new leaks found in /incoming.")
    exit(0)

con = duckdb.connect()

def hash_password(password):
    """Hash password using SHA256 for secure storage"""
    return hashlib.sha256(password.encode()).hexdigest()

for file_path in incoming_files:
    file_name = os.path.basename(file_path).replace('.txt', '')
    output_path = f'leaks/{file_name}.parquet'
    
    print(f"Processing {file_name}...")
    
    # Read CSV with auto-detected delimiter
    df = con.execute(f"""
        SELECT * FROM read_csv('{file_path}', 
            header=False, 
            columns={{'email': 'VARCHAR', 'password': 'VARCHAR'}}, 
            auto_detect=True)
    """).fetchall()
    
    # Hash passwords and prepare data
    hashed_rows = []
    for email, password in df:
        hashed_pwd = hash_password(password)
        hashed_rows.append((email, hashed_pwd))
    
    # Create temporary table with hashed data
    con.execute("DROP TABLE IF EXISTS temp_hashed")
    con.execute("""
        CREATE TABLE temp_hashed (
            email VARCHAR,
            password_hash VARCHAR
        )
    """)
    
    # Insert hashed data
    for email, password_hash in hashed_rows:
        con.execute(f"INSERT INTO temp_hashed VALUES (?, ?)", [email, password_hash])
    
    # Export to Parquet with ZSTD compression
    con.execute(f"""
        COPY temp_hashed TO '{output_path}' (FORMAT 'PARQUET', CODEC 'ZSTD')
    """)
    
    con.execute("DROP TABLE temp_hashed")
    
    # Remove raw file after successful conversion
    os.remove(file_path)
    print(f"Successfully converted and hashed {output_path}")
