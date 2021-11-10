from chess_const import *
from chess import *



chess = Chess()
chess.print_board()

while chess.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            chess.running = False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            chess.input.mouse_presses = pygame.mouse.get_pressed()
            if chess.input.mouse_presses[0]:
                chess.input.mouse_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if chess.input.mouse_pressed == True:
                chess.input.mouse_clicked = True
                chess.input.mouse_pressed = False
                chess.input.mx, chess.input.my = pygame.mouse.get_pos()
            else:
                chess.input.mouse_clicked = False


    if chess.input.mouse_clicked:
        chess.input.mouse_clicked = False
        isValid, mi, mj = chess.posPixel2Num(CHESS_BOARD_PADDING, CHESS_BOARD_PADDING, chess.input.mx, chess.input.my, CHESS_BOARD_CELL_PIXELS)
        if isValid:
            print(mi, mj)
            str_pos = chess.posNum2Str(mi,mj)        
            if str_pos[0]:
                if not chess.input.is_src_set:
                    chess.input.src_pos = str_pos
                    chess.input.src_rect = (mj * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, mi * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, CHESS_BOARD_CELL_PIXELS, CHESS_BOARD_CELL_PIXELS)
                    chess.input.src_horse_type = chess.board[mi][mj]
                    chess.input.is_src_set = True
                else:
                    chess.input.target_pos = str_pos
                    chess.input.target_rect = (mj * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, mi * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, CHESS_BOARD_CELL_PIXELS, CHESS_BOARD_CELL_PIXELS)
                    chess.input.is_target_set = True
        if chess.input.is_src_set and chess.input.is_target_set:
            # print(src_horse_type, src_pos[1], target_pos[1])
            chess.move_pawn(chess.input.src_horse_type + chess.input.src_pos[1] , chess.input.target_pos[1])
            chess.input.is_src_set = False
            chess.input.is_target_set = False


    # drawing the chess board
    for i in range(CHESS_BOARD_TOTAL_CELLS):
        for j in range(CHESS_BOARD_TOTAL_CELLS):
            rect = (j * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, i * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, CHESS_BOARD_CELL_PIXELS, CHESS_BOARD_CELL_PIXELS)  
            if (i + j) % 2 == 0:
                pygame.draw.rect(chess.display.SURFACE, (240,217,183), rect, 0)
            else:
                pygame.draw.rect(chess.display.SURFACE, (180, 136, 102), rect, 0)
    if chess.input.is_src_set:
        pygame.draw.rect(chess.display.SURFACE, CHESS_HORSE_START_COLOR, chess.input.src_rect, 0)
    if chess.input.is_target_set:
        pygame.draw.rect(chess.display.SURFACE, CHESS_HORSE_TARGET_COLOR, chess.input.target_rect, 0)


    # drawing the horses
    for N in range(CHESS_BOARD_TOTAL_CELLS):
        for M in range(CHESS_BOARD_TOTAL_CELLS):
            sprite_num = -1
            if chess.board[N][M][0] != EMPTY:
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
                
                # print(sprite_num)
                # if the horse is white
                if chess.board[N][M][0] == '[': 
                    chess.display.SURFACE.blit(chess.display.white_horse_list[sprite_num], (M * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, N * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING))
                elif chess.board[N][M][0] == ']':
                    chess.display.SURFACE.blit(chess.display.black_horse_list[sprite_num], (M * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, N * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING))

    pygame.display.update()

pygame.quit()

