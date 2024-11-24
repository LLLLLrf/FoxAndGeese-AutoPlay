import random

class Player:
    def print_board(self, board):
        print('')
        print('  0 1 2 3 4 5 6')
        for i in range(len(board)):
            txt = str(i) + ' '
            for j in range(len(board[i])):
                txt += board[i][j] + " "
            print(txt)
        print('')

    # -------------------------------------------------
    # Fox plays next
    def play_fox(self, board):
        self.print_board(board)

        # Find the fox's position
        fox_pos = None
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 'F':
                    fox_pos = [i, j]
                    break

        # Get all valid moves
        potential_moves = [
            [fox_pos[0] + dr, fox_pos[1] + dc]
            for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        ]

        valid_moves = [move for move in potential_moves if self.is_valid_fox_move(board, fox_pos, move)]

        if not valid_moves:
            print("Fox has no valid moves!")
            return [fox_pos]  # Return current position

        # Prioritize progressive moves or random if all are equivalent
        chosen_move = random.choice(valid_moves)
        print(f"Fox moves from {fox_pos} to {chosen_move}")
        return [fox_pos, chosen_move]

    @staticmethod
    def is_valid_fox_move(board, start, end):
        """
        Validates whether a fox's move from start to end is legal.
        """
        # Ensure the end position is within bounds
        if not (0 <= end[0] < len(board) and 0 <= end[1] < len(board[0])):
            return False

        # Check if the end position is empty
        if board[end[0]][end[1]] != '.':
            return False

        # Check if the move is diagonal and within one step
        row_diff = abs(end[0] - start[0])
        col_diff = abs(end[1] - start[1])
        if row_diff == 1 and col_diff == 1:
            return True  # Valid diagonal move

        return False  # Any other move is illegal



    # -------------------------------------------------
    # Goose plays next
    def play_goose(self, board):
        self.print_board(board)

        # Get all geese positions
        geese_positions = []
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 'G':
                    geese_positions.append([i, j])

        # Try to block the fox or form a wall
        fox_pos = None
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 'F':
                    fox_pos = [i, j]
                    break

        for goose_pos in geese_positions:
            valid_moves = self.get_valid_moves(board, goose_pos, is_fox=False)
            for move in valid_moves:
                if abs(move[0] - fox_pos[0]) <= 1 and abs(move[1] - fox_pos[1]) <= 1:
                    print(f"Goose moves to block the fox!")
                    return [goose_pos, move]

        # If no blocking move is possible, pick a random valid move
        random_goose = random.choice(geese_positions)
        random_move = random.choice(self.get_valid_moves(board, random_goose, is_fox=False))
        return [random_goose, random_move]

    # -------------------------------------------------
    # # Get valid moves for a piece
    def get_valid_moves(self, board, pos, is_fox):
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # Orthogonal moves
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal moves
        ] if is_fox else [
            (-1, 0), (1, 0), (0, -1), (0, 1)  # Geese only move orthogonally
        ]

        valid_moves = []
        for d in directions:
            new_pos = [pos[0] + d[0], pos[1] + d[1]]
            if 0 <= new_pos[0] < len(board) and 0 <= new_pos[1] < len(board[0]) and board[new_pos[0]][new_pos[1]] == '.':
                valid_moves.append(new_pos)
        return valid_moves

    # -------------------------------------------------
    # Check if a move is a capture move
    def is_capture_move(self, board, from_pos, to_pos):
        mid_pos = [(from_pos[0] + to_pos[0]) // 2, (from_pos[1] + to_pos[1]) // 2]
        return board[mid_pos[0]][mid_pos[1]] == 'G'

    # -------------------------------------------------
    # Simulate a move on the board
    def simulate_move(self, board, from_pos, to_pos):
        new_board = [row[:] for row in board]
        new_board[to_pos[0]][to_pos[1]] = new_board[from_pos[0]][from_pos[1]]
        new_board[from_pos[0]][from_pos[1]] = '.'
        return new_board
