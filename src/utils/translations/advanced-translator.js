import translationMappings from './mappings';

/**
 * Advanced translation system with fallback and caching capabilities
 */
class AdvancedTranslator {
  constructor() {
    this.mappings = translationMappings;
    this.translationCache = new Map();
    this.fallbackThreshold = 0.7; // Minimum match threshold for partial translations
  }

  /**
   * Translate content with fallback mechanisms
   * @param {string} content - Content to translate
   * @param {string} targetLang - Target language ('en' or 'ur')
   * @param {string} sourceLang - Source language ('en' or 'ur')
   * @returns {string} - Translated content with fallbacks applied
   */
  translateWithFallback(content, targetLang, sourceLang = 'en') {
    if (!content || typeof content !== 'string') {
      return content;
    }

    // Check cache first
    const cacheKey = `${content}_${targetLang}_${sourceLang}`;
    if (this.translationCache.has(cacheKey)) {
      return this.translationCache.get(cacheKey);
    }

    let translatedContent = content;

    // For Urdu translation, apply more comprehensive replacement
    if (targetLang === 'ur') {
      translatedContent = this.translateToUrdu(content);
    } else {
      // For English, we might be switching back from Urdu
      translatedContent = this.translateToEnglish(content);
    }

    // Cache the result
    this.translationCache.set(cacheKey, translatedContent);

    return translatedContent;
  }

  /**
   * Translate content to Urdu with comprehensive mapping
   * @param {string} content - Content to translate to Urdu
   * @returns {string} - Urdu translated content
   */
  translateToUrdu(content) {
    let result = content;

    // Apply exact matches first
    for (const [englishText, mapping] of Object.entries(this.mappings)) {
      if (englishText && mapping.ur) {
        // Use word boundaries to avoid partial matches in the middle of words
        const regex = new RegExp(`\\b${this.escapeRegExp(englishText)}\\b`, 'gi');
        result = result.replace(regex, mapping.ur);
      }
    }

    // Apply phrase-level matches
    for (const [englishText, mapping] of Object.entries(this.mappings)) {
      if (englishText && mapping.ur && englishText.length > 10) { // Focus on longer phrases
        const regex = new RegExp(this.escapeRegExp(englishText), 'gi');
        result = result.replace(regex, mapping.ur);
      }
    }

    return result;
  }

  /**
   * Translate content to English (reverse mapping)
   * @param {string} content - Content to translate to English
   * @returns {string} - English translated content
   */
  translateToEnglish(content) {
    let result = content;

    // Apply reverse mapping (Urdu to English)
    for (const [englishText, mapping] of Object.entries(this.mappings)) {
      if (mapping.ur && mapping.en) {
        const regex = new RegExp(this.escapeRegExp(mapping.ur), 'gi');
        result = result.replace(regex, mapping.en);
      }
    }

    return result;
  }

  /**
   * Add a new translation mapping
   * @param {string} englishText - English text
   * @param {string} urduText - Urdu translation
   */
  addMapping(englishText, urduText) {
    if (englishText && urduText) {
      this.mappings[englishText] = {
        en: englishText,
        ur: urduText
      };

      // Clear cache to avoid stale translations
      this.translationCache.clear();
    }
  }

  /**
   * Get a specific translation
   * @param {string} text - Text to translate
   * @param {string} targetLang - Target language
   * @returns {string|null} - Translated text or null if not found
   */
  getTranslation(text, targetLang) {
    if (!text) return null;

    const normalizedText = this.normalizeText(text);

    for (const [englishText, mapping] of Object.entries(this.mappings)) {
      const normalizedEnglish = this.normalizeText(englishText);

      if (normalizedEnglish === normalizedText) {
        return targetLang === 'ur' ? mapping.ur : mapping.en;
      }

      // Check for partial matches as fallback
      if (normalizedText.includes(normalizedEnglish) ||
          normalizedEnglish.includes(normalizedText)) {
        const similarity = this.calculateSimilarity(normalizedText, normalizedEnglish);
        if (similarity > this.fallbackThreshold) {
          return targetLang === 'ur' ? mapping.ur : mapping.en;
        }
      }
    }

    return null;
  }

  /**
   * Calculate similarity between two strings (0-1)
   * @param {string} str1 - First string
   * @param {string} str2 - Second string
   * @returns {number} - Similarity ratio
   */
  calculateSimilarity(str1, str2) {
    const longer = str1.length > str2.length ? str1 : str2;
    const shorter = str1.length > str2.length ? str2 : str1;

    if (longer.length === 0) {
      return 1.0;
    }

    const editDistance = this.levenshteinDistance(longer, shorter);
    return (longer.length - editDistance) / longer.length;
  }

  /**
   * Calculate Levenshtein distance between two strings
   * @param {string} str1 - First string
   * @param {string} str2 - Second string
   * @returns {number} - Edit distance
   */
  levenshteinDistance(str1, str2) {
    const matrix = Array(str2.length + 1).fill().map(() => Array(str1.length + 1).fill(0));

    for (let i = 0; i <= str1.length; i++) {
      matrix[0][i] = i;
    }

    for (let j = 0; j <= str2.length; j++) {
      matrix[j][0] = j;
    }

    for (let j = 1; j <= str2.length; j++) {
      for (let i = 1; i <= str1.length; i++) {
        const indicator = str1[i - 1] === str2[j - 1] ? 0 : 1;
        matrix[j][i] = Math.min(
          matrix[j][i - 1] + 1, // insertion
          matrix[j - 1][i] + 1, // deletion
          matrix[j - 1][i - 1] + indicator // substitution
        );
      }
    }

    return matrix[str2.length][str1.length];
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
   * Clear the translation cache
   */
  clearCache() {
    this.translationCache.clear();
  }

  /**
   * Get statistics about the translator
   * @returns {Object} - Statistics object
   */
  getStats() {
    return {
      mappingCount: Object.keys(this.mappings).length,
      cacheSize: this.translationCache.size,
      fallbackThreshold: this.fallbackThreshold
    };
  }
}

const advancedTranslator = new AdvancedTranslator();
export default advancedTranslator;