# PartDB-KiCad-Sync

Sync your [Part-DB](https://github.com/Part-DB/Part-DB-server) component library to a local SQLite database for use as a [KiCad Database Library](https://docs.kicad.org/9.0/en/eeschema/eeschema.html#database-libraries).

## Why?

Part-DB has built-in [KiCad HTTP Library](https://docs.part-db.de/usage/eda_integration.html) support, but it suffers from [missing field data in the symbol chooser](https://gitlab.com/kicad/code/kicad/-/issues/23023) and slow performance due to multiple round-trip API calls.

This script works around those issues by syncing Part-DB data to a local SQLite file via the full REST API, then connecting KiCad through its ODBC-based Database Library feature.

```
Part-DB Server  --REST API-->  sync_partdb.py  -->  partdb.sqlite  --ODBC-->  KiCad
```

## What you get

- All parts with symbol and footprint references (using your existing KiCad EDA config in Part-DB)
- Manufacturer and MPN
- Pricing at a configurable quantity break (default: 1000 pcs)
- Stock levels
- Supplier part numbers and URLs
- Datasheet links
- All Part-DB parameters as additional fields (electrical specs, package info, etc.)
- Direct link back to each part's Part-DB page
- Parts grouped by Part-DB category in the KiCad symbol chooser
- In-place database updates (no need to close KiCad, just re-open the symbol chooser)

## Prerequisites

- **Python 3.8+** (no third-party packages required, uses only stdlib)
- **SQLite3 ODBC Driver** (required by KiCad to read the database)
- **Part-DB server** with API access enabled and an API token
- **KiCad 7.0+** (database library support)

### Installing the SQLite3 ODBC Driver

**Windows:**

Download and install from http://www.ch-werner.de/sqliteodbc/ (`sqliteodbc_w64.exe` for 64-bit).

This registers the `SQLite3 ODBC Driver` that the `.kicad_dbl` config references.

**macOS:**

```bash
brew install sqliteodbc
```

The driver installs to `/opt/homebrew/lib/libsqlite3odbc.dylib` (Apple Silicon) or `/usr/local/lib/libsqlite3odbc.dylib` (Intel).

You may need to update the driver name in `partdb.kicad_dbl` from `{SQLite3 ODBC Driver}` to `{SQLite3}` depending on how it registers.

**Linux (Debian/Ubuntu):**

```bash
sudo apt install libsqliteodbc
```

### Getting a Part-DB API Token

1. Log into your Part-DB instance
2. Go to your user settings
3. Under API Tokens, create a new token
4. The token will look like `tcp_3d88537d89...`
5. Ensure the user has API read permissions (Miscellaneous -> API)

## Setup

1. Clone this repository (or download `sync_partdb.py` and `partdb_sync.json`):

```bash
git clone https://github.com/YOUR_USERNAME/partdb-kicad-sync.git
cd partdb-kicad-sync
```

2. Configure your Part-DB connection. There are three ways to provide the server URL and API token (highest priority wins):

   **Option A: Environment variables (recommended for CI/shared setups)**

   ```bash
   export PARTDB_URL="https://your-partdb-server.example.com"
   export PARTDB_TOKEN="tcp_your_api_token_here"
   python sync_partdb.py
   ```

   **Option B: Config file**

   Edit `partdb_sync.json`:

   ```json
   {
       "server_url": "https://your-partdb-server.example.com",
       "token": "tcp_your_api_token_here",
       "price_qty": 1000,
       "group_by": "category",
       "exclude_fields": []
   }
   ```

   **Option C: Command-line arguments**

   ```bash
   python sync_partdb.py --server "https://your-partdb-server.example.com" --token "tcp_your_token"
   ```

   You can mix these freely — for example, keep `server_url` and settings in the config file but pass the token via environment variable so it never touches disk.

3. Run the sync:

```bash
python sync_partdb.py
```

This creates two files:
- `partdb.sqlite` - the SQLite database with your parts
- `partdb.kicad_dbl` - the KiCad database library config (auto-generated)

4. Add the library to KiCad:
   - Open KiCad
   - Go to *Preferences* -> *Manage Symbol Libraries*
   - In the *Global Libraries* tab, click the **+** button
   - Browse to `partdb.kicad_dbl`
   - Set the Library Format to **Database**
   - Click OK

5. Test it:
   - Open a schematic
   - Place a symbol (*Place* -> *Add Symbol* or press `A`)
   - You should see your Part-DB categories in the library tree
   - Parts show with their IPN (Internal Part Number) as the identifier

## Configuration

All settings are in `partdb_sync.json`:

| Key | Default | Description |
|-----|---------|-------------|
| `server_url` | (required) | Your Part-DB server URL |
| `token` | `""` | Part-DB API token (Bearer auth) |
| `price_qty` | `1000` | Quantity break for pricing. Set to `1` for unit price, `100` for small batch, etc. |
| `group_by` | `"category"` | `"category"` creates one KiCad sub-library per Part-DB category. `"flat"` puts everything in a single table. |
| `exclude_fields` | `[]` | List of field/parameter column names to exclude from the KiCad library. Useful for hiding redundant fields. |

### Example with exclusions

```json
{
    "server_url": "https://partdb.example.com",
    "token": "tcp_your_token",
    "price_qty": 100,
    "group_by": "category",
    "exclude_fields": [
        "Mounting_Type",
        "Height_Seated_Max",
        "Number_of_Terminations"
    ]
}
```

## Updating

Just re-run the script:

```bash
python sync_partdb.py
```

The database is updated in-place using SQLite WAL mode, so KiCad can keep running. Re-open the symbol chooser to see changes.

## How it works

1. Fetches all parts from `/api/parts/` with pagination
2. For each part, fetches full details from `/api/parts/{id}` including:
   - EDA info (KiCad symbol, footprint, reference prefix)
   - Parameters (electrical specs from Part-DB)
   - Order details and pricing (finds the best price at the configured quantity break)
   - Attachments (first non-image attachment URL used as datasheet)
   - Stock levels
3. Groups parts by Part-DB category
4. Discovers all unique parameter names across all parts and creates columns for them
5. Writes/updates the SQLite database with WAL mode for concurrent access
6. Auto-generates the `.kicad_dbl` config matching the current database schema

### Part identifier (IPN)

The part identifier shown in KiCad's symbol chooser comes from Part-DB's **IPN** (Internal Part Number) field. If a part has no IPN assigned, the script falls back to the **MPN** (Manufacturer Part Number).

Assign IPNs in Part-DB for a clean library (e.g., `IC-0001`, `R-0402-10K`, `C-0402-100N`).

### Pricing logic

The script finds the best (lowest) price across all suppliers at the configured quantity break. It picks the highest available price break that doesn't exceed `price_qty`. For example, with `price_qty: 1000`:

- If breaks are at 1, 10, 100, 250, 500, 1000 -> uses the 1000-piece price
- If breaks are at 1, 10, 100 -> uses the 100-piece price (closest available)

## Files

| File | Description |
|------|-------------|
| `sync_partdb.py` | The sync script (Python 3.8+, no dependencies) |
| `partdb_sync.json` | Configuration (server URL, token, settings) |
| `partdb.sqlite` | Generated SQLite database (gitignored) |
| `partdb.kicad_dbl` | Generated KiCad database library config |

## Known limitations

- **Reference designator**: KiCad's database library format does not support overriding the reference prefix from the database. The reference comes from the KiCad symbol (e.g., `Device:R` -> "R", `Device:C` -> "C"). This is a [KiCad limitation](https://gitlab.com/kicad/code/kicad/-/issues/12845), not a bug in this script. Part-DB's HTTP library protocol supports this, but the ODBC/database library path does not.
- **Symbol chooser field display**: Unlike the HTTP library issue that motivated this project, the database library correctly shows all fields in the symbol chooser columns.
- **Read-only**: This is a one-way sync from Part-DB to KiCad. Changes made in KiCad are not written back to Part-DB.

## License

MIT
