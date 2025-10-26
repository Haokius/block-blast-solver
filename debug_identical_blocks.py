#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

import numpy as np
from solver import BlockBlastSolver

def debug_identical_blocks():
    """
    Debug why identical blocks aren't working
    """
    
    # Your original board configuration
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
    
    # Your ORIGINAL blocks (both identical vertical lines at column 1)
    blocks = [
        np.array([
            [1, 1, 1, 0, 0],
            [1, 1, 1, 0, 0],
            [1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]),
        np.array([
            [0, 1, 0, 0, 0],  # Vertical line at column 1
            [0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]),
        np.array([
            [0, 1, 0, 0, 0],  # Same vertical line at column 1
            [0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ])
    ]
    
    print("=== DEBUGGING IDENTICAL BLOCKS ===")
    print("Board:")
    print(board)
    print("\nBlocks:")
    for i, block in enumerate(blocks):
        print(f"Block {i+1}:")
        print(block)
        print()
    
    solver = BlockBlastSolver()
    
    # Check coordinates
    block1_coords = solver.extract_block_coordinates(blocks[0])
    block2_coords = solver.extract_block_coordinates(blocks[1])
    block3_coords = solver.extract_block_coordinates(blocks[2])
    
    print(f"Block 1 coordinates: {block1_coords}")
    print(f"Block 2 coordinates: {block2_coords}")
    print(f"Block 3 coordinates: {block3_coords}")
    
    # Test the strategy manually
    print("\n=== MANUAL STRATEGY TEST ===")
    
    # Strategy: Place Block 2 at top-left (2, -1) to hit column 0 at rows 2,3,4,5
    print("Testing Block 2 at top-left (2, -1):")
    top_left_row2, top_left_col2 = 2, -1
    
    print("Block 2 would be placed at:")
    for block_row, block_col in block2_coords:
        abs_row = top_left_row2 + block_row
        abs_col = top_left_col2 + block_col
        print(f"  ({block_row}, {block_col}) -> ({abs_row}, {abs_col}) = {board[abs_row][abs_col]}")
    
    can_place2 = solver.can_place_block(board, block2_coords, top_left_row2, top_left_col2)
    print(f"Can place Block 2: {can_place2}")
    
    if can_place2:
        board_after_2 = solver.place_block(board, block2_coords, top_left_row2, top_left_col2)
        print("Board after Block 2:")
        print(board_after_2)
        
        # Strategy: Place Block 3 at top-left (2, 6) to hit column 7 at rows 2,3,4,5
        print("\nTesting Block 3 at top-left (2, 6):")
        top_left_row3, top_left_col3 = 2, 6
        
        print("Block 3 would be placed at:")
        for block_row, block_col in block3_coords:
            abs_row = top_left_row3 + block_row
            abs_col = top_left_col3 + block_col
            print(f"  ({block_row}, {block_col}) -> ({abs_row}, {abs_col}) = {board_after_2[abs_row][abs_col]}")
        
        can_place3 = solver.can_place_block(board_after_2, block3_coords, top_left_row3, top_left_col3)
        print(f"Can place Block 3: {can_place3}")
        
        if can_place3:
            board_after_3 = solver.place_block(board_after_2, block3_coords, top_left_row3, top_left_col3)
            print("Board after Block 3:")
            print(board_after_3)
            
            # Clear lines
            board_after_3_cleared, lines_cleared = solver.clear_complete_lines(board_after_3)
            print(f"Lines cleared: {lines_cleared}")
            print("Board after clearing lines:")
            print(board_after_3_cleared)
            
            print("\n✅ Strategy works! The solver should find this solution.")
        else:
            print("❌ Block 3 placement failed")
    else:
        print("❌ Block 2 placement failed")

if __name__ == "__main__":
    debug_identical_blocks()
