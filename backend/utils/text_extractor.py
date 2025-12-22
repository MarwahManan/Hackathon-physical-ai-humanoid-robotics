"""
Text extraction utilities for Book Embeddings Pipeline
"""
import requests
from bs4 import BeautifulSoup
import re
from typing import Tuple, Optional
import logging
from config import Config


class TextExtractor:
    """Extracts clean text content from web pages"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        # Set a user agent to avoid being blocked
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def extract_text_from_url(self, url: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Extract clean text content from a URL

        Args:
            url: URL to extract text from

        Returns:
            Tuple of (title, content, hierarchy_path) or (None, None, None) on failure
        """
        try:
            self.logger.info(f"Extracting text from: {url}")

            response = self.session.get(url, timeout=15)
            if response.status_code != 200:
                self.logger.error(f"Failed to fetch {url}, status code: {response.status_code}")
                return None, None, None

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
                script.decompose()

            # Extract title
            title = self._extract_title(soup)

            # Extract main content
            content = self._extract_main_content(soup)

            # Determine hierarchy path from URL
            hierarchy_path = self._get_hierarchy_path(url)

            # Clean up the content
            content = self._clean_content(content)

            if not content or len(content.strip()) < 50:
                self.logger.warning(f"Content too short for {url}, length: {len(content) if content else 0}")
                return None, None, None

            self.logger.info(f"Successfully extracted content from {url} - Title: {title[:50] if title else 'No title'}...")
            return title, content, hierarchy_path

        except Exception as e:
            self.logger.error(f"Error extracting text from {url}: {str(e)}")
            return None, None, None

    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extract title from the soup object

        Args:
            soup: BeautifulSoup object

        Returns:
            Extracted title or None
        """
        # Try to find title in multiple ways
        title = None

        # Check for title tag
        if soup.title:
            title = soup.title.string.strip()

        # If no title found, try h1
        if not title or len(title) < 2:
            h1 = soup.find('h1')
            if h1:
                title = h1.get_text().strip()

        # If still no title, try any heading
        if not title or len(title) < 2:
            for i in range(1, 7):  # h1 to h6
                heading = soup.find(f'h{i}')
                if heading:
                    title = heading.get_text().strip()
                    break

        return title

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """
        Extract main content from the soup object

        Args:
            soup: BeautifulSoup object

        Returns:
            Extracted content string
        """
        # Try to find main content container using common selectors
        content_selectors = [
            'main',
            '.markdown',
            '.theme-doc-markdown',
            '.container',
            '.post-content',
            '.article-content',
            '.doc-content',
            '.content',
            '#content',
            '.main-content',
            '.post-body',
            '.article-body'
        ]

        content_element = None
        for selector in content_selectors:
            content_element = soup.select_one(selector)
            if content_element:
                break

        if content_element:
            # Remove navigation and sidebar elements that might be inside the main container
            for elem in content_element.find_all(['nav', 'header', 'footer', 'aside']):
                elem.decompose()

            # Extract text from remaining elements, prioritizing semantic HTML elements
            content_parts = []

            # Look for semantic content elements
            content_elements = content_element.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'blockquote', 'pre', 'code'])

            for elem in content_elements:
                text = elem.get_text().strip()
                if text and len(text) > 5:  # Filter out very short texts
                    content_parts.append(text)

            content = '\n\n'.join(content_parts)
        else:
            # If no specific container found, extract from body but exclude common non-content elements
            body = soup.find('body')
            if body:
                # Remove common non-content elements
                for elem in body.find_all(['nav', 'header', 'footer', 'aside', 'script', 'style']):
                    elem.decompose()

                # Extract all text
                content = body.get_text()
            else:
                content = soup.get_text()

        return content

    def _get_hierarchy_path(self, url: str) -> str:
        """
        Determine hierarchy path from URL

        Args:
            url: URL to extract hierarchy from

        Returns:
            Hierarchy path string
        """
        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        path_parts = [part for part in parsed_url.path.strip('/').split('/') if part]

        if len(path_parts) > 1:
            hierarchy_path = '/'.join(path_parts[:-1])  # Exclude the last part (the page itself)
        elif len(path_parts) == 1:
            hierarchy_path = path_parts[0]
        else:
            hierarchy_path = 'root'

        return hierarchy_path

    def _clean_content(self, content: str) -> str:
        """
        Clean up the extracted content

        Args:
            content: Raw content string

        Returns:
            Cleaned content string
        """
        if not content:
            return ""

        # Remove excessive whitespace while preserving paragraphs
        content = re.sub(r'\n\s*\n', '\n\n', content)  # Remove excessive newlines
        content = re.sub(r'[ \t]+', ' ', content)  # Normalize spaces
        content = content.strip()

        return content