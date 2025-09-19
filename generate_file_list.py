#!/usr/bin/env python3
"""
Script to generate file list for the VPN Gate mirror API
This script creates a JSON file with all available historical CSV files
"""

import os
import json
import glob
from datetime import datetime

def generate_file_list():
    """Generate a list of all available CSV files with metadata"""
    
    # Base URL for raw GitHub content
    base_url = "https://raw.githubusercontent.com/funcra/vg-mirror/main"
    
    # Get current servers.csv info
    latest_info = {
        "filename": "servers.csv",
        "url": f"{base_url}/servers.csv",
        "description": "Most recent VPN Gate servers data",
        "is_latest": True
    }
    
    # Get historical files
    historical_files = []
    history_dir = "servers_history"
    
    if os.path.exists(history_dir):
        # Find all servers-*.csv files
        pattern = os.path.join(history_dir, "servers-*.csv")
        files = glob.glob(pattern)
        
        # Sort by filename (which includes datetime)
        files.sort(reverse=True)
        
        for file_path in files:
            filename = os.path.basename(file_path)
            
            # Extract datetime from filename (servers-YYYYMMDD-HHMM.csv)
            if filename.startswith("servers-") and filename.endswith(".csv"):
                datetime_str = filename[8:-4]  # Remove "servers-" and ".csv"
                
                # Try to parse the datetime
                try:
                    dt = datetime.strptime(datetime_str, "%Y%m%d-%H%M")
                    formatted_datetime = dt.strftime("%Y-%m-%d %H:%M JST")
                except ValueError:
                    formatted_datetime = datetime_str
                
                historical_files.append({
                    "filename": filename,
                    "url": f"{base_url}/{history_dir}/{filename}",
                    "description": f"VPN Gate servers data from {formatted_datetime}",
                    "datetime": datetime_str,
                    "formatted_datetime": formatted_datetime
                })
    
    # Create the complete API response
    api_data = {
        "latest": latest_info,
        "historical": historical_files,
        "total_files": len(historical_files) + 1,
        "update_frequency": "Every 2 hours",
        "timezone": "JST (UTC+9)",
        "max_history": 10,
        "generated_at": datetime.now().isoformat(),
        "usage": {
            "latest_download": f"curl -O {base_url}/servers.csv",
            "historical_download": f"curl -O {base_url}/servers_history/servers-YYYYMMDD-HHMM.csv",
            "note": "Replace YYYYMMDD-HHMM with actual datetime from available files"
        }
    }
    
    return api_data

def main():
    """Main function to generate and save the file list"""
    try:
        api_data = generate_file_list()
        
        # Save to JSON file
        output_file = "servers_history/info.json"
        with open(output_file, 'w') as f:
            json.dump(api_data, f, indent=2)
        
        print(f"Generated file list with {api_data['total_files']} files")
        print(f"Latest: {api_data['latest']['filename']}")
        print(f"Historical: {len(api_data['historical'])} files")
        
        # Also print the latest few files for reference
        print("\nRecent files:")
        for i, file_info in enumerate(api_data['historical'][:5]):
            print(f"  {i+1}. {file_info['filename']} - {file_info['formatted_datetime']}")
        
        if len(api_data['historical']) > 5:
            print(f"  ... and {len(api_data['historical']) - 5} more files")
            
    except Exception as e:
        print(f"Error generating file list: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
