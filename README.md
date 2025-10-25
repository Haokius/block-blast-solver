# Block Blast Solver

A comprehensive Block Blast puzzle solver with a clean HTML/CSS/JavaScript frontend and Python backend. This tool helps you find optimal placement strategies for your blocks to maximize row and column clearing.

## Features

- **Interactive 8×8 Game Board**: Click to add/remove existing blocks
- **Smart Block Designers**: Three 5×5 grids with preset shapes (L, T, Z, Square, Cross, Line) and drag-to-create functionality
- **Smart Solver Algorithm**: Tries all permutations and placements to find optimal solutions
- **Solution Ranking**: Shows top 3 solutions with scores and placement details
- **Iterative Gameplay**: Accept solutions to continue to the next iteration
- **Modern UI**: Clean, responsive design with smooth animations and intuitive controls

## How It Works

The solver implements the algorithm you specified:

1. **Permutation Testing**: Tries all possible orders of the three blocks (t1, t2, t3)
2. **Position Testing**: For each permutation, tests all 64 possible center positions on the 8×8 board
3. **Placement Validation**: Checks if each block can be placed without overlapping existing blocks
4. **Line Clearing**: Automatically removes complete rows and columns after each placement
5. **Solution Scoring**: Ranks solutions based on lines cleared, blocks removed, and remaining blocks
6. **Top Results**: Returns the best 3 solutions for user selection

## Architecture

- **Frontend**: Pure HTML/CSS/JavaScript (no frameworks needed!)
- **Backend**: Python + Flask + NumPy
- **API**: RESTful communication between frontend and backend

## Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Setup

1. **Clone and install dependencies:**
```bash
git clone <repository-url>
cd block-blast-solver
npm run install:all
```

2. **Start the development servers:**
```bash
npm run dev
```

This will start:
- Frontend on http://localhost:3000 (simple HTML server)
- Backend API on http://localhost:5003

### Manual Setup

If you prefer to run the services separately:

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

**Frontend:**
```bash
python3 -m http.server 3000
```

## Usage

1. **Set up the board**: Click on the 8×8 grid to add/remove existing blocks (red cells)
2. **Design your blocks**: Click or drag on the 5×5 grids to draw the shapes of your three insertion blocks (blue cells)
3. **Find solutions**: Click "Find Solutions" to get optimal placement suggestions
4. **Review solutions**: Click on a solution to see its details and score
5. **Accept solution**: Click "Accept Solution" to apply the best placement and continue to the next iteration

### Block Design Features

The block designers now include:

**Preset Shapes:**
- **L-Shape**: Classic L-block for corners and edges
- **T-Shape**: T-block for strategic placements
- **Z-Shape**: Zigzag pattern for complex fills
- **Square**: 2×2 block for compact areas
- **Cross**: Plus-shaped block for intersections
- **Line**: Horizontal line for row clearing

**Custom Creation:**
- **Click**: Toggle individual cells
- **Drag**: Hold mouse down and drag across cells to create continuous shapes
- **Perfect for**: Creating custom patterns and complex block designs

## API Endpoints

- `POST /api/solve` - Solve an iteration with current board and blocks
- `POST /api/apply-solution` - Apply a selected solution to get final board state
- `GET /api/health` - Health check endpoint

## Frontend Features

The new HTML/CSS/JavaScript frontend provides:

- **Modern Design**: Clean, professional interface with gradient backgrounds and smooth animations
- **Responsive Layout**: Works on desktop and mobile devices
- **Drag Functionality**: Intuitive drag-to-create for block shapes
- **Real-time Updates**: Instant visual feedback for all interactions
- **No Dependencies**: Pure HTML/CSS/JS - no frameworks or build tools needed
- **Fast Loading**: Lightweight and fast compared to React-based solutions

## Algorithm Details

The solver uses a brute-force approach with optimizations:

1. **Block Coordinate Extraction**: Converts 5×5 block grids to coordinate lists
2. **Placement Validation**: Checks bounds and overlap constraints
3. **Line Clearing Logic**: Identifies and removes complete rows/columns
4. **Scoring System**: 
   - +10 points per line cleared
   - +2 points per block removed
   - -1 point per remaining block
5. **Solution Ranking**: Sorts by total score and returns top 3

## Performance Considerations

The algorithm has O(n³ × 3! × 64³) complexity in the worst case, where n is the board size. For an 8×8 board with 3 blocks, this results in testing up to 1,728,000 combinations per iteration. The solver is optimized for typical Block Blast scenarios and should provide results within a few seconds for most configurations.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the solver algorithm or user interface.

## License

MIT License - feel free to use this project for learning and development purposes.
