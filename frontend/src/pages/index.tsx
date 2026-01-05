// frontend/src/pages/index.tsx

import React from 'react';
import Link from 'next/link';
import Layout from '../components/layout/Layout';

const HomePage: React.FC = () => {
  return (
    <Layout>
      <div className="min-h-screen">
        {/* Hero Section */}
        <div className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white py-20">
          <div className="container mx-auto px-4">
            <div className="flex flex-col md:flex-row items-center">
              <div className="md:w-1/2 mb-10 md:mb-0">
                <h1 className="text-4xl md:text-5xl font-bold font-poppins mb-4 leading-tight">
                  Boost Your Productivity with TodoPro
                </h1>
                <p className="text-xl mb-8 text-indigo-100 max-w-lg">
                  Organize your tasks, track your progress, and achieve your goals with our intuitive task management platform.
                </p>
                <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
                  <Link
                    href="/signup"
                    className="btn btn-primary bg-white text-indigo-600 hover:bg-gray-100 font-bold py-3 px-8 rounded-full shadow-lg transition-all transform hover:scale-105 text-center"
                  >
                    Get Started
                  </Link>
                  <Link
                    href="/signin"
                    className="btn btn-outline border-2 border-white hover:bg-white/10 font-bold py-3 px-8 rounded-full transition-all text-center text-white"
                  >
                    Sign In
                  </Link>
                </div>
              </div>
              <div className="md:w-1/2 flex justify-center">
                <img
                  src="https://media.istockphoto.com/id/1490859869/vector/illustration-features-to-do-list-app-with-task-management-reminders-and-checklists-character.jpg?s=612x612&w=0&k=20&c=oZ4Ce3i-UgztkDuK57num42nQGBK1T0AP--EA0JcDKA="
                  alt="Productivity illustration"
                  className="rounded-xl shadow-2xl max-w-full h-auto"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="py-20 bg-gray-50 dark:bg-gray-900">
          <div className="container mx-auto px-4">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-gray-800 dark:text-white mb-4">Powerful Features</h2>
              <p className="text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
                TodoPro provides everything you need to stay organized and productive
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="bg-white dark:bg-gray-800 p-8 rounded-xl shadow-lg text-center transition-transform hover:scale-105">
                <div className="w-16 h-16 bg-indigo-100 dark:bg-indigo-900/30 rounded-full flex items-center justify-center mx-auto mb-6">
                  <span className="text-2xl">📋</span>
                </div>
                <h3 className="text-xl font-semibold text-gray-800 dark:text-white mb-3">Task Management</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Create, organize, and prioritize your tasks with our intuitive interface
                </p>
              </div>

              <div className="bg-white dark:bg-gray-800 p-8 rounded-xl shadow-lg text-center transition-transform hover:scale-105">
                <div className="w-16 h-16 bg-indigo-100 dark:bg-indigo-900/30 rounded-full flex items-center justify-center mx-auto mb-6">
                  <span className="text-2xl">📊</span>
                </div>
                <h3 className="text-xl font-semibold text-gray-800 dark:text-white mb-3">Progress Tracking</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Visualize your progress with charts and productivity metrics
                </p>
              </div>

              <div className="bg-white dark:bg-gray-800 p-8 rounded-xl shadow-lg text-center transition-transform hover:scale-105">
                <div className="w-16 h-16 bg-indigo-100 dark:bg-indigo-900/30 rounded-full flex items-center justify-center mx-auto mb-6">
                  <span className="text-2xl">🔒</span>
                </div>
                <h3 className="text-xl font-semibold text-gray-800 dark:text-white mb-3">Secure & Private</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Your data is encrypted and securely stored with industry-standard security
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="py-20 bg-gradient-to-r from-indigo-500 to-purple-600">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-3xl font-bold text-white mb-6">Ready to boost your productivity?</h2>
            <p className="text-indigo-100 text-xl mb-8 max-w-2xl mx-auto">
              Join thousands of users who have transformed their workflow with TodoPro
            </p>
            <Link
              href="/signup"
              className="btn btn-primary bg-white text-indigo-600 hover:bg-gray-100 font-bold py-4 px-10 rounded-full shadow-xl transition-all transform hover:scale-105"
            >
              Start Your Free Trial
            </Link>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default HomePage;