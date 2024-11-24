# Fox and Geese manual play example
# JC4004 Computational Intelligence 2024-25


class Player:
  
  # =================================================
  # Print the board
  def print_board(self,board):

    # Prints the current board
    print('')
    print('  0 1 2 3 4 5 6')
    for i in range(len(board)):
      txt = str(i) + ' '
      for j in range(len(board[i])):
        txt += board[i][j] + " "
      print(txt)
    print('')

  # =================================================
  # Play one move as a fox
  def play_fox(self, board):

    # First, print the current board
    self.print_board(board)

    # Find where the fox is
    fox_pos = [0,0]
    for i in range(len(board)):
      for j in range(len(board[i])):
        if board[i][j] == 'F':
          fox_pos = [i,j]
          break

    move = [fox_pos]

    # Get player input for new fox position
    cont = True
    print("Fox plays next!")
    print("Fox is in position (" + str(fox_pos[0]) + "," + str(fox_pos[1]) + ")")
    while cont:      
      new_pos = [int(i) for i in input("Give the new position for the fox (row,column): ").split(',')]
      move.append(new_pos)
      if abs(move[-1][0]-move[-2][0]) > 1 or abs(move[-1][1]-move[-2][1]) > 1:
        inp = input("Do you want to make another move [y/N]? ")
        if inp != 'y' and inp != 'Y':
          cont = False
      else:
        cont = False

    print(move)

    return move

  # =================================================
  # Play one move as a goose
  def play_goose(self, board):

    # First, print the current board
    self.print_board(board)

    # Get goose start position
    print("Goose plays next!")
    goose_pos = [int(i) for i in input("Give the position of the goose to move (row,column): ").split(',')]

    move = [goose_pos]

    # Get player input for goose next position
    new_pos = [int(i) for i in input("Give the new position (row,column): ").split(',')]
    move.append(new_pos)

    print(move)

    return move

# ==== End of file