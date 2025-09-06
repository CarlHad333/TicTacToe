from random import choice, randint
import math
import time

class Board():
    def __init__(self, grid = None):
        if grid == None:
            self._grid = [[" ", " ", " "],
                          [" ", " ", " "],
                          [" ", " ", " "]]
        else:
            self._grid = grid

    def empty_spots(self):
        res = []
        linear_board=self._grid[0]+self._grid[1]+self._grid[2]
        for i, s in enumerate(linear_board):
            if s == " ":
                res.append(i)
        return res

    def count_blanks(self):
        return len(self.empty_spots())

    def getBoard(self):
        return self._grid
    
    def setSpot(self, index_x, index_y, value):
        self._grid[index_x][index_y] = value

    def getSpot(self, index_x, index_y):
        return self._grid[index_x][index_y]
        
    def print_board(self):
        print("")
        i = 1
        for row in self._grid:
            for element in row:
                if element == " ":
                    print('| ' + str(i) + ' | ',end=" ")
                else:
                    print('| ' + str(element) + ' | ',end=" ")
                i += 1
            print("")
        print("")

        
class Player():
    def __init__(self, player_symbol, opponent_symbol, CLI=False):
        self.name=self._setAutoName()
        self.player_symbol=player_symbol
        self.opponent_symbol=opponent_symbol
        self.turn=False
        self.scores = { 'Tie': 0, player_symbol: 1, opponent_symbol: -1 }
    
    def _setAutoName(self):
        pass
        
    def put_mark(self, game):
        pass


class HumanPlayer(Player):
    count=0
    def __init__(self, player_symbol, opponent_symbol, CLI=False):
        self._isCLI = CLI
        super().__init__(player_symbol,opponent_symbol)
        

    def setName(self, username=f"Player{randint(0,100)}"):
        if self._isCLI:
            username = input("Insert the player's name: ")
        return username
    
    def _setAutoName(self):
        return self.setName()
    
    def put_mark(self, game):
        if self._isCLI:
            while self.turn:
                try:
                    spot = int(input(self.name + "'s turn. (" + self.player_symbol + ") Input your move (1-9): "))
                    spot -= 1
                    # spot = int(CurrentTurnInfos[m])
                    if spot not in game.board.empty_spots():
                        raise ValueError
                    self.turn=False
                except ValueError:
                    print("Invalid spot! Choose another one:",game.board.empty_spots())
            return spot

    
class RandomerPlayer(Player):
    count=0
    def __init__(self, player_symbol, opponent_symbol, CLI=False):
        super().__init__(player_symbol, opponent_symbol, CLI=False)
        RandomerPlayer.count+=1

    def _setAutoName(self):
        if RandomerPlayer.count==1:
            return "DumDum Bot"
        return "Random Bot, the Confused Walker"
    
    def put_mark(self, game):
        print(self.name + "'s turn. (" + self.player_symbol + "):")
        return choice(game.board.empty_spots())


class MinimaxPlayer(Player):
    count=0
    def __init__(self, player_symbol, opponent_symbol, CLI=False):
        super().__init__(player_symbol, opponent_symbol, CLI=False)
        MinimaxPlayer.count+=1

    def _setAutoName(self):
        if MinimaxPlayer.count==1:
            return "Unbeatable Bot"
        return "Minimax Bot, the Expert"

    def put_mark(self, game):
        print(self.name + "'s turn. (" + self.player_symbol + "):")
        copy_board = Board(game.board.getBoard())
        bestscore = -math.inf
        bestmove = ()
        def minimax(copy_board, alpha, beta, isMaximizing):
            result = game.check_winner(copy_board)
            if result != " ":
                game.winner = " "
                return self.scores[result]
            if isMaximizing:
                bestscore = -math.inf
                for i in range(0,3):
                    for j in range(0,3):
                        if copy_board.getSpot(i,j) == " ":
                            copy_board.setSpot(i, j, self.player_symbol)
                            score = minimax(copy_board, alpha, beta, False)
                            copy_board.setSpot(i, j, " ")
                            bestscore = max(score,bestscore)
                            alpha = max(alpha,bestscore)
                            if beta <= alpha:
                                break
                return bestscore
            else:
                bestscore = +math.inf
                for i in range(0,3):
                    for j in range(0,3):
                        if copy_board.getSpot(i,j) == " ":
                            copy_board.setSpot(i, j, self.opponent_symbol)
                            score = minimax(copy_board, alpha, beta, True)
                            copy_board.setSpot(i, j, " ")
                            bestscore = min(score, bestscore)
                            beta = min(beta, bestscore)
                            if beta <= alpha:
                                break
                return bestscore
        for i in range(0,3):
            for j in range(0,3):
                if copy_board.getSpot(i,j) == " ":
                    copy_board.setSpot(i, j, self.player_symbol)
                    score = minimax(copy_board, -math.inf, +math.inf, False)
                    copy_board.setSpot(i, j, " ")
                    if score > bestscore:
                        bestscore = score
                        bestmove = ( i, j )
        return 3*bestmove[0]+bestmove[1]
        

class TicTacToe():
    possible_players = { "H": HumanPlayer,
                         "R": RandomerPlayer,
                         "M": MinimaxPlayer}
    
    def __init__(self, CLI=False):
        self.board = Board()
        self._isCLI=CLI
        if CLI:
            self.setPlayersCLI()
        self.winner = " "

    def check_winner(self,board):
        EmptySpaceOnBoard = board.count_blanks()
        self.CheckWinning(board)

        if (self.winner == " " and EmptySpaceOnBoard == 0):
            return "Tie"
        else:
            return self.winner
    
    def setPlayersCLI(self):
        def _setPlayer(player_symbol, opponent_symbol):
            done = False
            while not done:
                try:
                    genre = input(f"Who is player {player_symbol} ? (insert H:Human, R:Random, M:Minimax)\n")
                    # genre = get_playerInfo(player_symbol)[k]
                    player = TicTacToe.possible_players[genre](player_symbol,opponent_symbol,True)
                    done = True
                except KeyError as e:
                    print("error: " + str(e))
                except Exception as e:
                    print("error: " + str(e))
            return player
        self.playerX = _setPlayer("X","O")
        self.playerO = _setPlayer("O","X")
        self.players_dict = {"X":self.playerX, "O":self.playerO}
    
    def setPlayers(self, genreX, genreO):
        self.playerX = TicTacToe.possible_players[genreX]("X", "O")
        self.playerO = TicTacToe.possible_players[genreO]("O", "X")
        self.players_dict = {"X":self.playerX, "O":self.playerO}
    
    def _do_turn(self, player):
        player.turn=True
        print("")
        spot = player.put_mark(self)
        self.board.setSpot(spot//3, spot%3, player.player_symbol)
        self.board.print_board()
        player.turn=False
        
    def CheckWinning(self,board):
        for i in range(3):
            if board.getSpot(i,0) == board.getSpot(i,1) == board.getSpot(i,2) != " ":
                self.winner = board.getSpot(i,0)
                return True
            if board.getSpot(0,i) == board.getSpot(1,i) == board.getSpot(2,i) != " ":
                self.winner = board.getSpot(0,i)
                return True
        if board.getSpot(0,0) == board.getSpot(1,1) == board.getSpot(2,2) != " ":
            self.winner = board.getSpot(0,0)
            return True
        if board.getSpot(0,2) == board.getSpot(1,1) == board.getSpot(2,0) != " ":
            self.winner = board.getSpot(0,2)
            return True
        else:
            return False
    
    def CheckGameDone(self):
        if self.CheckWinning(self.board) or self.board.count_blanks() == 0:
            return True
        return False
    
    def playCLI(self, starting_symbol):
        playing = starting_symbol
        print("Game started!")
        start = time.time()
        self.board.print_board()
        while not self.CheckGameDone():
            if playing == "X":
                self._do_turn(self.playerX)
                playing = "O"
            else:
                self._do_turn(self.playerO)
                playing = "X"
        print("Time Taken: " + str(time.time() - start))
        if self.winner != " ":
            print(self.winner,"wins! Congrats", self.players_dict[self.winner].name)
        else:
            print("Tie!")
            
    def playCLI(self, starting_symbol):
        playing = starting_symbol
        print("Game started!")
        start = time.time()
        self.board.print_board()
        while not self.CheckGameDone():
            if playing == "X":
                self._do_turn(self.playerX)
                playing = "O"
            else:
                self._do_turn(self.playerO)
                playing = "X"
        print("Time Taken: " + str(time.time() - start))
        if self.winner != " ":
            print(self.winner,"wins! Congrats", self.players_dict[self.winner].name)
        else:
            print("Tie!")


if __name__ == '__main__':
    t = TicTacToe(True)
    t.playCLI("X")
