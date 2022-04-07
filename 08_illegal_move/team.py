from chess_const import *
from piece import *
 
# 검은색/ 흰색 팀 만들기
class Team:
    def __init__(self, color):
        self.__checked = False
        self.__team = color
        self.__pieces = []
        self.set_init_pos()


    # 초기 말의 위치를 정함
    def set_init_pos(self):
        self.__pieces = []
         # 검은색 팀일 경우
        if self.__team == BLACK:
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
            self.__pieces[NUM_KING_PIECE].set_alive(True)
            self.__pieces[NUM_PAWN_PIECE_5].set_alive(True)
        # 흰색 팀일 경우
        else:
            for x in range(CHESS_NUM_CELLS):
                self.__pieces.append(Piece(self.__team, PAWN, [6, x], 20+int(x)))
            self.__pieces.append(Piece(self.__team, ROOK, [7, 0],28))
            self.__pieces.append(Piece(self.__team, KNIGHT, [7, 1],29))
            self.__pieces.append(Piece(self.__team, BISHOP, [7, 2],30))
            self.__pieces.append(Piece(self.__team, KING, [7, 4],31))
            self.__pieces.append(Piece(self.__team, QUEEN, [7, 3] ,32))
            self.__pieces.append(Piece(self.__team, BISHOP, [7, 5],33))
            self.__pieces.append(Piece(self.__team, KNIGHT, [7, 6],34))
            self.__pieces.append(Piece(self.__team, ROOK, [7, 7],35))
            self.__pieces[NUM_PAWN_PIECE_4].set_alive(True)
            self.__pieces[NUM_QUEEN_PIECE].set_alive(True)
            self.__pieces[NUM_KING_PIECE].set_alive(True)

    def get_all_pieces(self):
        return self.__pieces
    
    def get_piece(self, piece_num):
        return self.__pieces[piece_num]
    
    def get_checked(self):
        return self.__checked
    
    def set_checked(self, checked):
        self.__checked = checked