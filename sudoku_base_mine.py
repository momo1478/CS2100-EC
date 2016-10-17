from z3 import *
import sys

# Get input

# Solves the sudoku puzzle.
# n is the length of a sub-grid and puzzle is the provided puzzle
def solve_puzzle(n, puzzle):
  # Declare the grid for Z3
  grid = [[Int("X{0}_{1}".format(i, j)) for i in range(n*n)] for j in range(n*n)]

  # Create a solver instance for Z3
  s = Solver()

  # Add constraint that each cell is in [1,9]
  for i in range(n*n):
    for j in range(n*n):
      s.add(And(1 <= grid[i][j], grid[i][j] <= (n*n) ))

  # Add rule for rows having distinct values
  for r in range(n*n):
    s.add(Distinct([grid[r][c] for c in range(n*n)]))

  # Add rule for columns being distinct
  for c in range(n*n):
    s.add(Distinct([grid[r][c] for r in range(n*n)]))

  # Add rule for boxes being distinct
  for i in range(n):
    for j in range(n):
      s.add(Distinct([grid[r][c] for c in range(i*n, i*n+n) for r in range(j*n, j*n+n)]))

  # Give Z3 our puzzle
  for i in range(n*n):
    for j in range(n*n):
      # Skip if this is a blank square
      if puzzle[i][j] == ".":
        continue
      # Otherwise, add a constraint that this
      # square == the puzzle square
      s.add(grid[i][j] == puzzle[i][j])

  # Check if Z3 can solve the puzzle
  if s.check() == sat:
    # Get Z3's solution
    m = s.model()
    # Extract the solution into a python matrix
    solution = [[0 for i in range(n*n)] for j in range(n*n)]
    for i in range(n*n):
      for j in range(n*n):
        solution[i][j] = int(str(m.eval(grid[i][j])))

    # Print solution
    for i in range(n*n):
      row = ""
      for j in range(n*n):
        row = row + str(solution[i][j]) + " "
      print(row)

    # Check if solution is unique
    
    # Create constraint for one empty cell having a different value
    BigOr = []
    for i in range(n*n):
      for j in range(n*n):
        if puzzle[i][j] == ".": 
          BigOr.append(grid[i][j] != solution[i][j])

    s.add(Or(BigOr))
        
    # Check if s still has a solution
    if s.check() == sat:
      print("The solution is not unique")
    else:
      print("The solution is unique")
  else:
    print("No solution")

if __name__ == '__main__':
  if len(sys.argv) == 1:
    n = 3
    puzzle = [[8, ".", ".", ".", ".", ".", ".", ".", "."],
                [".", ".", 3, 6, ".", ".", ".", ".", "."],
                [".", 7, ".", ".", 9, ".", 2, ".", "."],
                [".", 5, ".", ".", ".", 7, ".", ".", "."],
                [".", ".", ".", ".", 4, 5, 7, ".", "."],
                [".", ".", ".", 1, ".", ".", ".", 3, "."],
                [".", ".", 1, ".", ".", ".", ".", 6, 8],
                [".",  ".", 8, 5, ".", ".", ".", 1, "."],
                [".", 9, ".", ".", ".", ".", 4, ".", "."]]

    solve_puzzle(n, puzzle)
  else:
    # grab data and get out
    with open(sys.argv[1]) as f:
      lines = [line.strip() for line in f]

    # remove empty lines
    lines = filter(lambda x: x != "", lines)

    # get dim
    n = int(lines[0])

    # split lines
    lines = [line.split() for line in lines[1:]]

    # cast ints
    for i in range(len(lines)):
      lines[i] = map(lambda x: x if x=='.' else int(x), lines[i])

    # call solver
    solve_puzzle(n, lines)
    
