import requests
from bs4 import BeautifulSoup
import csv
import json
import time
import os

# Create the project directory if it doesn't exist
project_dir = 'olx_car_cover_results'
os.makedirs(project_dir, exist_ok=True)

def scrape_olx_car_covers():
    """
    Scrape car cover listings from OLX India
    """
    url = 'https://www.olx.in/items/q-car-cover'
    
    # Headers to mimic a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    }
    
    try:
        print("Fetching data from OLX India...")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try multiple approaches to find listings
        # Approach 1: Look for 'a' tags with href containing '/item/'
        listings = soup.find_all('a', href=lambda href: href and '/item/' in href)
        
        # If that doesn't work, try a more general approach
        if not listings:
            print("Trying alternative approach to find listings...")
            # Look for divs or other containers that might contain listings
            listings = soup.find_all('div', class_=lambda x: x and ('item' in x.lower() or 'listing' in x.lower()))
            
        # If still no listings, get all 'a' tags as a last resort
        if not listings:
            print("Using fallback approach to find listings...")
            listings = soup.find_all('a')
        
        results = []
        
        print(f"Found {len(listings)} potential listings. Processing...")
        
        for listing in listings:
            try:
                # Get all text from the listing
                listing_text = listing.get_text(strip=True)
                
                # Skip if it doesn't seem to be related to car covers
                if listing_text and ("car cover" in listing_text.lower() or "car" in listing_text.lower() and "cover" in listing_text.lower()):
                    # Extract title
                    title = listing_text[:100] + "..." if len(listing_text) > 100 else listing_text
                    
                    # Extract price - look for price patterns
                    price = "N/A"
                    price_elem = listing.find(string=lambda text: text and '₹' in text)
                    if price_elem:
                        price = price_elem.strip()
                    else:
                        # Try to find price in the listing text
                        import re
                        price_match = re.search(r'₹\s*[\d,]+', listing_text)
                        if price_match:
                            price = price_match.group(0)
                    
                    # Extract location and date
                    location_date = "N/A"
                    # Look for common location/date patterns
                    import re
                    location_date_match = re.search(r'[A-Za-z]+,\s*[A-Za-z]+|\d+\s+[A-Za-z]+\s+ago|Today|Yesterday', listing_text)
                    if location_date_match:
                        location_date = location_date_match.group(0)
                    
                    # Extract link
                    link = "N/A"
                    if listing.get('href'):
                        href = listing.get('href')
                        if href.startswith('http'):
                            link = href
                        elif href.startswith('/'):
                            link = "https://www.olx.in" + href
                        else:
                            link = "https://www.olx.in/" + href
                    
                    results.append({
                        'title': title,
                        'price': price,
                        'location_date': location_date,
                        'link': link
                    })
                
                # Add a small delay to be respectful to the server
                time.sleep(0.05)
                
            except Exception as e:
                print(f"Error processing listing: {e}")
                continue
        
        # Remove duplicates based on title
        unique_results = []
        seen_titles = set()
        for result in results:
            if result['title'] not in seen_titles:
                seen_titles.add(result['title'])
                unique_results.append(result)
        
        return unique_results
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def save_to_csv(data, filename=None):
    """
    Save data to CSV file
    """
    if not filename:
        filename = f'olx_car_cover_results/olx_car_covers_{int(time.time())}.csv'
    
    if not data:
        print("No data to save.")
        return
        
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'price', 'location_date', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for item in data:
            writer.writerow(item)
    
    print(f"Data saved to {filename}")

def save_to_json(data, filename=None):
    """
    Save data to JSON file
    """
    if not filename:
        filename = f'olx_car_cover_results/olx_car_covers_{int(time.time())}.json'
    
    if not data:
        print("No data to save.")
        return
        
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=2, ensure_ascii=False)
    
    print(f"Data saved to {filename}")

def main():
    """
    Main function to run the scraper
    """
    print("Starting OLX Car Cover Scraper...")
    
    # Scrape the data
    results = scrape_olx_car_covers()
    
    if results:
        print(f"Scraped {len(results)} car cover listings.")
        
        # Save to both CSV and JSON
        save_to_csv(results)
        save_to_json(results)
        
        # Also print first few results
        print("\nFirst 5 results:")
        for i, result in enumerate(results[:5]):
            print(f"{i+1}. Title: {result['title']}")
            print(f"   Price: {result['price']}")
            print(f"   Location & Date: {result['location_date']}")
            print(f"   Link: {result['link']}")
            print()
    else:
        print("No car cover listings found.")
        
        # For debugging, let's save the raw HTML to see what we're working with
        try:
            url = 'https://www.olx.in/items/q-car-cover'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            }
            response = requests.get(url, headers=headers, timeout=30)
            with open('olx_car_cover_results/debug_page.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("Saved raw HTML to debug_page.html for analysis.")
        except Exception as e:
            print(f"Could not save debug HTML: {e}")

if __name__ == "__main__":
    main()
