from chess_const import *
from chess import *

chess = Chess()
chess.print_board()


mouse_pressed = False
mouse_clicked = False
is_src_set = False
is_target_set = False

while chess.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            chess.running = False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0]:
                mouse_pressed = True
                # print("mouse pressed")
        elif event.type == pygame.MOUSEBUTTONUP:
            # print("mouse up")
            if mouse_pressed:
                mouse_clicked = True
                mouse_pressed = False
                mx, my = pygame.mouse.get_pos()
            else:
                mouse_clicked = False

    if mouse_clicked:
        mouse_clicked = False
        isValid, mi, mj = chess.posPixel2Num(CHESS_BOARD_PADDING, CHESS_BOARD_PADDING, mx, my, CHESS_BOARD_CELL_PIXELS)
        if isValid:
            if not is_src_set:
                src_i, src_j = (mi, mj)
                src_rect = (mj * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, \
            mi * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, \
                CHESS_BOARD_CELL_PIXELS, CHESS_BOARD_CELL_PIXELS)
                
                src_horse_type = chess.board[mi][mj]
                is_src_set = True
            else:
                target_i, target_j = (mi, mj)
                target_rect = (mj * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, \
            mi * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, \
                CHESS_BOARD_CELL_PIXELS, CHESS_BOARD_CELL_PIXELS)
                target_horse_type = chess.board[mi][mj]
                is_target_set = True
        if is_src_set and is_target_set:
            # print("출발지:",  src_i, src_j, "목적지:", target_i, target_j)
            isValid = chess.move( src_i, src_j, target_i, target_j)
            is_src_set = False
            is_target_set = False



    # drawing the board
    for i in range(CHESS_BOARD_CELL_WIDTH):
        for j in range(CHESS_BOARD_CELL_WIDTH):
            rect = (j * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, \
                i * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, \
                    CHESS_BOARD_CELL_PIXELS, CHESS_BOARD_CELL_PIXELS)
            if (i + j) % 2 == 0:
                pygame.draw.rect(chess.display.SURFACE, (240, 217,183), rect, 0)
            else:
                pygame.draw.rect(chess.display.SURFACE, (180, 136, 102), rect, 0)

    if is_src_set:
        pygame.draw.rect(chess.display.SURFACE, CHESS_HORSE_SRC_COLOR, src_rect, 0)
    elif is_target_set:
        pygame.draw.rect(chess.display.SURFACE, CHESS_HORSE_TARGET_COLOR, taget_rect, 0)

    # drawing the horses
    # chess.board[N][M] => '[q'
    for N in range(CHESS_BOARD_CELL_WIDTH):
        for M in range(CHESS_BOARD_CELL_WIDTH):
            sprite_num = -1
            if chess.board[N][M][1] == KING:
                sprite_num = 1
            elif chess.board[N][M][1] == QUEEN:
                sprite_num = 0
            elif chess.board[N][M][1] == BISHOP:
                sprite_num = 2
            elif chess.board[N][M][1] == KNIGHT:
                sprite_num = 3
            elif chess.board[N][M][1] == ROOK:
                sprite_num = 4
            elif chess.board[N][M][1] == PAWN:
                sprite_num = 5

            if chess.board[N][M][0] == WHITE:
                chess.display.SURFACE.blit(chess.display.white_horse_list[sprite_num], (M * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, N * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING))
            elif chess.board[N][M][0] == BLACK:
                chess.display.SURFACE.blit(chess.display.black_horse_list[sprite_num], (M * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, N * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING))

                
    pygame.display.update()

pygame.quit()

            
