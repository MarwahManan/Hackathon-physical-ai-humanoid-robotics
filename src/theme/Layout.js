import React, { useState, lazy, Suspense } from 'react';
import Layout from '@theme-original/Layout';
import FloatingButton from '../components/Chatbot/FloatingButton';
import ErrorBoundary from '../components/Chatbot/ErrorBoundary';

// Lazy load the ChatWindow component since it's not always visible
const ChatWindow = lazy(() => import('../components/Chatbot/ChatWindow'));

export default function LayoutWrapper(props) {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  const closeChat = () => {
    setIsChatOpen(false);
  };

  return (
    <>
      <Layout {...props}>
        {props.children}
      </Layout>
      <FloatingButton isOpen={isChatOpen} onToggleChat={toggleChat} />
      {isChatOpen && (
        <ErrorBoundary>
          <Suspense fallback={null}>
            <ChatWindow isOpen={isChatOpen} onClose={closeChat} />
          </Suspense>
        </ErrorBoundary>
      )}
    </>
  );
}