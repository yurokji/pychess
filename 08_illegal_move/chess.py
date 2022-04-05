from pickle import TRUE
from platform import java_ver
import pygame
from pygame.locals import *
import math
from chess_const import *

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return x

       

class Display:
    def __init__(self):
        self.__SURFACE = pygame.display.set_mode((CHES_BOARD_SIZE,CHES_BOARD_SIZE))
        self.__img_piece = pygame.image.load((CHESS_PIECE_IMAGE_NAME))
        self.__white_piece_list = []
        self.__black_piece_list = []
        self.prep_piece_picture()
        self.__SURFACE.fill((100,100,100))

    
    def getSurface(self):
        return self.__SURFACE
    def getImgPiece(self):
        return self.__img_piece
    def getWhitePieceImgs(self):
        return self.__white_piece_list
    def getBlackPieceImgs(self):
        return self.__black_piece_list
    
       
    def prep_piece_picture(self):
        for i in range(2):
            for j in range(6):
                self.__img_piece = pygame.transform.scale(self.__img_piece, (CHESS_PIECE_PIXELS * 6,CHESS_PIECE_PIXELS * 2))
                cropped_region = (j * CHESS_PIECE_PIXELS, i * CHESS_PIECE_PIXELS, CHESS_PIECE_PIXELS, CHESS_PIECE_PIXELS)
                cropped = pygame.Surface((CHESS_PIECE_PIXELS, CHESS_PIECE_PIXELS), pygame.SRCALPHA)
                cropped.blit(self.getImgPiece(), (0,0), cropped_region)
                if i == 0:
                    self.getWhitePieceImgs().append(cropped)
                else:
                    self.getBlackPieceImgs().append(cropped)
    


# 기본적인 말
class Piece:
    def __init__(self, teamColor, type, pos, num):
        self.__type = type
        self.__team = teamColor
        self.__pos = pos
        self.__num = num
        self.__alive = True
        self.__moved = False
        
    def get_type(self):
        return self.__type
    
    def set_type(self, type):
        self.__type = type
        
    def get_team(self):
        return self.__team
    
    def get_pos(self):
        return self.__pos
    
    def set_pos(self, pos):
        self.__pos = pos
        
    def set_pos(self, i ,j):
        self.__pos = [i,j]
        
    def get_num(self):
        return self.__num
    
    def set_num(self, num):
        self.__num = num
        
    def get_moved(self):
        return self.__moved
    
    def set_moved(self, moved):
        self.__moved = moved  
        
    def get_alive(self):
        return self.__alive
    
    def set_alive(self, alive):
        self.__alive = alive

    
# 검은색/ 흰색 팀 만들기
class Team:
    def __init__(self, color):
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

    def get_pieces(self):
        return self.__pieces
    
    def get_piece(self, piece_num):
        return self.__pieces[piece_num]


  
class Chess:
    teams = {}
    def __init__(self):
        self.__board = []
        self.__turn = WHITE
        self.__team = {}
        self.__team[BLACK] = Team(BLACK)
        self.__team[WHITE] = Team(WHITE)
        self.clear_board()
        self.fill_board()
        self.__display = Display()
        self.__running = True


    def getBoard(self):
        return self.__board
    
    def getDisplay(self):
        return self.__display
    def getRunning(self):
        return self.__running
    def setRunning(self, running):
        self.__running = running
    
    def get_team(self, colorStr):
        return self.__team[colorStr]
   
    def clear_board(self):
        self.__board = []
        for N in range(CHESS_NUM_CELLS):
            row = []
            for M in range(CHESS_NUM_CELLS):
                row.append(EMPTY)
            self.__board.append(row)
    
    def print_board(self):
        for N in range(CHESS_NUM_CELLS):
            for M in range(CHESS_NUM_CELLS):
                print(self.__board[N][M][:2], end=" ")
            print()
        print()


    def erase_board(self):
        for N in range(CHESS_NUM_CELLS):
            for M in range(CHESS_NUM_CELLS):
                self.__board[N][M] = EMPTY


    def init(self):
        self.__num_moves = 0  
        self.__board = []
        self.__turn = WHITE
        self.__team = {}
        self.__team["black"] = Team(BLACK)
        self.__team["white"] = Team(WHITE)
        self.clear_board()
        self.fill_board()
        self.__display = Display()
        self.__running = True
    

    def is_valid_pos_str(self, pos_str):
        if len(pos_str) != 2:
            return False
        else:
            if ord(pos_str[0]) >= ord('a') and ord(pos_str[0]) <= ord('h'):
                if int(pos_str[1]) >= 1 and int(pos_str[1]) <= 8:
                    return True

    def is_valid_pos(self, i, j):
        if (i >= 0 and i <= 7) and (j >= 0 and j <= 7):
            return True
        return False

    def is_valid_pos(self, pos):
        i = pos[0]
        j = pos[1]
        return self.is_valid_pos(i,j)

    def is_valid_cell(self, i,j):
        if self.is_valid_pos_str(pos_str):
            i = CHESS_NUM_CELLS - int(pos_str[1])
            j = ord(pos_str[0]) - ord('a')
            return True, i, j
        else:
            return False, -1, -1
        

    # # 변환 'a8' --> (i=0, j=0)
    # # 변환 'b7' --> (i=1, j=1)
    # def posStr2Num(self, pos_str):
    #     if self.is_valid_pos_str(pos_str):
    #         i = CHESS_NUM_CELLS - int(pos_str[1])
    #         j = ord(pos_str[0]) - ord('a')
    #         return True, i, j
    #     else:
    #         return False, -1, -1

    def pos_2_ij(self, pos):
        i = pos[0]
        j = pos[1]
        return i,j

        
    # 픽셀 위치를 -> i, j롤 환산하는 함수
    def pixel_2_pos(self, sx, sy, px, py, stride):
        pad = 0.1
        i = (py - sy) / stride 
        j = (px - sx) / stride
        # i <= 4.801 --> 4 ;; 4.1 ~ 4.9
        # j <= 2.3 --> 2 ;; 2.1 ~ 2.9
        print(i,j)
        if i < 0 or i >= CHESS_NUM_CELLS \
            or j < 0 or j >= CHESS_NUM_CELLS:
                return False, -1, -1
        i_upper = math.floor(i) # 4
        i_lower = math.ceil(i) # 5
        j_left = math.floor(j) # 2
        j_right = math.ceil(j) # 3	
        if i >= i_upper + pad and i <= i_lower - pad:
            if j >= j_left + pad and j <= j_right - pad:
                return True, i_upper, j_left
        
        return False, i_upper, j_left


    #) 예 -> pos_2_str(i=1, j=1) --> 'b7'
    def pos_2_str(self, i, j):
        str_pos =""
        if self.is_valid_pos(i) and self.is_valid_pos(j):
            str_pos = chr(ord('a') + j) + str(CHESS_NUM_CELLS - i)
            # print(i,j, "-->", str_pos)
            return True, str_pos
        return False, str_pos
    
    
    def get_piece_team(self, i, j):
        return self.__board[i][j][0]
    
    def get_piece_type(self, i,j):
        return self.__board[i][j][1]

    
    def get_piece_num(self, color, pos):
        if color == BLACK:
            pieces = self.get_team("black").get_pieces()
        else:
            pieces = self.get_team("white").get_pieces()
        for idx, piece in enumerate(pieces):
            if piece.get_alive():
                pos_i, pos_j = piece.get_pos()
                if pos_i == pos[0] and pos_j == pos[1]:
                    return idx
        return -1
    
    
    def get_piece(self, piece_num):
        if piece_num < 20:
            pieces = self.get_team("black").get_pieces()
        else:
            pieces = self.get_team("white").get_pieces()

        for piece in pieces:
            if piece.get_num() == piece_num:
                return piece
            
    
    def is_piece_moved(self, team, piece_num):
        return self.get_team(team).get_piece(piece_num).get_moved()
    
    def set_piece_moved(self, team, piece_num, moved):
        self.get_team(team).get_piece(piece_num).set_moved(moved)

    def get_piece_pos(self, team, piece_num):
        return self.get_team(team).get_piece(piece_num).get_pos()
    
    def set_piece_pos(self, team, piece_num, pos):
        self.get_team(team).get_piece(piece_num).set_pos(pos)
   
   
    
    def set_piece_alive(self, piece_num, alive):
        if piece_num < 20:
            pieces = self.get_team("black").get_pieces()
        else:
            pieces = self.get_team("white").get_pieces()

        for piece in pieces:
            if piece.get_num() == piece_num:
                piece.set_alive(alive)
                break


    def get_piece_alive(self, piece_num):
        if piece_num < 20:
            pieces = self.get_team("black").get_pieces()
        else:
            pieces = self.get_team("white").get_pieces()

        for piece in pieces:
            if piece.get_num() == piece_num:
                return piece.get_alive()
    
    def get_cell(self, pos):
        return self.__board[pos[0]][pos[1]]
    
    def get_cell(self, i, j):
        return self.__board[i][j]
    
    def set_cell(self, colorStr, typeStr, i, j, num):
        self.__board[i][j] =  colorStr + typeStr + "{:02d}".format(num) 
        
    def set_cell(self, colorStr, typeStr, pos, num):
        self.__board[pos[0]][pos[1]] =  colorStr + typeStr + "{:02d}".format(num) 

    
    # def set_cell(self, pos_str, piece_type_str):
    #     isValid, i, j  = self.__posStr2Num(pos_str)
    #     if isValid:
    #         self.__board[i][j] = piece_type_str
    #         return True
    #     return False

    def fill_board(self):
        pieces = self.get_team("black").get_pieces()
        for piece in pieces:
            if piece.get_alive():
                self.set_cell(piece.get_team(), piece.get_type(), piece.get_pos(), piece.get_num())
        pieces = self.get_team("white").get_pieces()
        for piece in pieces:
            if piece.get_alive():
                self.set_cell(piece.get_team(), piece.get_type(), piece.get_pos(), piece.get_num())

    def update_board(self):
        self.clear_board()
        # print("cleared")
        # self.__print_board()
        self.fill_board()
        # self.__print_board()
        
    def get_turn(self):
        return self.__turn
    
    def set_turn(self, turn):
        self.__turn = turn
        
    def next_turn(self):
        if self.get_turn == WHITE:
            return self.set_turn(BLACK)
        else:
            return self.set_turn(WHITE)

    def is_horizontal_clear(self, pos_from, pos_to):
        i_from, j_from = self.pos_2_ij(pos_from)
        i_to, j_to = self.pos_2_ij(pos_to)
        diff_j = j_to - j_from 
        for di in range(1, abs(diff_j) + 1):
            if self.get_cell(i_from, j_from + sign(diff_j) * di) != EMPTY:
                return False
        return True
    
    def is_vertical_clear(self, pos_from, pos_to):
        i_from, j_from = self.pos_2_ij(pos_from)
        i_to, j_to = self.pos_2_ij(pos_to)
        diff_i = i_to - i_from 
        for di in range(1, abs(diff_i) + 1):
            if self.get_cell(i_from + sign(diff_i) * di, j_from) != EMPTY:
                return False  
        return True       

    # 대각선 방향 경로가 비워져있는지
    def is_diamovenal_clear(self, pos_from, pos_to):
        i_from, j_from = self.pos_2_ij(pos_from)
        i_to, j_to = self.pos_2_ij(pos_to)
        diff_i = i_to - i_from 
        diff_j = j_to - j_from 
        if abs(diff_i) != abs(diff_j):
            return False
        sign_i = sign(diff_i)
        sign_j = sign(diff_j) 
        for di in range(1, abs(diff_i) + 1):
            if self.get_cell(i_from + sign_i * di, j_from + sign_j * di) != EMPTY:
                return False  
        return True     


    def is_pos_same(self, pos1, pos2):
        if pos1[0] == pos2[0] and pos1[1] == pos2[1]:
            return False


    def put(self, pos_from, pos_to):
        is_two_pos_same = self.is_pos_same(pos_from, pos_to)
        is_not_valid_pos_from = not self.is_valid_pos(pos_from)
        is_not_valid_pos_to = not self.is_valid_pos(pos_to)
        
        if is_two_pos_same or is_not_valid_pos_from or is_not_valid_pos_to:
            return False
        
        src_cell = self.get_cell(pos_from)
        src_cell_team = src_cell[0]
        src_piece_num = self.get_piece_num(src_cell_team, pos_from)
        target_cell = self.get_cell(pos_to)
        target_cell_team = target_cell[0]
        target_piece_num = self.get_piece_num(target_cell_team, pos_to)
        
        is_not_my_turn = src_cell_team != self.get_turn()
        is_not_valid_teams = src_cell_team == target_cell_team
        if is_not_my_turn or is_not_valid_teams:
            return False
        
        isMoved = False
        isKilled = False
        if self.move(src_piece_num, target_piece_num, pos_from, pos_to):
            isMoved = True
        elif self.attack(src_piece_num, target_piece_num, pos_from, pos_to):
            isKilled = True
        # 허용되지 않은 수(illegal move)를 판단하는 부분:
        # (킹을 포함한) 자신의 어떤 기물이라도
        # 옮기거나 상대방의 기물을 잡으며 옮긴 후
        # 자신의 킹이 체크메이트가 되는 경우는 
        # 그 위치로 기물을 옮길 수 없다
        # 이 경우 이미 옮긴 위치에서 제자리로 돌리고
        # 만약 상대방의 기물을 잡은 경우
        # 다시 원상복귀시켜주고
        # 기물을 놓아도 되는 곳에 유저가 기물을 놓을때까지
        # 자신의 턴을 계속 유지하게 한다 
        if isMoved or isKilled:
            if self.is_legal_move():
                if isKilled:
                    self.set_piece_alive(target_piece_num, False)
                self.set_piece_pos(src_piece_num, i_to, j_to)
                return True
        return False
 
 
 ####################단순 기물 이동 부분#############################
    def move(self, src_piece_num, target_piece_num, pos_from, pos_to):
        is_target_filled = self.get_cell(pos_to) !=  EMPTY 
        if is_target_filled:
            return False
        src_team = self.get_turn()
        src_piece = self.get_team(src_team).get_piece(src_piece_num)
        src_piece_moved = src_piece.get_moved()
        src_piece_type = src_piece.get_type()
        if src_piece_type == PAWN:
            if not src_piece_moved:
                if self.pawn_twostep_move(src_piece, pos_to):
                    return True         
                elif self.pawn_move(src_piece, pos_to):
                    return True
        elif src_piece_type == ROOK:
            if self.rook_move(src_piece, pos_to):
                return True
        elif src_piece_type == BISHOP:
            if self.bishop_move(src_piece, pos_to):
                return True
        elif src_piece_type == KNIGHT:
            if self.knight_move(src_piece, pos_to):
                return True
        elif src_piece_type == QUEEN:
            if self.queen_move(src_piece, pos_to):
                return True
        elif src_piece_type == KING:
            if self.king_move(src_piece, pos_to):
                return True
        return False
 

    def pawn_twostep_move(self, src_piece, pos_to):
        src_team = src_piece.get_team()
        pos_from = src_piece.get_pos()
        isJPosNotSame = pos_from[1] != pos_to[1]
        isIPosSame = pos_from[0] == pos_to[0]
        if isJPosNotSame or isIPosSame:
            return False
        i_from, j_from = self.pos_2_ij(pos_from)
        i_to, j_to = self.pos_2_ij(pos_to)
        diff_i = i_to - i_from
        if src_team == BLACK and diff_i == 2:
            is_ok = True
            for di in range(1, diff_i + 1):
                if self.get_cell(i_from + di, j_from) != EMPTY:
                    is_ok = False
                    break
            if is_ok:
                return True
        elif src_team == WHITE and diff_i == -2:
            is_ok = True
            for di in range(1, abs(diff_i) + 1):
                if self.get_cell(i_from - di, j_from) != EMPTY:
                    is_ok = False
                    break
            if is_ok:
                return True
        return False
    def pawn_move(self, src_piece, pos_to):
        src_team = src_piece.get_team()
        pos_from = src_piece.get_pos()
        i_from, j_from = self.pos_2_ij(pos_from)
        i_to, j_to = self.pos_2_ij(pos_to)
        isJPosNotSame = j_from != j_to
        isIPosSame = i_from == i_to
        if isJPosNotSame or isIPosSame:
            return False
        diff_i = i_to - i_from
        if (src_team == BLACK and diff_i == 1) or \
            (src_team == WHITE and diff_i == -1):
            if self.get_cell(i_from + diff_i, j_from) == EMPTY:
                return True
        return False
    
    def rook_move(self, src_piece, pos_to):
        src_team = src_piece.get_team()
        pos_from = src_piece.get_pos()
        i_from, j_from = self.pos_2_ij(pos_from)
        i_to, j_to = self.pos_2_ij(pos_to)
        isHorizontal = i_from == i_to and j_from != j_to
        isVertical = i_from != i_to and j_from == j_to
        if not isHorizontal or not isVertical:
            return False
        # 룩이 수평 이동하는 경우
        if isHorizontal:
            if self.is_horizontal_clear(pos_from, pos_to):
                return True
        # 룩이 수직이동하는 경우
        elif isVertical:
            if self.is_vertical_clear(pos_from, pos_to):
                return True
        return False
    
    def bishop_move(self, src_piece, pos_to):
        src_team = src_piece.get_team()
        pos_from = src_piece.get_pos()
        i_from, j_from = self.pos_2_ij(pos_from)
        i_to, j_to = self.pos_2_ij(pos_to)
        diff_i = i_to - i_from 
        diff_j = j_to - j_from
        isNotDiamovenal = abs(diff_i) != abs(diff_j)
        if isNotDiamovenal:
            return False
        if self.is_diamovenal_clear(pos_from, pos_to):
            return True
        return False
    
    def knight_move(self, src_piece, pos_to):
        src_team = src_piece.get_team()
        pos_from = src_piece.get_pos()
        i_from, j_from = self.pos_2_ij(pos_from)
        i_to, j_to = self.pos_2_ij(pos_to)
        diff_i = i_to - i_from 
        diff_j = j_to - j_from
        move_cond1 =  abs(diff_i) >= 1 and abs(diff_i) << 2 
        move_cond2 =  abs(diff_j) >= 1 and abs(diff_j) << 2
        move_cond3 = (abs(diff_i) + abs(diff_j)) == 3
        if not move_cond1 or not move_cond2 or not move_cond3:
            return False
        return True  
    
    def queen_move(self, src_piece, pos_to):
        if self.rook_move(src_piece, pos_to):
            return True
        elif self.bishop_move(src_piece, pos_to):
            return True
        return False
    
    def king_move(self, src_piece, pos_to):
        src_team = src_piece.get_team()
        pos_from = src_piece.get_pos()
        i_from, j_from = self.pos_2_ij(pos_from)
        i_to, j_to = self.pos_2_ij(pos_to)
        diff_i = i_to - i_from 
        diff_j = j_to - j_from
        num_steps = (abs(diff_i) + abs(diff_j))
        isOneStep = num_steps == 1
        isTwoDiagStep = (abs(diff_i) == abs(diff_j)) and num_steps == 2
        if isOneStep or isTwoDiagStep:
            return True
        return False










####################기물 공격 부분#############################
    def attack(self, src_piece_num, target_piece_num, pos_from, pos_to):
        is_target_empty = self.get_cell(pos_to) ==  EMPTY 
        if is_target_empty:
            return False
        src_team = self.get_turn()
        src_piece = self.get_team(src_team).get_piece(src_piece_num)
        src_piece_moved = src_piece.get_moved()
        src_piece_type = src_piece.get_type()
        target_team = self.next_turn()
        target_piece = self.get_team(target_team).get_piece(target_piece_num)
        if src_piece_type == PAWN:
            if self.pawn_attack(src_piece, target_piece):
                return True
        elif src_piece_type == ROOK:
            if self.rook_attack(src_piece, target_piece):
                return True
        elif src_piece_type == BISHOP:
            if self.bishop_attack(src_piece, target_piece):
                return True
        elif src_piece_type == KNIGHT:
            if self.knight_attack(src_piece, target_piece):
                return True
        elif src_piece_type == QUEEN:
            if self.queen_attack(src_piece, target_piece):
                return True
        elif src_piece_type == KING:
            if self.king_attack(src_piece, target_piece):
                return True
        return False


    def pawn_attack(self, src_piece, target_piece):
        src_team = src_piece.get_team()
        pos_from = src_piece.get_pos()
        pos_to = target_piece.get_pos()
        i_from, j_from = self.pos_2_ij(pos_from)
        i_to, j_to = self.pos_2_ij(pos_to)
        diff_i = i_to - i_from
        diff_j = j_to - j_from
        # 움직임이 대각선인지 체크
        if abs(diff_i) != 1 or abs(diff_j) != 1:
            return False
        if (src_team == BLACK and diff_i == 1) or \
            (src_team == WHITE and diff_i == -1):
            return True             
        return False
       
    def rook_attack(self, src_piece, target_piece):
        pos_from = src_piece.get_pos()
        pos_to = target_piece.get_pos()
        i_from, j_from = self.pos_2_ij(pos_from)
        i_to, j_to = self.pos_2_ij(pos_to)
        diff_i = i_to - i_from
        diff_j = j_to - j_from

        isHorizontal = i_from == i_to and j_from != j_to
        isVertical = i_from != i_to and j_from == j_to
        if not isHorizontal or not isVertical:
            return False
        # 룩이 수평 이동하는 경우
        if isHorizontal:
            # 목적지 도착 직전 위치 계산
            j_to_before = j_from + (abs(j_to - j_from) - 1) * sign(j_to - j_from)
            # 다른 경로는 다 비어있고 
            # 마지막 목적지에만 적의 말이 놓여있는 경우
            # 말을 잡고 목적지로 움직인다
            if j_from == j_to_before:
                # print("옆의놈먹자")
                return True
            elif self.is_horizontal_clear(pos_from, (pos_to[0], j_to_before)):
                return True

        # 룩이 수직이동하는 경우
        elif isVertical:
            # 목적지 도착 직전 위치 계산
            i_to_before = i_from + (abs(i_to - i_from) - 1) * sign(i_to - i_from)
            # # 마지막 목적지에만 적의 말이 놓여있는 경우
            # # 말을 잡고 목적지로 움직인다
            if i_from == i_to_before:
                return True
            elif self.is_vertical_clear(pos_from, (i_to_before, pos_to[1])):
                return True
        return False   
   
    def bishop_attack(self, src_piece, target_piece):
        pos_from = src_piece.get_pos()
        pos_to = target_piece.get_pos()
        i_from, j_from = self.pos_2_ij(pos_from)
        i_to, j_to = self.pos_2_ij(pos_to)
        diff_i = i_to - i_from
        diff_j = j_to - j_from
        sign_i = sign(diff_i)
        sign_j = sign(diff_j)
        isNotDiamovenal = abs(diff_i) != abs(diff_j)
        if isNotDiamovenal:
            return False
        i_to_before = i_from + (abs(diff_i) - 1) * sign_i
        j_to_before = j_from + (abs(diff_j) - 1) * sign_j
        # 다른 경로는 다 비어있고 
        # 마지막 목적지에만 적의 말이 놓여있는 경우
        # 말을 잡고 목적지로 움직인다
        if self.is_pos_same((i_from, j_from), (i_to_before, j_to_before)):
            return True
        elif self.is_diamovenal_clear(pos_from, pos_to):
            return True
        return False
   
    def knight_attack(self, src_piece, target_piece):
        pos_from = src_piece.get_pos()
        pos_to = target_piece.get_pos()
        i_from, j_from = self.pos_2_ij(pos_from)
        i_to, j_to = self.pos_2_ij(pos_to)
        diff_i = i_to - i_from 
        diff_j = j_to - j_from
        move_cond1 =  abs(diff_i) >= 1 and abs(diff_i) << 2 
        move_cond2 =  abs(diff_j) >= 1 and abs(diff_j) << 2
        move_cond3 = (abs(diff_i) + abs(diff_j)) == 3
        if not move_cond1 or not move_cond2 or not move_cond3:
            return False
        return True  
    
       
    def queen_attack(self, src_piece, target_piece):
        if self.rook_attack(src_piece, target_piece):
            return True
        elif self.bishop_attack(src_piece, target_piece):
            return True
        return False             



    def king_attack(self, src_piece, target_piece):
        pos_from = src_piece.get_pos()
        pos_to = target_piece.get_pos()
        i_from, j_from = self.pos_2_ij(pos_from)
        i_to, j_to = self.pos_2_ij(pos_to)
        diff_i = i_to - i_from 
        diff_j = j_to - j_from
        num_steps = (abs(diff_i) + abs(diff_j))
        isOneStep = num_steps == 1
        isTwoDiagStep = (abs(diff_i) == abs(diff_j)) and num_steps == 2
        if isOneStep or isTwoDiagStep:
            return True
        return False
    
    
    # 킹이 옮기는 위치가 공격당할 수 있는 곳인지 확인한다
    def is_my_piece_vulnerable(self, my_team, i_whatif, j_whatif):

        print("옮기려는 위치:", i_whatif, j_whatif)
        for enemy_piece in enemy_pieces:
            if enemy_piece.get_alive():
                print(enemy_piece.get_team(), enemy_piece.get_type(), enemy_piece.get_pos())
                enemy_piece_pos = enemy_piece.get_pos()
                if self.attack(enemy_piece_pos[0],enemy_piece_pos[1], i_whatif, j_whatif, illegal=True):
                    return True
        return False
      
                
                
    def is_legal_move(self):
        if self.get_turn() == BLACK:
            enemy_pieces = self.get_team("white").get_pieces()
        else:
            enemy_pieces = self.get_team("black").get_pieces()
        # 적의 살아있는 기물이 자신의 킹을 잡을 수 있는지 판단한다
        # (즉, 체크메이트가 되는 형국인지)
        my_king_piece = self.get_team(self.get_turn()).get_pieces()
        for enemy_piece in enemy_pieces:
            if enemy_piece.get_alive():
                enemy_piece_pos = enemy_piece.get_pos()
                if self.attack(enemy_piece_pos[0],enemy_piece_pos[1], i_whatif, j_whatif, illegal=True):
        
            

    
    
ch = Chess()
ch.print_board()
