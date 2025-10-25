import { useState, useCallback } from 'react';
import { GameState, Cell, Block, Solution } from '../types';
import { ApiService } from '../services/api';

const createEmptyGrid = (size: number): Cell[][] => {
  return Array(size).fill(null).map(() => 
    Array(size).fill(null).map(() => ({ filled: false }))
  );
};

const createEmptyBlock = (): number[][] => {
  return Array(5).fill(null).map(() => Array(5).fill(0));
};

export const useGameState = () => {
  const [gameState, setGameState] = useState<GameState>({
    board: createEmptyGrid(8).map(row => row.map(cell => cell.filled ? 1 : 0)),
    blocks: [
      { cells: createEmptyBlock() },
      { cells: createEmptyBlock() },
      { cells: createEmptyBlock() }
    ],
    solutions: [],
    selectedSolution: null,
    isLoading: false,
    error: null,
    iteration: 1
  });

  const updateBoardCell = useCallback((row: number, col: number) => {
    setGameState(prev => {
      const newBoard = prev.board.map((boardRow, r) =>
        boardRow.map((cell, c) => 
          r === row && c === col ? (cell === 1 ? 0 : 1) : cell
        )
      );
      return { ...prev, board: newBoard };
    });
  }, []);

  const updateBlockCell = useCallback((blockIndex: number, row: number, col: number) => {
    setGameState(prev => {
      const newBlocks = [...prev.blocks];
      newBlocks[blockIndex] = {
        ...newBlocks[blockIndex],
        cells: newBlocks[blockIndex].cells.map((blockRow, r) =>
          blockRow.map((cell, c) => 
            r === row && c === col ? (cell === 1 ? 0 : 1) : cell
          )
        )
      };
      return { ...prev, blocks: newBlocks };
    });
  }, []);

  const clearBlock = useCallback((blockIndex: number) => {
    setGameState(prev => {
      const newBlocks = [...prev.blocks];
      newBlocks[blockIndex] = { cells: createEmptyBlock() };
      return { ...prev, blocks: newBlocks };
    });
  }, []);

  const solveIteration = useCallback(async () => {
    setGameState(prev => ({ ...prev, isLoading: true, error: null }));
    
    try {
      const response = await ApiService.solveIteration(
        gameState.board,
        gameState.blocks.map(block => block.cells)
      );
      
      setGameState(prev => ({
        ...prev,
        solutions: response.solutions,
        selectedSolution: response.solutions.length > 0 ? 0 : null,
        isLoading: false
      }));
    } catch (error) {
      setGameState(prev => ({
        ...prev,
        error: error instanceof Error ? error.message : 'Unknown error occurred',
        isLoading: false
      }));
    }
  }, [gameState.board, gameState.blocks]);

  const selectSolution = useCallback((index: number) => {
    setGameState(prev => ({ ...prev, selectedSolution: index }));
  }, []);

  const acceptSolution = useCallback(async () => {
    if (gameState.selectedSolution === null) return;

    const selectedSol = gameState.solutions[gameState.selectedSolution];
    if (!selectedSol) return;

    setGameState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      const response = await ApiService.applySolution(
        gameState.board,
        gameState.blocks.map(block => block.cells),
        selectedSol
      );

      setGameState(prev => ({
        ...prev,
        board: response.finalBoard,
        blocks: [
          { cells: createEmptyBlock() },
          { cells: createEmptyBlock() },
          { cells: createEmptyBlock() }
        ],
        solutions: [],
        selectedSolution: null,
        isLoading: false,
        iteration: prev.iteration + 1
      }));
    } catch (error) {
      setGameState(prev => ({
        ...prev,
        error: error instanceof Error ? error.message : 'Failed to apply solution',
        isLoading: false
      }));
    }
  }, [gameState.selectedSolution, gameState.solutions, gameState.board, gameState.blocks]);

  const resetGame = useCallback(() => {
    setGameState({
      board: createEmptyGrid(8).map(row => row.map(cell => cell.filled ? 1 : 0)),
      blocks: [
        { cells: createEmptyBlock() },
        { cells: createEmptyBlock() },
        { cells: createEmptyBlock() }
      ],
      solutions: [],
      selectedSolution: null,
      isLoading: false,
      error: null,
      iteration: 1
    });
  }, []);

  return {
    gameState,
    updateBoardCell,
    updateBlockCell,
    clearBlock,
    solveIteration,
    selectSolution,
    acceptSolution,
    resetGame
  };
};
