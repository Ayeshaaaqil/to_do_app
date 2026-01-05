// frontend/src/pages/todos/index.tsx

import React from 'react';
import { motion } from 'framer-motion';
import TodoList from '../../components/todos/TodoList';
import Layout from '../../components/layout/Layout';

const TodosPage: React.FC = () => {
  return (
    <Layout>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
        className="container mx-auto py-8"
      >
        {/* Hero Section with Illustration */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-2xl p-8 mb-8 text-white shadow-xl"
        >
          <div className="flex flex-col md:flex-row items-center">
            <div className="md:w-1/2 mb-6 md:mb-0">
              <motion.h1
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
                className="text-3xl md:text-4xl font-bold font-poppins mb-4"
              >
                Your Productivity Hub
              </motion.h1>
              <motion.p
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.3 }}
                className="text-lg mb-6"
              >
                Organize your tasks, boost your productivity, and achieve your goals.
              </motion.p>
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: 0.4 }}
                className="bg-white/20 backdrop-blur-sm rounded-lg p-4 max-w-md"
              >
                <div className="flex justify-between mb-2">
                  <span className="font-medium">Today's Progress</span>
                  <span className="font-bold">65%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2.5">
                  <motion.div
                    className="bg-green-400 h-2.5 rounded-full"
                    style={{ width: '65%' }}
                    initial={{ width: 0 }}
                    animate={{ width: '65%' }}
                    transition={{ duration: 1, delay: 0.5 }}
                  ></motion.div>
                </div>
              </motion.div>
            </div>
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: 0.5 }}
              className="md:w-1/2 flex justify-center"
            >
              <img
                src="https://www.shutterstock.com/image-vector/schedule-app-task-manager-ui-260nw-2155233345.jpg"
                alt="Productivity illustration"
                className="rounded-lg shadow-lg max-h-64 object-contain"
              />
            </motion.div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.6 }}
          className="task-list"
        >
          <TodoList />
        </motion.div>
      </motion.div>
    </Layout>
  );
};

export default TodosPage;