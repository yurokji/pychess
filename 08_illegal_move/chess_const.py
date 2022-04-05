CHESS_NUM_CELLS = 8
CHESS_BOARD_CELL_PIXELS = 80
CHESS_BOARD_PADDING = 80
CHESS_PIECE_PIXELS = 80
CHES_BOARD_SIZE = CHESS_BOARD_CELL_PIXELS * CHESS_NUM_CELLS + CHESS_BOARD_PADDING * 2
CHESS_PIECE_IMAGE_NAME = "./images/pieces.png"
CHESS_PIECE_SRC_COLOR = (240, 80, 80)
CHESS_PIECE_TARGET_COLOR = (80, 80, 240)

EMPTY = '  '
KING = 'k'
QUEEN = 'q'
BISHOP = 'b'
KNIGHT = 'n'
ROOK = 'r'
PAWN = 'w'


for x in range(CHESS_NUM_CELLS):
    self.__pieces.append(Piece(self.__team, PAWN, [1, x], int(x)))
self.__pieces.append(Piece(self.__team, ROOK, [0, 0], 8))
self.__pieces.append(Piece(self.__team, KNIGHT, [0, 1],9))
self.__pieces.append(Piece(self.__team, BISHOP, [0, 2],10))
self.__pieces.append(Piece(self.__team, KING, [0, 3],11))
self.__pieces.append(Piece(self.__team, QUEEN, [0, 4],12))
self.__pieces.append(Piece(self.__team, BISHOP, [0, 5],13))
self.__pieces.append(Piece(self.__team, KNIGHT, [0, 6],14))
self.__pieces.append(Piece(self.__team, ROOK, [0, 7],15))
# 흰색 팀일 경우
        
NUM_NO_PIECE = -1
NUM_PAWN_PIECE_1 = 0
NUM_PAWN_PIECE_2 = 1
NUM_PAWN_PIECE_3 = 2
NUM_PAWN_PIECE_4 = 3
NUM_PAWN_PIECE_5 = 4
NUM_ROOK_PIECE_1 = 5
NUM_KNIGHT_PIECE_1 = 6
NUM_BISHOP_PIECE_1 = 7
NUM_KING_PIECE = 8
NUM_QUEEN_PIECE = 9
NUM_BISHOP_PIECE_2 = 10
NUM_KNIGHT_PIECE_2 = 11
NUM_ROOK_PIECE_2 = 12





KING = 'k'
QUEEN = 'q'
BISHOP = 'b'
KNIGHT = 'n'
ROOK = 'r'
PAWN = 'w'



BLACK = '['
WHITE = ']'