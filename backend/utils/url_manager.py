"""
URL management utilities for Book Embeddings Pipeline
"""
import requests
from urllib.parse import urljoin, urlparse
from typing import List, Set
import xml.etree.ElementTree as ET
import logging
from config import Config


class URLManager:
    """Manages URL discovery and storage for the crawling process"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.visited_urls: Set[str] = set()
        self.target_base_url = Config.TARGET_BASE_URL

    def get_urls_from_sitemap(self, sitemap_url: str) -> List[str]:
        """
        Extract URLs from a sitemap

        Args:
            sitemap_url: URL of the sitemap to parse

        Returns:
            List of URLs extracted from the sitemap
        """
        try:
            self.logger.info(f"Fetching sitemap from: {sitemap_url}")
            response = requests.get(sitemap_url, timeout=30)
            response.raise_for_status()

            # Parse the XML sitemap
            root = ET.fromstring(response.content)

            urls = []
            # Handle both regular sitemaps and sitemap indexes
            for element in root:
                # Remove namespace if present
                tag = element.tag.split('}')[-1] if '}' in element.tag else element.tag

                if tag == 'url':
                    for loc in element:
                        loc_tag = loc.tag.split('}')[-1] if '}' in loc.tag else loc.tag
                        if loc_tag == 'loc':
                            url = loc.text.strip()
                            if self._is_valid_content_url(url):
                                urls.append(url)
                elif tag == 'sitemap':
                    for loc in element:
                        loc_tag = loc.tag.split('}')[-1] if '}' in loc.tag else loc.tag
                        if loc_tag == 'loc':
                            nested_sitemap_url = loc.text.strip()
                            self.logger.info(f"Found nested sitemap: {nested_sitemap_url}")
                            nested_urls = self.get_urls_from_sitemap(nested_sitemap_url)
                            urls.extend(nested_urls)

            self.logger.info(f"Found {len(urls)} URLs from sitemap")
            return urls

        except Exception as e:
            self.logger.error(f"Error parsing sitemap {sitemap_url}: {str(e)}")
            return []

    def crawl_for_urls(self, start_url: str, max_urls: int = 100) -> List[str]:
        """
        Crawl the website to discover all content URLs

        Args:
            start_url: Starting URL for crawling
            max_urls: Maximum number of URLs to discover

        Returns:
            List of discovered URLs
        """
        urls = set()
        to_crawl = [start_url]

        while to_crawl and len(urls) < max_urls:
            current_url = to_crawl.pop(0)

            if current_url in self.visited_urls or not current_url.startswith(self.target_base_url):
                continue

            self.visited_urls.add(current_url)
            self.logger.info(f"Crawling: {current_url}")

            try:
                response = requests.get(current_url, timeout=10)
                if response.status_code == 200:
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Find all links that are part of our documentation
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        full_url = urljoin(current_url, href)

                        # Only follow URLs within our domain and matching content paths
                        if (full_url.startswith(self.target_base_url) and
                            self._is_valid_content_url(full_url) and
                            full_url not in urls):
                            urls.add(full_url)
                            to_crawl.append(full_url)

                        # Limit the crawl to avoid infinite loops
                        if len(urls) >= max_urls:
                            break

            except Exception as e:
                self.logger.error(f"Error crawling {current_url}: {str(e)}")
                continue

        self.logger.info(f"Discovered {len(urls)} URLs through crawling")
        return list(urls)

    def _is_valid_content_url(self, url: str) -> bool:
        """
        Check if a URL is a valid content page

        Args:
            url: URL to check

        Returns:
            True if the URL is valid content, False otherwise
        """
        # Check if URL is from our target domain
        if not url.startswith(self.target_base_url):
            return False

        # Exclude common non-content URLs
        excluded_patterns = [
            '/tag/', '/category/', '/author/', '/feed', '/rss',
            '.jpg', '.jpeg', '.png', '.gif', '.pdf', '.zip', '.exe'
        ]

        for pattern in excluded_patterns:
            if pattern in url.lower():
                return False

        # Include content paths
        content_patterns = ['/docs/', '/blog/', '/modules/', '/research-articles', '/intro']
        has_content_pattern = any(pattern in url for pattern in content_patterns)

        # If no specific content pattern, check if it's not just the base URL
        if not has_content_pattern:
            # Allow base URL with path segments but not just the base
            parsed = urlparse(url)
            path_parts = [p for p in parsed.path.strip('/').split('/') if p]
            if len(path_parts) == 0:  # Just the base URL
                return False

        return True

    def get_all_urls(self) -> List[str]:
        """
        Get all URLs from both sitemap and crawling approaches

        Returns:
            Combined list of unique URLs
        """
        self.logger.info("Starting URL discovery process")

        # First try to get URLs from sitemap
        sitemap_urls = self.get_urls_from_sitemap(Config.TARGET_SITEMAP_URL)
        self.logger.info(f"Retrieved {len(sitemap_urls)} URLs from sitemap")

        # If sitemap doesn't have many URLs, also crawl
        if len(sitemap_urls) < 10:
            crawled_urls = self.crawl_for_urls(self.target_base_url)
            all_urls = list(set(sitemap_urls + crawled_urls))
        else:
            all_urls = sitemap_urls

        # Filter to only valid content URLs
        valid_urls = [url for url in all_urls if self._is_valid_content_url(url)]

        self.logger.info(f"Final URL count after filtering: {len(valid_urls)}")
        return valid_urls