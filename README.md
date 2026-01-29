# Private Leak Database & Search Service

A personal security service to store and search leaked database credentials for security monitoring purposes.

## Features

- **Data Ingestion**: Automatically converts text/CSV files to efficient Parquet format
- **Fast Search**: DuckDB-powered search for instant email/domain lookups
- **Web Interface**: Browser-based search with terminal-style UI
- **Automated Processing**: GitHub Actions workflow for batch processing

## Quick Start

### 1. Add Leaked Data

Place text files with credentials in the `incoming/` directory. Format should be:

```
email:password
email:password
...
```

### 2. Process Data

Run the ingestion script:

```bash
python scripts/ingest.py
```

This will:
- Parse the text files
- Hash all passwords using SHA256 (raw credentials are never stored)
- Convert to Parquet format with compression
- Store in `leaks/` directory
- Remove processed files from `incoming/`

### 3. Search

Open `index.html` in your browser (must be served via HTTP, not file://):

```bash
# Using Python's built-in server
python -m http.server 8000
```

Then visit `http://localhost:8000` and:
- **Search by email**: Enter full or partial email address
- **Search by domain**: Enter domain name (e.g., "gmail.com")
- **Browse all**: Click "Browse All" to see first 100 records
- **Hash verification**: Passwords are stored as SHA256 hashes for security verification

## File Structure

```
.
├── index.html              # Web search interface
├── scripts/
│   └── ingest.py          # Data ingestion script
├── incoming/              # Place raw text files here
├── leaks/                 # Processed Parquet files stored here
└── .github/workflows/
    └── process.yml        # Automated processing
```

## Data Format

The ingestion script expects delimited text files (CSV, colon-separated, etc.):
- Email in first column
- Password in second column
- Other columns ignored

Example formats:
```
email:password
email;password
email,password
```

## GitHub Actions

The workflow automatically:
1. Triggers on pushes to `incoming/`
2. Runs the ingestion script
3. Commits processed `.parquet` files
4. Removes processed `.txt` files

## Security Notes

- **Private use only**: This is for personal security monitoring
- **Keep private**: Ensure repository remains private
- **Local hosting**: Use local HTTP server, not public hosting
- **Data privacy**: Leaked credentials' passwords are hashed using SHA256 before storage; raw credentials are never persisted
- **Hash verification**: Use hashes to verify compromised accounts without exposing raw passwords

## Technologies

- **DuckDB**: Fast analytical database engine
- **Parquet**: Columnar storage with ZSTD compression
- **DuckDB-Wasm**: Client-side querying in browser
- **GitHub Actions**: Automated workflow processing
