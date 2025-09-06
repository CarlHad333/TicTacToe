from random import choice
import math
import time


class Board():
    def __init__(self, grid=None):
        if grid == None:
            self._grid = [[" ", " ", " "],
                          [" ", " ", " "],
                          [" ", " ", " "]]
        else:
            self._grid = grid

    def empty_spots(self):
        res = []
        linear_board = self._grid[0]+self._grid[1]+self._grid[2]
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

    def get_board(self):
        i = 1
        boardList = []

        for row in self._grid:
            subBoardList = []
            for element in row:
                if element == ' ':
                    subBoardList.append(str(i))
                else:
                    subBoardList.append(element)
                i += 1
            boardList.append(subBoardList)
            subBoardList = []

        return boardList


class Player():
    def __init__(self, player_symbol, opponent_symbol):
        self.name = self.setName()
        self.player_symbol = player_symbol
        self.opponent_symbol = opponent_symbol
        self.turn = False
        self.scores = {'Tie': 0, player_symbol: 1, opponent_symbol: -1}

class HumanPlayer(Player):
    def __init__(self, player_symbol, opponent_symbol):
        super().__init__(player_symbol, opponent_symbol)

    def put_mark(self, game, BoardIndex):
        return BoardIndex


class RandomerPlayer(Player):

    def __init__(self, player_symbol, opponent_symbol):
        super().__init__(player_symbol, opponent_symbol)

    def put_mark(self, game, BoardIndex):
        print(self.player_symbol + "'s turn.")
        return choice(game.board.empty_spots())



class MinimaxPlayer(Player):

    def __init__(self, player_symbol, opponent_symbol):
        super().__init__(player_symbol, opponent_symbol)

    def put_mark(self, game, BoardIndex):
        def BestMove():
            copy_board = Board(game.board.getBoard())
            bestscore = -math.inf
            bestmove = ()

            def minimax(copy_board, depth, alpha, beta, isMaximizing):
                result = game.check_winner(copy_board)
                if result != " ":
                    game.winner = " "
                    return self.scores[result]

                if isMaximizing:
                    bestscore = -math.inf
                    for i in range(0, 3):
                        for j in range(0, 3):
                            if copy_board.getSpot(i, j) == " ":
                                copy_board.setSpot(i, j, self.player_symbol)
                                score = minimax(
                                    copy_board, depth + 1, alpha, beta, False)
                                copy_board.setSpot(i, j, " ")
                                bestscore = max(score, bestscore)
                                alpha = max(alpha, bestscore)
                                if beta <= alpha:
                                    break
                    return bestscore

                else:
                    bestscore = +math.inf
                    for i in range(0, 3):
                        for j in range(0, 3):
                            if copy_board.getSpot(i, j) == " ":
                                copy_board.setSpot(i, j, self.opponent_symbol)
                                score = minimax(
                                    copy_board, depth + 1, alpha, beta, True)
                                copy_board.setSpot(i, j, " ")
                                bestscore = min(score, bestscore)
                                beta = min(beta, bestscore)
                                if beta <= alpha:
                                    break
                    return bestscore

            for i in range(0, 3):
                for j in range(0, 3):
                    if copy_board.getSpot(i, j) == " ":
                        copy_board.setSpot(i, j, self.player_symbol)
                        score = minimax(copy_board, 0, -
                                        math.inf, +math.inf, False)
                        copy_board.setSpot(i, j, " ")
                        if score > bestscore:
                            bestscore = score
                            bestmove = (i, j)

            return 3*bestmove[0]+bestmove[1]

        return BestMove()


class TicTacToe():
    possible_players = {"H": HumanPlayer,
                        "R": RandomerPlayer,
                        "M": MinimaxPlayer}

    def __init__(self):
        self.board = Board()
        self.playerX = Player("X", "O")
        self.playerO = Player("O", "X")
        self.players_dict = {}
        self.winner = " "
        self.playing_symbol = "X"
        self.opponent_symbol = "O"

    def check_winner(self, board):
        EmptySpaceOnBoard = board.count_blanks()
        self.CheckWinning(board)

        if (self.winner == " " and EmptySpaceOnBoard == 0):
            self.winner = "Tie"

        return self.winner

    def setPlayers(self, genreX, genreO):
        self.playerX = TicTacToe.possible_players[genreX]("X", "O")
        self.playerO = TicTacToe.possible_players[genreO]("O", "X")
        self.players_dict = {"X": self.playerX, "O": self.playerO}

    def do_turn(self, BoardIndex):
        if self.playing_symbol == "X":
            self.player = self.playerX
            self.playing_symbol = "O"
            self.opponent_symbol = "X"
        else:
            self.player = self.playerO
            self.playing_symbol = "X"
            self.opponent_symbol = "O"

        # spot = self.player.put_mark(self, BoardIndex=0)
        spot = BoardIndex
        self.board.setSpot(spot//3, spot % 3, self.playing_symbol)

        report = {"board": self.board.get_board(),
                  "game_finished": self.CheckGameDone(),
                  "winner": self.winner,
                  "Player1": self.playing_symbol,
                  "Player2": self.opponent_symbol}

        return report

    def CheckWinning(self, board):
        for i in range(3):
            if board.getSpot(i, 0) == board.getSpot(i, 1) == board.getSpot(i, 2) != " ":
                self.winner = board.getSpot(i, 0)
                return True
            if board.getSpot(0, i) == board.getSpot(1, i) == board.getSpot(2, i) != " ":
                self.winner = board.getSpot(0, i)
                return True
        if board.getSpot(0, 0) == board.getSpot(1, 1) == board.getSpot(2, 2) != " ":
            self.winner = board.getSpot(0, 0)
            return True
        if board.getSpot(0, 2) == board.getSpot(1, 1) == board.getSpot(2, 0) != " ":
            self.winner = board.getSpot(0, 2)
            return True
        else:
            return False

    def CheckGameDone(self):
        if self.CheckWinning(self.board) or self.board.count_blanks() == 0:
            return True
        return False


if __name__ == '__main__':
    start = time.time()
    t = TicTacToe()
    i = 0
    while not t.CheckGameDone():
        if player == "X":
            t.do_turn("X")
            player = "O"
        else:
            t.do_turn("O")
            player = "X"

    print("Time Taken: " + str(time.time() - start))
