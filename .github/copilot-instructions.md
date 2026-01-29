# AI Coding Agent Instructions

This is a **Private Leak Database & Search Service** - a personal security tool for storing and searching compromised database credentials using DuckDB for fast queries.

## Architecture Overview

The project has three integrated components:

1. **Data Ingestion** (`scripts/ingest.py`): Converts raw text/CSV files from `incoming/` to compressed Parquet format in `leaks/` using DuckDB's `read_csv()` with auto-detection and ZSTD compression
2. **Web Interface** (`index.html`): Browser-based search UI using DuckDB-Wasm for client-side querying (no backend)
3. **Automation** (`.github/workflows/process.yml`): GitHub Actions automatically triggers ingestion when files are pushed to `incoming/`, then commits Parquet output and removes processed files

## Critical Patterns & Conventions

### Data Processing (ingest.py)
- Uses `duckdb.connect()` for in-memory database operations
- **Password hashing**: All passwords are hashed using SHA256 before storage; raw credentials are never persisted
- Assumes delimited text format with email (column 1) and password (column 2); other columns ignored
- **Auto-detection**: `auto_detect=True` in `read_csv()` handles multiple delimiters (`:`, `,`, `;`)
- **Compression**: Always use ZSTD codec for Parquet output (`CODEC 'ZSTD'`) for optimal data compression
- **Error handling**: Script silently exits if `incoming/` is empty; GitHub Actions uses `2>/dev/null || true` to suppress errors during cleanup
- **File cleanup**: Always remove processed `.txt` files after successful conversion to prevent re-processing

### Web Frontend (index.html)
- **DuckDB-Wasm**: Loads from CDN v1.28.0 with dual bundle selection (MVP fallback, EH primary)
- **Search logic**: 
  - Query with `@` → exact email search using `ILIKE '%email%'` (case-insensitive)
  - Query without `@` → domain search using `ILIKE '%@%domain%'`
  - Empty query → browse first 100 records
- **Data source**: Queries glob pattern `read_parquet('leaks/*.parquet')` to read all processed files
- **Column mapping**: `email` and `password_hash` (SHA256-hashed); passwords are never displayed in plain text
- **Results limit**: Hard-capped at 100 rows to prevent browser freezing with large datasets
- **Security**: Uses `escapeHtml()` for XSS prevention; SQL injection mitigated with `.replace(/'/g, "''")` (though ILIKE is safer than WHERE IN)
- **Status tracking**: Updates `statusEl` with "Initializing", "Searching", "Found X results", etc. for user feedback

### Styling
- Retro terminal theme: `#00ff00` (green) on `#0a0a0a` (dark black)
- Sticky table headers for scrolling through results
- Hover states on buttons and table rows for interactivity

## Developer Workflows

### Local Development
```bash
# Serve the web interface locally (required - file:// protocol breaks DuckDB-Wasm)
python -m http.server 8000
```

Then visit `http://localhost:8000`

### Local Data Ingest
```bash
# Place raw credential files in incoming/
cp leak-data.txt incoming/
python scripts/ingest.py
```

### Automated Processing (GitHub Actions)
- Trigger: Push any `.txt` file to `incoming/` directory
- Runs on Ubuntu with Python 3.10
- Commits `.parquet` files to `leaks/`
- Removes processed `.txt` files
- Commits changes with message "Auto-processed new leak data"

## Key Dependencies
- **DuckDB**: Backend data engine (both server-side Python and client-side Wasm)
- **Parquet**: Columnar storage format for efficient compression
- **GitHub Actions**: Automation orchestration
- **No backend server**: Wasm-based frontend queries Parquet files directly

## Important Notes for AI Agents
- **Glob pattern queries**: DuckDB's `read_parquet('leaks/*.parquet')` automatically discovers all Parquet files; no manual file listing needed
- **Delimiter auto-detection**: Don't assume fixed delimiters - DuckDB handles `:`, `,`, `;` automatically
- **Browser compatibility**: Must serve over HTTP/HTTPS; file:// protocol breaks DuckDB-Wasm worker initialization
- **Query safety**: ILIKE is safe for untrusted input; manual escaping uses SQL quote doubling, not dynamic value insertion
- **Large datasets**: Always add LIMIT clauses to prevent browser memory exhaustion
