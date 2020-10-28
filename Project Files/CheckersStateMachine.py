import turtle
import numpy

# Methods are in alphabetical order. main() is at the bottom.

class myWindow():

    def __init__(self):
        # define all global variables
        # after spending some time passing objects around I decided to convert most of them to global variables
        # this made the code much less complex.

        global ROW_COUNT
        global COLUMN_COUNT
        global TILE_SIZE
        global GAME_BOARD
        global STATE
        global MATRIX_COLUMN_COORD
        global MATRIX_ROW_COORD
        global OWN_ROW
        global OWN_COLUMN
        global TARGET_ROW
        global TARGET_COLUMN
        global TOTAL_TURNS
        global PLAYER_TURNS
        global PC_TURNS
        global NUM_PLAYER_PIECES
        global NUM_PC_PIECES
        global CAPTURED

        ROW_COUNT = 8
        COLUMN_COUNT = 8
        TILE_SIZE = 100

        #create a 8x8 matrix. See method for detail.
        GAME_BOARD = self.createBoard()

        STATE = 0 # tracks the current state of the game. See advanceStateMachine() for detail
        MATRIX_COLUMN_COORD = 0 # these are used to store input from the player
        MATRIX_ROW_COORD = 0

        OWN_ROW = 0 # after the input has been recieved, it is copied to these variables for later use
        OWN_COLUMN = 0
        TARGET_ROW = 0
        TARGET_COLUMN = 0

        TOTAL_TURNS = 0 # dunno if we need these? I included them here but they don't get incremented. Must check the spec.
        PLAYER_TURNS = 0
        PC_TURNS = 0

        NUM_PLAYER_PIECES = 12
        NUM_PC_PIECES = 12

        CAPTURED = False

        self.main()

    def advanceStateMachine(self, mouseX, mouseY):

        # High level Overview: this method is called every time the screen is clicked.
        # It is used to advance the state of the game.
        # in STATE 0, it gets the player to select a piece.
        # in STATE 1, it gets the player to select a target.
        # in STATE 2 and STATE 3, it gets the pc (player 2) to select a piece and then a target.

        global GAME_BOARD
        global MATRIX_COLUMN_COORD
        global MATRIX_ROW_COORD
        global OWN_ROW
        global OWN_COLUMN
        global TARGET_ROW
        global TARGET_COLUMN
        global STATE
        global CAPTURED
        global NUM_PLAYER_PIECES
        global NUM_PC_PIECES

        CAPTURED = False

        self.drawBoard()
        self.countPieces()
        print("Player pieces remaining: ", NUM_PLAYER_PIECES)
        print("PC pieces remaining:     ", NUM_PC_PIECES)

        # our intention was to update the game panel every time either player made a move.
        # game_panel.GamePanel().redrawUI()

        if STATE == 0:
            self.printBoard()
            print("STATE 0")

            self.clearHighlight()
            self.drawBoard()
            self.getMatrixCoord(mouseX, mouseY)

            if self.validPiece(2) or self.validPiece(4):
                print("Valid piece selected: ", MATRIX_ROW_COORD, MATRIX_COLUMN_COORD)

                # highlight the selected piece
                if GAME_BOARD[MATRIX_ROW_COORD][MATRIX_COLUMN_COORD] == 2:
                    GAME_BOARD[MATRIX_ROW_COORD][MATRIX_COLUMN_COORD] = 6
                elif GAME_BOARD[MATRIX_ROW_COORD][MATRIX_COLUMN_COORD] == 4:
                    GAME_BOARD[MATRIX_ROW_COORD][MATRIX_COLUMN_COORD] = 8
                    self.drawBoard() #update the board to show the highlighted piece

                # now we check if the selected piece can capture or move. If either statement validates, the game will save the choice made and proceed to STATE 1
                if self.playerCaptureAvailable():
                    print("Capture available")

                    OWN_ROW = MATRIX_ROW_COORD
                    OWN_COLUMN = MATRIX_COLUMN_COORD

                    STATE = 1 # update the state variable, so that when the player clicks, the game will proceed
                else:
                    print("That piece cannot capture")

                if self.movesAvailable():
                    print("Moves available")

                    OWN_ROW = MATRIX_ROW_COORD
                    OWN_COLUMN = MATRIX_COLUMN_COORD

                    STATE = 1 # update the state variable, so that when the player clicks, the game will proceed
                else:
                    print("That piece cannot move to an adjacent empty tile")

                # update the screen
                self.promotePieces()
                self.drawBoard()
            else:
                print("Invalid choice. Please select a red piece with an available move")

        elif STATE == 1:

            print("Please select a tile to move to: ")  # prompt the player to proceed
            #wait for the player to choose a target
            self.getMatrixCoord(mouseX, mouseY)

            print("\nSTATE 1")
            print("Target selected: ", MATRIX_ROW_COORD, MATRIX_COLUMN_COORD)

            # save the choice of target tile
            TARGET_ROW = MATRIX_ROW_COORD
            TARGET_COLUMN = MATRIX_COLUMN_COORD

            if self.movePiece():
                print("\nmove completed: ")
                print("From:  OWN_ROW: ", OWN_ROW, "   OWN_COLUMN: ", OWN_COLUMN)
                print("To: TARGET_ROW: ", TARGET_ROW, "TARGET_COLUMN: ", TARGET_COLUMN)
                #printBoard() # print the board to the terminal (debug command)
                self.clearHighlight()
                self.drawBoard() # update the mainWindow by calling drawBoard()

                if CAPTURED == True and self.playerCaptureAvailable():
                    CAPTURED = False

                    self.drawBoard()
                    STATE = 1

                    OWN_ROW = TARGET_ROW
                    OWN_COLUMN = TARGET_COLUMN

                    print("Player 1, please select a new target: ")
                else:
                    STATE = 2 # allow the game to proceed
            else:
                print("movePiece == False")

            # update the screen
            self.countPieces()
            self.clearHighlight()
            self.promotePieces()
            self.drawBoard()
            self.printBoard() # print the board to the terminal.

        elif STATE == 2:
            #STATE 2 and STATE 3 are the same as STATE 0 and STATE 1, but are used for the pc/player 2.
            print("STATE 2")

            self.clearHighlight()
            self.drawBoard()
            self.getMatrixCoord(mouseX, mouseY)

            if self.validPiece(3) or self.validPiece(5):  # if the chosen piece owned by the pc
                print("Valid piece selected: ", MATRIX_ROW_COORD, MATRIX_COLUMN_COORD)

                # highlighting
                if GAME_BOARD[MATRIX_ROW_COORD][MATRIX_COLUMN_COORD] == 3:
                    GAME_BOARD[MATRIX_ROW_COORD][MATRIX_COLUMN_COORD] = 7
                elif GAME_BOARD[MATRIX_ROW_COORD][MATRIX_COLUMN_COORD] == 5:
                    GAME_BOARD[MATRIX_ROW_COORD][MATRIX_COLUMN_COORD] = 9
                self.drawBoard()

                if self.pcCaptureAvailable():
                    print("Captures available")

                    # save the pcs choice
                    OWN_ROW = MATRIX_ROW_COORD
                    OWN_COLUMN = MATRIX_COLUMN_COORD

                    STATE = 3
                else:
                    print("That piece cannot capture")

                if self.movesAvailable():
                    print("Moves available")

                    # save the pcs choice
                    OWN_ROW = MATRIX_ROW_COORD
                    OWN_COLUMN = MATRIX_COLUMN_COORD

                    STATE = 3
                else:
                    print("That piece cannot move to an adjacent empty tile")

                self.promotePieces()
                self.drawBoard()
            else:
                print("Invalid choice. Please select a blue piece with an available move")

        elif STATE == 3:
            print("Please select a tile to move to: ")

            self.getMatrixCoord(mouseX, mouseY)
            print("\nSTATE 3")
            print("Target selected: ", MATRIX_ROW_COORD, MATRIX_COLUMN_COORD)

            # save the choice of target tile
            TARGET_ROW = MATRIX_ROW_COORD
            TARGET_COLUMN = MATRIX_COLUMN_COORD

            CAPTURED = False
            if self.movePiece():
                print("\nmove completed: ")
                print("From:  OWN_ROW: ", OWN_ROW, "   OWN_COLUMN: ", OWN_COLUMN)
                print("To: TARGET_ROW: ", TARGET_ROW, "TARGET_COLUMN: ", TARGET_COLUMN)

                #printBoard() # print the board to the terminal (debug command)
                self.clearHighlight()
                self.promotePieces()
                self.drawBoard() # update the board

                if CAPTURED == True and self.pcCaptureAvailable():
                    CAPTURED = False

                    self.drawBoard()

                    STATE = 3

                    OWN_ROW = TARGET_ROW
                    OWN_COLUMN = TARGET_COLUMN

                    print("Player 2, please select a new target: ")
                else:
                    STATE = 0 # allow the game to proceed
            self.countPieces()

    def clearHighlight(self):

        # high level overview: This method iterates over the board and sets any highlighted pieces back to their default values, per the table below.

        global GAME_BOARD

        # default piece values:
        # 0 = white tile
        # 1 = gray/black tile
        # 2 = player piece
        # 3 = pc piece
        # 4 = player king
        # 5 = pc king

        # highlighted piece values and correct default value
        # 6 = player_highlighted -> 2
        # 7 = pc_highlighted -> 3
        # 8 = playerKing_highlighted -> 4
        # 9 = pcKing_highlighted -> 5
        # 10 = blackTile_highlighted -> 1

        for r in range(0,8):
            for c in range(0,8):
                if GAME_BOARD[r][c] == 10:
                    GAME_BOARD[r][c] = 1
                if GAME_BOARD[r][c] == 9:
                    GAME_BOARD[r][c] = 5
                if GAME_BOARD[r][c] == 8:
                    GAME_BOARD[r][c] = 4
                if GAME_BOARD[r][c] == 7:
                    GAME_BOARD[r][c] = 3
                if GAME_BOARD[r][c] == 6:
                    GAME_BOARD[r][c] = 2

    def convertPieceToActualValue(self, piece):

        # High level overview:
        # this method is used to convert highlighted pieces into standard pieces.
        # unlike clearHighlight(), this method returns a value/piece, and does not update the board.

        # piece key:
        # 0 = white tile
        # 1 = gray/black tile
        # 2 = player piece
        # 3 = pc piece
        # 4 = player king
        # 5 = pc king
        # 6 = player_highlighted -> 2
        # 7 = pc_highlighted -> 3
        # 8 = playerKing_highlighted -> 4
        # 9 = pcKing_highlighted -> 5
        # 10 = blackTile_highlighted

        if piece == 9:
            piece = 5
        elif piece == 8:
            piece = 4
        elif piece == 7:
            piece = 3
        elif piece == 6:
            piece = 2

        return piece

    def countPieces(self):

        #High level overview: This method iterates over the game board and counts the number of pieces each player has in play

        global GAME_BOARD
        global NUM_PLAYER_PIECES
        global NUM_PC_PIECES

        NUM_PLAYER_PIECES = 0
        NUM_PC_PIECES = 0

        for r in range(0,8):
            for c in range(0,8):
                if GAME_BOARD[r][c] == 2 or GAME_BOARD[r][c] == 4:
                    NUM_PLAYER_PIECES = NUM_PLAYER_PIECES + 1
                elif GAME_BOARD[r][c] == 3 or GAME_BOARD[r][c] == 5:
                    NUM_PC_PIECES = NUM_PC_PIECES + 1

    def createBoard(self): # creates a game board using an 8x8 matrix
        global ROW_COUNT
        global COLUMN_COUNT

        board = numpy.zeros((ROW_COUNT, COLUMN_COUNT))  # .zeros() sets everything in the matrix to zero

        # piece key:
        # 0 = white tile
        # 1 = gray/black tile
        # 2 = player piece
        # 3 = pc piece
        # 4 = player king
        # 5 = pc king
        # 6 = player_highlighted
        # 7 = pc_highlighted
        # 8 = playerKing_highlighted
        # 9 = pcKing_highlighted
        # 10 = blackTile_highlighted

        # Resulting board/matrix:
        # 0, 0, 0, 0, 0, 0, 0, 0
        # 0, 0, 0, 0, 0, 0, 0, 0
        # 0, 0, 0, 0, 0, 0, 0, 0
        # 0, 0, 0, 0, 0, 0, 0, 0
        # 0, 0, 0, 0, 0, 0, 0, 0
        # 0, 0, 0, 0, 0, 0, 0, 0
        # 0, 0, 0, 0, 0, 0, 0, 0
        # 0, 0, 0, 0, 0, 0, 0, 0

        # tile the board. 1 = white tile, 2 = black tile
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT):
                if r % 2 == 0:
                    if c % 2 != 0:
                        board[r][c] = 1
                else:  # if row % 2 != 0:
                    if c % 2 == 0:
                        board[r][c] = 1

        # Resulting board/matrix:
        # 0, 1, 0, 1, 0, 1, 0, 1
        # 1, 0, 1, 0, 1, 0, 1, 0
        # 0, 1, 0, 1, 0, 1, 0, 1
        # 1, 0, 1, 0, 1, 0, 1, 0
        # 0, 1, 0, 1, 0, 1, 0, 1
        # 1, 0, 1, 0, 1, 0, 1, 0
        # 0, 1, 0, 1, 0, 1, 0, 1
        # 1, 0, 1, 0, 1, 0, 1, 0


        # add player pieces to the board. 2 = player piece
        for r in range(5, ROW_COUNT):
            for c in range(COLUMN_COUNT):
                if board[r][c] == 1:
                    board[r][c] = 2

        # Resulting board/matrix:
        # 0, 1, 0, 1, 0, 1, 0, 1
        # 1, 0, 1, 0, 1, 0, 1, 0
        # 0, 1, 0, 1, 0, 1, 0, 1
        # 1, 0, 1, 0, 1, 0, 1, 0
        # 0, 1, 0, 1, 0, 1, 0, 1
        # 2, 0, 2, 0, 2, 0, 2, 0 # player pieces are here
        # 0, 2, 0, 2, 0, 2, 0, 2 #
        # 2, 0, 2, 0, 2, 0, 2, 0 #

        # add PC pieces to the board
        for r in range(ROW_COUNT - 5):
            for c in range(COLUMN_COUNT):
                if board[r][c] == 1:
                    board[r][c] = 3

        # Final board/matrix:
        # 0, 3, 0, 3, 0, 3, 0, 3 # pc pieces are here
        # 3, 0, 3, 0, 3, 0, 3, 0 #
        # 0, 3, 0, 3, 0, 3, 0, 3 #
        # 1, 0, 1, 0, 1, 0, 1, 0
        # 0, 1, 0, 1, 0, 1, 0, 1
        # 2, 0, 2, 0, 2, 0, 2, 0
        # 0, 2, 0, 2, 0, 2, 0, 2
        # 2, 0, 2, 0, 2, 0, 2, 0

        #misc board layout commands for debugging
        """#immediate capture testing for both sides
        board[4][1] = 4
        board[4][3] = 2
        board[4][5] = 4
        board[4][7] = 2
        
        board[3][0] = 3
        board[3][2] = 3
        board[3][4] = 3
        board[3][6] = 3"""

        """board[2][1] = 2
        board[2][3] = 2
        board[2][5] = 2
        board[2][7] = 4
    
        board[7][0] = 5
        board[7][2] = 5
        board[7][4] = 5
        board[7][6] = 5
    
        board[0][1] = 4"""

        """#move and capture testing for both sides
        board[2][1] = 3
        board[2][3] = 3
        board[2][5] = 3
        board[2][7] = 3
    
        board[4][1] = 2
        board[4][3] = 2
        board[4][5] = 2
        board[4][7] = 2
        board[7][6] = 2"""

        """# chain capture test, red vs blue
        board[7][0] = 2
        board[6][1] = 3
        board[4][3] = 3
        board[4][1] = 3
        board[2][5] = 3
        board[0][7] = 3"""

        """# chain capture test, blue vs red
        board[0][7] = 3
        board[1][6] = 2
        board[3][4] = 2
        board[3][6] = 2
        board[5][2] = 2
        board[7][0] = 2
        board[7][6] = 2 #cause red goes first"""

        return board

    def drawBoard(self):
        #draws the board to the screen.

        global GAME_BOARD

        pen = turtle.Turtle() # create a new turtle
        #pen.hideturtle()  # for debugging. hides the turtle head.
        #pen.speed(10) #for debugging. Remember to comment out tracer in main while using this.

        pen.color("black")

        # the window coordinates work as follows for an 800x800 window:
        #
        #          +400y
        #            |
        #            |
        # -400x ----------- +400x
        #            |
        #            |
        #          -400y

        # therefore, we define the starting coordinates for the pen as the top left corner of the screen as follows:
        xCoord = -400
        yCoord = 400

        pen.penup() # take the pen off the canvas while it is moved to the start position to avoid drawing extra lines.
        pen.setposition(xCoord, yCoord) # move the pen to the start position

        # piece key:
        # 0 = white tile
        # 1 = gray/black tile
        # 2 = player piece
        # 3 = pc piece
        # 4 = player king
        # 5 = pc king
        # 6 = player_highlighted
        # 7 = pc_highlighted
        # 8 = playerKing_highlighted
        # 9 = pcKing_highlighted
        # 10 = blackTile_highlighted

        # for loop works as follows:
        # loop through each position in the matrix
        # read in the value at that position
        # draw the appropriate tile, and increment the x and y coords as appropriate
        for r in range(0,8):
            for c in range(0,8):
                if GAME_BOARD[r][c] == 0: # white tile
                    pen.penup()
                    pen.setposition(xCoord + c*100, yCoord - r*100)
                    self.paintTile_white(pen)
                if GAME_BOARD[r][c] == 1: # gray tile
                    pen.penup()
                    pen.setposition(xCoord + c * 100, yCoord - r * 100)
                    self.paintTile_black(pen)
                if GAME_BOARD[r][c] == 2: # player tile (red)
                    pen.penup()
                    pen.setposition(xCoord + c * 100, yCoord - r * 100)
                    self.paintTile_playerSoldier(pen)
                if GAME_BOARD[r][c] == 3: # pc tile (blue)
                    pen.penup()
                    pen.setposition(xCoord + c * 100, yCoord - r * 100)
                    self.paintTile_pcSoldier(pen)
                if GAME_BOARD[r][c] == 4: # player king (red and gold)
                    pen.penup()
                    pen.setposition(xCoord + c * 100, yCoord - r * 100)
                    self.paintTile_playerKing(pen)
                if GAME_BOARD[r][c] == 5: # pc king (blue and gold)
                    pen.penup()
                    pen.setposition(xCoord + c * 100, yCoord - r * 100)
                    self.paintTile_pcKing(pen)
                if GAME_BOARD[r][c] == 6: # player soldier, highlighted
                    pen.penup()
                    pen.setposition(xCoord + c * 100, yCoord - r * 100)
                    self.paintTile_playerSoldier_highlighted(pen)
                if GAME_BOARD[r][c] == 7:  # pc soldier, highlighted
                    pen.penup()
                    pen.setposition(xCoord + c * 100, yCoord - r * 100)
                    self.paintTile_pcSoldier_highlighted(pen)
                if GAME_BOARD[r][c] == 8:  # player king, highlighted
                    pen.penup()
                    pen.setposition(xCoord + c * 100, yCoord - r * 100)
                    self.paintTile_playerKing_highlighted(pen)
                if GAME_BOARD[r][c] == 9:  # pc king, highlighted
                    pen.penup()
                    pen.setposition(xCoord + c * 100, yCoord - r * 100)
                    self.paintTile_pcKing_highlighted(pen)
                if GAME_BOARD[r][c] == 10: # black/gray tile, highlighted
                    pen.penup()
                    pen.setposition(xCoord + c * 100, yCoord - r * 100)
                    self.paintTile_black_highlighted(pen)

    def getMatrixCoord(self, turtleX, turtleY):
        #print(turtleX, turtleY)

        # high level overview:
        # this method converts mouse click on the turtle screen to coordinates in the gameboard/matrix.
        # To simplify the conversion logic, the turtle x and y coordinates are increased by 400.
        # Turtle coordinates range from -400 to +400, left to right, and 400 to -400, top to bottom.
        # After incrementing the raw coordinates, the scale goes from 0 to 800, and 800 to 0, respectively.
        #
        # Clicks on tile borders and clicks which are out of bounds are also dealt with at the end of the method

        # before:
        #         +400
        #           |
        #           |
        # -400 ---------- +400
        #           |
        #           |
        #         -400

        # after:
        #
        #       0
        #       |
        #       |
        # 0 ---------- 800
        #       |
        #       |
        #      800


        global MATRIX_COLUMN_COORD
        global MATRIX_ROW_COORD

        turtleX = turtleX + 400
        turtleY = turtleY + 400

        # x coordinate conversion
        if turtleX > 0 and turtleX < 100:
            MATRIX_COLUMN_COORD = 0
        elif turtleX > 100 and turtleX < 200:
            MATRIX_COLUMN_COORD = 1
        elif turtleX > 200 and turtleX < 300:
            MATRIX_COLUMN_COORD = 2
        elif turtleX > 300 and turtleX < 400:
            MATRIX_COLUMN_COORD = 3
        elif turtleX > 400 and turtleX < 500:
            MATRIX_COLUMN_COORD = 4
        elif turtleX > 500 and turtleX < 600:
            MATRIX_COLUMN_COORD = 5
        elif turtleX > 600 and turtleX < 700:
            MATRIX_COLUMN_COORD = 6
        elif turtleX > 700 and turtleX < 800:
            MATRIX_COLUMN_COORD = 7

        #y coordinate conversion
        if turtleY < 800 and turtleY > 700:
            MATRIX_ROW_COORD = 0
        elif turtleY < 700 and turtleY > 600:
            MATRIX_ROW_COORD = 1
        elif turtleY < 600 and turtleY > 500:
            MATRIX_ROW_COORD = 2
        elif turtleY < 500 and turtleY > 400:
            MATRIX_ROW_COORD = 3
        elif turtleY < 400 and turtleY > 300:
            MATRIX_ROW_COORD = 4
        elif turtleY < 300 and turtleY > 200:
            MATRIX_ROW_COORD = 5
        elif turtleY < 200 and turtleY > 100:
            MATRIX_ROW_COORD = 6
        elif turtleY < 100 and turtleY > 0:
            MATRIX_ROW_COORD = 7

        # these two if statements account for edge cases, and out of bounds clicks.
        # since white tiles are never interacted with, setting the coordinates of these clicks to 0,0
        # renders them invalid (i.e. prevents them from being interpreted by the state machine)
        if (turtleX < 0 or turtleX > 800) or (turtleY > 800 or turtleY < 0):
            MATRIX_COLUMN_COORD = 0
            MATRIX_ROW_COORD = 0

        if turtleX % 100 == 0 or turtleY % 100 == 0:
            MATRIX_COLUMN_COORD = 0
            MATRIX_ROW_COORD = 0

        #print("getMatrixCoord method, MATRIX COL: ", MATRIX_COLUMN_COORD, " MATRIX ROW: ",MATRIX_ROW_COORD)

    def getNumPlayerPieces(self):
        global NUM_PLAYER_PIECES
        return NUM_PLAYER_PIECES

    def movesAvailable(self):

        # high level overview:
        # this method checks if the selected piece can move to an empty, adjacent, tile.
        # it does this by checking tiles around the selected piece.
        # Because checking an out of bounds index will cause an exception, the method first
        # determines where the selected piece is on the board and then checks valid locations based on that.
        # If a valid location is found, it is highlighted (i.e. set to 10 -> highlighted black tile)

        # get the global variables we need
        global GAME_BOARD
        global MATRIX_ROW_COORD
        global MATRIX_COLUMN_COORD

        # because there might be several moves available, we want the method to check every possible location.
        # therefore, a counter is used. If the counter is > 0, then the method will return true.
        numMovesAvailable = 0

        piece = GAME_BOARD[MATRIX_ROW_COORD][MATRIX_COLUMN_COORD] # get the selected piece from the board
        piece = self.convertPieceToActualValue(piece)
        #print("movesAvailable method, converted piece: ", piece)

        #player logic
        if piece == 2 and MATRIX_COLUMN_COORD == 0: # player, left edge
            if GAME_BOARD[MATRIX_ROW_COORD-1][MATRIX_COLUMN_COORD+1] == 1: # is there a free spot above and to the right?
                GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD + 1] = 10
                print("movesAvailable method, block one")
                numMovesAvailable = numMovesAvailable + 1

        if piece == 2 and MATRIX_ROW_COORD > 1 and MATRIX_COLUMN_COORD == 7: # player, right edge, but not in the top slot:
            if GAME_BOARD[MATRIX_ROW_COORD-1][MATRIX_COLUMN_COORD-1] == 1: # is there a free spot above and to the left?
                GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD - 1] = 10
                print("movesAvailable method, block two")
                numMovesAvailable = numMovesAvailable + 1

        if piece == 2 and MATRIX_ROW_COORD > 0 and MATRIX_COLUMN_COORD > 0 and MATRIX_COLUMN_COORD < 7: # player, and not on the edges:
            if GAME_BOARD[MATRIX_ROW_COORD-1][MATRIX_COLUMN_COORD-1] == 1: # is there a free spot above and to the left?
                GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD - 1] = 10
                print("movesAvailable method, block three a")
                numMovesAvailable = numMovesAvailable + 1
            if GAME_BOARD[MATRIX_ROW_COORD-1][MATRIX_COLUMN_COORD+1] == 1: # is there a free sport above and to the right?
                GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD + 1] = 10
                print("movesAvailable method, block three b")
                numMovesAvailable = numMovesAvailable + 1

        #PC logic
        if piece == 3 and MATRIX_ROW_COORD < 6 and MATRIX_COLUMN_COORD == 0: # PC, left edge
            if GAME_BOARD[MATRIX_ROW_COORD+1][MATRIX_COLUMN_COORD+1] == 1: # is there a free spot below and to the right?
                GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD + 1] = 10
                print("movesAvailable method, block four")
                numMovesAvailable = numMovesAvailable + 1

        if piece == 3 and MATRIX_COLUMN_COORD == 7: # PC, right edge, but not in the top slot:
            if GAME_BOARD[MATRIX_ROW_COORD+1][MATRIX_COLUMN_COORD-1] == 1: # is there a free spot below and to the left?
                GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD - 1] = 10
                print("movesAvailable method, block five")
                numMovesAvailable = numMovesAvailable + 1

        if piece == 3 and MATRIX_ROW_COORD < 7 and MATRIX_COLUMN_COORD > 0 and MATRIX_COLUMN_COORD < 7: # PC, not on the edges or the top:
            if GAME_BOARD[MATRIX_ROW_COORD+1][MATRIX_COLUMN_COORD-1] == 1: # is there a free spot below and to the left?
                GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD - 1] = 10
                print("movesAvailable method, block six a")
                numMovesAvailable = numMovesAvailable + 1
            if GAME_BOARD[MATRIX_ROW_COORD+1][MATRIX_COLUMN_COORD+1] == 1: # is there a free sport below and to the right?
                GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD + 1] = 10
                print("movesAvailable method, block six b")
                numMovesAvailable = numMovesAvailable + 1

        if piece == 4 or piece == 5: # player and pc kings
            print("movesAvailable method, kings block")
            if MATRIX_COLUMN_COORD == 0 and MATRIX_ROW_COORD > 0 and MATRIX_ROW_COORD < 7: #left edge
                if GAME_BOARD[MATRIX_ROW_COORD+1][MATRIX_COLUMN_COORD+1] == 1: #if there's a free spot below and to the right
                    GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD + 1] = 10
                    print("movesAvailable method, kings block a")
                    numMovesAvailable = numMovesAvailable + 1
                if GAME_BOARD[MATRIX_ROW_COORD-1][MATRIX_COLUMN_COORD+1] == 1: #if there's a free spot above and to the right
                    GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD + 1] = 10
                    print("movesAvailable method, kings block b")
                    numMovesAvailable = numMovesAvailable + 1

            if MATRIX_COLUMN_COORD == 7 and MATRIX_ROW_COORD > 0 and MATRIX_ROW_COORD < 7: #right edge
                if GAME_BOARD[MATRIX_ROW_COORD+1][MATRIX_COLUMN_COORD-1] == 1: #if there's a free spot below and to the left
                    GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD - 1] = 10
                    print("movesAvailable method, kings block c")
                    numMovesAvailable = numMovesAvailable + 1
                if GAME_BOARD[MATRIX_ROW_COORD-1][MATRIX_COLUMN_COORD-1] == 1: #if there's a free spot above and to the left
                    GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD - 1] = 10
                    print("movesAvailable method, kings block d")
                    numMovesAvailable = numMovesAvailable + 1

            if MATRIX_COLUMN_COORD == 7 and MATRIX_ROW_COORD == 0: #top right corner
                if GAME_BOARD[MATRIX_ROW_COORD+1][MATRIX_COLUMN_COORD-1] == 1: #if there's a free spot below and to the left
                    GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD - 1] = 10
                    print("movesAvailable method, kings block e")
                    numMovesAvailable = numMovesAvailable + 1

            if MATRIX_ROW_COORD == 0 and MATRIX_COLUMN_COORD < 7: # top row, excluding the corner
                if GAME_BOARD[MATRIX_ROW_COORD+1][MATRIX_COLUMN_COORD+1] == 1:
                    GAME_BOARD[MATRIX_ROW_COORD+1][MATRIX_COLUMN_COORD+1] = 10
                    print("movesAvailable method, kings block f")
                    numMovesAvailable = numMovesAvailable + 1
                if GAME_BOARD[MATRIX_ROW_COORD+1][MATRIX_COLUMN_COORD-1] == 1:
                    GAME_BOARD[MATRIX_ROW_COORD+1][MATRIX_COLUMN_COORD-1] = 10
                    print("movesAvailable method, kings block g")
                    numMovesAvailable = numMovesAvailable + 1

            if MATRIX_ROW_COORD == 7 and MATRIX_COLUMN_COORD > 0: # bottom row, excluding the corner
                if GAME_BOARD[MATRIX_ROW_COORD-1][MATRIX_COLUMN_COORD+1] == 1:
                    GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD + 1] = 10
                    print("movesAvailable method, kings block h")
                    numMovesAvailable = numMovesAvailable + 1
                if GAME_BOARD[MATRIX_ROW_COORD-1][MATRIX_COLUMN_COORD-1] == 1:
                    GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD - 1] = 10
                    print("movesAvailable method, kings block i")
                    numMovesAvailable = numMovesAvailable + 1

            if MATRIX_ROW_COORD == 7 and MATRIX_COLUMN_COORD == 0: # bottom left corner
                if GAME_BOARD[MATRIX_ROW_COORD-1][MATRIX_COLUMN_COORD+1] == 1:
                    GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD + 1] = 10
                    print("movesAvailable method, kings block j")
                    numMovesAvailable = numMovesAvailable + 1

            if MATRIX_COLUMN_COORD > 0 and MATRIX_COLUMN_COORD < 7 and MATRIX_ROW_COORD > 0 and MATRIX_ROW_COORD < 7: # centre of the board
                if GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD - 1] == 1: #top left available?
                    GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD - 1] = 10
                    print("movesAvailable method, kings block k")
                    numMovesAvailable = numMovesAvailable + 1
                if GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD + 1] == 1: #top right available?
                    GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD + 1] = 10
                    print("movesAvailable method, kings block l")
                    numMovesAvailable = numMovesAvailable + 1
                if GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD - 1] == 1: #bottom left available?
                    GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD - 1] = 10
                    print("movesAvailable method, kings block m")
                    numMovesAvailable = numMovesAvailable + 1
                if GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD + 1] == 1: #bottom right available?
                    GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD + 1] = 10
                    print("movesAvailable method, kings block n")
                    numMovesAvailable = numMovesAvailable + 1

        #printBoard()
        if numMovesAvailable > 0:
            return True
    #end of movesAvailable()

    def movePiece(self):

        # High level overview
        # this method determines if you are moving a piece to an adjacent empty tile or if you are capturing an enemy piece.
        # if removes the selected piece from the board, and places it in the new position. An enemy piece is removed,
        # if relevant.

        global GAME_BOARD
        global OWN_ROW
        global OWN_COLUMN
        global TARGET_ROW
        global TARGET_COLUMN
        global CAPTURED

        piece = GAME_BOARD[OWN_ROW][OWN_COLUMN]
        piece = self.convertPieceToActualValue(piece)
        print("movePiece method, piece conversion check: ", piece)

        if not (TARGET_ROW == OWN_ROW and TARGET_COLUMN == OWN_COLUMN): # If you have not selected your current tile
            if piece == 2 or piece == 4:  # player owned piece
                if abs(TARGET_ROW - OWN_ROW) == 1 and abs(TARGET_COLUMN - OWN_COLUMN) == 1: # and there is a difference of 1,1 between your position and the target position
                    if TARGET_ROW < OWN_ROW: # and you're moving forwards
                        if GAME_BOARD[TARGET_ROW][TARGET_COLUMN] == 10: # and if the target tile is empty
                            GAME_BOARD[OWN_ROW][OWN_COLUMN] = 1  # remove the current piece from the gameBoard
                            GAME_BOARD[TARGET_ROW][TARGET_COLUMN] = piece  # place the current piece in the new position
                            print("movePiece Method, block one")
                            return True
                    if piece == 4:
                        if TARGET_ROW > OWN_ROW: # king moving down the board
                            if GAME_BOARD[TARGET_ROW][TARGET_COLUMN] == 10:  # and if the target tile is empty
                                GAME_BOARD[OWN_ROW][OWN_COLUMN] = 1  # remove the current piece from the gameBoard
                                GAME_BOARD[TARGET_ROW][TARGET_COLUMN] = piece  # place the current piece in the new position
                                print("movePiece Method, block two")
                                return True
                elif abs(TARGET_ROW - OWN_ROW) == 2 and abs(TARGET_COLUMN - OWN_COLUMN) == 2: # if there is a difference of 2,2 between your position and the target position
                    if TARGET_ROW < OWN_ROW:
                        if GAME_BOARD[TARGET_ROW][TARGET_COLUMN] == 10:  # and if the target tile is empty
                            if TARGET_COLUMN < OWN_COLUMN: # if the target column is less than the current column, the player is moving left.
                                if GAME_BOARD[OWN_ROW - 1][OWN_COLUMN - 1] == 3 or GAME_BOARD[OWN_ROW - 1][OWN_COLUMN - 1] == 5:  # and if the piece in the middle is an enemy
                                    GAME_BOARD[OWN_ROW][OWN_COLUMN] = 1  # remove the current piece from the gameBoard
                                    GAME_BOARD[OWN_ROW - 1][OWN_COLUMN - 1] = 1  # remove the enemy piece
                                    GAME_BOARD[TARGET_ROW][TARGET_COLUMN] = piece  # place the current piece in the new position
                                    CAPTURED = True
                                    print("movePiece Method, block three")
                                    return True
                            if TARGET_COLUMN > OWN_COLUMN: # if the target column is greater than the current column, the player is moving right
                                if GAME_BOARD[OWN_ROW - 1][OWN_COLUMN + 1] == 3 or GAME_BOARD[OWN_ROW - 1][OWN_COLUMN + 1] == 5:  # and if the piece in the middle is an enemy
                                    GAME_BOARD[OWN_ROW][OWN_COLUMN] = 1  # remove the current piece from the gameBoard
                                    GAME_BOARD[OWN_ROW - 1][OWN_COLUMN + 1] = 1  # remove the enemy piece
                                    GAME_BOARD[TARGET_ROW][TARGET_COLUMN] = piece  # place the current piece in the new position
                                    CAPTURED = True
                                    print("movePiece Method, block four")
                                    return True
                    if piece == 4 and TARGET_ROW > OWN_ROW: # i.e. moving down the board
                        if GAME_BOARD[TARGET_ROW][TARGET_COLUMN] == 10: # towards an available tile
                            if TARGET_COLUMN < OWN_COLUMN: # i.e. moving left
                                if GAME_BOARD[OWN_ROW+1][OWN_COLUMN-1] == 3 or GAME_BOARD[OWN_ROW+1][OWN_COLUMN-1] == 5: #if the piece in the middle is an enemy
                                    GAME_BOARD[OWN_ROW][OWN_COLUMN] = 1 # remove own piece from the board
                                    GAME_BOARD[OWN_ROW+1][OWN_COLUMN-1] = 1 # remove the enemy piece
                                    GAME_BOARD[TARGET_ROW][TARGET_COLUMN] = piece # move the piece to the empty tile
                                    return True
                            if TARGET_COLUMN > OWN_COLUMN: # i.e. moving right
                                if GAME_BOARD[OWN_ROW+1][OWN_COLUMN+1] == 3 or GAME_BOARD[OWN_ROW+1][OWN_COLUMN+1] == 5:
                                    GAME_BOARD[OWN_ROW][OWN_COLUMN] = 1 # remove own piece from the board
                                    GAME_BOARD[OWN_ROW+1][OWN_COLUMN+1] = 1  # remove the enemy piece
                                    GAME_BOARD[TARGET_ROW][TARGET_COLUMN] = piece # move the piece to the empty tile
                                    return True
            print(piece)
            if piece == 3 or piece == 5:  # pc owned piece
                if abs(TARGET_ROW - OWN_ROW) == 1 and abs(TARGET_COLUMN - OWN_COLUMN) == 1: # and there is a difference of 1,1 between your position and the target position
                    if TARGET_ROW > OWN_ROW: # and you're moving forwards
                        if GAME_BOARD[TARGET_ROW][TARGET_COLUMN] == 10: # and if the target tile is empty
                            GAME_BOARD[OWN_ROW][OWN_COLUMN] = 1  # remove the current piece from the gameBoard
                            GAME_BOARD[TARGET_ROW][TARGET_COLUMN] = piece  # place the current piece in the new position
                            print("movePiece Method, block four")
                            return True
                    if piece == 5:
                        if TARGET_ROW < OWN_ROW:  # king moving up the board
                            if GAME_BOARD[TARGET_ROW][TARGET_COLUMN] == 10:  # and if the target tile is empty
                                GAME_BOARD[OWN_ROW][OWN_COLUMN] = 1  # remove the current piece from the gameBoard
                                GAME_BOARD[TARGET_ROW][TARGET_COLUMN] = piece  # place the current piece in the new position
                                print("movePiece Method, block two")
                                return True
                elif abs(TARGET_ROW - OWN_ROW) == 2 and abs(TARGET_COLUMN - OWN_COLUMN) == 2: # if there is a difference of 2,2 between your position and the target position
                    if TARGET_ROW > OWN_ROW: # ie. moving down the board
                        if GAME_BOARD[TARGET_ROW][TARGET_COLUMN] == 10:  # and if the target tile is empty
                            if TARGET_COLUMN > OWN_COLUMN: # if the target column is less than the current column, the pc is moving right.
                                if GAME_BOARD[OWN_ROW + 1][OWN_COLUMN + 1] == 2 or GAME_BOARD[OWN_ROW + 1][OWN_COLUMN + 1] == 4:  # and if the piece in the middle is an enemy
                                    GAME_BOARD[OWN_ROW][OWN_COLUMN] = 1  # remove the current piece from the gameBoard
                                    GAME_BOARD[OWN_ROW + 1][OWN_COLUMN + 1] = 1  # remove the enemy piece
                                    GAME_BOARD[TARGET_ROW][TARGET_COLUMN] = piece  # place the current piece in the new position
                                    CAPTURED = True
                                    print("movePiece Method, block five")
                                    return True
                            if TARGET_COLUMN < OWN_COLUMN: # if the target column is greater than the current column, the pc is moving left
                                if GAME_BOARD[OWN_ROW + 1][OWN_COLUMN - 1] == 2 or GAME_BOARD[OWN_ROW + 1][OWN_COLUMN - 1] == 4:  # and if the piece in the middle is an enemy
                                    GAME_BOARD[OWN_ROW][OWN_COLUMN] = 1  # remove the current piece from the gameBoard
                                    GAME_BOARD[OWN_ROW + 1][OWN_COLUMN - 1] = 1  # remove the enemy piece
                                    GAME_BOARD[TARGET_ROW][TARGET_COLUMN] = piece  # place the current piece in the new position
                                    CAPTURED = True
                                    print("movePiece Method, block six")
                                    return True
                    if piece == 5 and TARGET_ROW > OWN_ROW:  # i.e. king moving up the board
                        if GAME_BOARD[TARGET_ROW][TARGET_COLUMN] == 10:  # towards an available tile
                            if TARGET_COLUMN < OWN_COLUMN:  # i.e. moving left
                                if GAME_BOARD[OWN_ROW - 1][OWN_COLUMN - 1] == 2 or GAME_BOARD[OWN_ROW - 1][OWN_COLUMN - 1] == 4:  # if the piece in the middle is an enemy
                                    GAME_BOARD[OWN_ROW][OWN_COLUMN] = 1  # remove own piece from the board
                                    GAME_BOARD[OWN_ROW - 1][OWN_COLUMN - 1] = 1  # remove the enemy piece
                                    GAME_BOARD[TARGET_ROW][TARGET_COLUMN] = piece  # move the piece to the empty tile
                                    return True
                            if TARGET_COLUMN > OWN_COLUMN:  # i.e. moving right
                                if GAME_BOARD[OWN_ROW - 1][OWN_COLUMN + 1] == 2 or GAME_BOARD[OWN_ROW - 1][OWN_COLUMN + 1] == 4:
                                    GAME_BOARD[OWN_ROW][OWN_COLUMN] = 1  # remove own piece from the board
                                    GAME_BOARD[OWN_ROW - 1][OWN_COLUMN + 1] = 1  # remove the enemy piece
                                    GAME_BOARD[TARGET_ROW][TARGET_COLUMN] = piece  # move the piece to the empty tile
                                    return True
    # end of movePiece()

    def pcCaptureAvailable(self):
        global GAME_BOARD
        global MATRIX_ROW_COORD
        global MATRIX_COLUMN_COORD

        piece = GAME_BOARD[MATRIX_ROW_COORD][MATRIX_COLUMN_COORD]
        print("pcCaptureAvailable, piece value: ", piece)
        piece = self.convertPieceToActualValue(piece)
        print("pcCaptureAvailable, converted piece value: ", piece)

        numMovesAvailable = 0

        # for the pc, capture is never possible from row 6 or row 7. The pc captures in the row+ direction.

        # for column 0 and column 1, capture to the right is possible, but capture to the left is impossible.
        if piece == 3:
            if MATRIX_ROW_COORD < 6 and (MATRIX_COLUMN_COORD == 0 or MATRIX_COLUMN_COORD == 1):  # if a pc piece is on the left edge of the board...
                if GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD + 1] == 2 or GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD + 1] == 4:  # and if the piece below and to the right is an enemy...
                    if GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD + 2] == 1:  # and if the tile to the bottom right of the enemy piece is empty...
                        GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD + 2] = 10
                        print("pcCaptureAvailable method, block one")
                        numMovesAvailable = numMovesAvailable + 1  # capture is possible

            # for column 7 and 6, capture to the left is possible, but capture to the right is impossible
            if MATRIX_ROW_COORD < 6 and (MATRIX_COLUMN_COORD == 7 or MATRIX_COLUMN_COORD == 6):  # if a pc piece is on the right edge of the board...
                if GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD - 1] == 2 or GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD - 1] == 4:  # and if the piece above and to the left is an enemy...
                    if GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD - 2] == 1:  # and if the tile to the bottom right of the enemy piece is empty...
                        GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD - 2] = 10
                        print("pcCaptureAvailable method, block two")
                        numMovesAvailable = numMovesAvailable + 1  # capture is possible

            # for the rest of the board (row 0 - 5, column 2 - 5)
            if MATRIX_ROW_COORD < 6 and MATRIX_COLUMN_COORD > 1 and MATRIX_COLUMN_COORD < 6:  # if a pc piece is not in the top two rows, the left edge, or the right edge...
                if GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD - 1] == 2 or GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD - 1] == 4:  # and if the piece below and to the left is an enemy...
                    if GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD - 2] == 1:  # and if the tile below and to the left of the enemy piece is free...
                        GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD - 2] = 10
                        print("pcCaptureAvailable method, block three")
                        numMovesAvailable = numMovesAvailable + 1  # capture is possible

                if GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD + 1] == 2 or GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD + 1] == 4:  # or if the piece below and to the right is an enemy...
                    if GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD + 2] == 1:  # and if the tile above and to the right of the enemy piece is free...
                        GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD + 2] = 10
                        print("pcCaptureAvailable method, block four")
                        numMovesAvailable = numMovesAvailable + 1  # capture is possible

        # kings
        if piece == 5:
            if MATRIX_COLUMN_COORD == 0 or MATRIX_COLUMN_COORD == 1:
                if MATRIX_ROW_COORD < 6:
                    if GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD + 1] == 2 or GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD + 1] == 4:
                        if GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD + 2] == 1:
                            GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD + 2] = 10
                            print("pcCaptureAvailable method, block five")
                            numMovesAvailable = numMovesAvailable + 1  # capture is possible in the row+ direction (i.e. downwards)
                if MATRIX_ROW_COORD > 1:
                    if GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD + 1] == 2 or GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD + 1] == 4:
                        if GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_COLUMN_COORD + 2] == 1:
                            GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_COLUMN_COORD + 2] = 10
                            print("pcCaptureAvailable method, block six")
                            numMovesAvailable = numMovesAvailable + 1  # capture is possible in the row- direction

            if MATRIX_COLUMN_COORD == 7 or MATRIX_COLUMN_COORD == 6:
                if MATRIX_ROW_COORD < 6:
                    if GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD - 1] == 2 or GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD - 1] == 4:
                        if GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD - 2] == 1:
                            GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD - 2] = 10
                            print("pcCaptureAvailable method, block seven")
                            numMovesAvailable = numMovesAvailable + 1  # capture is possible in the row+ direction
                if MATRIX_ROW_COORD > 1:
                    if GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD - 1] == 2 or GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD - 1] == 4:
                        if GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_COLUMN_COORD - 2] == 1:
                            GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_COLUMN_COORD - 2] = 10
                            print("pcCaptureAvailable method, block eight")
                            numMovesAvailable = numMovesAvailable + 1  # capture is possible in the row- direction

            if MATRIX_ROW_COORD == 0 or MATRIX_ROW_COORD == 1:
                if MATRIX_COLUMN_COORD > 1:
                    if GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD - 1] == 2 or GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD - 1] == 4:
                        if GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD - 2] == 1:
                            GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD - 2] = 10
                            print("pcCaptureAvailable method, block nine")
                            numMovesAvailable = numMovesAvailable + 1  # capture is possible in the column- direction

                if MATRIX_COLUMN_COORD < 6:
                    if GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD + 1] == 2 or GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD + 1] == 4:
                        if GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD + 2] == 1:
                            GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD + 2] = 10
                            print("pcCaptureAvailable method, block ten")
                            numMovesAvailable = numMovesAvailable + 1  # capture is possible in the column+ direction

            if MATRIX_ROW_COORD == 7 or MATRIX_ROW_COORD == 6:
                if MATRIX_COLUMN_COORD < 6:
                    if GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD + 1] == 2 or GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD + 1] == 4:
                        if GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_ROW_COORD + 2] == 1:
                            GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_ROW_COORD + 2] = 10
                            print("pcCaptureAvailable method, block eleven")
                            numMovesAvailable = numMovesAvailable + 1  # capture is possible in the column+ direction
                if MATRIX_COLUMN_COORD > 1:
                    if GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD - 1] == 2 or GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD - 1] == 4:
                        if GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_COLUMN_COORD - 2] == 1:
                            GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_COLUMN_COORD - 2] = 10
                            print("pcCaptureAvailable method, block twelve")
                            numMovesAvailable = numMovesAvailable + 1  # capture is possible in the column- direction

            if MATRIX_ROW_COORD > 1 and MATRIX_ROW_COORD < 6 and MATRIX_COLUMN_COORD > 1 and MATRIX_COLUMN_COORD < 6:
                if GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD - 1] == 2 or GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD - 1] == 4:
                    if GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_COLUMN_COORD - 2] == 1:
                        GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_COLUMN_COORD - 2] = 10
                        print("pcCaptureAvailable method, block thirteen")
                        numMovesAvailable = numMovesAvailable + 1  # capture is possible in the row-, column- direction
                if GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD + 1] == 2 or GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD + 1] == 4:
                    if GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_COLUMN_COORD + 2] == 1:
                        GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_COLUMN_COORD + 2] = 10
                        print("pcCaptureAvailable method, block fourteen")
                        numMovesAvailable = numMovesAvailable + 1  # capture is possible in the row-, column+ direction
                if GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD - 1] == 2 or GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD - 1] == 4:
                    if GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD - 2] == 1:
                        GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD - 2] = 10
                        print("pcCaptureAvailable method, block fifteen")
                        numMovesAvailable = numMovesAvailable + 1  # capture is possible in the row+, column- direction
                if GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD + 1] == 2 or GAME_BOARD[MATRIX_ROW_COORD + 1][MATRIX_COLUMN_COORD + 1] == 4:
                    if GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD + 2] == 1:
                        GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD + 2] = 10
                        print("pcCaptureAvailable method, block sixteen")
                        numMovesAvailable = numMovesAvailable + 1  # capture is possible in the row+, column+ direction

        #printBoard()
        if numMovesAvailable > 0:
            return True
    # end of playerCaptureAvailable()

    def playerCaptureAvailable(self):  # checks if the selected player piece can capture an opponent

        # high level overview:
        # This method checks to see if the selected piece is able to capture any enemy pieces.
        # It does this by determining where on the board the selected piece is, and then checking adjacent locations to see
        # if an enemy is present.
        # It then checks to see if the enemy is adjacent to an empty tile.
        # If this is the case, this method highlights the empty tile, and returns true.
        # All adjacent locations are tested and highlighted as appropriate.

        global GAME_BOARD
        global MATRIX_ROW_COORD
        global MATRIX_COLUMN_COORD

        piece = GAME_BOARD[MATRIX_ROW_COORD][MATRIX_COLUMN_COORD] # get value of the selected piece
        #print("playerCaptureAvailable, piece selected: ", piece)
        piece = self.convertPieceToActualValue(piece)
        #print("Converted piece value: ", piece)

        numMovesAvailable = 0

        # for player soldiers, capture is never possible from row 0 or row 1. The player captures in the row- direction.
        # for column 0 and column 1, capture to the right is possible, but capture to the left is impossible.
        if piece == 2:
            if MATRIX_ROW_COORD > 2 and MATRIX_COLUMN_COORD == 0 or MATRIX_COLUMN_COORD == 1:  # if a player piece is on the left edge of the board...
                if GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD + 1] == 3 or GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD + 1] == 5:  # and if the piece above and to the right is an enemy...
                    if GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_COLUMN_COORD + 2] == 1:  # and if the tile to the above right of the enemy piece is empty...
                        GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_COLUMN_COORD + 2] = 10
                        print("playerCaptureAvailable method, block one")
                        numMovesAvailable = numMovesAvailable + 1  # capture is possible

            # for column 7 and 6, capture to the left is possible, but capture to the right is impossible
            if MATRIX_ROW_COORD > 1 and MATRIX_COLUMN_COORD == 7 or MATRIX_COLUMN_COORD == 6:  # if a player piece is on the right edge of the board...
                if GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD - 1] == 3 or GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD - 1] == 5:  # and if the piece above and to the left is an enemy...
                    if GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_COLUMN_COORD - 2] == 1:  # and if the tile to the above right of the enemy piece is empty...
                        GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_COLUMN_COORD - 2] = 10
                        print("playerCaptureAvailable method, block two")
                        numMovesAvailable = numMovesAvailable + 1  # capture is possible

            # for the rest of the board (row 0 - 5, column 2 - 5)
            if MATRIX_ROW_COORD > 1 and MATRIX_COLUMN_COORD > 1 and MATRIX_COLUMN_COORD < 6:  # if a player piece is not in the top two rows, the left edge, or the right edge...
                if GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD - 1] == 3 or GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD - 1] == 5:  # and if the piece above and to the left is an enemy...
                    if GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_COLUMN_COORD - 2] == 1:  # and if the tile above and to the left of the enemy piece is free...
                        GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_COLUMN_COORD - 2] = 10
                        print("playerCaptureAvailable method, block three")
                        numMovesAvailable = numMovesAvailable + 1  # capture is possible

                if GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD + 1] == 3 or GAME_BOARD[MATRIX_ROW_COORD - 1][MATRIX_COLUMN_COORD + 1] == 5:  # or if the piece above and to the right is an enemy...
                    if GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_COLUMN_COORD + 2] == 1:  # and if the tile above and to the right of the enemy piece is free...
                        GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_COLUMN_COORD + 2] = 10
                        print("playerCaptureAvailable method, block four")
                        numMovesAvailable = numMovesAvailable + 1  # capture is possible

        # kings
        if piece == 4:
            if MATRIX_COLUMN_COORD == 0 or MATRIX_COLUMN_COORD == 1:
                if MATRIX_ROW_COORD < 6:
                    if GAME_BOARD[MATRIX_ROW_COORD+1][MATRIX_COLUMN_COORD+1] == 3 or GAME_BOARD[MATRIX_ROW_COORD+1][MATRIX_COLUMN_COORD+1] == 5:
                        if GAME_BOARD[MATRIX_ROW_COORD+2][MATRIX_COLUMN_COORD+2] == 1:
                            GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD + 2] = 10
                            print("playerCaptureAvailable method, block five")
                            numMovesAvailable = numMovesAvailable + 1 # capture is possible in the row+ direction (i.e. downwards)
                if MATRIX_ROW_COORD > 1:
                    if GAME_BOARD[MATRIX_ROW_COORD-1][MATRIX_COLUMN_COORD+1] == 3 or GAME_BOARD[MATRIX_ROW_COORD-1][MATRIX_COLUMN_COORD+1] == 5:
                        if GAME_BOARD[MATRIX_ROW_COORD-2][MATRIX_COLUMN_COORD+2] == 1:
                            GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_COLUMN_COORD + 2] = 10
                            print("playerCaptureAvailable method, block six")
                            numMovesAvailable = numMovesAvailable + 1 # capture is possible in the row- direction

            if MATRIX_COLUMN_COORD == 7 or MATRIX_COLUMN_COORD == 6:
                if MATRIX_ROW_COORD < 6:
                    if GAME_BOARD[MATRIX_ROW_COORD+1][MATRIX_COLUMN_COORD-1] == 3 or GAME_BOARD[MATRIX_ROW_COORD+1][MATRIX_COLUMN_COORD-1] == 5:
                        if GAME_BOARD[MATRIX_ROW_COORD+2][MATRIX_COLUMN_COORD-2] == 1:
                            GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD - 2] = 10
                            print("playerCaptureAvailable method, block seven")
                            numMovesAvailable = numMovesAvailable + 1 # capture is possible in the row+ direction
                if MATRIX_ROW_COORD > 1:
                    if GAME_BOARD[MATRIX_ROW_COORD-1][MATRIX_COLUMN_COORD-1] == 3 or GAME_BOARD[MATRIX_ROW_COORD-1][MATRIX_COLUMN_COORD-1] == 5:
                        if GAME_BOARD[MATRIX_ROW_COORD-2][MATRIX_COLUMN_COORD-2] == 1:
                            GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_COLUMN_COORD - 2] = 10
                            print("playerCaptureAvailable method, block eight")
                            numMovesAvailable = numMovesAvailable + 1 # capture is possible in the row- direction

            if MATRIX_ROW_COORD == 0 or MATRIX_ROW_COORD == 1:
                if MATRIX_COLUMN_COORD > 1:
                    if GAME_BOARD[MATRIX_ROW_COORD+1][MATRIX_COLUMN_COORD-1] == 3 or GAME_BOARD[MATRIX_ROW_COORD+1][MATRIX_COLUMN_COORD-1] == 5:
                        if GAME_BOARD[MATRIX_ROW_COORD+2][MATRIX_COLUMN_COORD-2] == 1:
                            GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD - 2] = 10
                            print("playerCaptureAvailable method, block nine")
                            numMovesAvailable = numMovesAvailable + 1 # capture is possible in the column- direction

                if MATRIX_COLUMN_COORD < 6:
                    if GAME_BOARD[MATRIX_ROW_COORD+1][MATRIX_COLUMN_COORD+1] == 3 or GAME_BOARD[MATRIX_ROW_COORD+1][MATRIX_COLUMN_COORD+1] == 5:
                        if GAME_BOARD[MATRIX_ROW_COORD+2][MATRIX_COLUMN_COORD+2] == 1:
                            GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD + 2] = 10
                            print("playerCaptureAvailable method, block ten")
                            numMovesAvailable = numMovesAvailable + 1 # capture is possible in the column+ direction

            if MATRIX_ROW_COORD == 7 or MATRIX_ROW_COORD == 6:
                if MATRIX_COLUMN_COORD < 6:
                    if GAME_BOARD[MATRIX_ROW_COORD-1][MATRIX_COLUMN_COORD+1] == 3 or GAME_BOARD[MATRIX_ROW_COORD-1][MATRIX_COLUMN_COORD+1] == 5:
                        if GAME_BOARD[MATRIX_ROW_COORD-2][MATRIX_ROW_COORD+2] == 1:
                            GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_ROW_COORD + 2] = 10
                            print("playerCaptureAvailable method, block eleven")
                            numMovesAvailable = numMovesAvailable + 1 # capture is possible in the column+ direction
                if MATRIX_COLUMN_COORD > 1:
                    if GAME_BOARD[MATRIX_ROW_COORD-1][MATRIX_COLUMN_COORD-1] == 3 or GAME_BOARD[MATRIX_ROW_COORD-1][MATRIX_COLUMN_COORD-1] == 5:
                        if GAME_BOARD[MATRIX_ROW_COORD-2][MATRIX_COLUMN_COORD-2] == 1:
                            GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_COLUMN_COORD - 2] = 10
                            print("playerCaptureAvailable method, block twelve")
                            numMovesAvailable = numMovesAvailable + 1 # capture is possible in the column- direction

            if MATRIX_ROW_COORD > 1 and MATRIX_ROW_COORD < 6 and MATRIX_COLUMN_COORD > 1 and MATRIX_COLUMN_COORD < 6:
                if GAME_BOARD[MATRIX_ROW_COORD-1][MATRIX_COLUMN_COORD-1] == 3 or GAME_BOARD[MATRIX_ROW_COORD-1][MATRIX_COLUMN_COORD-1] == 5:
                    if GAME_BOARD[MATRIX_ROW_COORD-2][MATRIX_COLUMN_COORD-2] == 1:
                        GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_COLUMN_COORD - 2] = 10
                        print("playerCaptureAvailable method, block thirteen")
                        numMovesAvailable = numMovesAvailable + 1 # capture is possible in the row-, column- direction
                if GAME_BOARD[MATRIX_ROW_COORD-1][MATRIX_COLUMN_COORD+1] == 3 or GAME_BOARD[MATRIX_ROW_COORD-1][MATRIX_COLUMN_COORD+1] == 5:
                    if GAME_BOARD[MATRIX_ROW_COORD-2][MATRIX_COLUMN_COORD+2] == 1:
                        GAME_BOARD[MATRIX_ROW_COORD - 2][MATRIX_COLUMN_COORD + 2] = 10
                        print("playerCaptureAvailable method, block fourteen")
                        numMovesAvailable = numMovesAvailable + 1 # capture is possible in the row-, column+ direction
                if GAME_BOARD[MATRIX_ROW_COORD+1][MATRIX_COLUMN_COORD-1] == 3 or GAME_BOARD[MATRIX_ROW_COORD+1][MATRIX_COLUMN_COORD-1] == 5:
                    if GAME_BOARD[MATRIX_ROW_COORD+2][MATRIX_COLUMN_COORD-2] == 1:
                        GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD - 2] = 10
                        print("playerCaptureAvailable method, block fifteen")
                        numMovesAvailable = numMovesAvailable + 1 # capture is possible in the row+, column- direction
                if GAME_BOARD[MATRIX_ROW_COORD+1][MATRIX_COLUMN_COORD+1] == 3 or GAME_BOARD[MATRIX_ROW_COORD+1][MATRIX_COLUMN_COORD+1] == 5:
                    if GAME_BOARD[MATRIX_ROW_COORD+2][MATRIX_COLUMN_COORD+2] == 1:
                        GAME_BOARD[MATRIX_ROW_COORD + 2][MATRIX_COLUMN_COORD + 2] = 10
                        print("playerCaptureAvailable method, block sixteen")
                        numMovesAvailable = numMovesAvailable + 1 # capture is possible in the row+, column+ direction

        if numMovesAvailable > 0:
            return True
    #end of playerCaptureAvailable()

    def promotePieces(self):

        # high level overview:
        # this method checks for soldiers in the correct position and promotes them as appropriate

        global GAME_BOARD

        for c in range(0,8):
            if GAME_BOARD[0][c] == 2: # player solider in the top row
                GAME_BOARD[0][c] = 4 # becomes player king in the top row
            if GAME_BOARD[7][c] == 3: # pc soldier in the bottom row
                GAME_BOARD[7][c] = 5 # becomes pc king in the bottom row

    def paintTile_black(self, pen):
        pen.pendown()

        # this draws a gray box.
        pen.begin_fill()
        pen.color(183, 137, 91)
        for x in range(4):
            pen.forward(100)
            pen.right(90)
        pen.end_fill()

        # this draws the outline around the box.
        pen.color("black")
        for x in range(0, 4):
            pen.forward(100)
            pen.right(90)

        pen.penup

    def paintTile_black_highlighted(self, pen):
        pen.pendown()

        # this draws a gray box.
        pen.begin_fill()
        pen.color(183, 137, 91)
        for x in range(4):
            pen.forward(100)
            pen.right(90)
        pen.end_fill()

        # this draws the outline around the box.
        pen.color("black")
        for x in range(0, 4):
            pen.forward(100)
            pen.right(90)

        pen.penup

        xcoord = 15
        ycoord = 52

        # position the pen to draw the outline
        pen.penup()
        pen.forward(xcoord)
        pen.right(90)
        pen.forward(ycoord)
        pen.pendown()

        # draw the outline on the tile

        pen.color("yellow")
        pen.width(4)
        pen.circle(35)
        pen.width(1)

        pen.penup()

        # reset the pen position
        pen.right(180)
        pen.forward(ycoord)
        pen.left(90)
        pen.forward(xcoord)
        pen.right(180)

    def paintTile_pcKing(self, pen):
        pen.pendown()

        # this draws a gray box.
        pen.begin_fill()
        pen.color(183, 137, 91)
        for x in range(4):
            pen.forward(100)
            pen.right(90)
        pen.end_fill()

        # this draws the outline around the box.
        pen.color("black")
        for x in range(0, 4):
            pen.forward(100)
            pen.right(90)

        xcoord = 15
        ycoord = 52

        # position the pen to draw the piece
        pen.penup()
        pen.forward(xcoord)
        pen.right(90)
        pen.forward(ycoord)
        pen.pendown()

        # draw the piece on the tile
        pen.begin_fill()
        pen.color("light blue")
        pen.circle(35)
        pen.end_fill()

        pen.width(10)
        pen.color("blue")
        pen.circle(35)
        pen.width(1)

        pen.penup()

        # reset the pen position
        pen.right(180)
        pen.forward(ycoord)
        pen.left(90)
        pen.forward(xcoord)
        pen.right(180)

    def paintTile_pcKing_highlighted(self, pen):
        pen.pendown()

        # this draws a gray box.
        pen.begin_fill()
        pen.color(183, 137, 91)
        for x in range(4):
            pen.forward(100)
            pen.right(90)
        pen.end_fill()

        # this draws the outline around the box.
        pen.color("black")
        for x in range(0, 4):
            pen.forward(100)
            pen.right(90)

        xcoord = 15
        ycoord = 52

        # position the pen to draw the piece
        pen.penup()
        pen.forward(xcoord)
        pen.right(90)
        pen.forward(ycoord)
        pen.pendown()

        # draw the piece on the tile
        pen.begin_fill()
        pen.color("light blue")
        pen.circle(35)
        pen.end_fill()

        pen.width(10)
        pen.color("yellow")
        pen.circle(35)
        pen.width(1)

        pen.penup()

        # reset the pen position
        pen.right(180)
        pen.forward(ycoord)
        pen.left(90)
        pen.forward(xcoord)
        pen.right(180)

    def paintTile_pcSoldier(self, pen):
        pen.pendown()

        # this draws a gray box.
        pen.begin_fill()
        pen.color(183, 137, 91)
        for x in range(4):
            pen.forward(100)
            pen.right(90)
        pen.end_fill()

        # this draws the outline around the box.
        pen.color("black")
        for x in range(0, 4):
            pen.forward(100)
            pen.right(90)

        xcoord = 15
        ycoord = 52

        # position the pen to draw the piece
        pen.penup()
        pen.forward(xcoord)
        pen.right(90)
        pen.forward(ycoord)
        pen.pendown()

        # draw the piece on the tile
        pen.begin_fill()
        pen.color("blue")
        pen.circle(35)
        pen.end_fill()

        pen.penup()

        # reset the pen position
        pen.right(180)
        pen.forward(ycoord)
        pen.left(90)
        pen.forward(xcoord)
        pen.right(180)

    def paintTile_pcSoldier_highlighted(self, pen):
        pen.pendown()

        # this draws a gray box.
        pen.begin_fill()
        pen.color(183, 137, 91)
        for x in range(4):
            pen.forward(100)
            pen.right(90)
        pen.end_fill()

        # this draws the outline around the box.
        pen.color("black")
        for x in range(0, 4):
            pen.forward(100)
            pen.right(90)

        xcoord = 15
        ycoord = 52

        # position the pen to draw the piece
        pen.penup()
        pen.forward(xcoord)
        pen.right(90)
        pen.forward(ycoord)
        pen.pendown()

        # draw the piece on the tile
        pen.begin_fill()
        pen.color("blue")
        pen.circle(35)
        pen.end_fill()

        pen.color("yellow")
        pen.width(4)
        pen.circle(35)
        pen.width(1)
        pen.penup()

        # reset the pen position
        pen.right(180)
        pen.forward(ycoord)
        pen.left(90)
        pen.forward(xcoord)
        pen.right(180)

    def paintTile_playerKing(self, pen):
        pen.pendown()

        # this draws a gray box.
        pen.begin_fill()
        pen.color(183, 137, 91)
        for x in range(4):
            pen.forward(100)
            pen.right(90)
        pen.end_fill()

        # this draws the outline around the box.
        pen.color("black")
        for x in range(0, 4):
            pen.forward(100)
            pen.right(90)

        xcoord = 15
        ycoord = 52

        # position the pen to draw the piece
        pen.penup()
        pen.forward(xcoord)
        pen.right(90)
        pen.forward(ycoord)
        pen.pendown()

        # draw the piece on the tile
        pen.begin_fill()
        pen.color("red")
        pen.circle(35)
        pen.end_fill()

        pen.width(10)
        pen.color("dark red")
        pen.circle(35)
        pen.width(1)

        pen.penup()

        # reset the pen position
        pen.right(180)
        pen.forward(ycoord)
        pen.left(90)
        pen.forward(xcoord)
        pen.right(180)

    def paintTile_playerKing_highlighted(self, pen):
        pen.pendown()

        # this draws a gray box.
        pen.begin_fill()
        pen.color(183, 137, 91)
        for x in range(4):
            pen.forward(100)
            pen.right(90)
        pen.end_fill()

        # this draws the outline around the box.
        pen.color("black")
        for x in range(0, 4):
            pen.forward(100)
            pen.right(90)

        xcoord = 15
        ycoord = 52

        # position the pen to draw the piece
        pen.penup()
        pen.forward(xcoord)
        pen.right(90)
        pen.forward(ycoord)
        pen.pendown()

        # draw the piece on the tile
        pen.begin_fill()
        pen.color("red")
        pen.circle(35)
        pen.end_fill()

        #highlighting
        pen.width(10)
        pen.color("yellow")
        pen.circle(35)
        pen.width(1)

        pen.penup()

        # reset the pen position
        pen.right(180)
        pen.forward(ycoord)
        pen.left(90)
        pen.forward(xcoord)
        pen.right(180)

    def paintTile_playerSoldier(self, pen):
        pen.pendown()

        # this draws a gray box.
        pen.begin_fill()
        pen.color(183, 137, 91)
        for x in range(4):
            pen.forward(100)
            pen.right(90)
        pen.end_fill()

        # this draws the outline around the box.
        pen.color("black")
        for x in range(0, 4):
            pen.forward(100)
            pen.right(90)

        xcoord = 15
        ycoord = 52

        # position the pen to draw the piece
        pen.penup()
        pen.forward(xcoord)
        pen.right(90)
        pen.forward(ycoord)
        pen.pendown()

        # draw the piece on the tile
        pen.begin_fill()
        pen.color("red")
        pen.circle(35)
        pen.end_fill()

        pen.penup()

        # reset the pen position
        pen.right(180)
        pen.forward(ycoord)
        pen.left(90)
        pen.forward(xcoord)
        pen.right(180)

    def paintTile_playerSoldier_highlighted(self, pen):
        pen.pendown()

        # this draws a gray box.
        pen.begin_fill()
        pen.color(183, 137, 91)
        for x in range(4):
            pen.forward(100)
            pen.right(90)
        pen.end_fill()

        # this draws the outline around the box.
        pen.color("black")
        for x in range(0, 4):
            pen.forward(100)
            pen.right(90)

        xcoord = 15
        ycoord = 52

        # position the pen to draw the piece
        pen.penup()
        pen.forward(xcoord)
        pen.right(90)
        pen.forward(ycoord)
        pen.pendown()

        # draw the piece on the tile
        pen.begin_fill()
        pen.color("red")
        pen.circle(35)
        pen.end_fill()

        #highlighting
        pen.color("yellow")
        pen.width(4)
        pen.circle(35)
        pen.width(1)

        pen.penup()

        # reset the pen position
        pen.right(180)
        pen.forward(ycoord)
        pen.left(90)
        pen.forward(xcoord)
        pen.right(180)

    def paintTile_white(self, pen):
        pen.pendown()

        # this draws a white box.
        pen.begin_fill()
        pen.color(226, 215, 215) # myo change colour
        for x in range(4):
            pen.forward(100)
            pen.right(90)
        pen.end_fill()

        # this draws the outline around the box.
        pen.color("black")
        for x in range(0, 4):
            pen.forward(100)
            pen.right(90)

        pen.penup()

    def printBoard(self):

        #High level overview: This method prints the game board to the console

        global GAME_BOARD
        print("\n",GAME_BOARD,"\n")

    def validPiece(self, piece):

        # high level overview:
        # this method checks if the piece passed in matches the piece recorded in the matrix.
        # i.e. it is used to ensure that the players have clicked on a piece that they own

        global GAME_BOARD
        global MATRIX_ROW_COORD
        global MATRIX_COLUMN_COORD

        if GAME_BOARD[MATRIX_ROW_COORD][MATRIX_COLUMN_COORD] == piece:
            return True

    def main(self):
        # screen setup
        turtle.setup(800, 800, 300, 100) # sets the paramaters of the screen. 800x800 and it is placed at 900x100 (right hand side)
        mainWindow = turtle.Screen() # create a screen that the turtle can draw on
        mainWindow.title("Checkers Board")
        mainWindow.bgcolor("white") # background colour
        mainWindow.tracer(0,0) # enables the turtle to draw instantly
        # myo added
        mainWindow.colormode(255)

        self.drawBoard() # this method draws the board on screen.
        print("Player 1, please click on the piece you would like to move: ") # start the game

        mainWindow.onscreenclick(self.advanceStateMachine) # Binds the event handler to adcanveStateMachine() method, which controls the game
        mainWindow.listen() # listen for events.
        mainWindow.mainloop() # keeps focus on the mainWindow, and keeps it updated.