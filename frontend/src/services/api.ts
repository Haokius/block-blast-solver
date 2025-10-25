import { SolverResponse, Solution } from '../types';

const API_BASE_URL = '/api';

export class ApiService {
  static async solveIteration(board: number[][], blocks: number[][][]): Promise<SolverResponse> {
    const response = await fetch(`${API_BASE_URL}/solve`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        board,
        blocks
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to solve iteration');
    }

    return response.json();
  }

  static async applySolution(
    board: number[][], 
    blocks: number[][][], 
    solution: Solution
  ): Promise<{ finalBoard: number[][] }> {
    const response = await fetch(`${API_BASE_URL}/apply-solution`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        board,
        blocks,
        solution
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to apply solution');
    }

    return response.json();
  }

  static async healthCheck(): Promise<{ status: string; message: string }> {
    const response = await fetch(`${API_BASE_URL}/health`);
    
    if (!response.ok) {
      throw new Error('API health check failed');
    }

    return response.json();
  }
}
