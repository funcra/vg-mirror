# VPN Gate Mirror

A GitHub Actions-powered mirror for VPN Gate servers data that automatically updates every 2 hours (JST).

## Overview

This repository automatically mirrors the VPN Gate servers CSV file from `http://www.vpngate.net/api/iphone/` and keeps it up-to-date using GitHub Actions. The mirror runs every 2 hours (JST) and commits any changes to the repository.

## Features

- **Automated Updates**: Runs every 2 hours (JST) via GitHub Actions cron job
- **Manual Trigger**: Supports manual execution via GitHub Actions workflow dispatch
- **Automatic Commits**: Automatically commits and pushes changes when the source data is updated
- **Reliable Source**: Mirrors data from the official VPN Gate API

## How It Works

1. The GitHub Actions workflow runs every 2 hours (JST)
2. Downloads the latest servers.csv from VPN Gate's API
3. Maintains rolling history of latest 10 CSV files total (1 current + 9 historical with datetime stamps)
4. Always commits new data since VPN Gate returns different data each time
5. Generates API metadata for easy programmatic access
6. The workflow can also be triggered manually

## Files

- `servers.csv` - The latest VPN Gate servers data (automatically updated)
- `servers_history/` - Directory containing up to 9 historical versions with datetime stamps
- `servers_history/info.json` - API metadata for all available files
- `servers_history/index.html` - Web interface for browsing historical data
- `.github/workflows/update-csv.yml` - GitHub Actions workflow configuration

## Usage

### Automatic Updates

The mirror runs automatically every 2 hours. No manual intervention required.

### Manual Updates

You can trigger a manual update by:

1. Going to the Actions tab in this repository
2. Selecting "Update CSV Mirror" workflow
3. Clicking "Run workflow"

### Accessing the Data

The `servers.csv` file contains the latest VPN Gate servers data and can be accessed directly from this repository. The file is updated automatically, so you can always get the most recent data.

## API Endpoints

### Latest Data
**Direct Download:**
```
https://raw.githubusercontent.com/funcra/vg-mirror/main/servers.csv
```

### Historical Data
**Format:** `servers-YYYYMMDD-HHMM.csv`
```
https://raw.githubusercontent.com/funcra/vg-mirror/main/servers_history/servers-20250919-1253.csv
```

### API Metadata
**Get list of all available files:**
```
https://raw.githubusercontent.com/funcra/vg-mirror/main/servers_history/info.json
```

### Web Interface
**Browse historical data:**
```
https://raw.githubusercontent.com/funcra/vg-mirror/main/servers_history/index.html
```

## Usage Examples

### Bash/Shell
```bash
# Download latest
curl -O https://raw.githubusercontent.com/funcra/vg-mirror/main/servers.csv

# Download specific version
curl -O https://raw.githubusercontent.com/funcra/vg-mirror/main/servers_history/servers-20250919-1253.csv

# Get list of available files
curl -s https://raw.githubusercontent.com/funcra/vg-mirror/main/servers_history/info.json | jq '.historical[].filename'
```

### Python
```python
import requests
import json

# Download latest
response = requests.get('https://raw.githubusercontent.com/funcra/vg-mirror/main/servers.csv')
with open('servers.csv', 'wb') as f:
    f.write(response.content)

# Get available files
api_response = requests.get('https://raw.githubusercontent.com/funcra/vg-mirror/main/servers_history/info.json')
files = json.loads(api_response.text)
print("Available files:", [f['filename'] for f in files['historical']])
```

### JavaScript/Node.js
```javascript
const https = require('https');
const fs = require('fs');

// Download latest
const file = fs.createWriteStream('servers.csv');
https.get('https://raw.githubusercontent.com/funcra/vg-mirror/main/servers.csv', (response) => {
    response.pipe(file);
});

// Get available files
https.get('https://raw.githubusercontent.com/funcra/vg-mirror/main/servers_history/info.json', (response) => {
    let data = '';
    response.on('data', (chunk) => data += chunk);
    response.on('end', () => {
        const files = JSON.parse(data);
        console.log('Available files:', files.historical.map(f => f.filename));
    });
});
```

## Workflow Schedule

- **Frequency**: Every 2 hours
- **Timezone**: JST (UTC+9)
- **Cron Expression**: `0 */2 * * *`

## Contributing

This is an automated mirror repository. The `servers.csv` file is automatically maintained and should not be manually edited. If you need to modify the update frequency or add additional features, please submit a pull request with your changes.

## License

This project mirrors data from VPN Gate. Please refer to VPN Gate's terms of service for data usage guidelines.

## Related

- [VPN Gate Official Website](http://www.vpngate.net/)