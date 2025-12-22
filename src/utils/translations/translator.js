import advancedTranslator from './advanced-translator';

/**
 * Main translator interface that uses the advanced translation system
 */
class Translator {
  /**
   * Translate a single text string from English to Urdu or vice versa
   * @param {string} text - The text to translate
   * @param {string} targetLang - Target language ('en' or 'ur')
   * @param {string} sourceLang - Source language ('en' or 'ur'), defaults to 'en'
   * @returns {string} - Translated text
   */
  translateText(text, targetLang, sourceLang = 'en') {
    return advancedTranslator.translateWithFallback(text, targetLang, sourceLang);
  }

  /**
   * Translate a block of HTML content
   * @param {string} htmlContent - HTML content to translate
   * @param {string} targetLang - Target language ('en' or 'ur')
   * @returns {string} - Translated HTML content
   */
  translateHTMLContent(htmlContent, targetLang) {
    return advancedTranslator.translateWithFallback(htmlContent, targetLang);
  }

  /**
   * Add a new translation mapping
   * @param {string} englishText - English text
   * @param {string} urduText - Urdu translation
   */
  addMapping(englishText, urduText) {
    advancedTranslator.addMapping(englishText, urduText);
  }

  /**
   * Get a specific translation
   * @param {string} text - Text to translate
   * @param {string} targetLang - Target language
   * @returns {string|null} - Translated text or null if not found
   */
  getTranslation(text, targetLang) {
    return advancedTranslator.getTranslation(text, targetLang);
  }

  /**
   * Get statistics about the translator
   * @returns {Object} - Statistics object
   */
  getStats() {
    return advancedTranslator.getStats();
  }

  /**
   * Clear the translation cache
   */
  clearCache() {
    advancedTranslator.clearCache();
  }

  /**
   * Get all available mappings
   * @returns {Object} - Translation mappings
   */
  getAllMappings() {
    return advancedTranslator.mappings;
  }
}

// Create a singleton instance
const translator = new Translator();
export default translator;