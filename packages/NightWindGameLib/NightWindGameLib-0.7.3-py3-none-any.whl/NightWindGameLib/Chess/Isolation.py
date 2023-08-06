import random
import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from NightWindGameLib.Chess.chess import (
    Game, GameState, Board,
    strategic_player, human_player,
    random_player
)


from NightWindGameLib.Qt.fixQt import FixPySide2
fix = FixPySide2()
fix.start_fix()


class Ui_Isolation(object):
    def setupUi(self, Isolation):
        if not Isolation.objectName():
            Isolation.setObjectName(u"Isolation")
        Isolation.resize(500, 500)
        self.centralwidget = QWidget(Isolation)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pbtn_list = []
        self.label_title = QLabel(self.centralwidget)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setGeometry(QRect(140, 10, 171, 41))
        font = QFont()
        font.setPointSize(18)
        self.label_title.setFont(font)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.cb_level = QComboBox(self.centralwidget)
        self.cb_level.addItem("")
        self.cb_level.addItem("")
        self.cb_level.addItem("")
        self.cb_level.setObjectName(u"cb_level")
        self.cb_level.setGeometry(QRect(30, 10, 101, 41))
        font1 = QFont()
        font1.setPointSize(15)
        self.cb_level.setFont(font1)
        self.cb_first = QComboBox(self.centralwidget)
        self.cb_first.addItem("")
        self.cb_first.addItem("")
        self.cb_first.setObjectName(u"cb_first")
        self.cb_first.setGeometry(QRect(30, 60, 101, 41))
        self.cb_first.setFont(font1)
        self.pbtn_rule = QPushButton(self.centralwidget)
        self.pbtn_rule.setObjectName(u"pbtn_rule")
        self.pbtn_rule.setGeometry(QRect(310, 10, 181, 41))
        font2 = QFont()
        font2.setPointSize(9)
        self.pbtn_rule.setFont(font2)
        self.label_status = QLabel(self.centralwidget)
        self.label_status.setObjectName(u"label_status")
        self.label_status.setGeometry(QRect(250, 60, 81, 41))
        font3 = QFont()
        font3.setPointSize(13)
        self.label_status.setFont(font3)
        self.label_moves = QLabel(self.centralwidget)
        self.label_moves.setObjectName(u"label_moves")
        self.label_moves.setGeometry(QRect(350, 60, 141, 41))
        self.label_moves.setFont(font3)
        self.pbtn_start = QPushButton(self.centralwidget)
        self.pbtn_start.setObjectName(u"pbtn_start")
        self.pbtn_start.setGeometry(QRect(140, 60, 101, 41))
        self.pbtn_start.setFont(font3)
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(60, 120, 381, 371))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.pbtn_board = QButtonGroup(Isolation)
        self.pbtn_board.setObjectName(u"pbtn_board")
        for i in range(0, 8):
            for j in range(0, 8):
                pbtn = QPushButton(self.gridLayoutWidget)
                pbtn.setFont(font1)
                self.pbtn_board.addButton(pbtn)
                self.gridLayout.addWidget(pbtn, i, j, 1, 1)
                self.pbtn_list.append(pbtn)

        Isolation.setCentralWidget(self.centralwidget)

        self.retranslateUi(Isolation)

        QMetaObject.connectSlotsByName(Isolation)
    # setupUi

    def retranslateUi(self, Isolation):
        for i in range(len(self.pbtn_list)):
            if i == 0:
                self.pbtn_list[i].setText(
                    QCoreApplication.translate("Isolation", u"X", None))
            elif i == 63:
                self.pbtn_list[i].setText(
                    QCoreApplication.translate("Isolation", u"O", None))
            else:
                self.pbtn_list[i].setText(
                    QCoreApplication.translate("Isolation", u"\u00b7", None))

        Isolation.setWindowTitle(
            QCoreApplication.translate("Isolation",
                                       u"\u5b64\u7acb\u6e38\u620f", None))
        self.label_title.setText(
            QCoreApplication.translate("Isolation",
                                       u"\u5b64\u7acb\u6e38\u620f", None))
        self.cb_level.setItemText(0,
                                  QCoreApplication.translate("Isolation",
                                                             u"\u7b80\u5355", None))
        self.cb_level.setItemText(1,
                                  QCoreApplication.translate("Isolation",
                                                             u"\u4e2d\u7b49", None))
        self.cb_level.setItemText(2,
                                  QCoreApplication.translate("Isolation",
                                                             u"\u56f0\u96be", None))

        self.cb_first.setItemText(0,
                                  QCoreApplication.translate("Isolation",
                                                             u"\u5148\u624b", None))
        self.cb_first.setItemText(1,
                                  QCoreApplication.translate("Isolation",
                                                             u"\u540e\u624b", None))

        self.pbtn_rule.setText(
            QCoreApplication.translate("Isolation",
                                       u"\u7b2c\u4e00\u6b21\u73a9\uff1f\u83b7\u53d6\u6e38\u620f\u89c4\u5219",
                                       None))
        self.label_status.setText("")
        self.label_moves.setText("")
        self.pbtn_start.setText(
            QCoreApplication.translate("Isolation",
                                       u"\u5f00\u59cb\u6e38\u620f", None))
        # retranslateUi


class Isolation(Game):
    def __init__(self, width=8, height=8, players=('X', 'O'), to_move='X'):
        self.players = players
        player_squares = {players[0]: (1, 1),
                          players[1]: (width, height)}
        board = IsolationBoard(width, height)
        for player, square in player_squares.items():
            board[square] = player
        self.initial = IsolationState(board=board,
                                      player_squares=player_squares,
                                      to_move=to_move)
        super().__init__(initial=self.initial, players=self.players)

    def moves(self, state):
        return state.open_moves(state.to_move)

    def transition(self, state, move):
        if move not in self.moves(state):
            return state

        player = state.to_move
        board = state.board.new()
        board.update({move: player, state.player_squares[player]: '*'})
        player_squares = state.player_squares.copy()
        player_squares.update({player: move})
        to_move = self.opponent(player)
        return IsolationState(board=board,
                              player_squares=player_squares,
                              to_move=to_move)

    def utility(self, state, player):
        if player == state.to_move:
            return -1
        else:
            return 1


class IsolationState(GameState):
    def __init__(self, board, player_squares, to_move):
        self.board = board
        self.player_squares = player_squares
        self.to_move = to_move
        super().__init__(board=self.board, to_move=self.to_move)

    def open_moves(self, player):
        return self.board.open_squares(self.player_squares[player])


class IsolationBoard(Board):
    def open_squares(self, square):
        open_squares = []
        for delta in ((0, 1), (1, 0), (1, 1), (1, -1)):
            (delta_x, delta_y) = delta
            x, y = square
            x, y = x + delta_x, y + delta_y
            if self.in_board((x, y)) and not self.get((x, y)):
                open_squares.append((x, y))

            x, y = square
            x, y = x - delta_x, y - delta_y
            if self.in_board((x, y)) and not self.get((x, y)):
                open_squares.append((x, y))

        return open_squares

    def in_board(self, square):
        x, y = square
        return 1 <= x <= self.width and 1 <= y <= self.height


def center_evaluation(game, state, player):
    square = state.player_squares[player]
    board = state.board
    center_x, center_y = (board.width + 1) / 2, (board.height + 1) / 2
    return 1 - abs(square[0] - center_x) - abs(square[1] - center_y)


def open_evaluation(game, state, player):
    own_moves = len(state.open_moves(player))
    opp_moves = len(state.open_moves(game.opponent(player)))
    return own_moves - opp_moves


def mixed_evaluation(game, state, player):
    if len(state.board.blank_squares()) / len(state.board.squares) >= 0.6:
        return center_evaluation(game, state, player)
    else:
        return open_evaluation(game, state, player)


def minimax_search(game: Game, state: GameState, depth_limit, eval_fn):
    player = state.to_move

    def max_value(state, depth):
        # 计算子状态中的最大效用值
        if game.terminal_test(state):
            return game.utility(state=state, player=player)
        if depth > depth_limit:
            return eval_fn(game, state, player)

        v = -float('inf')
        for m in game.moves(state):
            v = max(v, min_value(game.transition(state, m), depth + 1))
        return v

    def min_value(state, depth):
        # 计算子状态中的最小效用值
        if game.terminal_test(state):
            return game.utility(state=state, player=player)
        if depth > depth_limit:
            return eval_fn(game, state, player)

        v = float('inf')
        for m in game.moves(state):
            v = min(v, max_value(game.transition(state, m), depth + 1))
        return v

    return max(game.moves(state),
               key=lambda m: min_value(game.transition(state, m), 1))


class Game(QMainWindow, Ui_Isolation):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.pbtn_start.clicked.connect(self.IsoLaTion)
        self.pbtn_rule.clicked.connect(self.get_rule)
        self.info = "游戏规则\n双方位于棋盘对角，由X玩家先手下棋，双方可以移动到" \
                    "和自己当前格子有公共边或公共点的格子中，走过的地方不允许再次被踏足，" \
                    "直到有一方所处格子有公共边或有公共点的格子全部被踏足过，无法移动，游戏结束"

    def get_rule(self):
        QMessageBox.about(self, "游戏规则", self.info)

    def IsoLaTion(self):
        level = self.cb_level.currentText()
        first = self.cb_first.currentText()

        center_player = strategic_player(minimax_search,
                                         depth_limit=4,
                                         eval_fn=center_evaluation)
        open_player = strategic_player(minimax_search,
                                       depth_limit=4,
                                       eval_fn=open_evaluation)
        mixed_player = strategic_player(minimax_search,
                                        depth_limit=4,
                                        eval_fn=mixed_evaluation)
        if first == "先手":
            self.label_status.setText("你是X玩家")
            if level == "简单":
                isolation = Isolation(players=('X', 'O'), to_move='X')
                end = isolation.play_game(
                    dict(X=human_player, O=random_player), verbose=True)
            elif level == "中等":
                isolation = Isolation(players=('X', 'O'), to_move='X')
                end = isolation.play_game(
                    dict(X=human_player,
                         O=random.choice([open_player, center_player])),
                    verbose=True)
            else:
                isolation = Isolation(players=('X', 'O'), to_move='X')
                end = isolation.play_game(
                    dict(X=human_player, O=mixed_player), verbose=True)

            result = isolation.utility(end, 'X')
            if result == 1:
                self.label_status.setText("你赢了！")
            elif result == 0:
                self.label_status.setText("平局！")
            elif result == -1:
                self.label_status.setText("你输了！")

        else:
            self.label_status.setText("你是O玩家")
            if level == "简单":
                isolation = Isolation(players=('X', 'O'), to_move='X')
                end = isolation.play_game(
                    dict(X=center_player, O=human_player), verbose=True)
            elif level == "中等":
                isolation = Isolation(players=('X', 'O'), to_move='X')
                end = isolation.play_game(
                    dict(X=open_player, O=human_player), verbose=True)
            else:
                isolation = Isolation(players=('X', 'O'), to_move='X')
                end = isolation.play_game(
                    dict(X=mixed_player, O=human_player), verbose=True)

            result = isolation.utility(end, 'O')
            if result == 1:
                self.label_status.setText("你赢了！")
            elif result == 0:
                self.label_status.setText("平局！")
            elif result == -1:
                self.label_status.setText("你输了！")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Game()
    sys.exit(app.exec_())
