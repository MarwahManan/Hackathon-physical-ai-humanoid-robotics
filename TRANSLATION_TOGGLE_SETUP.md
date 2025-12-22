# Urdu Translation Toggle Feature Documentation

## Overview

The Urdu Translation Toggle feature enables readers of the Physical AI & Humanoid Robotics book to switch between English and Urdu content on any chapter page. The feature provides a "Translate to Urdu / اردو میں پڑھیں" button that appears at the top of every chapter, allowing instant switching between languages with proper RTL (right-to-left) formatting.

## Features

- **Language Toggle**: Switch between English and Urdu content instantly
- **RTL Support**: Proper right-to-left text formatting for Urdu
- **Content Preservation**: All functionality and navigation preserved after translation
- **Responsive Design**: Works on mobile and desktop devices
- **Offline Compatible**: Pre-generated translations work without internet
- **GitHub Pages Compatible**: Optimized for deployment on GitHub Pages

## Setup Instructions

### 1. Installation

The feature is already integrated into the Docusaurus site. No additional installation is required.

### 2. Adding New Translations

To add new English ↔ Urdu translation pairs:

1. Open `src/utils/translations/mappings.js`
2. Add new mappings in the format:

```javascript
'English text': {
  en: 'English text',
  ur: 'اردو ترجمہ'
},
```

### 3. Customization Options

#### Modify Button Text
Edit the button text in `src/theme/TranslationToggle/index.js`:

```javascript
const buttonText = currentLanguage === 'en'
  ? 'Translate to Urdu / اردو میں پڑھیں'  // English button text
  : 'English / انگریزی میں واپس جائیں';   // Urdu button text
```

#### Customize Styling
Modify styles in `src/theme/TranslationToggle/TranslationToggle.module.css`

## Usage Guide

### For Readers
1. Navigate to any chapter page in the book
2. Locate the "Translate to Urdu / اردو میں پڑھیں" button at the top of the page
3. Click the button to switch to Urdu with RTL formatting
4. Click again to switch back to English
5. Continue reading with all navigation functionality preserved

### For Content Authors
1. Add new content as normal in English
2. Add corresponding Urdu translations to the mappings file
3. The system will automatically provide toggle functionality

## Technical Implementation

### Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    Docusaurus Book Site                     │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────┐  ┌──────────────────────────────────┐   │
│ │   Header        │  │     Chapter Content              │   │
│ │                 │  │                                  │   │
│ │ [Translate Btn] │  │ [English ↔ Urdu Content]       │   │
│ │ Translate to Urdu│  │ [RTL CSS Applied When Urdu]    │   │
│ │ / اردو میں پڑھیں │  │                                  │   │
│ └─────────────────┘  └──────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

1. **TranslationToggle Component** (`src/theme/TranslationToggle/index.js`)
   - Provides the UI button and state management
   - Uses React Context for state sharing

2. **Translation System** (`src/utils/translations/`)
   - `translator.js`: Main interface
   - `advanced-translator.js`: Comprehensive translation logic
   - `mappings.js`: English ↔ Urdu content mappings

3. **Content Translator** (`src/utils/translations/content-translator.js`)
   - Handles DOM content translation
   - Manages real-time content switching

4. **Global Wrapper** (`src/theme/Root.js`)
   - Provides translation context to the entire app

### Styling & RTL Support

- **RTL Direction**: Applied to the entire document when Urdu is selected
- **Typography**: Optimized for Urdu readability with Noto Nastaliq Urdu font stack
- **Layout**: All elements adapt to right-to-left direction
- **Code Blocks**: Maintain LTR direction for proper display
- **Responsive**: Works on all screen sizes

## Maintenance Instructions

### Adding New Content Mappings
1. Edit `src/utils/translations/mappings.js`
2. Add new English ↔ Urdu pairs
3. Test the new translations

### Performance Optimization
- The system uses caching to improve performance
- Translation mappings are loaded once and reused
- DOM updates are optimized for smooth transitions

### Troubleshooting

#### Translation not appearing
- Check that the text exists in `mappings.js`
- Verify proper formatting of mapping entries
- Check browser console for errors

#### RTL formatting issues
- Ensure CSS classes are properly applied
- Verify `dir="rtl"` attribute is set on content elements
- Check that font stack supports Urdu characters

#### Button not appearing
- Verify that `Root.js` wrapper is active
- Check Docusaurus build process completed successfully

## Limitations

1. **Content Coverage**: Only content in the mappings file gets translated
2. **Dynamic Content**: Real-time translation of new content not supported
3. **Font Dependencies**: Relies on Urdu-compatible fonts being available
4. **Code Syntax**: Code blocks remain in LTR direction (as they should)

## Future Improvements

1. **Automatic Translation**: Integration with translation APIs for dynamic content
2. **Font Optimization**: Bundle Urdu fonts for better consistency
3. **Voice Support**: Add text-to-speech for both languages
4. **Custom Dictionary**: User-customizable translation preferences

## Testing & Validation

The feature includes a comprehensive test suite:
- Basic translation functionality
- Content translation
- RTL application
- Fallback mechanisms
- Performance testing

To run tests, see `src/utils/translations/test-translations.js`

## Deployment

The feature is optimized for GitHub Pages deployment:
- Minimal bundle size impact
- No external dependencies
- Works offline with pre-generated translations
- Compatible with static site generation

## Support & Contributing

For issues or contributions:
1. Check existing issues for similar problems
2. Create a new issue with detailed problem description
3. Follow the established code patterns for contributions
4. Ensure translations are accurate and culturally appropriate

---

This documentation provides comprehensive guidance for setting up, using, and maintaining the Urdu Translation Toggle feature. The system is designed to be user-friendly while providing robust translation functionality.