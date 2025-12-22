import translationMappings from './mappings';

/**
 * Advanced content translator for translating entire document sections
 */
class ContentTranslator {
  constructor() {
    this.mappings = translationMappings;
  }

  /**
   * Translate content elements in the DOM
   * @param {string} targetLang - Target language ('en' or 'ur')
   */
  translateDOMContent(targetLang) {
    // Translate main content areas
    this.translateElementsBySelector('.markdown', targetLang);
    this.translateElementsBySelector('h1', targetLang);
    this.translateElementsBySelector('h2', targetLang);
    this.translateElementsBySelector('h3', targetLang);
    this.translateElementsBySelector('h4', targetLang);
    this.translateElementsBySelector('p', targetLang);
    this.translateElementsBySelector('li', targetLang);
    this.translateElementsBySelector('.container', targetLang);
  }

  /**
   * Translate elements by CSS selector
   * @param {string} selector - CSS selector for elements to translate
   * @param {string} targetLang - Target language ('en' or 'ur')
   */
  translateElementsBySelector(selector, targetLang) {
    const elements = document.querySelectorAll(selector);

    elements.forEach(element => {
      // Skip if it's the translation toggle button to avoid translation
      if (element.classList.contains('translateButton') ||
          element.closest('.translationToggle')) {
        return;
      }

      // Translate the text content
      const originalText = element.textContent;
      const translatedText = this.translateText(originalText, targetLang);

      if (originalText !== translatedText) {
        // Only update if translation is different
        element.textContent = translatedText;

        // For headings and other important elements, also update the direction
        if (['H1', 'H2', 'H3', 'H4', 'P'].includes(element.tagName)) {
          element.dir = targetLang === 'ur' ? 'rtl' : 'ltr';
          element.style.textAlign = targetLang === 'ur' ? 'right' : 'left';
        }
      }
    });
  }

  /**
   * Translate a single text string
   * @param {string} text - Text to translate
   * @param {string} targetLang - Target language ('en' or 'ur')
   * @returns {string} - Translated text
   */
  translateText(text, targetLang) {
    if (!text || typeof text !== 'string') {
      return text;
    }

    // Check if we have a direct mapping for this text
    const normalizedText = this.normalizeText(text);

    for (const [englishText, mapping] of Object.entries(this.mappings)) {
      const normalizedEnglish = this.normalizeText(englishText);

      if (normalizedText.includes(normalizedEnglish)) {
        const replacement = targetLang === 'ur' ? mapping.ur : mapping.en;
        return text.replace(new RegExp(this.escapeRegExp(englishText), 'gi'), replacement);
      }
    }

    return text;
  }

  /**
   * Normalize text for comparison
   * @param {string} text - Text to normalize
   * @returns {string} - Normalized text
   */
  normalizeText(text) {
    if (!text) return '';
    return text.trim().toLowerCase().replace(/\s+/g, ' ');
  }

  /**
   * Escape special characters in a string for use in a RegExp
   * @param {string} string - String to escape
   * @returns {string} - Escaped string
   */
  escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  /**
   * Add CSS classes for RTL styling
   * @param {string} targetLang - Target language
   */
  applyStyling(targetLang) {
    if (targetLang === 'ur') {
      // Add RTL-specific classes to body
      document.body.classList.add('urdu-content');
      document.body.classList.remove('english-content');
    } else {
      document.body.classList.add('english-content');
      document.body.classList.remove('urdu-content');
    }
  }
}

const contentTranslator = new ContentTranslator();
export default contentTranslator;