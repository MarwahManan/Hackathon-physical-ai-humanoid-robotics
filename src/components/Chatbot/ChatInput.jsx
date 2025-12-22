import React, { useState } from 'react';
import './Chatbot.css';

const ChatInput = ({ onSendMessage, disabled }) => {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim() && !disabled) {
      onSendMessage(inputValue.trim());
      setInputValue('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form className="chatbot-input-area" onSubmit={handleSubmit} role="form" aria-label="Chat input form">
      <input
        type="text"
        className="chatbot-input"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Type your question..."
        disabled={disabled}
        aria-label="Type your message to the AI assistant"
        role="textbox"
        tabIndex="0"
        autoComplete="off"
        aria-autocomplete="none"
        aria-disabled={disabled}
        aria-describedby="chat-input-description"
      />
      <span id="chat-input-description" className="sr-only">Enter your question and press Enter to send</span>
      <button
        type="submit"
        className="chatbot-send-button"
        disabled={disabled || !inputValue.trim()}
        aria-label="Send message"
        title="Send message (Enter key)"
        tabIndex="0"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <path d="M22 2L11 13M22 2L15 22L11 13M11 13L2 9L22 2" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </button>
    </form>
  );
};

export default ChatInput;