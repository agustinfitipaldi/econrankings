#!/usr/bin/env python3

import glob
import re
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path

def extract_category_from_filename(filename):
    """Extract three-letter category code from filename like 'top.cdm.html'"""
    match = re.search(r'top\.([a-z]{3})\.html', filename)
    return match.group(1) if match else None

def clean_institution_name(html_content):
    """Extract clean institution name from HTML link"""
    soup = BeautifulSoup(html_content, 'html.parser')
    link = soup.find('a')
    if link:
        return link.get_text().strip()
    return html_content.strip()

def parse_ranking_file(filepath):
    """Parse a single HTML ranking file and return institution data"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all table rows with ranking data
    # Look for TR tags that contain TD with institution links
    rows = soup.find_all('tr')
    
    institutions = {}
    
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 5:  # Rank, Institution, Score, Authors, Share
            try:
                # Skip header rows and malformed data
                rank_cell = cells[0].get_text().strip()
                if not rank_cell or rank_cell in ['Entity', 'TD']:
                    continue
                
                institution_html = str(cells[1])
                institution_name = clean_institution_name(institution_html)
                
                # Skip empty institution names
                if not institution_name:
                    continue
                
                overall_score = float(cells[2].get_text().strip())
                author_count = int(cells[3].get_text().strip())
                author_share = float(cells[4].get_text().strip())
                
                institutions[institution_name] = {
                    'overall_score': overall_score,
                    'author_count': author_count,
                    'author_share': author_share
                }
                
            except (ValueError, IndexError):
                # Skip rows with invalid data
                continue
    
    return institutions

def main():
    """Main function to process all ranking files and generate CSV outputs"""
    
    # Find all ranking HTML files
    html_files = glob.glob('top.*.html')
    
    if not html_files:
        print("No ranking HTML files found in current directory")
        return
    
    print(f"Found {len(html_files)} ranking files")
    
    # Data structures to hold all institutions and categories
    all_institutions = set()
    category_data = {}
    
    # Process each HTML file
    for filepath in html_files:
        category = extract_category_from_filename(filepath)
        if not category:
            print(f"Skipping {filepath} - couldn't extract category")
            continue
            
        print(f"Processing {filepath} (category: {category})")
        
        institutions = parse_ranking_file(filepath)
        category_data[category] = institutions
        all_institutions.update(institutions.keys())
        
        print(f"  Found {len(institutions)} institutions")
    
    # Convert to sorted list for consistent ordering
    all_institutions = sorted(all_institutions)
    categories = sorted(category_data.keys())
    
    print(f"\nTotal unique institutions: {len(all_institutions)}")
    print(f"Categories: {', '.join(categories)}")
    
    # Create DataFrames for each metric
    overall_scores = pd.DataFrame(index=all_institutions, columns=categories)
    author_counts = pd.DataFrame(index=all_institutions, columns=categories)
    author_shares = pd.DataFrame(index=all_institutions, columns=categories)
    
    # Fill in the data
    for category, institutions in category_data.items():
        for institution, data in institutions.items():
            overall_scores.loc[institution, category] = data['overall_score']
            author_counts.loc[institution, category] = data['author_count']
            author_shares.loc[institution, category] = data['author_share']
    
    # Save to CSV files
    overall_scores.to_csv('rankings_overall_scores.csv')
    author_counts.to_csv('rankings_author_counts.csv')
    author_shares.to_csv('rankings_author_shares.csv')
    
    print(f"\nGenerated CSV files:")
    print("- rankings_overall_scores.csv")
    print("- rankings_author_counts.csv")  
    print("- rankings_author_shares.csv")

if __name__ == '__main__':
    main()