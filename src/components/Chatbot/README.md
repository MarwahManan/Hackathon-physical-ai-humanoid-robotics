# AI Robotics Assistant Chatbot

A fully-featured chatbot component for the Physical AI Humanoid Robotics Book website. This component provides an interactive AI assistant that can answer questions about the book content using RAG (Retrieval-Augmented Generation) technology.

## Features

- Floating chat button visible on all pages
- Smooth animations and professional UI
- Real-time conversation with AI assistant
- Multi-turn conversation support with context
- Mobile-responsive design
- Accessibility compliant (keyboard navigation, screen readers)
- Error handling and fallback UIs
- Loading states and visual feedback

## Architecture

The chatbot consists of the following components:

- `FloatingButton.jsx` - The persistent floating button that appears on all pages
- `ChatWindow.jsx` - The main chat interface window with message history
- `ChatMessage.jsx` - Individual message display component
- `ChatInput.jsx` - Input area with text field and send button
- `ErrorBoundary.jsx` - Error handling wrapper
- `Chatbot.css` - Comprehensive styling with animations

## Integration

The chatbot is integrated into the Docusaurus theme via `src/theme/Layout.js`, which wraps the default layout and adds the floating button and chat window globally.

## API Connection

The component connects to the backend RAG API at `http://localhost:8000/ask` (this can be configured). It sends user questions and receives AI-generated responses with source citations.

## Customization

### Styling
- Modify `Chatbot.css` to change colors, fonts, and visual styles
- The design uses a blue color scheme that can be easily updated

### API Endpoint
- Update the API URL in `ChatWindow.jsx` if the backend endpoint changes

### Initial Message
- Modify the initial welcome message in `ChatWindow.jsx`

## Accessibility

The component includes:
- Proper ARIA labels and roles
- Keyboard navigation (Escape to close, Enter to send)
- Screen reader support
- Focus management
- Semantic HTML structure

## Performance

- Lazy loading for the chat window component
- Conditional rendering (only renders when open)
- Efficient state management
- Minimal dependencies

## Error Handling

- Network error handling with user-friendly messages
- Error boundaries to prevent app crashes
- Loading states during API requests
- Graceful degradation when API is unavailable

## Development

To modify the component:

1. The main logic is in `ChatWindow.jsx`
2. Styling is controlled by `Chatbot.css`
3. The global integration is handled in `src/theme/Layout.js`

## Testing

The component has been tested for:
- Cross-browser compatibility
- Mobile responsiveness
- Accessibility compliance
- Error handling scenarios
- Performance optimization