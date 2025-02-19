from termcolor import colored

def is_valid_solution(board, solution):
    def is_valid_group(group):
        return sorted(group) == list(range(1, 10))  # Must contain 1-9 exactly once

    errors = []  # Store errors
    error_positions = set()  # Track incorrect cells

    # Check rows & columns
    for i in range(9):
        if not is_valid_group(solution[i]):
            errors.append(f"❌ Row {i+1} is invalid: {solution[i]}")
            for j in range(9):
                error_positions.add((i, j))

        col = [solution[j][i] for j in range(9)]
        if not is_valid_group(col):
            errors.append(f"❌ Column {i+1} is invalid: {col}")
            for j in range(9):
                error_positions.add((j, i))

    # Check 3x3 subgrids
    for box_row in range(3):
        for box_col in range(3):
            subgrid = []
            subgrid_positions = []
            for r in range(3):
                for c in range(3):
                    row, col = box_row * 3 + r, box_col * 3 + c
                    subgrid.append(solution[row][col])
                    subgrid_positions.append((row, col))
            if not is_valid_group(subgrid):
                errors.append(f"❌ Subgrid ({box_row+1},{box_col+1}) is invalid: {subgrid}")
                error_positions.update(subgrid_positions)

    # Check pre-filled numbers
    for r in range(9):
        for c in range(9):
            if board[r][c] != 0 and board[r][c] != solution[r][c]:
                errors.append(f"❌ Mismatch at ({r+1},{c+1}): Expected {board[r][c]}, found {solution[r][c]}")
                error_positions.add((r, c))

    # Print board with errors highlighted
    print("\n🔹 Sudoku Solution Check 🔹")
    for r in range(9):
        """if r % 3 == 0 and r != 0:
            print("-" * 21)  # Horizontal separator for 3x3 grids"""
        for c in range(9):
            num = solution[r][c]
            if (r, c) in error_positions:
                print(colored(f"{num}", "red"), end=" ")  # Print errors in red
                #print(f"{num}",)
            else:
                print(num, end=" ")
            """if c % 3 == 2 and c != 8:
                print("|", end=" ")  # Vertical separator for 3x3 grids"""
        print()  # New line for next row

    if errors:
        print("\n".join(errors))
        print("❌ The solution is incorrect.")
        return False

    print("✅ The solution is correct!")
    return True




if __name__ == '__main__':
    import os
    import platform 

    if platform.system() == "Windows":
        os.environ["ANSI_COLORS_DISABLED"] = "1"
    # Example Sudoku Board
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

    # Test with an incorrect solution
    solution_wrong = [
        [9, 3, 4, 6, 7, 8, 9, 1, 2],  # Mistake: First element should be 5
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]
    ]

    # Convert to list of lists
    #solution_list = [list(map(int, row.split())) for row in solution.strip().split("\n")]


    # Run the checker
    is_valid_solution(board, solution_wrong)
    
    
    
        