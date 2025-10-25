export interface Cell {
  filled: boolean;
  isBlock?: boolean;
  isSuggestion?: boolean;
}

export interface Grid {
  cells: Cell[][];
}

export interface Block {
  cells: number[][]; // 5x5 grid with 0s and 1s
}

export interface Placement {
  blockIndex: number;
  centerRow: number;
  centerCol: number;
}

export interface Solution {
  blockOrder: number[];
  placements: Placement[];
  finalBoard: number[][];
  linesCleared: number;
  score: number;
}

export interface SolverResponse {
  solutions: Solution[];
  totalSolutions: number;
}

export interface GameState {
  board: number[][]; // 8x8 grid
  blocks: Block[]; // 3 blocks, each 5x5
  solutions: Solution[];
  selectedSolution: number | null;
  isLoading: boolean;
  error: string | null;
  iteration: number;
}
