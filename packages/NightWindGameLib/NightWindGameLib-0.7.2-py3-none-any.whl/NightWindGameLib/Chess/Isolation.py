import random
try:
    from .chess import (
        Game, GameState,
        Board, human_player,
        strategic_player,
        random_player
    )
except ImportError:
    from chess import (
        Game, GameState,
        Board, human_player,
        strategic_player,
        random_player
    )


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


def isoLaTion():
    level = input("请选择难度：简单/中等/较难")
    while level != "简单" and level != "中等" and level != "较难":
        print("难度输入有误，请重新选择！")
        level = input("请选择难度：简单或较难")

    first = input("你想先手还是后手？")
    while first != "先手" and first != "后手":
        print("先后手输入有误，请重新选择！")
        first = input("你想先手还是后手？")

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
        print("你是X玩家，电脑为O玩家")
        if level == "简单":
            isolation = Isolation(players=('X', 'O'), to_move='X')
            end = isolation.play_game(
                dict(X=human_player, O=random_player), verbose=True)
        elif level == "中等":
            isolation = Isolation(players=('X', 'O'), to_move='X')
            end = isolation.play_game(
                dict(X=human_player, O=random.choice([open_player, center_player])),
                verbose=True)
        else:
            isolation = Isolation(players=('X', 'O'), to_move='X')
            end = isolation.play_game(
                dict(X=human_player, O=mixed_player), verbose=True)

        result = isolation.utility(end, 'X')
        if result == 1:
            print("你赢了！")
        elif result == 0:
            print("平局！")
        elif result == -1:
            print("你输了！")

    else:
        print("电脑为X玩家，你是O玩家")
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
            print("你赢了！")
        elif result == 0:
            print("平局！")
        elif result == -1:
            print("你输了！")


if __name__ == "__main__":
    isoLaTion()
