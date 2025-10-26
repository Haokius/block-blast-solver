"""
Flask API server for Block Blast Solver
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from solver import BlockBlastSolver
import json

app = Flask(__name__)
CORS(app)

# Initialize the solver
solver = BlockBlastSolver()

@app.route('/api/solve', methods=['POST'])
def solve():
    """
    Solve a Block Blast iteration.
    
    Expected JSON payload:
    {
        "board": [[0,1,0,...], ...],  // 8x8 grid
        "blocks": [
            [[0,1,0,...], ...],       // First 5x5 block
            [[1,1,0,...], ...],       // Second 5x5 block  
            [[0,0,1,...], ...]        // Third 5x5 block
        ]
    }
    
    Returns:
    {
        "solutions": [
            {
                "block_order": [0, 1, 2],
                "placements": [
                    {"block_index": 0, "center_row": 3, "center_col": 4},
                    {"block_index": 1, "center_row": 2, "center_col": 1},
                    {"block_index": 2, "center_row": 5, "center_col": 6}
                ],
                "final_board": [[0,0,0,...], ...],
                "lines_cleared": 2,
                "score": 25
            },
            ...
        ]
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        board = data.get('board')
        blocks = data.get('blocks')
        
        # Debug: Print what we received
        print("=== BACKEND DEBUG ===")
        print("Received board:")
        for i, row in enumerate(board):
            print(f"Row {i}: {row}")
        print("\nReceived blocks:")
        for i, block in enumerate(blocks):
            print(f"Block {i+1}:")
            for j, row in enumerate(block):
                print(f"  Row {j}: {row}")
        print("===================")
        
        if not board or not blocks:
            return jsonify({'error': 'Missing board or blocks data'}), 400
        
        if len(board) != 8 or any(len(row) != 8 for row in board):
            return jsonify({'error': 'Board must be 8x8'}), 400
        
        if len(blocks) != 3:
            return jsonify({'error': 'Must provide exactly 3 blocks'}), 400
        
        for i, block in enumerate(blocks):
            if len(block) != 5 or any(len(row) != 5 for row in block):
                return jsonify({'error': f'Block {i+1} must be 5x5'}), 400
        
        # Solve the iteration
        solutions = solver.solve_iteration(board, blocks)
        
        print(f"Found {len(solutions)} solutions")
        
        return jsonify({
            'solutions': solutions,
            'total_solutions': len(solutions)
        })
        
    except Exception as e:
        print(f"Error in solve endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/apply-solution', methods=['POST'])
def apply_solution():
    """
    Apply a solution to get the final board state.
    
    Expected JSON payload:
    {
        "board": [[0,1,0,...], ...],  // 8x8 grid
        "blocks": [
            [[0,1,0,...], ...],       // First 5x5 block
            [[1,1,0,...], ...],       // Second 5x5 block  
            [[0,0,1,...], ...]        // Third 5x5 block
        ],
        "solution": {
            "block_order": [0, 1, 2],
            "placements": [...],
            ...
        }
    }
    
    Returns:
    {
        "final_board": [[0,0,0,...], ...]
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        board = data.get('board')
        blocks = data.get('blocks')
        solution = data.get('solution')
        
        if not all([board, blocks, solution]):
            return jsonify({'error': 'Missing required data'}), 400
        
        # Apply the solution
        final_board = solver.apply_solution(board, blocks, solution)
        
        return jsonify({
            'final_board': final_board
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Block Blast Solver API is running'})

if __name__ == '__main__':
    print("Starting Block Blast Solver API...")
    print("API will be available at: http://localhost:8000")
    print("Health check: http://localhost:8000/api/health")
    app.run(debug=True, host='0.0.0.0', port=8000)
