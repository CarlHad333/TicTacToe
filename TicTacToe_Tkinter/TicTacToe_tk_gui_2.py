from tkinter import messagebox

class TicTacToe:
    def __init__(self, player):
        # current player's character (X or O)
        self.player = str.upper(player)
        # current turn count
        self.count = 0
        # display board
        self.board = {
            '7': " " , '8': " " , '9': " ",
            '4': " " , '5': " " , '6': " ",
            '1': " " , '2': " " , '3': " "
        }
        # board to print on the interface
        self.printedBoard = ""
        # check if game is over or not
        self.gameOver = False
        # check current state of the game
        self.winningState = ""
        # all keys inside the right now
        self.board_keys = []
        for key in self.board:
            self.board_keys.append(key)

    # getter method for the winning state
    def getWinningState(self):
        return self.winningState

    # setter method for the winning state
    def setWinningState(self, winningState):
        self.winningState = winningState

    # getter method for the board to be printed
    def getPrintedBoard(self):
        return self.printedBoard

    # setter method for the board to be printed
    def setPrintedBoard(self, printedBoard):
        self.printedBoard = printedBoard

    # adjust the current board
    def AdjustBoard(self):
        def getCharacter(char):
            if self.board[char] == " ":
                return char
            else:
                return self.board[char]

        # board to be printed on the interface
        boardToPrint = (
            getCharacter("7") + '   |   ' + getCharacter("8") + '   |   ' + getCharacter('9') + "\n" +
            "-----------" + "\n" +
            getCharacter('4') + '   |   ' + getCharacter('5') + '   |   ' + getCharacter('6') + "\n" +
            "-----------" + "\n" +
            getCharacter('1') + '   |   ' + getCharacter('2') + '   |   ' + getCharacter('3')
        )
        self.setPrintedBoard(boardToPrint)

    # Check for all the winning conditions in the tic tac toe game
    def checkWinningConditions(self):
        if self.board['7'] == self.board['8'] == self.board['9'] != " ": # across the top
            self.AdjustBoard()
            self.setWinningState("Game over, player " + self.player + " has won.")              
            self.gameOver = True           
                
        elif self.board['4'] == self.board['5'] == self.board['6'] != " ": # across the middle
            self.AdjustBoard()
            self.setWinningState("Game over, player " + self.player + " has won.")               
            self.gameOver = True
            
        elif self.board['1'] == self.board['2'] == self.board['3'] != " ": # across the bottom
            self.AdjustBoard()
            self.setWinningState("Game over, player " + self.player + " has won.")            
            self.gameOver = True
            
        elif self.board['1'] == self.board['4'] == self.board['7'] != " ": # down the left side
            self.AdjustBoard()
            self.setWinningState("Game over, player " + self.player + " has won.")              
            self.gameOver = True
            
        elif self.board['2'] == self.board['5'] == self.board['8'] != " ": # down the middle
            self.AdjustBoard()
            self.setWinningState("Game over, player " + self.player + " has won.")                
            self.gameOver = True
            
        elif self.board['3'] == self.board['6'] == self.board['9'] != " ": # down the right side
            self.AdjustBoard()
            self.setWinningState("Game over, player " + self.player + " has won.")                
            self.gameOver = True
             
        elif self.board['7'] == self.board['5'] == self.board['3'] != " ": # diagonal
            self.AdjustBoard()
            self.setWinningState("Game over, player " + self.player + " has won.")                
            self.gameOver = True
            
        elif self.board['1'] == self.board['5'] == self.board['9'] != " ": # diagonal
            self.AdjustBoard()
            self.setWinningState("Game over, player " + self.player + " has won.")                
            self.gameOver = True
             
    # Every player's turn
    def turn(self,chosenmove):

        # The current player's move
        move = chosenmove.get()
        
        # First we convert move to an integer so we can handle the error.
        move = int(move)
        if move > 9 or move < 1:
            messagebox.showerror("Error!","You must put a number between 1 and 9 :/")
            return
        # We then convert it back to a string to check with the board dictionnary.
        move = str(move)

        # If the position chosen by the player has not been taken, place the player's marker on the board
        # Otherwise, force the player to pick another position
        if self.board[move] == " ":
            self.board[move] = self.player
            self.count += 1
        else:
            messagebox.showerror("Error!","This place is already taken")
            return
        
        # First adjust the board then make the player pick a number on the board
        self.AdjustBoard()

        # Make the program check for winning conditions
        self.checkWinningConditions()

        # If the count is at 9 and no changes have been made to the game so far, print that the game is a tie
        if self.count == 9:
            messagebox.showinfo("Oops.","It's a tie!")
            return

        # Switch player on each turn
        if self.player == "X":
            self.player = "O"
        else:
            self.player = "X"

    def launch(self,chosenmove):
        if self.count <= 9 and self.gameOver == False:
            self.turn(chosenmove)


from tkinter import *
from tkinter import ttk

class App:
    def __init__(self):
        #Fenetre
        self.fenetre = Tk()
        self.fenetre.title("Tic Tac Toe")
        self.fenetre.minsize(500,300)

        #Frames
        self.frame1 = ttk.Frame(self.fenetre,padding=20)
        self.frame1.grid(row=0,column=0)
        self.frameLabel = ttk.LabelFrame(self.frame1,padding=20,text="Player")
        self.frameLabel.grid(row=2,columnspan=2,padx=10,pady=10,sticky=(W,E))
        self.frame2 = ttk.Frame(self.fenetre,padding=20)
        self.frame2.grid(row=0,column=1)
        
        #Variables
        NumberChosen = IntVar()
        Win_LoseCondition = StringVar()
        player = StringVar()
        Board = StringVar()
        #Launch
        def startTicTacToe():
            global TTT
            TTT = TicTacToe(player.get())
            self.PlayerXRadioButton["state"]="disabled"
            self.PlayerORadioButton["state"]="disabled"
        def submitTicTacToe():
            TTT.launch(NumberChosen)
            Board.set(TTT.getPrintedBoard())
            Win_LoseCondition.set(TTT.getWinningState())
        def restartTicTacToe():
            TTT = TicTacToe(player.get())
            TTT.launch(NumberChosen)
            Board.set(TTT.getPrintedBoard())
            Win_LoseCondition.set(TTT.getWinningState())
        def playTicTacToe():
            TTT = TicTacToe(player.get())
        def close():
            self.fenetre.destroy()
        
        #Widget
        self.PlayButton = ttk.Button(self.frame1,text="Play",command=startTicTacToe)
        self.PlayButton.grid(row=0,column=0,pady = 10,sticky=W,padx = 10)
        self.RestartButton = ttk.Button(self.frame1,text="Restart",command=restartTicTacToe)
        self.RestartButton.grid(row=0,column=1,pady = 10,sticky=E,padx = 10)
        self.ChooseEntry = ttk.Entry(self.frame1,textvariable=NumberChosen)
        self.ChooseEntry.grid(row=1,columnspan=2,sticky=(W,E),padx=10,pady=10)
        self.PlayerXRadioButton = ttk.Radiobutton(self.frameLabel,text="Player X",variable=player,value="x",command=playTicTacToe)
        self.PlayerXRadioButton.grid(sticky=W)
        self.PlayerORadioButton = ttk.Radiobutton(self.frameLabel,text="Player O",variable=player,value="o",command=playTicTacToe)
        self.PlayerORadioButton.grid(sticky=W)
        self.SubmitButton = ttk.Button(self.frame1,text="Submit",command=submitTicTacToe)
        self.SubmitButton.grid(row=3,columnspan=2,padx=10,pady=10)
        self.CloseButton = ttk.Button(self.frame1,text="Close",command=close)
        self.CloseButton.grid(row=4,columnspan=2,padx=10,pady=10)
        self.TicTacToeLabel = ttk.Label(self.frame2,textvariable=Board)
        self.TicTacToeLabel.grid(row=0,column=0)
        self.Win_LoseConditionLabel = ttk.Label(self.frame2,textvariable=Win_LoseCondition)
        self.Win_LoseConditionLabel.grid(row=1,column=0)

        self.fenetre.mainloop()
        
MyInterface = App()
