import React from 'react';
import './Chatbot.css';

const ChatMessage = ({ message, sender }) => {
  const isUser = sender === 'user';
  const messageRole = isUser ? 'user' : 'agent';

  return (
    <div
      className={`chatbot-message ${isUser ? 'chatbot-message-user' : 'chatbot-message-bot'}`}
      role="logitem"
      aria-label={`${messageRole} message`}
      tabIndex="0"
    >
      {message}
    </div>
  );
};

export default ChatMessage;