// frontend/src/components/Chat/FloatingChatWidget.tsx

import React, { useState } from 'react';
import { MessageCircle, X } from 'lucide-react';
import ChatInterface from './ChatInterface';

const FloatingChatWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {isOpen ? (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-2xl w-80 h-96 flex flex-col border-2 border-indigo-500/30">
          <div className="flex justify-between items-center bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-3 rounded-t-xl">
            <span className="font-semibold flex items-center">
              <MessageCircle size={18} className="mr-2" />
              AI Assistant
            </span>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white hover:text-gray-200 focus:outline-none rounded-full p-1 hover:bg-black/10 transition-colors"
              aria-label="Close chat"
            >
              <X size={20} />
            </button>
          </div>
          <div className="flex-1 overflow-hidden">
            <ChatInterface />
          </div>
        </div>
      ) : (
        <button
          onClick={() => setIsOpen(true)}
          className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-4 rounded-full shadow-xl hover:shadow-2xl focus:outline-none focus:ring-4 focus:ring-indigo-500/50 transition-all transform hover:scale-110 animate-pulse"
          aria-label="Open chat"
          title="Open AI Assistant"
        >
          <MessageCircle size={24} />
        </button>
      )}
    </div>
  );
};

export default FloatingChatWidget;