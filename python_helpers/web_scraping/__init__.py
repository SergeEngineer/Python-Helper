"""
Web Scraping Module

Utilities for web scraping and HTTP operations.
Note: Requires requests and beautifulsoup4 packages
"""

from typing import Dict, Any, Optional, List
import time
import random


def safe_request(url: str, headers: Optional[Dict[str, str]] = None, 
                timeout: int = 10, retries: int = 3) -> Optional[object]:
    """
    Make a safe HTTP request with retry logic.
    
    Args:
        url: URL to request
        headers: Optional HTTP headers
        timeout: Request timeout in seconds
        retries: Number of retry attempts
        
    Returns:
        Response object if successful, None otherwise
    """
    try:
        import requests
        
        default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        if headers:
            default_headers.update(headers)
            
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=default_headers, 
                                      timeout=timeout)
                response.raise_for_status()
                return response
                
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(random.uniform(1, 3))  # Random delay before retry
                    continue
                else:
                    print(f"Error after {retries} attempts: {e}")
                    return None
                    
    except ImportError:
        print("requests library not installed. Use: pip install requests")
        return None


def parse_html(html_content: str, parser: str = 'html.parser'):
    """
    Parse HTML content using BeautifulSoup.
    
    Args:
        html_content: HTML string to parse
        parser: Parser to use ('html.parser', 'lxml', etc.)
        
    Returns:
        BeautifulSoup object or None if failed
    """
    try:
        from bs4 import BeautifulSoup
        return BeautifulSoup(html_content, parser)
    except ImportError:
        print("beautifulsoup4 library not installed. Use: pip install beautifulsoup4")
        return None


def extract_links(soup_object, base_url: str = "") -> List[Dict[str, str]]:
    """
    Extract all links from a BeautifulSoup object.
    
    Args:
        soup_object: BeautifulSoup parsed HTML
        base_url: Base URL to resolve relative links
        
    Returns:
        List of dictionaries with link information
    """
    if not soup_object:
        return []
        
    links = []
    
    for link in soup_object.find_all('a', href=True):
        href = link['href']
        text = link.get_text(strip=True)
        
        # Handle relative URLs
        if base_url and href.startswith('/'):
            href = base_url.rstrip('/') + href
        elif base_url and not href.startswith(('http://', 'https://')):
            href = base_url.rstrip('/') + '/' + href.lstrip('/')
            
        links.append({
            'url': href,
            'text': text,
            'title': link.get('title', '')
        })
        
    return links


def extract_text(soup_object, tag: str = None, class_: str = None) -> List[str]:
    """
    Extract text from specific HTML elements.
    
    Args:
        soup_object: BeautifulSoup parsed HTML
        tag: HTML tag to search for (e.g., 'p', 'h1')
        class_: CSS class name to filter by
        
    Returns:
        List of text strings
    """
    if not soup_object:
        return []
        
    if tag:
        if class_:
            elements = soup_object.find_all(tag, class_=class_)
        else:
            elements = soup_object.find_all(tag)
    else:
        elements = [soup_object]
        
    return [elem.get_text(strip=True) for elem in elements if elem.get_text(strip=True)]


def download_file(url: str, filename: str, headers: Optional[Dict[str, str]] = None) -> bool:
    """
    Download a file from URL.
    
    Args:
        url: URL of the file to download
        filename: Local filename to save as
        headers: Optional HTTP headers
        
    Returns:
        True if successful, False otherwise
    """
    try:
        import requests
        
        response = safe_request(url, headers=headers)
        
        if response:
            with open(filename, 'wb') as f:
                f.write(response.content)
            return True
        return False
        
    except ImportError:
        print("requests library not installed. Use: pip install requests")
        return False
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False


# Export main functions
__all__ = [
    'safe_request',
    'parse_html',
    'extract_links',
    'extract_text',
    'download_file'
]