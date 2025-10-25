"""
Block Blast Solver Algorithm

This module implements the core algorithm for solving Block Blast puzzles.
The solver tries all permutations of the three blocks and all possible positions
to find the best placement strategies.
"""

import numpy as np
from itertools import permutations
from typing import List, Tuple, Optional, Dict, Any
import copy


class BlockBlastSolver:
    def __init__(self, board_size: int = 8):
        self.board_size = board_size
        
    def extract_block_coordinates(self, block_grid: List[List[int]]) -> List[Tuple[int, int]]:
        """
        Extract coordinates of filled cells from a 5x5 block grid.
        Returns list of (row, col) coordinates relative to the block's top-left corner.
        """
        coordinates = []
        for row in range(5):
            for col in range(5):
                if block_grid[row][col] == 1:
                    coordinates.append((row, col))
        return coordinates
    
    def can_place_block(self, board: np.ndarray, block_coords: List[Tuple[int, int]], 
                       center_row: int, center_col: int) -> bool:
        """
        Check if a block can be placed at the given center position on the board.
        """
        for block_row, block_col in block_coords:
            # Calculate absolute position on the board
            abs_row = center_row - 2 + block_row  # -2 to center the 5x5 block
            abs_col = center_col - 2 + block_col
            
            # Check bounds
            if abs_row < 0 or abs_row >= self.board_size or abs_col < 0 or abs_col >= self.board_size:
                return False
            
            # Check if position is already occupied
            if board[abs_row][abs_col] == 1:
                return False
                
        return True
    
    def place_block(self, board: np.ndarray, block_coords: List[Tuple[int, int]], 
                   center_row: int, center_col: int) -> np.ndarray:
        """
        Place a block on the board at the given center position.
        Returns a copy of the board with the block placed.
        """
        new_board = board.copy()
        for block_row, block_col in block_coords:
            abs_row = center_row - 2 + block_row
            abs_col = center_col - 2 + block_col
            new_board[abs_row][abs_col] = 1
        return new_board
    
    def clear_complete_lines(self, board: np.ndarray) -> Tuple[np.ndarray, int]:
        """
        Clear all complete rows and columns from the board.
        Returns the updated board and the number of lines cleared.
        """
        new_board = board.copy()
        lines_cleared = 0
        
        # Check and clear complete rows
        rows_to_clear = []
        for row in range(self.board_size):
            if np.all(new_board[row, :] == 1):
                rows_to_clear.append(row)
        
        # Check and clear complete columns
        cols_to_clear = []
        for col in range(self.board_size):
            if np.all(new_board[:, col] == 1):
                cols_to_clear.append(col)
        
        # Clear the identified rows and columns
        for row in rows_to_clear:
            new_board[row, :] = 0
            lines_cleared += 1
            
        for col in cols_to_clear:
            new_board[:, col] = 0
            lines_cleared += 1
        
        return new_board, lines_cleared
    
    def calculate_score(self, initial_board: np.ndarray, final_board: np.ndarray, 
                       lines_cleared: int) -> int:
        """
        Calculate a score for a solution based on various factors.
        Higher score is better.
        """
        # Base score from lines cleared
        score = lines_cleared * 10
        
        # Bonus for clearing more blocks
        initial_blocks = np.sum(initial_board)
        final_blocks = np.sum(final_board)
        blocks_cleared = initial_blocks - final_blocks
        score += blocks_cleared * 2
        
        # Penalty for remaining blocks (encourage clearing more)
        score -= final_blocks * 1
        
        return score
    
    def solve_iteration(self, initial_board: List[List[int]], 
                       blocks: List[List[List[int]]]) -> List[Dict[str, Any]]:
        """
        Solve one iteration of Block Blast with the given board and three blocks.
        
        Args:
            initial_board: 8x8 grid representing the current board state
            blocks: List of three 5x5 grids representing the blocks to place
            
        Returns:
            List of top solutions, each containing placement info and score
        """
        # Convert to numpy arrays for easier manipulation
        board = np.array(initial_board, dtype=int)
        
        # Extract coordinates for each block
        block_coords_list = [self.extract_block_coordinates(block) for block in blocks]
        
        # If any block is empty, return empty solution
        if any(len(coords) == 0 for coords in block_coords_list):
            return []
        
        solutions = []
        
        # Try all permutations of the three blocks
        for perm in permutations(range(3)):
            block_order = [block_coords_list[i] for i in perm]
            
            # Try all possible positions for the first block
            for center_row in range(self.board_size):
                for center_col in range(self.board_size):
                    if not self.can_place_block(board, block_order[0], center_row, center_col):
                        continue
                    
                    # Place first block
                    board_after_first = self.place_block(board, block_order[0], center_row, center_col)
                    board_after_first, lines_cleared_first = self.clear_complete_lines(board_after_first)
                    
                    # Try all possible positions for the second block
                    for center_row2 in range(self.board_size):
                        for center_col2 in range(self.board_size):
                            if not self.can_place_block(board_after_first, block_order[1], center_row2, center_col2):
                                continue
                            
                            # Place second block
                            board_after_second = self.place_block(board_after_first, block_order[1], center_row2, center_col2)
                            board_after_second, lines_cleared_second = self.clear_complete_lines(board_after_second)
                            
                            # Try all possible positions for the third block
                            for center_row3 in range(self.board_size):
                                for center_col3 in range(self.board_size):
                                    if not self.can_place_block(board_after_second, block_order[2], center_row3, center_col3):
                                        continue
                                    
                                    # Place third block
                                    board_after_third = self.place_block(board_after_second, block_order[2], center_row3, center_col3)
                                    board_after_third, lines_cleared_third = self.clear_complete_lines(board_after_third)
                                    
                                    # Calculate total score
                                    total_lines_cleared = lines_cleared_first + lines_cleared_second + lines_cleared_third
                                    score = self.calculate_score(board, board_after_third, total_lines_cleared)
                                    
                                    # Store solution
                                    solution = {
                                        'block_order': list(perm),
                                        'placements': [
                                            {'block_index': int(perm[0]), 'center_row': int(center_row), 'center_col': int(center_col)},
                                            {'block_index': int(perm[1]), 'center_row': int(center_row2), 'center_col': int(center_col2)},
                                            {'block_index': int(perm[2]), 'center_row': int(center_row3), 'center_col': int(center_col3)}
                                        ],
                                        'final_board': board_after_third.tolist(),
                                        'lines_cleared': int(total_lines_cleared),
                                        'score': int(score)
                                    }
                                    solutions.append(solution)
        
        # Sort solutions by score (descending) and return top 3
        solutions.sort(key=lambda x: x['score'], reverse=True)
        return solutions[:3]
    
    def apply_solution(self, initial_board: List[List[int]], 
                      blocks: List[List[List[int]]], 
                      solution: Dict[str, Any]) -> List[List[int]]:
        """
        Apply a solution to the board and return the final board state.
        """
        board = np.array(initial_board, dtype=int)
        block_coords_list = [self.extract_block_coordinates(block) for block in blocks]
        
        for placement in solution['placements']:
            block_index = placement['block_index']
            center_row = placement['center_row']
            center_col = placement['center_col']
            
            board = self.place_block(board, block_coords_list[block_index], center_row, center_col)
            board, _ = self.clear_complete_lines(board)
        
        return board.tolist()
