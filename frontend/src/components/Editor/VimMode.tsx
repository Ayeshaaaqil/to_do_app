// frontend/src/components/Editor/VimMode.tsx

import React, { useState, useEffect, useRef, KeyboardEvent } from 'react';

interface VimModeProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  rows?: number;
  className?: string;
}

type VimMode = 'normal' | 'insert' | 'visual';

const VimMode: React.FC<VimModeProps> = ({
  value,
  onChange,
  placeholder,
  rows = 3,
  className = ''
}) => {
  const [mode, setMode] = useState<VimMode>('insert');
  const [cursorPosition, setCursorPosition] = useState(0);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // Handle vim mode switching
    if (e.key === 'Escape') {
      e.preventDefault();
      setMode('normal');
      return;
    }

    // In normal mode, handle vim commands
    if (mode === 'normal') {
      e.preventDefault();

      switch (e.key) {
        case 'i':
          setMode('insert');
          break;
        case 'a':
          setMode('insert');
          // Move cursor forward
          if (cursorPosition < value.length) {
            setCursorPosition(cursorPosition + 1);
          }
          break;
        case 'h': // Move left
          if (cursorPosition > 0) {
            setCursorPosition(cursorPosition - 1);
          }
          break;
        case 'l': // Move right
          if (cursorPosition < value.length) {
            setCursorPosition(cursorPosition + 1);
          }
          break;
        case 'j': // Move down (line)
          moveDown();
          break;
        case 'k': // Move up (line)
          moveUp();
          break;
        case 'x': // Delete character
          if (cursorPosition < value.length) {
            const newValue = value.slice(0, cursorPosition) + value.slice(cursorPosition + 1);
            onChange(newValue);
          }
          break;
        case 'w': // Move to next word
          moveToNextWord();
          break;
        case 'b': // Move to previous word
          moveToPreviousWord();
          break;
        case '0': // Move to beginning of line
          moveToLineStart();
          break;
        case '$': // Move to end of line
          moveToLineEnd();
          break;
        default:
          // For other keys in normal mode, ignore
          break;
      }
    }
  };

  const moveDown = () => {
    if (!textareaRef.current) return;

    const textarea = textareaRef.current;
    const lines = value.split('\n');
    const currentLineIndex = value.substring(0, cursorPosition).split('\n').length - 1;

    if (currentLineIndex < lines.length - 1) {
      // Calculate new cursor position at the same column in the next line
      const currentColumn = cursorPosition - value.lastIndexOf('\n', cursorPosition - 1) - 1;
      const nextLineStart = value.indexOf('\n', value.substring(0, cursorPosition).lastIndexOf('\n')) + 1;
      const newCursorPos = Math.min(nextLineStart + currentColumn, nextLineStart + lines[currentLineIndex + 1].length);
      setCursorPosition(newCursorPos);
    }
  };

  const moveUp = () => {
    if (!textareaRef.current) return;

    const textarea = textareaRef.current;
    const currentLineIndex = value.substring(0, cursorPosition).split('\n').length - 1;

    if (currentLineIndex > 0) {
      // Calculate new cursor position at the same column in the previous line
      const currentColumn = cursorPosition - value.lastIndexOf('\n', cursorPosition - 1) - 1;
      const prevLineStart = value.lastIndexOf('\n', value.lastIndexOf('\n', cursorPosition - 1) - 1) + 1;
      const newCursorPos = Math.min(prevLineStart + currentColumn, prevLineStart + value.split('\n')[currentLineIndex - 1].length);
      setCursorPosition(newCursorPos);
    }
  };

  const moveToNextWord = () => {
    const wordRegex = /\W+\w/; // Non-word chars followed by word char
    const nextWordMatch = value.substring(cursorPosition).search(wordRegex);

    if (nextWordMatch !== -1) {
      setCursorPosition(cursorPosition + nextWordMatch + 1);
    } else {
      // Move to end if no more words
      setCursorPosition(value.length);
    }
  };

  const moveToPreviousWord = () => {
    const wordRegex = /\w\W/; // Word char followed by non-word char
    const prevText = value.substring(0, cursorPosition);
    const reversedText = prevText.split('').reverse().join('');
    const prevWordMatch = reversedText.search(wordRegex);

    if (prevWordMatch !== -1) {
      const actualPos = prevText.length - prevWordMatch - 1;
      setCursorPosition(actualPos);
    } else {
      // Move to start if no previous word
      setCursorPosition(0);
    }
  };

  const moveToLineStart = () => {
    const lineStart = value.lastIndexOf('\n', cursorPosition - 1) + 1;
    setCursorPosition(lineStart);
  };

  const moveToLineEnd = () => {
    const lineEnd = value.indexOf('\n', cursorPosition);
    if (lineEnd !== -1) {
      setCursorPosition(lineEnd);
    } else {
      setCursorPosition(value.length);
    }
  };

  const handleInput = (e: React.FormEvent<HTMLTextAreaElement>) => {
    const newValue = e.currentTarget.value;
    onChange(newValue);
    setCursorPosition(e.currentTarget.selectionStart);
  };

  const handleFocus = () => {
    // When textarea is focused, enter insert mode
    setMode('insert');
  };

  const handleBlur = () => {
    // When textarea loses focus, enter normal mode
    setMode('normal');
  };

  const handleSelectionChange = () => {
    if (textareaRef.current) {
      setCursorPosition(textareaRef.current.selectionStart);
    }
  };

  // Mode indicator
  const modeIndicator = (
    <div className="absolute top-2 right-2 text-xs px-2 py-1 rounded bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300">
      {mode.toUpperCase()}
    </div>
  );

  return (
    <div className="relative">
      {modeIndicator}
      <textarea
        ref={textareaRef}
        value={value}
        onChange={handleInput}
        onKeyDown={handleKeyDown}
        onFocus={handleFocus}
        onBlur={handleBlur}
        onSelect={handleSelectionChange}
        placeholder={placeholder}
        rows={rows}
        className={`form-control ${className}`}
      />
      <div className="mt-1 text-xs text-gray-500 dark:text-gray-400">
        Vim Mode: Press 'Esc' for normal mode, 'i' to insert
      </div>
    </div>
  );
};

export default VimMode;