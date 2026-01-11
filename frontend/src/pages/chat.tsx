// frontend/src/pages/chat.tsx

import React from 'react';
import ChatInterface from '../components/Chat/ChatInterface';
import Layout from '../components/layout/Layout';

const ChatPage: React.FC = () => {
  return (
    <Layout>
      <div className="container mx-auto py-8 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800 dark:text-white mb-2">AI Todo Assistant</h1>
            <p className="text-gray-600 dark:text-gray-300">
              Manage your todos using natural language
            </p>
          </div>
          
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <div className="h-[500px] flex flex-col">
              <ChatInterface />
            </div>
          </div>
          
          <div className="mt-8 bg-gray-50 dark:bg-gray-700 rounded-lg p-6">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">How to use the AI Assistant</h2>
            <ul className="list-disc pl-5 space-y-2 text-gray-600 dark:text-gray-300">
              <li>Ask to create a new todo: "Add 'buy groceries' to my todos"</li>
              <li>Ask to view your todos: "Show me my todos"</li>
              <li>Ask to update a todo: "Update 'buy groceries' to 'buy groceries and milk'"</li>
              <li>Ask to mark a todo as complete: "Mark 'buy groceries' as complete"</li>
              <li>Ask to delete a todo: "Delete 'buy groceries'"</li>
            </ul>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default ChatPage;