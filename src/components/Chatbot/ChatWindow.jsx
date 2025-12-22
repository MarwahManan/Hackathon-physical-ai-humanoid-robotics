import React, { useState, useEffect, useRef } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import './Chatbot.css';

const ChatWindow = ({ isOpen, onClose }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm your AI assistant for the Physical AI Humanoid Robotics book. How can I help you today?",
      sender: 'bot'
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const [conversationId, setConversationId] = useState(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (text) => {
    // Add user message immediately
    const userMessage = {
      id: Date.now(),
      text: text,
      sender: 'user'
    };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Make API call to backend
      const response = await fetch('https://marwah-manan-book-chatbot.hf.space/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: text,
          conversation_id: conversationId
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Update conversation ID if new one was created
      if (data.conversation_id && !conversationId) {
        setConversationId(data.conversation_id);
      }

      // Add bot response
      const botMessage = {
        id: Date.now() + 1,
        text: data.answer,
        sender: 'bot'
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: "Sorry, I encountered an error. Please try again.",
        sender: 'bot'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Add keyboard navigation support
  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      onClose();
    }
  };

  return (
    <div
      className={`chatbot-window ${isOpen ? 'open' : ''}`}
      role="dialog"
      aria-modal="true"
      aria-label="AI Robotics Assistant Chat"
      onKeyDown={handleKeyDown}
      tabIndex="-1"
    >
      <div className="chatbot-header" role="banner">
        <h4 className="chatbot-header-title" tabIndex="0">AI Robotics Assistant</h4>
        <button
          className="chatbot-close-button"
          onClick={onClose}
          aria-label="Close chat"
          title="Close chat (Escape key)"
          tabIndex="0"
        >
          ×
        </button>
      </div>

      <div
        className="chatbot-messages"
        role="log"
        aria-live="polite"
        aria-label="Chat messages"
        tabIndex="0"
      >
        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            message={message.text}
            sender={message.sender}
          />
        ))}
        {isLoading && (
          <div
            className="chatbot-message chatbot-message-bot"
            role="status"
            aria-label="Loading response"
          >
            <div className="chatbot-loading">
              <div className="loading-spinner" aria-hidden="true"></div>
              <span className="sr-only">Loading response...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} aria-hidden="true" />
      </div>

      <ChatInput
        onSendMessage={handleSendMessage}
        disabled={isLoading}
      />
    </div>
  );
};

export default ChatWindow;