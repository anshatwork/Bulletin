import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import pandas as pd
import os

def save_html_content(html_content):
    """Save the HTML content to a file in the current working directory"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"eternal_finance_{timestamp}.html"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(html_content))
        print(f"\nHTML content saved to: {os.path.abspath(filename)}")
    except Exception as e:
        print(f"Error saving HTML content: {e}")

def get_eternal_financial_info():
    url = "https://www.google.com/finance/quote/ETERNAL:NSE"
    
    try:
        # Headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Make the request
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Save the HTML content
        save_html_content(soup.prettify())
        
        # Extract key metrics
        metrics = {}
        
        # Find all data containers with class P6K39c or QXDnM
        data_containers = soup.find_all('div', class_=['P6K39c', 'QXDnM'])
        
        for container in data_containers:
            # Find the label (previous sibling or parent's previous sibling)
            label_element = container.find_previous('div', recursive=False)
            if label_element:
                label = label_element.text.strip()
                value = container.text.strip()
                
                if 'Market cap' in label:
                    metrics['Market Cap'] = value
                elif 'Volume' in label:
                    metrics['Average Trading Volume'] = value
        
        # Revenue data (Quarterly and Annual)
        revenue_data = {
            'Quarterly': {},
            'Annual': {}
        }
        
        # Find revenue containers
        revenue_sections = soup.find_all('div', class_=['P6K39c', 'QXDnM'], string=lambda text: text and 'Revenue' in text)
        
        for section in revenue_sections:
            # Get the time period (could be in a nearby element)
            period_element = section.find_next('div', class_=['P6K39c', 'QXDnM'])
            if period_element:
                period = period_element.text.strip()
                value = section.text.strip()
                
                # Determine if it's quarterly or annual based on the format
                if 'Q' in period:
                    revenue_data['Quarterly'][period] = value
                else:
                    revenue_data['Annual'][period] = value
        
        metrics['Revenue Data'] = revenue_data
        
        return metrics
    
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Error processing data: {e}")
        return None

def display_metrics(metrics):
    if not metrics:
        print("No data available")
        return
    
    print("\n=== Eternal Financial Metrics ===\n")
    
    # Display Market Cap and Volume
    print(f"Market Cap: {metrics.get('Market Cap', 'N/A')}")
    print(f"Average Trading Volume: {metrics.get('Average Trading Volume', 'N/A')}")
    
    # Display Revenue Data
    print("\nQuarterly Revenue:")
    quarterly_data = metrics.get('Revenue Data', {}).get('Quarterly', {})
    for quarter, revenue in quarterly_data.items():
        print(f"{quarter}: {revenue}")
    
    print("\nAnnual Revenue:")
    annual_data = metrics.get('Revenue Data', {}).get('Annual', {})
    for year, revenue in annual_data.items():
        print(f"{year}: {revenue}")

if __name__ == "__main__":
    metrics = get_eternal_financial_info()
    display_metrics(metrics) 