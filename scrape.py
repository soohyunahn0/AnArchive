import requests
from bs4 import BeautifulSoup
import time
import json
from urllib.parse import urljoin

class Scraper:
    def __init__(self):
        self.session = requests.Session()
        # Set a user agent to be respectful
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_work(self, url):
        """
        Scrape a single AO3 work page for title, author, tags, and summary.
        
        Args:
            url (str): The URL of the AO3 work
            
        Returns:
            dict: Dictionary containing scraped information
        """
        try:
            time.sleep(1)
            
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract work information
            work_data = {
                'url': url,
                'title': self._get_title(soup),
                'author': self._get_author(soup),
                'tags': self._get_tags(soup),
                'summary': self._get_summary(soup),
                'additional_tags': self._get_additional_tags(soup),
                'rating': self._get_rating(soup),
                'warnings': self._get_warnings(soup),
                'word_count': self._get_word_count(soup),
                'chapters': self._get_chapters(soup)
            }
            
            return work_data
            
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
        except Exception as e:
            print(f"Error parsing {url}: {e}")
            return None
    
    def _get_title(self, soup):
        """Extract the work title"""
        title_elem = soup.find('h2', class_='title heading')
        return title_elem.get_text(strip=True) if title_elem else "No title found"
    
    def _get_author(self, soup):
        """Extract the author name(s)"""
        author_elem = soup.find('h3', class_='byline heading')
        if author_elem:
            # Get all author links
            author_links = author_elem.find_all('a', rel='author')
            if author_links:
                authors = [link.get_text(strip=True) for link in author_links]
                return ', '.join(authors)
        return "No author found"
    
    def _get_tags(self, soup):
        """Extract all tags (fandom, relationship, character, etc.)"""
        tags = {}
        
        # Fandom tags
        fandom_list = soup.find('dd', class_='fandom tags')
        if fandom_list:
            tags['fandoms'] = [tag.get_text(strip=True) for tag in fandom_list.find_all('a', class_='tag')]
        
        # Relationship tags
        relationship_list = soup.find('dd', class_='relationship tags')
        if relationship_list:
            tags['relationships'] = [tag.get_text(strip=True) for tag in relationship_list.find_all('a', class_='tag')]
        
        # Character tags
        character_list = soup.find('dd', class_='character tags')
        if character_list:
            tags['characters'] = [tag.get_text(strip=True) for tag in character_list.find_all('a', class_='tag')]
        
        # Additional tags
        additional_list = soup.find('dd', class_='freeform tags')
        if additional_list:
            tags['additional_tags'] = [tag.get_text(strip=True) for tag in additional_list.find_all('a', class_='tag')]
        
        return tags
    
    def _get_additional_tags(self, soup):
        """Extract additional/freeform tags specifically"""
        additional_list = soup.find('dd', class_='freeform tags')
        if additional_list:
            return [tag.get_text(strip=True) for tag in additional_list.find_all('a', class_='tag')]
        return []
    
    def _get_summary(self, soup):
        """Extract the work summary"""
        summary_elem = soup.find('div', class_='summary')
        if summary_elem:
            # Get the blockquote content, which contains the actual summary
            blockquote = summary_elem.find('blockquote')
            if blockquote:
                return blockquote.get_text(strip=True)
        return "No summary found"
    
    def _get_rating(self, soup):
        """Extract the rating"""
        rating_elem = soup.find('dd', class_='rating tags')
        if rating_elem:
            rating_tag = rating_elem.find('a', class_='tag')
            return rating_tag.get_text(strip=True) if rating_tag else "No rating found"
        return "No rating found"
    
    def _get_warnings(self, soup):
        """Extract warnings"""
        warnings_elem = soup.find('dd', class_='warning tags')
        if warnings_elem:
            warning_tags = warnings_elem.find_all('a', class_='tag')
            return [tag.get_text(strip=True) for tag in warning_tags]
        return []
    
    def _get_word_count(self, soup):
        """Extract word count"""
        stats = soup.find('dl', class_='stats')
        if stats:
            word_elem = stats.find('dd', class_='words')
            return word_elem.get_text(strip=True) if word_elem else "Unknown"
        return "Unknown"
    
    def _get_chapters(self, soup):
        """Extract chapter information"""
        stats = soup.find('dl', class_='stats')
        if stats:
            chapter_elem = stats.find('dd', class_='chapters')
            return chapter_elem.get_text(strip=True) if chapter_elem else "Unknown"
        return "Unknown"
    
    def scrape_multiple_works(self, urls):
        """
        Scrape multiple AO3 works
        
        Args:
            urls (list): List of AO3 work URLs
            
        Returns:
            list: List of dictionaries containing work information
        """
        results = []
        
        for i, url in enumerate(urls, 1):
            print(f"Scraping work {i}/{len(urls)}: {url}")
            work_data = self.scrape_work(url)
            if work_data:
                results.append(work_data)
                print(f"Successfully scraped: {work_data['title']}")
            else:
                print(f"Failed to scrape: {url}")
        
        return results
    
    def save_to_json(self, data, filename='works.json'):
        """Save scraped data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to {filename}")

# Example usage
if __name__ == "__main__":
    scraper = Scraper()
    
    # Example URLs - replace with actual AO3 work URLs
    # urls = [
    #    "https://archiveofourown.org/works/12345678",
    #    "https://archiveofourown.org/works/87654321",
    #     Add more URLs as needed
    # ]
    
    # Scrape single work
    print("=== Scraping Single Work ===")
    single_work = scraper.scrape_work("https://archiveofourown.org/works/12345678")
    if single_work:
        print(f"Title: {single_work['title']}")
        print(f"Author: {single_work['author']}")
        print(f"Summary: {single_work['summary'][:100]}...")
        print(f"Tags: {single_work['tags']}")
    
    # Scrape multiple works
    #print("\n=== Scraping Multiple Works ===")
    # all_works = scraper.scrape_multiple_works(urls)
    
    # Save to JSON
    # scraper.save_to_json(all_works)
    
    # Print basic info for each work
    #for work in all_works:
    #     print(f"\nTitle: {work['title']}")
    #     print(f"Author: {work['author']}")
    #     print(f"Word Count: {work['word_count']}")
    #     print(f"Chapters: {work['chapters']}")