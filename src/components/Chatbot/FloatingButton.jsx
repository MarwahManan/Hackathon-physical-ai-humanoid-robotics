import React from 'react';
import './Chatbot.css';

const FloatingButton = ({ onToggleChat, isOpen }) => {
  // Hide the button when chat is open
  if (isOpen) {
    return null;
  }

  return (
    <div className="chatbot-container" role="complementary" aria-label="Chatbot interface">
      <button
        className="chatbot-float-button"
        onClick={onToggleChat}
        aria-label="Open chatbot assistant"
        title="Open AI Robotics Assistant"
        role="button"
        tabIndex="0"
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <path d="M12 2C6.48 2 2 6.48 2 12C2 13.54 2.36 15.01 3.02 16.35L2 22L7.65 20.98C8.99 21.64 10.46 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2Z" fill="currentColor"/>
          <path d="M9.5 13.5L14.5 10.5" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </button>
    </div>
  );
};

export default FloatingButton;