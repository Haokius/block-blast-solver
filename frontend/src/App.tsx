import React from 'react';
import Grid from './components/Grid';
import BlockEditor from './components/BlockEditor';
import SolutionsPanel from './components/SolutionsPanel';
import { useGameState } from './hooks/useGameState';
import { Cell } from './types';

const App: React.FC = () => {
  const {
    gameState,
    updateBoardCell,
    updateBlockCell,
    clearBlock,
    solveIteration,
    selectSolution,
    acceptSolution,
    resetGame
  } = useGameState();

  // Convert board to Cell format for display
  const boardCells: Cell[][] = gameState.board.map(row =>
    row.map(cell => ({ filled: cell === 1 }))
  );

  // Convert blocks to Cell format for display
  const blockCells: Cell[][][] = gameState.blocks.map(block =>
    block.cells.map(row =>
      row.map(cell => ({ filled: cell === 1 }))
    )
  );

  const hasBlocks = gameState.blocks.some(block => 
    block.cells.some(row => row.some(cell => cell === 1))
  );

  return (
    <div className="app">
      <header className="header">
        <h1>Block Blast Solver</h1>
        <p>Design your blocks and get optimal placement suggestions</p>
        <p>Iteration: {gameState.iteration}</p>
      </header>

      <div className="game-container">
        {/* Main 8x8 Board */}
        <div className="board-section">
          <h3 className="section-title">Game Board (8×8)</h3>
          <Grid
            cells={boardCells}
            onCellClick={updateBoardCell}
            size="8x8"
          />
          <div className="controls">
            <button
              className="button button-secondary"
              onClick={resetGame}
            >
              Reset Board
            </button>
          </div>
        </div>

        {/* Block Editors */}
        <div className="blocks-section">
          <h3 className="section-title">Block Designers (5×5)</h3>
          {gameState.blocks.map((_, index) => (
            <BlockEditor
              key={index}
              blockIndex={index}
              cells={blockCells[index]}
              onCellClick={(row, col) => updateBlockCell(index, row, col)}
              onClear={() => clearBlock(index)}
            />
          ))}
          
          <div className="controls">
            <button
              className="button button-primary"
              onClick={solveIteration}
              disabled={!hasBlocks || gameState.isLoading}
            >
              {gameState.isLoading ? 'Solving...' : 'Find Solutions'}
            </button>
          </div>
        </div>

        {/* Solutions Panel */}
        <SolutionsPanel
          solutions={gameState.solutions}
          selectedSolution={gameState.selectedSolution}
          onSolutionSelect={selectSolution}
          onAcceptSolution={acceptSolution}
          isLoading={gameState.isLoading}
          error={gameState.error}
        />
      </div>

      {/* Instructions */}
      <div style={{ 
        maxWidth: '800px', 
        margin: '30px auto', 
        padding: '20px',
        background: 'white',
        borderRadius: '12px',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
      }}>
        <h3 style={{ color: '#2c3e50', marginBottom: '15px' }}>How to Use:</h3>
        <ol style={{ lineHeight: '1.6', color: '#555' }}>
          <li><strong>Set up the board:</strong> Click on the 8×8 grid to add/remove existing blocks (red cells)</li>
          <li><strong>Design your blocks:</strong> Click on the 5×5 grids to draw the shapes of your three insertion blocks (blue cells)</li>
          <li><strong>Find solutions:</strong> Click "Find Solutions" to get optimal placement suggestions</li>
          <li><strong>Review solutions:</strong> Click on a solution to see its details and score</li>
          <li><strong>Accept solution:</strong> Click "Accept Solution" to apply the best placement and continue to the next iteration</li>
        </ol>
        <p style={{ marginTop: '15px', color: '#7f8c8d', fontStyle: 'italic' }}>
          The solver tries all possible placements and orders of your three blocks to find the best strategies for clearing rows and columns.
        </p>
      </div>
    </div>
  );
};

export default App;
