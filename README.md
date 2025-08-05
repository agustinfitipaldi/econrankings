# RePEc Rankings Parser

Converts RePEc HTML ranking tables into CSV format. Takes the mess of HTML tables and gives you clean CSV files you can actually work with.

## What it does

Parses HTML files from RePEc's field rankings (like `top.cdm.html`, `top.mic.html`, etc.) and extracts:

- Institution names
- Overall scores  
- Author counts
- Author shares

Outputs three CSV files with institutions as rows and field categories as columns:

- `rankings_overall_scores.csv` - The main ranking scores
- `rankings_author_counts.csv` - Number of authors per institution per field
- `rankings_author_shares.csv` - Author share percentages

## Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

1. Put your RePEc HTML files in the same directory as the script
2. Files should be named like `top.{category}.html` (e.g., `top.cdm.html`, `top.mic.html`)
3. Run the parser:

```bash
source venv/bin/activate
python parse_rankings.py
```

## File Format Expected

The script expects RePEc HTML files with tables containing:
- Rank (1st column)
- Institution name with link (2nd column) 
- Overall score (3rd column)
- Number of authors (4th column)
- Author share (5th column)

## Output

Three CSV files will be generated in the same directory. Missing data (institutions not ranked in certain fields) will show as NaN in the CSV.

## Dependencies

- Python 3.6+
- pandas
- beautifulsoup4