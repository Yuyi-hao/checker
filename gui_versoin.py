
from pyray import *

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 900
PRIMARY_BOARD_COLOR = Color(54, 22, 7, 100)
SECOND_BOARD_COLOR = Color(5, 56, 18, 100)
DANGER_CELL_COLOR = Color(255, 0, 8, 75)
BLACK_PIECE_COLOR = Color(100, 100, 100, 100)
WHITE_PIECE_COLOR = Color(179, 121, 80, 100)
MOVES_COLOR = Color(10, 18, 247, 100)
BOARD_WIDTH = 640
BOARD_HEIGHT = 640
CELL_SIZE = 80
BOARD_POS_X = (WINDOW_WIDTH - BOARD_WIDTH)//2
BOARD_POS_Y = (WINDOW_HEIGHT - BOARD_HEIGHT)//2
PIECE_COLOR_DICT = {
    1: WHITE_PIECE_COLOR,
    2: BLACK_PIECE_COLOR,
    3: MOVES_COLOR
}

# GAME VARIABLE
"""
WHITE = 1
BLACK = 2

"""

GAME_GRID = [[0]*8 for _ in range(8)]
WHITE_PIECES_POSITIONS = []
BLACK_PIECES_POSITIONS = []
WHITE_KINGS = set()
BLACK_KINGS = set()

def init_game_grid():
    # initialize grid
    
    global GAME_GRID
    GAME_GRID = [[0]*8 for _ in range(8)]
    global WHITE_PIECES_POSITIONS
    WHITE_PIECES_POSITIONS.clear()
    global BLACK_PIECES_POSITIONS
    BLACK_PIECES_POSITIONS.clear()
    global WHITE_KINGS
    WHITE_KINGS.clear()
    global BLACK_KINGS
    BLACK_KINGS.clear()
    
    for row in range(3):
        for col in range(8):
            if row&1 == col&1:
                GAME_GRID[row][col] = 1
                WHITE_PIECES_POSITIONS.append((row, col))
                
    for row in range(5, 8):
        for col in range(8):
            if row&1 == col&1:
                GAME_GRID[row][col] = 2
                BLACK_PIECES_POSITIONS.append((row, col))
                  


def draw_board(moves, danger):
    # Draw board
    draw_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, Color(30, 30, 30, 100))
    for row in range(8):
        for col in range(8):
            x = BOARD_POS_X + (col*CELL_SIZE)
            y = BOARD_POS_Y + (row*CELL_SIZE)
            if row&1 and col&1 or (not row&1 and not col&1):
                draw_rectangle(x, y, CELL_SIZE, CELL_SIZE, SECOND_BOARD_COLOR)
            else:
                draw_rectangle(x, y, CELL_SIZE, CELL_SIZE, PRIMARY_BOARD_COLOR)
            if (row, col) in danger:
                draw_rectangle(x, y, CELL_SIZE, CELL_SIZE, DANGER_CELL_COLOR)
                
            if GAME_GRID[row][col] != 0:
                draw_circle(x+40, y+40, 30, PIECE_COLOR_DICT[GAME_GRID[row][col]])
            if (row, col) in moves:
                draw_circle(x+40, y+40, 20, PIECE_COLOR_DICT[3])
            if (row, col) in WHITE_KINGS or (row, col) in BLACK_KINGS:
                draw_circle(x+40, y+40, 10, YELLOW)
        

    # draw border
    draw_rectangle_lines_ex(Rectangle(BOARD_POS_X-5, BOARD_POS_Y-5, BOARD_WIDTH+10, BOARD_HEIGHT+10), 5, ORANGE)


def handle_mouse_click(mouse_pos):
    x, y = mouse_pos.x, mouse_pos.y
    cell_x, cell_y = None, None
    if(BOARD_POS_X <= x <= BOARD_POS_X+BOARD_WIDTH and  BOARD_POS_Y <= y <=BOARD_POS_Y+ BOARD_HEIGHT):
        original_x = x - BOARD_POS_X
        original_y = y - BOARD_POS_Y
        cell_x, cell_y = int(original_x//CELL_SIZE), int(original_y//CELL_SIZE)
    return cell_y, cell_x

def get_moves(grid, piece_row, piece_col, king=False):
    piece = grid[piece_row][piece_col]
    dr = 1 # delta row
    
    if piece == 2:
        dr *= -1
    moves = []
    if 0 <= piece_row+dr <= 7 and 0 <= piece_col+1 <= 7 and  grid[piece_row+dr][piece_col+1] == 0:
        moves.append((piece_row+dr, piece_col+1))
    if 0 <= piece_row+dr <= 7 and 0 <= piece_col-1 <= 7 and  grid[piece_row+dr][piece_col-1] == 0:
        moves.append((piece_row+dr, piece_col-1))

    dr2 = 2
    if piece == 2:
        dr2 *= -1
    if 0 <= piece_row+dr2 <= 7 and 0 <= piece_col+2 <= 7 and  grid[piece_row+dr2][piece_col+2] == 0:
        if grid[piece_row+dr][piece_col+1] != 0 and grid[piece_row+dr][piece_col+1] != piece:
            moves.append((piece_row+dr2, piece_col+2))
    if 0 <= piece_row+dr2 <= 7 and 0 <= piece_col-2 <= 7 and  grid[piece_row+dr2][piece_col-2] == 0:
        if grid[piece_row+dr][piece_col-1] != 0 and grid[piece_row+dr][piece_col-1] != piece:
            moves.append((piece_row+dr2, piece_col-2))

    if king:
        dr *= -1
        dr2 *= -1 
        if 0 <= piece_row+dr <= 7 and 0 <= piece_col+1 <= 7 and  grid[piece_row+dr][piece_col+1] == 0:
            moves.append((piece_row+dr, piece_col+1))
        if 0 <= piece_row+dr <= 7 and 0 <= piece_col-1 <= 7 and  grid[piece_row+dr][piece_col-1] == 0:
            moves.append((piece_row+dr, piece_col-1))
        if 0 <= piece_row+dr2 <= 7 and 0 <= piece_col+2 <= 7 and  grid[piece_row+dr2][piece_col+2] == 0:
            if grid[piece_row+dr][piece_col+1] != 0 and grid[piece_row+dr][piece_col+1] != piece:
                moves.append((piece_row+dr2, piece_col+2))
        if 0 <= piece_row+dr2 <= 7 and 0 <= piece_col-2 <= 7 and  grid[piece_row+dr2][piece_col-2] == 0:
            if grid[piece_row+dr][piece_col-1] != 0 and grid[piece_row+dr][piece_col-1] != piece:
                moves.append((piece_row+dr2, piece_col-2))
   
    return moves

def update_game_grid(grid, piece_row, piece_col, move):
    move_row, move_col = move
    grid[piece_row][piece_col], grid[move_row][move_col] = grid[move_row][move_col], grid[piece_row][piece_col]
    if abs(piece_row - move_row) > 1:
        if move_row - piece_row < 0:
            if move_col - piece_col < 0:
                return (piece_row - 1, piece_col - 1)
            else:
                return (piece_row - 1, piece_col + 1)
        else:
            if move_col - piece_col < 0:
                return (piece_row + 1, piece_col - 1)
            else:
                return (piece_row + 1, piece_col + 1)
    return () 


def check_game_status(white_count, black_count):
    if white_count == 0 or black_count == 0:
        return False, 1 if white_count > black_count else 2
    moves = 0
    for row, col  in WHITE_PIECES_POSITIONS:
        moves += len(get_moves(GAME_GRID, row, col, ((row, col) in WHITE_KINGS) or ((row, col) in BLACK_KINGS)))

    if not moves:
        return False, 0
    
    moves = 0
    for row, col  in BLACK_PIECES_POSITIONS:
        moves += len(get_moves(GAME_GRID, row, col, ((row, col) in WHITE_KINGS) or ((row, col) in BLACK_KINGS)))
    if not moves:
        return False, 0
    
    return True, 0
    
def draw_player_status(player, color):
    n = player
    # background
    startx = 10
    starty = BOARD_POS_Y if color == 1 else BOARD_POS_Y + 320 + 5
    width = BOARD_POS_X - 25
    height = 320
    background_rect = (startx, starty, width, height)
    draw_rectangle_rounded(background_rect, 0.10, 4, Color(50, 50, 50, 100))
    # name
    draw_text(f"Player: {color}", startx+25, starty + 30, 25, BLUE)
    
    for col in range(2):
        for row in range(6):
            if n:
                x = startx + 35 + col* (width//2)
                y = starty + 100 + row * 35
                draw_circle(x, y, 10, PIECE_COLOR_DICT[color])
                n -= 1

                
def main():
    init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Checker")
    # initialize grid
    init_game_grid()
    moves = []
    danger_cells = []
    turn = 2
    status = "menu"
    winning = None
    while not window_should_close():
        begin_drawing()

        if status == "game":
            draw_board(moves, danger_cells)
            draw_player_status(len(WHITE_PIECES_POSITIONS), 1)
            draw_player_status(len(BLACK_PIECES_POSITIONS), 2)

            if is_mouse_button_down(MOUSE_LEFT_BUTTON):
                mouse_pos = get_mouse_position()
                # if game_running:
                click_row, click_col= handle_mouse_click(mouse_pos)
                print(click_row, click_col)
                if click_row != None and click_col != None and 0 <= click_row <= 7 and 0<= click_col <= 7 :
                    if GAME_GRID[click_row][click_col] == turn:
                        selected_piece_row, selected_piece_col = click_row, click_col
                        moves = get_moves(GAME_GRID, selected_piece_row, selected_piece_col, ((selected_piece_row, selected_piece_col) in WHITE_KINGS) or ((selected_piece_row, selected_piece_col) in BLACK_KINGS))
                    elif moves and (click_row, click_col) in moves:
                        taken_piece = update_game_grid(GAME_GRID, selected_piece_row, selected_piece_col, (click_row, click_col))
                        if (click_row == 0) or click_row == 7:
                            if turn == 1 and click_row == 7:
                                WHITE_KINGS.add((click_row, click_col))
                            elif turn == 2 and click_row == 0:
                                BLACK_KINGS.add((click_row, click_col))
                        moves.clear()
                        if turn == 1:
                            WHITE_PIECES_POSITIONS.remove((selected_piece_row, selected_piece_col))
                            WHITE_PIECES_POSITIONS.append((click_row, click_col))
                            if (selected_piece_row, selected_piece_col) in WHITE_KINGS:
                                WHITE_KINGS.remove((selected_piece_row, selected_piece_col))
                                WHITE_KINGS.add((click_row, click_col))
                        else:
                            BLACK_PIECES_POSITIONS.remove((selected_piece_row, selected_piece_col))
                            BLACK_PIECES_POSITIONS.append((click_row, click_col))
                            if (selected_piece_row, selected_piece_col) in BLACK_KINGS:
                                BLACK_KINGS.remove((selected_piece_row, selected_piece_col))
                                BLACK_KINGS.add((click_row, click_col))
                        if taken_piece:
                            turn = turn
                            if turn == 1:
                                BLACK_PIECES_POSITIONS.remove(taken_piece)
                                if taken_piece in BLACK_KINGS:
                                    BLACK_KINGS.remove(taken_piece)
                            elif turn == 2:
                                WHITE_PIECES_POSITIONS.remove(taken_piece)
                                if taken_piece in WHITE_KINGS:
                                    WHITE_KINGS.remove(taken_piece)
                            GAME_GRID[taken_piece[0]][taken_piece[1]] = 0
                        else:
                            turn = 1 if turn == 2 else 2
            game_status, winning = check_game_status(len(WHITE_PIECES_POSITIONS), len(BLACK_PIECES_POSITIONS))
            if not game_status:
                status = "game over"
        elif status == "game over":
            draw_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, BLACK)
            draw_text(f"Game over", 100, 100, 50, BLUE)
            if winning:
                game_text = f"Player {winning} won"
            else:
                game_text = "This is draw"
            draw_text(game_text, 100, 300, 50, WHITE)
            # play button
            play_again_btn = Rectangle(WINDOW_WIDTH // 2 - 100, 500, 200, 40)
            draw_rectangle(int(play_again_btn.x), int(play_again_btn.y), int(play_again_btn.width), int(play_again_btn.height), BLUE)
            draw_text("Play Again", int(play_again_btn.x)+20,int(play_again_btn.y)+5, 30, WHITE)
            menu_btn = Rectangle(WINDOW_WIDTH // 2 - 100, 570, 200, 40)
            draw_rectangle(int(menu_btn.x), int(menu_btn.y), int(menu_btn.width), int(menu_btn.height), BLUE)
            draw_text("Menu", int(menu_btn.x)+20,int(menu_btn.y)+5, 30, WHITE)
            if is_mouse_button_down(MOUSE_LEFT_BUTTON):
                mouse_pos = get_mouse_position()
                if play_again_btn.x <= mouse_pos.x <= play_again_btn.x+play_again_btn.width  and play_again_btn.y <= mouse_pos.y <= play_again_btn.y + play_again_btn.height:
                    init_game_grid()
                    status = "game"
                elif menu_btn.x <= mouse_pos.x  <= menu_btn.x + menu_btn.width and menu_btn.y <= mouse_pos.y <= menu_btn.y + menu_btn.height:
                    status = "menu"
                    
        if status == "menu":
            draw_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, Color(100, 100, 100, 100))
            play_btn = Rectangle(WINDOW_WIDTH // 2 - 100, 380, 200, 40)
            draw_rectangle(int(play_btn.x), int(play_btn.y), int(play_btn.width), int(play_btn.height), BLUE)
            draw_text("Play", int(play_btn.x)+20,int(play_btn.y)+5, 30, WHITE)
            help_btn = Rectangle(WINDOW_WIDTH // 2 - 100, 430, 200, 40)
            draw_rectangle(int(help_btn.x), int(help_btn.y), int(help_btn.width), int(help_btn.height), BLUE)
            draw_text("Help", int(help_btn.x)+20,int(help_btn.y)+5, 30, WHITE)
            if is_mouse_button_down(MOUSE_LEFT_BUTTON):
                mouse_pos = get_mouse_position()
                if play_btn.x <= mouse_pos.x <= play_btn.x+play_btn.width  and play_btn.y <= mouse_pos.y <= play_btn.y + play_btn.height:
                    init_game_grid()
                    status = "game"
                elif help_btn.x <= mouse_pos.x <= help_btn.x + help_btn.width and help_btn.y <= mouse_pos.y <= help_btn.y + help_btn.height:
                    status = "help"

        elif status == "help":
            satus = "menu"
            
        end_drawing()
    close_window()
        
if __name__=="__main__":
    main()
