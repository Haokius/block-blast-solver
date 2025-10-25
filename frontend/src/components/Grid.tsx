import React from 'react';
import { Cell } from '../types';

interface GridProps {
  cells: Cell[][];
  onCellClick?: (row: number, col: number) => void;
  size: '8x8' | '5x5';
  title?: string;
  className?: string;
}

const Grid: React.FC<GridProps> = ({ 
  cells, 
  onCellClick, 
  size, 
  title, 
  className = '' 
}) => {
  const gridSize = size === '8x8' ? 8 : 5;
  const cellSize = size === '8x8' ? '35px' : '25px';

  return (
    <div className={`grid-section ${className}`}>
      {title && <h3 className="section-title">{title}</h3>}
      <div 
        className={`grid grid-${size}`}
        style={{
          gridTemplateColumns: `repeat(${gridSize}, ${cellSize})`,
          gridTemplateRows: `repeat(${gridSize}, ${cellSize})`
        }}
      >
        {cells.map((row, rowIndex) =>
          row.map((cell, colIndex) => (
            <div
              key={`${rowIndex}-${colIndex}`}
              className={`cell ${
                cell.filled 
                  ? 'filled' 
                  : cell.isBlock 
                    ? 'block-cell' 
                    : cell.isSuggestion 
                      ? 'suggestion' 
                      : ''
              }`}
              onClick={() => onCellClick?.(rowIndex, colIndex)}
              style={{ width: cellSize, height: cellSize }}
            />
          ))
        )}
      </div>
    </div>
  );
};

export default Grid;
