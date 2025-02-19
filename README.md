# Sudoku Solver and Generator Project

## Research Paper:

You can access the full paper here: [arxiv:2305.08291](https://arxiv.org/pdf/2305.08291)

## Project Overview

This project consists of several components for generating and solving Sudoku puzzles. It includes:

1. **Sudoku Generator**: Generates Sudoku puzzles of varying difficulties.
2. **Sudoku Solver**: Solves Sudoku puzzles using different algorithms (Tree-of-Thought approach and backtracking).
3. **Tree-based search:** Utilizes a search tree where each node represents a partially solved board.
4. **Backtracking with heuristics:** Avoids dead-end paths by identifying invalid moves early.
5. **LLM-powered move generation:** Uses an AI model to suggest the best possible move.
6. **Dynamic decision-making:** Adjusts strategy based on the number of failed attempts.
7. **Scoring system for candidate moves:** Ranks numbers based on their probability of success.
8. **Solution Checker**: Validates the correctness of a Sudoku solution.
9. **GUI**: A graphical user interface for playing Sudoku.

## Key Features

- **Sudoku Generation**: Generate Sudoku puzzles with different difficulty levels.
- **Sudoku Solving**: Solve Sudoku puzzles using advanced algorithms.
- **Solution Validation**: Check the correctness of a Sudoku solution.
- **GUI Interface**: Play Sudoku with an interactive graphical user interface.

## Installation

### Dependencies

- Python 3.8 or higher
- `tkinter` for the GUI
- `termcolor` for colored output in the solution checker
- `llama_cpp_python` for the LLM-based solving approach (optional)

### Setup Instructions

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/zocainViken/ToTSudokuSolver4Gguf.git
    cd ToTSudokuSolver4Gguf
    ```

2. **Install Dependencies**:
    ```sh
    python -m pip install -r requirements.txt
    ```

3. **Install `llama_cpp`** (optional):
    Follow the instructions on the [llama_cpp GitHub repository](https://github.com/abetlen/llama-cpp-python) to install the `llama_cpp` library.

## Usage

### Sudoku Generator

To generate a Sudoku puzzle:
```python
from generator import SudokuGenerator

generator = SudokuGenerator(difficulty="hard")
sudoku_puzzle = generator.generate_sudoku()
generator.print_board(sudoku_puzzle)
```

### Sudoku Solver

To solve a Sudoku puzzle:
```python
from solver import TreeSearchSudokuSolver

solver = TreeSearchSudokuSolver(sudoku_puzzle)
solution = solver.solve_with_tot()
print("TreeSearch solution:", solution)
    
solver = BacktrackingSudokuSolver(sudoku_puzzle)
solution = solver.solve_with_tot()
solver.print_thoughts()  # Print reasoning process
print("Backtracking solution:\n", solution)
```

---

You could also solve a Sudoku Puzzle with an LLM:
- sudoku/config.py need to be filled with your configuration.
- use the the right chat-format, depending on your own model.
- example sudoku/llm_solver.py
```python
from config import MODEL_PATH
from llama_cpp import Llama

llm = Llama(
    MODEL_PATH,
    chat_format='chat-format',
    n_batch=4096,
    n_ctx=4096,
    max_tokens = 4096,
    verbose = False)

board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

solver = LlmSudokuSolver(board)
solution = solver.solve_with_tot()
print("\nFinal Solution:")
solver.print_board(solution) 
```

### Solution Checker

To validate a Sudoku solution:
```python
from check_solution import is_valid_solution

is_valid_solution(sudoku_puzzle, solution)
```

### GUI Interface

To run the GUI:
```sh
python sudoku_gui.py
```

## Example Usage

### Main Script

The `main.py` script demonstrates the complete workflow:
1. Generate a Sudoku puzzle.
2. Solve the puzzle.
3. Validate the solution.

```python
from generator import SudokuGenerator
from solver import TreeSearchSudokuSolver
from check_solution import is_valid_solution

generator = SudokuGenerator(difficulty="hard")
sudoku_puzzle = generator.generate_sudoku()
generator.print_board(sudoku_puzzle)

solver = TreeSearchSudokuSolver(sudoku_puzzle)
solution = solver.solve_with_tot()

solution_list = [list(map(int, row.split())) for row in solution.strip().split("\n")]
is_valid_solution(sudoku_puzzle, solution_list)
```
you could also make an .exe app of the playable gui by running the following command:
```bash
pyinstaller --onefile --windowed --add-data "sudoku\generator.py;." --name "SudokuGame" sudoku_gui.py
```

## Code Structure
### **1. TreeNode (Search Tree Representation)**
- Represents a Sudoku board state.
- Stores parent-child relationships for backtracking.

### **2. ToTController (Backtracking Manager)**
- Determines when backtracking is necessary.
- Stops execution if too many failed attempts occur.

### **3. SudokuSolver (Main Solver Class)**
- **find_empty_location()**: Locates the next empty cell.
- **prompt_llm()**: Requests a move from the LLM.
- **solve_with_tot()**: Main solving loop using LLM and backtracking.
- **apply_move()**: Applies and validates a move.
- **print_board()**: Displays the Sudoku board.

### **4. LLM Integration**
- Uses **Llama** to generate the best possible move.
- The model responds in a structured format: `(row, col, num)`.

### **5. Alternative Approaches**
- **TreeSearchSudokuSolver**: Uses a scoring system to prioritize moves.
- **BacktrackingSudokuSolver**: Implements classic recursive backtracking.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.


---
This project showcases the power of **Tree of Thoughts (ToT)** combined with **LLMs** for solving complex problems like Sudoku.