from chess_const import *
from chess import *

chess = Chess()
chess_disp_surf = chess.getDisplay().getSurface()
chess.print_board()


mouse_pressed = False
mouse_clicked = False
is_src_set = False
is_target_set = False

while chess.getRunning():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            chess.setRunning(False)
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
        isValid, mi, mj = chess.pixel_2_pos(CHESS_BOARD_PADDING, CHESS_BOARD_PADDING, mx, my, CHESS_BOARD_CELL_PIXELS)
        if not isValid:
            mouse_pressed = False
            is_src_set = False
            is_target_set = False
            continue
        else:
            if not is_src_set:
                src_pos = (mi, mj)
                src_rect = (mj * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, \
            mi * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, \
                CHESS_BOARD_CELL_PIXELS, CHESS_BOARD_CELL_PIXELS)
                
                src_piece_type = chess.get_cell_from_board(src_pos)
                is_src_set = True
            else:
                target_pos = (mi, mj)
                target_rect = (mj * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, \
            mi * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, \
                CHESS_BOARD_CELL_PIXELS, CHESS_BOARD_CELL_PIXELS)
                target_piece_type = chess.get_cell_from_board(target_pos)
                is_target_set = True
        if is_src_set and is_target_set:
            if chess.put(src_pos, target_pos):
                chess.set_turn(chess.get_next_turn())
            is_src_set = False
            is_target_set = False



    # drawing the board
    for i in range(CHESS_NUM_CELLS):
        for j in range(CHESS_NUM_CELLS):
            rect = (j * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, \
                i * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, \
                    CHESS_BOARD_CELL_PIXELS, CHESS_BOARD_CELL_PIXELS)
            if (i + j) % 2 == 0:
                pygame.draw.rect(chess_disp_surf, (240, 217,183), rect, 0)
            else:
                pygame.draw.rect(chess_disp_surf, (180, 136, 102), rect, 0)

    if is_src_set:
        pygame.draw.rect(chess_disp_surf, CHESS_PIECE_SRC_COLOR, src_rect, 0)
    elif is_target_set:
        pygame.draw.rect(chess_disp_surf, CHESS_PIECE_TARGET_COLOR, target_rect, 0)

    # drawing the pieces
    for N in range(CHESS_NUM_CELLS):
        for M in range(CHESS_NUM_CELLS):
            cell_team = chess.get_cell_from_board((N,M))[0]
            cell_type = chess.get_cell_from_board((N,M))[1]
            sprite_num = -1
            if cell_type == KING:
                sprite_num = 0
            elif cell_type == QUEEN:
                sprite_num = 1
            elif cell_type == BISHOP:
                sprite_num = 2
            elif cell_type == KNIGHT:
                sprite_num = 3
            elif cell_type == ROOK:
                sprite_num = 4
            elif cell_type == PAWN:
                sprite_num = 5

            if cell_team == WHITE:
                chess_disp_surf.blit(chess.getDisplay().getWhitePieceImgs()[sprite_num],\
                    (M * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, N * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING))
            elif cell_team == BLACK:
                chess_disp_surf.blit(chess.getDisplay().getBlackPieceImgs()[sprite_num], \
                    (M * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, N * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING))

                
    pygame.display.update()

pygame.quit()

            
