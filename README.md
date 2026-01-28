# Private Leak Database & Search Service

A personal security service to store and search leaked database credentials for security monitoring purposes.

## Features

- **🔐 Firebase Authentication**: Real server-side authentication (not just client-side)
- **Data Ingestion**: Automatically converts text/CSV files to efficient Parquet format
- **Fast Search**: DuckDB-powered search for instant email/domain lookups
- **Web Interface**: Browser-based search with terminal-style UI
- **Automated Processing**: GitHub Actions workflow for batch processing

## Security & Authentication

This site uses **Firebase Authentication** for real server-side security:

- ✅ No passwords stored in code
- ✅ Managed by Google's infrastructure
- ✅ Add/remove users via Firebase Console
- ✅ Token-based authentication
- ✅ Brute-force protection included

**Setup Required:** You must configure Firebase to use this application.

👉 **[Complete Firebase Setup Guide →](FIREBASE_SETUP.md)**

**Quick Summary:**
1. Create free Firebase project
2. Enable Email/Password authentication
3. Add authorized users (email + password)
4. Copy Firebase config to `index.html`
5. Deploy and sign in with your credentials

**No Firebase setup yet?** The site will show authentication errors until you complete the Firebase configuration.

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
- **Data privacy**: Leaked credentials should never be shared

## Technologies

- **DuckDB**: Fast analytical database engine
- **Parquet**: Columnar storage with ZSTD compression
- **DuckDB-Wasm**: Client-side querying in browser
- **GitHub Actions**: Automated workflow processing
