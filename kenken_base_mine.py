from z3 import *
import sys

def tryCastInt(val):
  try:
    return int(val)
  except ValueError:
    return val


# Get input

# Solves the sudoku puzzle.
# n is the length of a sub-grid and puzzle is the provided puzzle
def solve_puzzle(n, puzzle):
  # Declare the grid for Z3
  grid = [[Int("X{0}_{1}".format(i, j)) for i in range(n)] for j in range(n)]

  # Create a solver instance for Z3
  s = Solver()

  # Add constraint that each cell is in [1,9]
  for i in range(n):
    for j in range(n):
      s.add(And(1 <= grid[i][j], grid[i][j] <= (n) ))

  # Add rule for rows having distinct values
  for r in range(n):
    s.add(Distinct([grid[r][c] for c in range(n)]))

  # Add rule for columns being distinct
  for c in range(n):
    s.add(Distinct([grid[r][c] for r in range(n)]))

  #Add operation constraints
  #For each "grid rule"
  for i in range (0,len(puzzle)):
    tempArr = []
    if puzzle[i][1] == "+":
      for o in range (1 , len(puzzle[i])/2):
        tempArr.append( grid[ puzzle[i][2*o] ][ puzzle[i][2*o + 1] ])
      s.add( Sum( tempArr ) == puzzle[i][0] )
    elif puzzle[i][1] == "*":
      for o in range (1 , len(puzzle[i])/2):
        tempArr.append( grid[ puzzle[i][2*o] ][ puzzle[i][2*o + 1] ])
      s.add( Product( tempArr ) == puzzle[i][0] )
    elif puzzle[i][1] == "/":
      s.add( Or( grid[ puzzle[i][2] ][ puzzle[i][3] ] / grid[ puzzle[i][4] ][ puzzle[i][5] ] == puzzle[i][0] ,
                 grid[ puzzle[i][4] ][ puzzle[i][5] ] / grid[ puzzle[i][2] ][ puzzle[i][3] ] == puzzle[i][0]) )
    elif puzzle[i][1] == "-":
      s.add( Or( grid[ puzzle[i][2] ][ puzzle[i][3] ] - grid[ puzzle[i][4] ][ puzzle[i][5] ] == puzzle[i][0] ,
                 grid[ puzzle[i][4] ][ puzzle[i][5] ] - grid[ puzzle[i][2] ][ puzzle[i][3] ] == puzzle[i][0]) )
    elif puzzle[i][1] == "g":
      s.add( grid[ puzzle[i][2] ][ puzzle [i][3] ] == puzzle[i][0] )

  # Give Z3 our puzzle
  for i in range(n):
    for j in range(n):
      # Skip if this is a blank square
      if puzzle[i][j] == ".":
        continue
      # Otherwise, add a constraint that this
      # square == the puzzle square
      # s.add( grid[i][j] == puzzle[i][j] )

  # Check if Z3 can solve the puzzle
  if s.check() == sat:
    # Get Z3's solution
    m = s.model()
    # Extract the solution into a python matrix
    solution = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
      for j in range(n):
        solution[i][j] = int(str(m.eval(grid[i][j])))

    # Print solution
    for i in range(n):
      row = ""
      for j in range(n):
        row = row + str(solution[i][j]) + " "
      print(row)
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
      lines[i] = map(lambda x: x if x=='.' else tryCastInt(x), lines[i])

    # call solver
    solve_puzzle(n, lines)
    
