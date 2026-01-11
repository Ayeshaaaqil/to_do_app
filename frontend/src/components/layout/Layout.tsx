// frontend/src/components/layout/Layout.tsx

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { motion, AnimatePresence } from 'framer-motion';
import { Moon, Sun, Menu, X, MessageCircle } from 'lucide-react';
import { isAuthenticated, clearAuth } from '../../services/auth';
import FloatingChatWidget from '../Chat/FloatingChatWidget';

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const router = useRouter();
  const [darkMode, setDarkMode] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    // Check system preference or saved preference
    const isDark = localStorage.getItem('darkMode') === 'true' ||
                  (window.matchMedia('(prefers-color-scheme: dark)').matches &&
                   localStorage.getItem('darkMode') !== 'false');
    setDarkMode(isDark);
  }, []);

  useEffect(() => {
    // Apply dark mode class to document
    if (darkMode) {
      document.documentElement.classList.add('dark');
      document.documentElement.setAttribute('data-theme', 'dark');
      localStorage.setItem('darkMode', 'true');
    } else {
      document.documentElement.classList.remove('dark');
      document.documentElement.setAttribute('data-theme', 'light');
      localStorage.setItem('darkMode', 'false');
    }
  }, [darkMode]);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  const handleSignOut = () => {
    clearAuth();
    router.push('/signin');
  };

  const isAuthPage = router.pathname === '/signin' || router.pathname === '/signup';

  // Check authentication status
  const [authChecked, setAuthChecked] = useState(false);
  const [isAuth, setIsAuth] = useState(false);

  useEffect(() => {
    setIsAuth(isAuthenticated());
    setAuthChecked(true);
  }, []);

  return (
    <div className="app-container">
      {!isAuthPage && (
        <motion.nav
          initial={{ y: -100 }}
          animate={{ y: 0 }}
          transition={{ duration: 0.5 }}
          className="bg-indigo-600 text-white shadow-lg"
        >
          <div className="container mx-auto px-4 py-3">
            <div className="flex justify-between items-center">
              <Link href="/" className="text-xl font-bold font-poppins">
                <span className="text-yellow-300">✓</span> TodoPro
              </Link>

              {/* Desktop Navigation */}
              <div className="hidden md:flex items-center space-x-6">
                {authChecked && isAuth ? (
                  <>
                    <motion.div whileHover={{ y: -2 }}>
                      <Link href="/todos" className="hover:underline font-medium transition-all duration-300 hover:text-indigo-200">
                        My Tasks
                      </Link>
                    </motion.div>
                    <motion.div whileHover={{ y: -2 }}>
                      <Link href="/chat" className="hover:underline font-medium transition-all duration-300 hover:text-indigo-200">
                        AI Assistant
                      </Link>
                    </motion.div>
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={handleSignOut}
                      className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded-md transition-colors font-medium"
                    >
                      Sign Out
                    </motion.button>
                  </>
                ) : authChecked ? (
                  <>
                    <motion.div whileHover={{ y: -2 }}>
                      <Link href="/signin" className="hover:underline font-medium transition-all duration-300 hover:text-indigo-200">
                        Sign In
                      </Link>
                    </motion.div>
                    <motion.div whileHover={{ y: -2 }}>
                      <Link href="/signup" className="bg-white text-indigo-600 hover:bg-gray-100 px-4 py-2 rounded-md transition-colors font-medium">
                        Sign Up
                      </Link>
                    </motion.div>
                  </>
                ) : (
                  // Show loading state while checking auth
                  <div className="text-gray-300">Loading...</div>
                )}
                {authChecked && isAuth && (
                  <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
                    <Link href="/chat" className="p-2 rounded-full hover:bg-indigo-700 transition-colors theme-toggle" aria-label="Open AI Assistant">
                      <MessageCircle size={20} />
                    </Link>
                  </motion.div>
                )}
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={toggleDarkMode}
                  className="p-2 rounded-full hover:bg-indigo-700 transition-colors theme-toggle"
                  aria-label={darkMode ? "Switch to light mode" : "Switch to dark mode"}
                >
                  {darkMode ? <Sun size={20} /> : <Moon size={20} />}
                </motion.button>
              </div>

              {/* Mobile menu button */}
              <div className="md:hidden flex items-center space-x-3">
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={toggleDarkMode}
                  className="p-2 rounded-full hover:bg-indigo-700 transition-colors theme-toggle"
                  aria-label={darkMode ? "Switch to light mode" : "Switch to dark mode"}
                >
                  {darkMode ? <Sun size={20} /> : <Moon size={20} />}
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                  className="p-2 rounded-md hover:bg-indigo-700 transition-colors"
                  aria-label="Toggle menu"
                >
                  {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
                </motion.button>
              </div>
            </div>

            {/* Mobile Navigation */}
            <AnimatePresence>
              {mobileMenuOpen && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.3 }}
                  className="md:hidden mt-4 pb-4"
                >
                  <div className="flex flex-col space-y-3">
                    {authChecked && isAuth ? (
                      <>
                        <Link
                          href="/todos"
                          className="hover:underline font-medium py-2 px-4 rounded hover:bg-indigo-700 transition-colors"
                          onClick={() => setMobileMenuOpen(false)}
                        >
                          My Tasks
                        </Link>
                        <Link
                          href="/chat"
                          className="hover:underline font-medium py-2 px-4 rounded hover:bg-indigo-700 transition-colors flex items-center"
                          onClick={() => setMobileMenuOpen(false)}
                        >
                          <MessageCircle size={16} className="mr-2" /> AI Assistant
                        </Link>
                        <button
                          onClick={() => {
                            handleSignOut();
                            setMobileMenuOpen(false);
                          }}
                          className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded-md transition-colors font-medium text-left"
                        >
                          Sign Out
                        </button>
                      </>
                    ) : authChecked ? (
                      <>
                        <Link
                          href="/signin"
                          className="hover:underline font-medium py-2 px-4 rounded hover:bg-indigo-700 transition-colors"
                          onClick={() => setMobileMenuOpen(false)}
                        >
                          Sign In
                        </Link>
                        <Link
                          href="/signup"
                          className="bg-white text-indigo-600 hover:bg-gray-100 px-4 py-2 rounded-md transition-colors font-medium"
                          onClick={() => setMobileMenuOpen(false)}
                        >
                          Sign Up
                        </Link>
                      </>
                    ) : (
                      // Show loading state while checking auth
                      <div className="py-2 px-4 text-gray-300">Loading...</div>
                    )}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </motion.nav>
      )}

      <motion.main
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
        className="main-content"
      >
        {children}
        {/* Show floating chat widget only when authenticated */}
        {authChecked && isAuth && !isAuthPage && <FloatingChatWidget />}
      </motion.main>

      <motion.footer
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="bg-gray-800 text-white py-8 mt-12 dark:bg-gray-900"
      >
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-4 md:mb-0">
              <h3 className="text-lg font-semibold font-poppins">TodoPro</h3>
              <p className="text-gray-400 mt-1">Your productivity companion</p>
            </div>
            <div className="text-center md:text-right">
              <p className="text-gray-400">© {new Date().getFullYear()} TodoPro. All rights reserved.</p>
              <p className="text-gray-500 text-sm mt-1">Designed with Ayesha Aaqil❤️ </p>
            </div>
          </div>
        </div>
      </motion.footer>
    </div>
  );
};

export default Layout;