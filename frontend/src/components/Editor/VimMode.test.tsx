// frontend/src/components/Editor/VimMode.test.tsx

import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import VimMode from './VimMode';

describe('VimMode', () => {
  const mockOnChange = jest.fn();

  beforeEach(() => {
    mockOnChange.mockClear();
  });

  it('renders correctly with initial value', () => {
    render(
      <VimMode
        value="Initial text"
        onChange={mockOnChange}
        placeholder="Test placeholder"
      />
    );

    expect(screen.getByPlaceholderText('Test placeholder')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Initial text')).toBeInTheDocument();
    expect(screen.getByText('INSERT')).toBeInTheDocument(); // Should start in insert mode
  });

  it('switches to normal mode when Escape is pressed', () => {
    render(
      <VimMode
        value="Test text"
        onChange={mockOnChange}
      />
    );

    const textarea = screen.getByDisplayValue('Test text');

    // Initially in insert mode
    expect(screen.getByText('INSERT')).toBeInTheDocument();

    // Press Escape to enter normal mode
    fireEvent.keyDown(textarea, { key: 'Escape' });

    // Should now be in normal mode
    expect(screen.getByText('NORMAL')).toBeInTheDocument();
  });

  it('switches to insert mode when "i" is pressed in normal mode', () => {
    render(
      <VimMode
        value="Test text"
        onChange={mockOnChange}
      />
    );

    const textarea = screen.getByDisplayValue('Test text');

    // First press Escape to enter normal mode
    fireEvent.keyDown(textarea, { key: 'Escape' });
    expect(screen.getByText('NORMAL')).toBeInTheDocument();

    // Then press 'i' to enter insert mode
    fireEvent.keyDown(textarea, { key: 'i' });
    expect(screen.getByText('INSERT')).toBeInTheDocument();
  });

  it('deletes character when "x" is pressed in normal mode', () => {
    render(
      <VimMode
        value="Test"
        onChange={mockOnChange}
      />
    );

    const textarea = screen.getByDisplayValue('Test');

    // Press Escape to enter normal mode
    fireEvent.keyDown(textarea, { key: 'Escape' });

    // Press 'x' to delete the character at cursor position (default 0)
    fireEvent.keyDown(textarea, { key: 'x' });

    // Should have called onChange with the modified text
    expect(mockOnChange).toHaveBeenCalledWith('est');
  });

  it('handles movement with h, j, k, l keys in normal mode', () => {
    render(
      <VimMode
        value="Test\nText"
        onChange={mockOnChange}
      />
    );

    const textarea = screen.getByRole('textbox');

    // Press Escape to enter normal mode
    fireEvent.keyDown(textarea, { key: 'Escape' });

    // Press 'l' to move right
    fireEvent.keyDown(textarea, { key: 'l' });

    // Press 'j' to move down
    fireEvent.keyDown(textarea, { key: 'j' });

    // Press 'k' to move up
    fireEvent.keyDown(textarea, { key: 'k' });

    // Press 'h' to move left
    fireEvent.keyDown(textarea, { key: 'h' });

    // The value should remain unchanged as these are movement commands
    expect(mockOnChange).not.toHaveBeenCalled();
  });

  it('updates value when typing in insert mode', () => {
    render(
      <VimMode
        value="Test"
        onChange={mockOnChange}
      />
    );

    const textarea = screen.getByDisplayValue('Test');

    // Type in insert mode
    fireEvent.change(textarea, { target: { value: 'Test updated' } });

    expect(mockOnChange).toHaveBeenCalledWith('Test updated');
  });
});