# A sudoku solver for a LeetCode challenge. 
# Written by Kane Xie in 2022. 

# Quite inefficient, but I wanted to use the Wave Function Collapse Algorithm,
# where each cell is set up as a superposition of possibilities and then collapsed. 

class Solution(object):

    def solveSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: None Do not return anything, modify board in-place instead.
        """
        # Set up the save field as a history of boards.
        self.save = [board]

        # The log field is a history of how a set of possibilities was collapsed.
        self.log = []
        
        self.solve(board)
        
        # Copy over the solution to the original board.
        for i in range(len(board[0])):
            for j in range(len(board)):
                board[i][j] = self.save[-1][i][j]


    def solve(self, board):
        """Solves the sudoku board by adding iterations to the save field."""
        alphabet = {'1','2','3','4','5','6','7','8','9'}
        while not self.checkFinished(board):
            shortest = ('123456789', ())
            changed = False
            for i in range(len(board[0])):
                for j in range(len(board)):
                    # Check if a cell is not certain yet.
                    if board[i][j] not in alphabet:
                        # Look for the smallest possibility.
                        if len(board[i][j]) < len(shortest[0]) and len(board[i][j]) > 1:
                            shortest = (board[i][j], (i, j))

                        # Remove possibilities for this cell. This is not perfect, but is good enough for the recursive wave function collapse to work. 
                        stuffs = set(alphabet)
                        stuffs -= set(board[i])
                        stuffs -= set([x[j] for x in board])
                        
                        square = sum([[board[x][y] for y in range((j//3)*3, (j//3)*3+3)] for x in range((i//3)*3, (i//3)*3+3)], [])
                        stuffs -= set(square)
                        
                        if len(stuffs) == 1:
                            changed = True
                            board[i][j] = list(stuffs)[0]
                        elif not stuffs:
                            return False
                        else:
                            board[i][j] = ''.join(stuffs)

            # If the board was not changed in the last iteration, the next step requires a guess. 
            # This is done recursively by solving each possibility. If none of its children can be solved, 
            # the function moves on to the next possibility. 
            if not changed:
                self.log.append(shortest)

                for p in self.log[-1][0]:
                    self.save.append([r[:] for r in self.save[-1]])
                    i, j = self.log[-1][1]
                    self.save[-1][i][j] = p

                    if self.solve(self.save[-1]):
                        return True
                    else:
                        self.save.pop()
                self.log.pop()
                return False
        return True

    def checkFinished(self, board):
        'Check if the board is complete'
        for i in range(len(board[0])):
            for j in range(len(board)):
                if board[i][j] not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    return False
        return True