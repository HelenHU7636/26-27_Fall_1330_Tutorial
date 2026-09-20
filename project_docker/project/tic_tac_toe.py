"""A small container demo. Run with: python tic_tac_toe.py"""
import curses
import os
import random
import sys

LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)


def winner(board):
    for a, b, c in LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return None


def available_moves(board):
    return [i for i, cell in enumerate(board) if cell == " "]


def computer_move(board):
    """Win if possible, block an immediate loss, then choose a free square."""
    choices = available_moves(board)
    if not choices:
        raise ValueError("There are no free squares.")
    for mark in ("O", "X"):
        for move in choices:
            trial = board.copy()
            trial[move] = mark
            if winner(trial) == mark:
                return move
    if 4 in choices:
        return 4
    return random.choice(choices)


WIDTH = 80
HEIGHT = 24


STYLES = {
    "title": curses.A_BOLD, "X": curses.A_BOLD, "O": curses.A_BOLD,
    "success": curses.A_BOLD, "warning": curses.A_BOLD, "muted": curses.A_DIM,
}


def setup_colours():
    """Use the terminal background and retain readable monochrome fallbacks."""
    if not curses.has_colors():
        return
    try:
        curses.start_color()
        background = -1
        try:
            curses.use_default_colors()
        except curses.error:
            background = curses.COLOR_BLACK
        for number, (name, foreground) in enumerate((
            ("title", curses.COLOR_CYAN), ("X", curses.COLOR_CYAN),
            ("O", curses.COLOR_YELLOW), ("success", curses.COLOR_GREEN),
            ("warning", curses.COLOR_RED),
        ), start=1):
            curses.init_pair(number, foreground, background)
            STYLES[name] = curses.color_pair(number) | curses.A_BOLD
    except curses.error:
        pass  # Limited-colour terminals keep the remaining fallback styles.


def put(screen, row, text, style=0):
    """Keep every line inside the game area, avoiding the last terminal cell."""
    screen.addnstr(row, 0, text, WIDTH - 1, style)


def draw_screen(screen, board, message, replay):
    screen.erase()
    put(screen, 0, "TIC-TAC-TOE", STYLES["title"])
    put(screen, 2, "You are X. The computer is O.")
    screen.addstr(2, 8, "X", STYLES["X"])
    screen.addstr(2, 26, "O", STYLES["O"])
    put(screen, 3, "Get three in a row, column or diagonal.")
    for row in range(3):
        cells = [board[row * 3 + col] for col in range(3)]
        cells = [str(row * 3 + col + 1) if cell == " " else cell
                 for col, cell in enumerate(cells)]
        put(screen, 6 + row * 2, "  " + "  |  ".join(cells))
        for col in range(3):
            mark = board[row * 3 + col]
            screen.addstr(6 + row * 2, 2 + col * 6, cells[col],
                          STYLES.get(mark, STYLES["muted"]))
        if row < 2:
            put(screen, 7 + row * 2, "-----+-----+-----")
    style = 0
    if message == "You win!":
        style = STYLES["success"]
    elif message.startswith("Computer"):
        style = STYLES["O"]
    elif message.startswith(("Press one", "That square")):
        style = STYLES["warning"]
    put(screen, 13, message, style)
    put(screen, 15, "Play again? Press y or n." if replay
        else "Press a square (1-9), or q to quit. No Enter needed.")
    screen.refresh()


def read_key(screen, board, message, replay=False):
    """Pause while undersized; polling also detects terminal resizes."""
    previous = None
    while True:
        actual = os.get_terminal_size(sys.stdin.fileno())
        size = (max(1, actual.lines), max(1, actual.columns))
        if size != screen.getmaxyx():
            curses.resizeterm(*size)
        if size != previous:
            previous = size
            if size[0] >= HEIGHT and size[1] >= WIDTH:
                draw_screen(screen, board, message, replay)
            else:
                screen.erase()
                # Short, clipped lines also work in very small terminals.
                for row, line in enumerate(("Resize to 80 x 24", "Press q to quit")):
                    if row < size[0] and size[1] > 1:
                        screen.addnstr(row, 0, line, size[1] - 1)
                screen.refresh()
        try:
            key = screen.get_wch()
        except curses.error:  # No key during the timeout.
            continue
        if key == curses.KEY_RESIZE:
            previous = None
            continue
        if key in ("q", "Q", "\x03"):
            return "q"
        if size[0] < HEIGHT or size[1] < WIDTH:
            continue  # Discard input while paused; never advance the game.
        if isinstance(key, str):
            return key.lower()


def play_round(screen, human_first=True):
    board = [" "] * 9
    human_turn = human_first
    message = "You go first." if human_first else "Computer goes first."
    while True:
        if human_turn:
            answer = read_key(screen, board, message)
            if answer == "q":
                return False
            if answer not in tuple("123456789"):
                message = "Press one number from 1 to 9."
                continue
            move = int(answer) - 1
            if board[move] != " ":
                message = "That square is occupied. Choose an empty one."
                continue
            board[move] = "X"
        else:
            move = computer_move(board)
            board[move] = "O"
            message = f"Computer chooses square {move + 1}."

        result = winner(board)
        if result or not available_moves(board):
            message = {"X": "You win!", "O": "Computer wins. Try again!"}.get(
                result, "It's a draw."
            )
            while True:
                answer = read_key(screen, board, message, replay=True)
                if answer in ("y", "n", "q"):
                    return answer == "y"
        human_turn = not human_turn


def run_game(screen):
    setup_colours()
    curses.noecho()
    screen.keypad(True)
    screen.timeout(100)
    try:
        curses.curs_set(0)
    except curses.error:
        pass  # Some terminals cannot hide the cursor.
    human_first = True
    while play_round(screen, human_first):
        human_first = not human_first


def main():
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        print("Run this game in an interactive terminal (without -T).")
        return
    # Environment dimensions are layout defaults, not physical window size.
    # Let curses read the PTY size and react to host-window resize events.
    os.environ.pop("COLUMNS", None)
    os.environ.pop("LINES", None)
    curses.use_env(False)
    try:
        curses.wrapper(run_game)
    except KeyboardInterrupt:
        pass
    print("Thanks for playing!")


if __name__ == "__main__":
    main()
