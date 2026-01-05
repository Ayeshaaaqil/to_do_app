// frontend/src/components/todos/TodoItem.tsx

import React, { useState, useEffect } from 'react';
import { Todo } from '../../types';
import { CheckCircle, Circle, SquarePen, Trash2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import Confetti from 'react-confetti';
import VimMode from '../Editor/VimMode';

interface TodoItemProps {
  todo: Todo;
  onUpdate: (id: string, updates: { title?: string; description?: string }) => void;
  onToggleComplete: (id: string, isCompleted: boolean) => void;
  onDelete: (id: string) => void;
}

const TodoItem: React.FC<TodoItemProps> = ({ todo, onUpdate, onToggleComplete, onDelete }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(todo.title);
  const [description, setDescription] = useState(todo.description || '');
  const [showConfetti, setShowConfetti] = useState(false);
  const [windowSize, setWindowSize] = useState({
    width: 0,
    height: 0,
  });

  useEffect(() => {
    // Set window size for confetti
    setWindowSize({
      width: window.innerWidth,
      height: window.innerHeight,
    });

    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const handleSave = () => {
    onUpdate(todo.id, { title, description: description || undefined });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setTitle(todo.title);
    setDescription(todo.description || '');
    setIsEditing(false);
  };

  const handleToggleComplete = () => {
    const newStatus = !todo.is_completed;
    if (newStatus) {
      // Show confetti when marking as complete
      setShowConfetti(true);
      setTimeout(() => setShowConfetti(false), 3000);
    }
    onToggleComplete(todo.id, newStatus);
  };

  const handleDelete = () => {
    onDelete(todo.id);
  };

  return (
    <motion.li
      layout
      initial={{ opacity: 0, y: -20 }}
      animate={{
        opacity: 1,
        y: 0,
        transition: {
          type: "spring",
          stiffness: 300,
          damping: 25
        }
      }}
      exit={{
        opacity: 0,
        x: -20,
        scale: 0.9,
        transition: { duration: 0.2 }
      }}
      whileHover={{
        y: -3,
        boxShadow: "0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
        transition: { duration: 0.2 }
      }}
      className={`task-card ${todo.is_completed ? 'completed' : ''}`}
    >
      {showConfetti && (
        <Confetti
          width={windowSize.width}
          height={windowSize.height}
          recycle={false}
          numberOfPieces={200}
          gravity={0.1}
        />
      )}

      {isEditing ? (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="task-form"
        >
          <div className="form-group">
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="form-control"
              placeholder="Task title"
            />
          </div>
          <div className="form-group">
            <VimMode
              value={description}
              onChange={setDescription}
              placeholder="Task description (optional)"
              rows={2}
            />
          </div>
          <div className="task-actions-container">
            <button
              onClick={handleSave}
              className="btn btn-success"
            >
              Save
            </button>
            <button
              onClick={handleCancel}
              className="btn btn-outline"
            >
              Cancel
            </button>
          </div>
        </motion.div>
      ) : (
        <div>
          <div className="task-header">
            <div className="task-checkbox">
              <i
                type="checkbox"
                id={`todo-${todo.id}`}
                checked={todo.is_completed}
                onChange={() => handleToggleComplete(todo.id, !todo.is_completed)}
              />
              <span className="checkmark"></span>
            </div>
            <div className="task-content">
              <h3 className={`task-title ${todo.is_completed ? 'line-through' : ''}`}>
                {todo.title}
              </h3>
              {todo.description && (
                <p className={`task-description ${todo.is_completed ? 'line-through' : ''}`}>
                  {todo.description}
                </p>
              )}
              <div className="task-meta">
                <div className="meta-item">
                  <span className="meta-label">Created</span>
                  <span className="meta-value">{new Date(todo.created_at).toLocaleString()}</span>
                </div>
              </div>
            </div>
            <AnimatePresence>
              <motion.div
                className="task-actions"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
              >
                <button
                  onClick={() => setIsEditing(true)}
                  className="task-action-btn"
                  title="Edit"
                >
                  <SquarePen size={18} />
                </button>
                <button
                  onClick={handleDelete}
                  className="task-action-btn"
                  title="Delete"
                >
                  <Trash2 size={18} />
                </button>
              </motion.div>
            </AnimatePresence>
          </div>
        </div>
      )}
    </motion.li>
  );
};

export default TodoItem;