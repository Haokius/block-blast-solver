#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

import numpy as np
from solver import BlockBlastSolver

def test_backend_case():
    """
    Test case that demonstrates the working strategy:
    1. 4x6 rectangle of filled cells in the middle
    2. Two vertical lines to clear the rows
    3. 3x3 square to place on the cleared board
    """
    
    # Board with 4x6 rectangle of filled cells (rows 2-5, columns 1-6)
    board = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ])
    
    # Blocks designed for the strategy:
    # Block 1: 3x3 square (to place after clearing)
    # Block 2: 1x4 vertical line at LEFT edge (column 0)
    # Block 3: 1x4 vertical line at RIGHT edge (column 4)
    blocks = [
        np.array([
            [1, 1, 1, 0, 0],
            [1, 1, 1, 0, 0],
            [1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]),
        np.array([
            [1, 0, 0, 0, 0],  # Vertical line at column 0 (left edge)
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]),
        np.array([
            [0, 0, 0, 0, 1],  # Vertical line at column 4 (right edge)
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0]
        ])
    ]
    
    print("=== BLOCK BLAST SOLVER TEST CASE ===")
    print("Board (4x6 rectangle of filled cells):")
    print(board)
    print("\nBlocks:")
    for i, block in enumerate(blocks):
        print(f"Block {i+1}:")
        print(block)
        print()
    
    # Test the solver
    solver = BlockBlastSolver()
    solutions = solver.solve_iteration(board, blocks)
    
    print(f"Number of solutions found: {len(solutions)}")
    
    if solutions:
        print("\n✅ SOLVER SUCCESS! Found solutions:")
        for i, solution in enumerate(solutions):
            print(f"\nSolution {i+1}:")
            print(f"  Block order: {solution['block_order']}")
            print(f"  Placements: {solution['placements']}")
            print(f"  Lines cleared: {solution['lines_cleared']}")
            print(f"  Score: {solution['score']}")
            
            # Show the final board state
            print(f"  Final board:")
            final_board = np.array(solution['final_board'])
            print(final_board)
    else:
        print("❌ No solutions found by solver")
        
        # Debug: Let's manually test the strategy
        print("\n=== MANUAL STRATEGY DEBUG ===")
        
        # Get block coordinates
        block1_coords = solver.extract_block_coordinates(blocks[0])
        block2_coords = solver.extract_block_coordinates(blocks[1])
        block3_coords = solver.extract_block_coordinates(blocks[2])
        
        print(f"Block 1 coordinates: {block1_coords}")
        print(f"Block 2 coordinates: {block2_coords}")
        print(f"Block 3 coordinates: {block3_coords}")
        
        # Test placing Block 2 at center (4, 2) - should hit rows 2,3,4,5 at column 0
        print("\nTesting Block 2 placement at center (4, 2):")
        center_row2, center_col2 = 4, 2
        can_place2 = solver.can_place_block(board, block2_coords, center_row2, center_col2)
        print(f"Can place Block 2: {can_place2}")
        
        if can_place2:
            board_after_2 = solver.place_block(board, block2_coords, center_row2, center_col2)
            print("Board after Block 2:")
            print(board_after_2)
            
            # Test placing Block 3 at center (4, 5) - should hit rows 2,3,4,5 at column 7
            print("\nTesting Block 3 placement at center (4, 5):")
            center_row3, center_col3 = 4, 5
            can_place3 = solver.can_place_block(board_after_2, block3_coords, center_row3, center_col3)
            print(f"Can place Block 3: {can_place3}")
            
            if can_place3:
                board_after_3 = solver.place_block(board_after_2, block3_coords, center_row3, center_col3)
                print("Board after Block 3:")
                print(board_after_3)
                
                # Clear lines
                board_after_3_cleared, lines_cleared = solver.clear_complete_lines(board_after_3)
                print(f"Lines cleared: {lines_cleared}")
                print("Board after clearing lines:")
                print(board_after_3_cleared)
                
                print("\n✅ Manual strategy works! The solver should find this solution.")

if __name__ == "__main__":
    test_backend_case()
