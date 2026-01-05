// frontend/src/components/todos/AddTodoForm.tsx

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import VimMode from '../Editor/VimMode';

interface AddTodoFormProps {
  onAddTodo: (title: string, description?: string) => void;
  onCancel?: () => void;
}

const AddTodoForm: React.FC<AddTodoFormProps> = ({ onAddTodo, onCancel }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    onAddTodo(title.trim(), description.trim() || undefined);

    // Reset form
    setTitle('');
    setDescription('');
    setError(null);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: 20, scale: 0.95 }}
      className="task-form"
    >
      <motion.h2
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="task-list-title"
      >
        Add New Task
      </motion.h2>

      {error && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="mb-3 p-2 bg-red-100 text-red-700 rounded dark:bg-red-900/30 dark:text-red-300"
        >
          {error}
        </motion.div>
      )}

      <motion.form
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
        onSubmit={handleSubmit}
      >
        <div className="form-group">
          <motion.input
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="form-control"
            placeholder="What needs to be done?"
            whileFocus={{ scale: 1.02 }}
          />
        </div>

        <div className="form-group">
          <motion.div
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
          >
            <VimMode
              value={description}
              onChange={setDescription}
              placeholder="Description (optional)"
              rows={2}
            />
          </motion.div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="task-actions-container"
        >
          <motion.button
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.98 }}
            type="submit"
            className="btn btn-primary"
          >
            Add Task
          </motion.button>
          {onCancel && (
            <motion.button
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.98 }}
              type="button"
              onClick={onCancel}
              className="btn btn-outline"
            >
              Cancel
            </motion.button>
          )}
        </motion.div>
      </motion.form>
    </motion.div>
  );
};

export default AddTodoForm;