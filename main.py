
from sudoku.generator import SudokuGenerator
from sudoku.solver import TreeSearchSudokuSolver
from sudoku.check_solution import is_valid_solution
import os
import platform 

if platform.system() == "Windows":
    os.environ["ANSI_COLORS_DISABLED"] = "1"



generator = SudokuGenerator(difficulty="hard")
sudoku_puzzle = generator.generate_sudoku()
generator.print_board()
generator.solution_board()
print()




solver = TreeSearchSudokuSolver(sudoku_puzzle)
solution = solver.solve_with_tot()
#solver.print_thoughts()  # Print reasoning process
print("TreeSearch solution:\n", solution)



# Convert to list of lists
solution_list = [list(map(int, row.split())) for row in solution.strip().split("\n")]
# Run the checker
is_valid_solution(sudoku_puzzle, solution_list)