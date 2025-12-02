#!/usr/bin/env python3
"""
Script to convert C# data seeding code to JSON files:
- POIs to places.json
- ArticleSources to source-articles/*.json
"""

import re
import json
import os
from pathlib import Path

def slugify(text):
    """Convert text to URL-friendly slug"""
    # Polish characters mapping
    replacements = {
        'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n',
        'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
        'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N',
        'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Convert to lowercase and replace spaces/special chars with underscores
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '_', text)
    return text.strip('_')

def extract_pois(content):
    """Extract Points of Interest from C# code"""
    pois = []
    # Pattern to match PointOfInterest objects
    pattern = r'new PointOfInterest\s*\{([^}]+)\}'
    
    matches = re.finditer(pattern, content, re.DOTALL)
    
    for match in matches:
        poi_content = match.group(1)
        
        # Extract Name
        name_match = re.search(r'Name\s*=\s*"([^"]+)"', poi_content)
        name = name_match.group(1) if name_match else ""
        
        # Extract Latitude
        lat_match = re.search(r'Latitude\s*=\s*([\d.]+)', poi_content)
        latitude = float(lat_match.group(1)) if lat_match else 0.0
        
        # Extract Longitude
        lon_match = re.search(r'Longitude\s*=\s*([\d.]+)', poi_content)
        longitude = float(lon_match.group(1)) if lon_match else 0.0
        
        # Extract ThumbnailUrl
        thumb_match = re.search(r'ThumbnailUrl\s*=\s*"([^"]+)"', poi_content)
        thumbnail = thumb_match.group(1) if thumb_match else ""
        
        if name:
            poi_id = slugify(name)
            pois.append({
                "id": poi_id,
                "name": name,
                "thumbnail": thumbnail,
                "description": ""  # Will be filled later or left empty
            })
    
    return pois

def extract_article_sources(content):
    """Extract ArticleSource objects from C# code"""
    sources = []
    
    # Split by "new ArticleSource" to find all instances
    parts = content.split('new ArticleSource')
    
    for part in parts[1:]:  # Skip first part (before first ArticleSource)
        # Extract PointOfInterestId
        poi_match = re.search(r'PointOfInterestId\s*=\s*pois\[(\d+)\]\.Id', part)
        if not poi_match:
            continue
        poi_index = int(poi_match.group(1))
        
        # Extract SourceUrl - find the first SourceUrl assignment
        url_match = re.search(r'SourceUrl\s*=\s*"([^"]+)"', part)
        if not url_match:
            continue
        source_url = url_match.group(1)
        
        # Extract Content - this is tricky because it can contain escaped quotes and newlines
        # Find Content = "..." pattern, handling escaped characters
        content_start = part.find('Content = "')
        if content_start == -1:
            continue
        
        content_start += len('Content = "')
        content_text = ""
        i = content_start
        escape_next = False
        
        while i < len(part):
            char = part[i]
            
            if escape_next:
                if char == 'r' and i + 1 < len(part) and part[i+1] == '\\' and i + 2 < len(part) and part[i+2] == 'n':
                    content_text += '\n'
                    i += 3
                elif char == 'n':
                    content_text += '\n'
                    i += 1
                elif char == '\\':
                    content_text += '\\'
                    i += 1
                elif char == '"':
                    content_text += '"'
                    i += 1
                else:
                    content_text += '\\' + char
                    i += 1
                escape_next = False
                continue
            
            if char == '\\':
                escape_next = True
                i += 1
                continue
            
            if char == '"':
                # Check if this is the end of Content or part of the string
                # Look ahead to see if we have ", followed by whitespace/newline and Comment or }
                look_ahead = part[i+1:].strip()
                if look_ahead.startswith(',') or look_ahead.startswith('Comment') or look_ahead.startswith('}'):
                    break
                content_text += char
                i += 1
                continue
            
            content_text += char
            i += 1
        
        article_content = content_text
        
        # Extract Comment
        comment_match = re.search(r'Comment\s*=\s*"([^"]*)"', part)
        comment = comment_match.group(1) if comment_match else ""
        
        sources.append({
            "poi_index": poi_index,
            "sourceUrl": source_url,
            "content": article_content,
            "comment": comment
        })
    
    return sources

def main():
    # Read the C# file
    script_dir = Path(__file__).parent
    cs_file = script_dir / "data.cs"
    
    if not cs_file.exists():
        print(f"Error: {cs_file} not found!")
        return
    
    with open(cs_file, 'r', encoding='utf-8') as f:
        cs_content = f.read()
    
    # Extract POIs
    print("Extracting POIs...")
    pois = extract_pois(cs_content)
    print(f"Found {len(pois)} POIs")
    
    # Extract ArticleSources
    print("Extracting ArticleSources...")
    article_sources = extract_article_sources(cs_content)
    print(f"Found {len(article_sources)} ArticleSources")
    
    # Group ArticleSources by POI index
    sources_by_poi = {}
    for source in article_sources:
        poi_idx = source["poi_index"]
        if poi_idx not in sources_by_poi:
            sources_by_poi[poi_idx] = []
        sources_by_poi[poi_idx].append({
            "sourceUrl": source["sourceUrl"],
            "content": source["content"],
            "comment": source["comment"]
        })
    
    # Write places.json
    places_file = script_dir / "places.json"
    with open(places_file, 'w', encoding='utf-8') as f:
        json.dump(pois, f, ensure_ascii=False, indent=2)
    print(f"Written {len(pois)} places to {places_file}")
    
    # Write source articles
    source_articles_dir = script_dir / "source-articles"
    source_articles_dir.mkdir(exist_ok=True)
    
    for poi_idx, sources in sources_by_poi.items():
        if poi_idx < len(pois):
            poi_id = pois[poi_idx]["id"]
            source_file = source_articles_dir / f"{poi_id}.json"
            
            with open(source_file, 'w', encoding='utf-8') as f:
                json.dump(sources, f, ensure_ascii=False, indent=2)
            print(f"Written {len(sources)} sources to {source_file}")
    
    print("\nConversion completed!")

if __name__ == "__main__":
    main()

