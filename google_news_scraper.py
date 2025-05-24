from GoogleNews import GoogleNews
import json
from datetime import datetime
from dateutil import parser
import sys
import requests
from bs4 import BeautifulSoup
import time

def setup_google_news():
    """Initialize GoogleNews with appropriate settings."""
    googlenews = GoogleNews()
    googlenews.set_lang('en')
    googlenews.set_period('7d')  # Get news from last 7 days
    return googlenews

def parse_date(date_str):
    """Parse date string from Google News into DD/MM/YYYY format."""
    try:
        # First try parsing with dateutil
        try:
            return parser.parse(str(date_str)).strftime('%d/%m/%Y')
        except:
            pass
        
        # If that fails, try handling relative dates
        date_str = str(date_str).lower()
        today = datetime.now()
        
        if 'hour' in date_str or 'minute' in date_str:
            return today.strftime('%d/%m/%Y')
        elif 'day' in date_str:
            try:
                days = int(''.join(filter(str.isdigit, date_str)))
                result_date = today.replace(day=today.day - days)
                return result_date.strftime('%d/%m/%Y')
            except:
                return today.strftime('%d/%m/%Y')
        
        # If all else fails, return today's date
        return today.strftime('%d/%m/%Y')
    except Exception as e:
        print(f"Error parsing date '{date_str}': {e}")
        return datetime.now().strftime('%d/%m/%Y')

def fetch_eternal_news():
    """Fetch news about Eternal stock from Google News."""
    try:
        googlenews = setup_google_news()
        search_term = "Eternal stock market"
        print(f"Fetching news for: {search_term}")
        
        googlenews.get_news(search_term)
        news_items = googlenews.results()
        
        if not news_items:
            print("No news items found.")
            return []
        
        formatted_news = []
        for item in news_items:
            try:
                # Get the date string and parse it
                date_str = parse_date(item.get('datetime', ''))
                
                # Get the article link and fetch its content
                link = item.get('link', '')
                print(f"Fetching content for: {item.get('title', 'No title')}")
                content = fetch_article_content(link) if link else ""
                
                news_item = {
                    "date": date_str,
                    "title": item.get('title', 'No title'),
                    "link": link,
                    "content": content
                }
                formatted_news.append(news_item)
                
                # Add a small delay between requests to be polite to the servers
                time.sleep(2)
                
            except Exception as e:
                print(f"Error processing news item: {e}")
                continue
        
        return formatted_news
    
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def save_news_to_file(news_items, filename="eternal_stock_news.json"):
    """Save news items to a JSON file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(news_items, f, indent=4, ensure_ascii=False)
        print(f"\nNews items saved to {filename}")
    except Exception as e:
        print(f"Error saving to file: {e}")

def fetch_article_content(url):
    """Fetch and extract the main content from a news article URL."""
    try:
        # Add headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Make the request with a timeout
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to find the main article content
        # This is a basic implementation - might need adjustment for specific news sites
        article_text = ""
        
        # Look for common article content containers
        content_containers = soup.find_all(['article', 'div'], class_=['article-content', 'article-body', 'story-content', 'content-body'])
        
        if content_containers:
            for container in content_containers:
                # Get all paragraphs within the container
                paragraphs = container.find_all('p')
                article_text += "\n".join([p.get_text().strip() for p in paragraphs])
        
        # If no content found in common containers, try getting all paragraphs
        if not article_text:
            paragraphs = soup.find_all('p')
            article_text = "\n".join([p.get_text().strip() for p in paragraphs])
        
        return article_text.strip()
    
    except Exception as e:
        print(f"Error fetching article content from {url}: {e}")
        return ""

def main():
    print("Starting Eternal Stock News Scraper...")
    news_items = fetch_eternal_news()
    
    if news_items:
        print(f"\nFound {len(news_items)} news items:")
        for item in news_items:
            print(f"\nDate: {item['date']}")
            print(f"Title: {item['title']}")
            print(f"Link: {item['link']}")
            if item['content']:
                print("\nContent Preview:")
                # Display first 500 characters of content with "..." if truncated
                content_preview = item['content'][:500]
                if len(item['content']) > 500:
                    content_preview += "..."
                print(content_preview)
            else:
                print("\nNo content available")
            print("\n" + "="*80)  # Separator between articles
        
        save_news_to_file(news_items)
    else:
        print("No news items were found or an error occurred.")

if __name__ == "__main__":
    main() 