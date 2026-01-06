// frontend/src/components/todos/TodoList.tsx

import React, { useState, useEffect, useRef } from 'react';
import { todoAPI } from '../../services/api';
import { isAuthenticated } from '../../services/auth';
import TodoItem from './TodoItem';
import AddTodoForm from './AddTodoForm';
import { Todo } from '../../types';
import { Plus } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const TodoList: React.FC = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [completedCount, setCompletedCount] = useState(0);
  const formRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isAuthenticated()) {
      fetchTodos();
    } else {
      // If not authenticated, redirect to sign in
      if (typeof window !== 'undefined') {
        window.location.href = '/signin';
      }
    }
  }, []);

  useEffect(() => {
    // Calculate completed tasks
    const completed = Array.isArray(todos) ? todos.filter(todo => todo.is_completed).length : 0;
    setCompletedCount(completed);
  }, [todos]);

  const fetchTodos = async () => {
    // Check if user is still authenticated before making request
    if (!isAuthenticated()) {
      setError('User not authenticated');
      if (typeof window !== 'undefined') {
        window.location.href = '/signin';
      }
      return;
    }

    try {
      setLoading(true);
      const data = await todoAPI.getTodos();
      setTodos(data);
      setError(null);
    } catch (err: any) {
      // If authentication error, redirect to sign in
      if (err.message &&
          (err.message.includes('401') ||
           err.message.includes('403') ||
           err.message.toLowerCase().includes('auth') ||
           err.message.toLowerCase().includes('unauthorized') ||
           err.message.toLowerCase().includes('forbidden'))) {
        setError(err.message);
        // Redirect to sign in page after a short delay
        setTimeout(() => {
          if (typeof window !== 'undefined') {
            window.location.href = '/signin';
          }
        }, 1000);
      } else {
        setError(err.message || 'Failed to fetch todos');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleAddTodo = async (title: string, description?: string) => {
    if (!isAuthenticated()) {
      setError('User not authenticated');
      if (typeof window !== 'undefined') {
        window.location.href = '/signin';
      }
      return;
    }

    try {
      const newTodo = await todoAPI.createTodo(title, description);
      setTodos(prevTodos => Array.isArray(prevTodos) ? [...prevTodos, newTodo] : [newTodo]);
      setShowForm(false);
    } catch (err: any) {
      // If authentication error, redirect to sign in
      if (err.message &&
          (err.message.includes('401') ||
           err.message.includes('403') ||
           err.message.toLowerCase().includes('auth') ||
           err.message.toLowerCase().includes('unauthorized') ||
           err.message.toLowerCase().includes('forbidden'))) {
        setError(err.message);
        setTimeout(() => {
          if (typeof window !== 'undefined') {
            window.location.href = '/signin';
          }
        }, 1000);
      } else {
        setError(err.message || 'Failed to add todo');
      }
    }
  };

  const handleUpdateTodo = async (id: string, updates: { title?: string; description?: string }) => {
    if (!isAuthenticated()) {
      setError('User not authenticated');
      if (typeof window !== 'undefined') {
        window.location.href = '/signin';
      }
      return;
    }

    try {
      const updatedTodo = await todoAPI.updateTodo(id, updates);
      setTodos(prevTodos => Array.isArray(prevTodos) ? prevTodos.map(todo => todo.id === id ? updatedTodo : todo) : []);
    } catch (err: any) {
      // If authentication error, redirect to sign in
      if (err.message &&
          (err.message.includes('401') ||
           err.message.includes('403') ||
           err.message.toLowerCase().includes('auth') ||
           err.message.toLowerCase().includes('unauthorized') ||
           err.message.toLowerCase().includes('forbidden'))) {
        setError(err.message);
        setTimeout(() => {
          if (typeof window !== 'undefined') {
            window.location.href = '/signin';
          }
        }, 1000);
      } else {
        setError(err.message || 'Failed to update todo');
      }
    }
  };

  const handleToggleComplete = async (id: string, isCompleted: boolean) => {
    if (!isAuthenticated()) {
      setError('User not authenticated');
      if (typeof window !== 'undefined') {
        window.location.href = '/signin';
      }
      return;
    }

    try {
      const updatedTodo = await todoAPI.toggleTodoComplete(id, isCompleted);
      setTodos(prevTodos => Array.isArray(prevTodos) ? prevTodos.map(todo => todo.id === id ? updatedTodo : todo) : []);
    } catch (err: any) {
      // If authentication error, redirect to sign in
      if (err.message &&
          (err.message.includes('401') ||
           err.message.includes('403') ||
           err.message.toLowerCase().includes('auth') ||
           err.message.toLowerCase().includes('unauthorized') ||
           err.message.toLowerCase().includes('forbidden'))) {
        setError(err.message);
        setTimeout(() => {
          if (typeof window !== 'undefined') {
            window.location.href = '/signin';
          }
        }, 1000);
      } else {
        setError(err.message || 'Failed to update todo status');
      }
    }
  };

  const handleDeleteTodo = async (id: string) => {
    if (!isAuthenticated()) {
      setError('User not authenticated');
      if (typeof window !== 'undefined') {
        window.location.href = '/signin';
      }
      return;
    }

    try {
      await todoAPI.deleteTodo(id);
      setTodos(prevTodos => Array.isArray(prevTodos) ? prevTodos.filter(todo => todo.id !== id) : []);
    } catch (err: any) {
      // If authentication error, redirect to sign in
      if (err.message &&
          (err.message.includes('401') ||
           err.message.includes('403') ||
           err.message.toLowerCase().includes('auth') ||
           err.message.toLowerCase().includes('unauthorized') ||
           err.message.toLowerCase().includes('forbidden'))) {
        setError(err.message);
        setTimeout(() => {
          if (typeof window !== 'undefined') {
            window.location.href = '/signin';
          }
        }, 1000);
      } else {
        setError(err.message || 'Failed to delete todo');
      }
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  if (error) {
    // If the error is authentication-related, redirect to sign in
    if (error.includes('401') || error.includes('403') ||
        error.toLowerCase().includes('auth') ||
        error.toLowerCase().includes('unauthorized') ||
        error.toLowerCase().includes('forbidden')) {
      // Redirect to sign in page
      if (typeof window !== 'undefined') {
        window.location.href = '/signin';
      }
      return null; // Return null while redirecting
    }

    return (
      <div className="mb-4 p-4 bg-red-100 text-red-700 rounded-lg dark:bg-red-900/30 dark:text-red-300">
        Error: {error}
      </div>
    );
  }

  if (todos.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center py-12"
      >
        <div className="mb-8">
          <img
            src="https://cdn.dribbble.com/userupload/4102500/file/original-f6ba6380a9f34b6d073e4bc56ca0c549.png?format=webp&resize=400x300&vertical=center"
            alt="No tasks illustration"
            className="mx-auto max-w-xs rounded-lg shadow-md"
          />
        </div>
        <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-2">No tasks yet</h2>
        <p className="text-gray-600 dark:text-gray-300 mb-6">Add your first task to get started on your productivity journey</p>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setShowForm(!showForm)}
          className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-6 rounded-full shadow-lg transition-all transform"
        >
          Add Your First Task
        </motion.button>
        <AnimatePresence>
          {showForm && (
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              ref={formRef}
              className="mt-6 max-w-lg mx-auto"
            >
              <AddTodoForm onAddTodo={handleAddTodo} onCancel={() => setShowForm(false)} />
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="relative"
    >
      <div className="task-list-header">
        <motion.h2
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="task-list-title"
        >
          Your Tasks
        </motion.h2>
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="text-sm text-gray-600 dark:text-gray-400"
        >
          {completedCount} of {todos.length} completed
        </motion.div>
      </div>

      <div className="relative">
        <AnimatePresence>
          <ul className="task-list">
            {Array.isArray(todos) && todos.map((todo, index) => (
              <motion.div
                key={todo.id}
                initial={{ opacity: 0, y: 20, scale: 0.95 }}
                animate={{
                  opacity: 1,
                  y: 0,
                  scale: 1,
                  transition: {
                    type: "spring",
                    stiffness: 300,
                    damping: 25,
                    delay: index * 0.05 // Stagger animation
                  }
                }}
                exit={{
                  opacity: 0,
                  x: -20,
                  scale: 0.95,
                  transition: { duration: 0.2 }
                }}
                className={`task-card ${todo.is_completed ? 'completed' : ''}`}
              >
                <TodoItem
                  todo={todo}
                  onUpdate={handleUpdateTodo}
                  onToggleComplete={handleToggleComplete}
                  onDelete={handleDeleteTodo}
                />
              </motion.div>
            ))}
          </ul>
        </AnimatePresence>

        {/* Floating Add Button */}
        <motion.button
          whileHover={{ scale: 1.1, y: -2 }}
          whileTap={{ scale: 0.9 }}
          animate={{
            scale: [1, 1.05, 1],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            repeatType: "reverse"
          }}
          onClick={() => setShowForm(!showForm)}
          className="add-task-btn"
          aria-label="Add new task"
        >
          <Plus size={24} />
        </motion.button>

        {/* Add Todo Form (when button is clicked) */}
        <AnimatePresence>
          {showForm && (
            <motion.div
              initial={{ opacity: 0, y: 20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 20, scale: 0.95 }}
              className="mt-6"
            >
              <AddTodoForm onAddTodo={handleAddTodo} onCancel={() => setShowForm(false)} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  );
};

export default TodoList;