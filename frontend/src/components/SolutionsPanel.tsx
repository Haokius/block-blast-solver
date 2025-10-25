import React from 'react';
import { Solution } from '../types';

interface SolutionsPanelProps {
  solutions: Solution[];
  selectedSolution: number | null;
  onSolutionSelect: (index: number) => void;
  onAcceptSolution: () => void;
  isLoading: boolean;
  error: string | null;
}

const SolutionsPanel: React.FC<SolutionsPanelProps> = ({
  solutions,
  selectedSolution,
  onSolutionSelect,
  onAcceptSolution,
  isLoading,
  error
}) => {
  if (isLoading) {
    return (
      <div className="solutions-section">
        <h3 className="section-title">Solutions</h3>
        <div className="loading">Finding optimal solutions...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="solutions-section">
        <h3 className="section-title">Solutions</h3>
        <div className="error">{error}</div>
      </div>
    );
  }

  if (solutions.length === 0) {
    return (
      <div className="solutions-section">
        <h3 className="section-title">Solutions</h3>
        <div className="error">No valid solutions found. Try different block configurations.</div>
      </div>
    );
  }

  return (
    <div className="solutions-section">
      <h3 className="section-title">Solutions ({solutions.length})</h3>
      
      {solutions.map((solution, index) => (
        <div
          key={index}
          className={`solution ${selectedSolution === index ? 'selected' : ''}`}
          onClick={() => onSolutionSelect(index)}
        >
          <div className="solution-header">
            <span>Solution {index + 1}</span>
            <span className="solution-score">Score: {solution.score}</span>
          </div>
          <div className="solution-details">
            <div>Lines Cleared: {solution.linesCleared}</div>
            <div>Block Order: {solution.blockOrder.map(i => i + 1).join(' → ')}</div>
            <div>
              Placements: {solution.placements.map(p => 
                `B${p.blockIndex + 1}@(${p.centerRow},${p.centerCol})`
              ).join(', ')}
            </div>
          </div>
        </div>
      ))}

      <div className="controls">
        <button
          className="button button-success"
          onClick={onAcceptSolution}
          disabled={selectedSolution === null}
        >
          Accept Solution
        </button>
      </div>
    </div>
  );
};

export default SolutionsPanel;
