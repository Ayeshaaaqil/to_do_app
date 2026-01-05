// frontend/src/components/Editor/Editor.test.tsx

import React from 'react';
import { render, screen } from '@testing-library/react';
import VimMode from './VimMode';

describe('Editor Integration', () => {
  it('should render the VimMode component with correct styling', () => {
    render(
      <VimMode 
        value="" 
        onChange={jest.fn()} 
        placeholder="Test editor" 
        rows={4}
      />
    );

    const textarea = screen.getByPlaceholderText('Test editor');
    const modeIndicator = screen.getByText('INSERT');
    const helpText = screen.getByText('Vim Mode: Press \'Esc\' for normal mode, \'i\' to insert');

    expect(textarea).toBeInTheDocument();
    expect(textarea).toHaveClass('w-full');
    expect(modeIndicator).toBeInTheDocument();
    expect(helpText).toBeInTheDocument();
  });

  it('should handle different rows prop', () => {
    render(
      <VimMode 
        value="" 
        onChange={jest.fn()} 
        placeholder="Test editor" 
        rows={6}
      />
    );

    const textarea = screen.getByPlaceholderText('Test editor');
    expect(textarea).toHaveAttribute('rows', '6');
  });
});