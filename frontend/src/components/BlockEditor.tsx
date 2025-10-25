import React from 'react';
import Grid from './Grid';
import { Cell } from '../types';

interface BlockEditorProps {
  blockIndex: number;
  cells: Cell[][];
  onCellClick: (row: number, col: number) => void;
  onClear: () => void;
}

const BlockEditor: React.FC<BlockEditorProps> = ({ 
  blockIndex, 
  cells, 
  onCellClick, 
  onClear 
}) => {
  return (
    <div className="block-editor">
      <h3 className="block-title">Block {blockIndex + 1}</h3>
      <Grid
        cells={cells}
        onCellClick={onCellClick}
        size="5x5"
        className="block-grid"
      />
      <div className="block-controls">
        <button 
          className="button button-secondary"
          onClick={onClear}
          style={{ marginTop: '10px', minWidth: '100px' }}
        >
          Clear Block
        </button>
      </div>
    </div>
  );
};

export default BlockEditor;
