# OLX Car Cover Scraper

This Python script scrapes car cover listings from OLX India (https://www.olx.in/items/q-car-cover) and saves the results to both CSV and JSON files.

## Features

- Extracts car cover listings from OLX India
- Saves data in both CSV and JSON formats
- Handles errors gracefully
- Respects server by adding delays between requests
- Removes duplicate listings
- Includes debugging features

## Requirements

- Python 3.6 or higher
- requests library
- beautifulsoup4 library
- lxml parser

## Installation

1. Clone or download this repository
2. Install the required packages:

```bash
pip install requests beautifulsoup4 lxml
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

## Usage

Run the script using Python:

```bash
python olx_scraper.py
```

The script will create a folder named `olx_car_cover_results` and save the scraped data in both CSV and JSON formats with timestamps in the filenames.

If the script doesn't find any listings, it will save the raw HTML to `olx_car_cover_results/debug_page.html` for analysis.

## Output Format

The scraped data includes:
- **title**: The listing title
- **price**: The listed price
- **location_date**: Location and posting date information
- **link**: Direct link to the OLX listing

## Troubleshooting

If you encounter issues:

1. Make sure you have Python installed (check with `python --version`)
2. Ensure all required packages are installed
3. Check your internet connection
4. OLX may block automated requests - try running the script again later
5. If problems persist, check the debug HTML file for insights into the page structure

## Disclaimer

This script is for educational purposes only. Please respect OLX's terms of service and robots.txt. Use responsibly and avoid making too many requests in a short period of time.

## License

This project is open source and available under the MIT License.
