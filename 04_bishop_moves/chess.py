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
    def getType(self):
        return self.__type
    def setType(self, type):
        self.__type = type
    def get_team(self):
        return self.__team
    def get_pos(self):
        return self.__pos
    def setPos(self, pos):
        self.__pos = pos
    def setPos(self, i ,j):
        self.__pos = [i,j]
    def get_num(self):
        return self.__num
    def setNum(self, num):
        self.__num = num
    def getMoved(self):
        return self.__moved
    def setMoved(self, moved):
        self.__moved = moved  
    def get_alive(self):
        return self.__alive
    def setAlive(self, alive):
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
            for x in range(CHESS_BOARD_CELL_WIDTH):
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
            for x in range(CHESS_BOARD_CELL_WIDTH):
                self.__pieces.append(Piece(self.__team, PAWN, [6, x], 20+int(x)))
            self.__pieces.append(Piece(self.__team, ROOK, [7, 0],28))
            self.__pieces.append(Piece(self.__team, KNIGHT, [7, 1],29))
            self.__pieces.append(Piece(self.__team, BISHOP, [7, 2],30))
            self.__pieces.append(Piece(self.__team, KING, [7, 3],31))
            self.__pieces.append(Piece(self.__team, QUEEN, [7, 4],32))
            self.__pieces.append(Piece(self.__team, BISHOP, [7, 5],33))
            self.__pieces.append(Piece(self.__team, KNIGHT, [7, 6],34))
            self.__pieces.append(Piece(self.__team, ROOK, [7, 7],35))
    
    def get_pieces(self):
        return self.__pieces
    
        


  
class Chess:
    teams = {}
    def __init__(self):
        self.__board = []
        self.__turn = WHITE
        self.__team = {}
        self.__team["black"] = Team(BLACK)
        self.__team["white"] = Team(WHITE)
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
        for N in range(CHESS_BOARD_CELL_WIDTH):
            row = []
            for M in range(CHESS_BOARD_CELL_WIDTH):
                row.append(EMPTY)
            self.__board.append(row)
    
    def print_board(self):
        for N in range(CHESS_BOARD_CELL_WIDTH):
            for M in range(CHESS_BOARD_CELL_WIDTH):
                print(self.__board[N][M][:2], end=" ")
            print()
        print()


    def erase_board(self):
        for N in range(CHESS_BOARD_CELL_WIDTH):
            for M in range(CHESS_BOARD_CELL_WIDTH):
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


    def is_valid_cell(self, i,j):
        if self.is_valid_pos_str(pos_str):
            i = CHESS_BOARD_CELL_WIDTH - int(pos_str[1])
            j = ord(pos_str[0]) - ord('a')
            return True, i, j
        else:
            return False, -1, -1
        

    # # 변환 'a8' --> (i=0, j=0)
    # # 변환 'b7' --> (i=1, j=1)
    # def posStr2Num(self, pos_str):
    #     if self.is_valid_pos_str(pos_str):
    #         i = CHESS_BOARD_CELL_WIDTH - int(pos_str[1])
    #         j = ord(pos_str[0]) - ord('a')
    #         return True, i, j
    #     else:
    #         return False, -1, -1


    # 픽셀 위치를 -> i, j롤 환산하는 함수
    def pixel_2_pos(self, sx, sy, px, py, stride):
        pad = 0.1
        i = (py - sy) / stride 
        j = (px - sx) / stride
        # i <= 4.801 --> 4 ;; 4.1 ~ 4.9
        # j <= 2.3 --> 2 ;; 2.1 ~ 2.9
        
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
            str_pos = chr(ord('a') + j) + str(CHESS_BOARD_CELL_WIDTH - i)
            # print(i,j, "-->", str_pos)
            return True, str_pos
        return False, str_pos
    
    
    def get_piece_team(self, i, j):
        return self.__board[i][j][0]
    
    def get_piece_type(self, i,j):
        return self.__board[i][j][1]

    
    def get_piece_num(self, color, i,j):
        if color == BLACK:
            pieces = self.get_team("black").get_pieces()
        else:
            pieces = self.get_team("white").get_pieces()
        for piece in pieces:
            if piece.get_alive():
                pos_i, pos_j = piece.get_pos()
                if pos_i == i and pos_j == j:
                    return piece.get_num()
        return -1
    
    def is_piece_moved(self, piece_num):
        if piece_num < 20:
            pieces = self.get_team("black").get_pieces()
        else:
            pieces = self.get_team("white").get_pieces()

        for piece in pieces:
            if piece.get_num() == piece_num:
                return piece.getMoved()
        return -1
    
    def set_piece_moved(self, piece_num, moved):
        if piece_num < 20:
            pieces = self.get_team("black").get_pieces()
        else:
            pieces = self.get_team("white").get_pieces()

        for piece in pieces:
            if piece.get_num() == piece_num:
                piece.setMoved(moved)

    def get_piece_pos(self, piece_num):
        if piece_num < 20:
            pieces = self.get_team("black").get_pieces()
        else:
            pieces = self.get_team("white").get_pieces()

        for piece in pieces:
            if piece.get_num() == piece_num:
                return piece.get_pos()
        return -1, -1
    
    def set_piece_pos(self, piece_num, i_to, j_to):
        if piece_num < 20:
            pieces = self.get_team("black").get_pieces()
        else:
            pieces = self.get_team("white").get_pieces()

        for piece in pieces:
            if piece.get_num() == piece_num:
                piece.setPos(i_to, j_to)
                break
   
   
    def set_piece_alive(self, piece_num, alive):
        if piece_num < 20:
            pieces = self.get_team("black").get_pieces()
        else:
            pieces = self.get_team("white").get_pieces()

        for piece in pieces:
            if piece.get_num() == piece_num:
                piece.setAlive(alive)
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
                self.set_cell(piece.get_team(), piece.getType(), piece.get_pos(), piece.get_num())
        pieces = self.get_team("white").get_pieces()
        for piece in pieces:
            if piece.get_alive():
                self.set_cell(piece.get_team(), piece.getType(), piece.get_pos(), piece.get_num())

    def update_board(self):
        self.clear_board()
        # print("cleared")
        # self.__print_board()
        self.fill_board()
        # self.__print_board()
        
    def nextTurn(self, moved):
        if moved:
            if self.__turn == WHITE:
                self.__turn = BLACK
            else:
                self.__turn = WHITE

    def checkPieceType(self, i, j, PIECETYPE):
        return PIECETYPE == self.get_piece_type(i,j)

    def is_horizontal_clear(self, i_from, j_from, i_to, j_to):
        diff = j_to - j_from 
        for di in range(1, abs(diff) + 1):
            if self.__board[i_from][j_from + sign(diff) * di] != EMPTY:
                return False
        return True
    
    def is_vertical_clear(self, i_from, j_from, i_to, j_to):
        diff = i_to - i_from 
        for di in range(1, abs(diff) + 1):
            if self.__board[i_from + sign(diff) * di][j_from] != EMPTY:
                return False  
        return True       

    # 대각선 방향 경로가 비워져있는지
    def is_diagonal_clear(self, i_from, j_from, i_to, j_to):
        diff_i = i_to - i_from 
        diff_j = j_to - j_from
        if abs(diff_i) != abs(diff_j):
            return False
        sign_i = sign(diff_i)
        sign_j = sign(diff_j) 
        for di in range(1, abs(diff_i) + 1):
            if self.__board[i_from + sign_i * di][j_from + sign_j * di] != EMPTY:
                return False  
        return True     

    def move(self, i_from, j_from, i_to, j_to):
        if i_from == i_to and j_from == j_to:
            return False
        src_piece = self.get_cell(i_from, j_from)
        src_piece_team = src_piece[0]
        src_piece_num = self.get_piece_num(src_piece_team,i_from, j_from)
        target_piece = self.get_cell(i_to, j_to)
        target_piece_team = target_piece[0]
        target_piece_num = self.get_piece_num(target_piece_team,i_to, j_to)
        colorStr = ""
        if src_piece_team == BLACK:
            colorStr = "검은색"
        else:
            colorStr = "흰색"
            
        isSrcTurn = (self.__turn == src_piece_team)
        isValid_from = self.is_valid_pos(i_from, j_from)
        isValid_to = self.is_valid_pos(i_to, j_to)
        if not isSrcTurn or not isValid_from or not isValid_to:
            return False
        moveSuccess = False
        moved = self.is_piece_moved(src_piece_num)
        

        if self.checkPieceType(i_from, j_from, PAWN):
            if not moved:
                if self.pawn_twostep_move(i_from, j_from, i_to, j_to):
                    print(colorStr+"폰 두칸 이동")
                    moveSuccess = True
                    self.set_piece_moved(src_piece_num, True)
            if self.pawn_move(i_from, j_from, i_to, j_to):
                print(colorStr+"폰 이동")
                moveSuccess = True
            elif self.pawn_attack(i_from, j_from, i_to, j_to):
                print(colorStr+"폰 공격")
                moveSuccess = True
        elif self.checkPieceType(i_from, j_from, ROOK):
            if self.rook_move(i_from, j_from, i_to, j_to):
                print(colorStr+"룩 이동")
                moveSuccess = True
            elif self.rook_attack(i_from, j_from, i_to, j_to):
                print(colorStr+"룩 공격")
                moveSuccess = True
        elif self.checkPieceType(i_from, j_from, BISHOP):
            print("비숍 이동 차례")
            if self.bishop_move(i_from, j_from, i_to, j_to):
                print(colorStr+"비숍 이동")
                moveSuccess = True
            elif self.bishop_attack(i_from, j_from, i_to, j_to):
                print(colorStr+"비숍 공격")
                moveSuccess = True
        # 말이 성공적으로 움직였다면
        if moveSuccess: 
             # 보드 업데이트
            self.update_board()
               # 상대편 차례
            self.nextTurn(moveSuccess)
                
    
    
    # 폰 첫번째 2칸 움직임
    def pawn_twostep_move(self, i_from, j_from, i_to, j_to):
        src_piece = self.get_cell(i_from, j_from)
        src_piece_team = src_piece[0]
        target_piece = self.get_cell(i_to, j_to)
        target_piece_team = target_piece[0]
        src_num = self.get_piece_num(src_piece_team, i_from, j_from)
        target_num = self.get_piece_num(target_piece_team, i_to, j_to)
        print("소스넘버",src_num, "타겟넘버", target_num)
        isJPosSame = j_from == j_to
        isIPosNotSame = i_from != i_to
        isTargetEmpty = self.__board[i_to][j_to] ==  EMPTY 
        
        isValid = isJPosSame and isIPosNotSame and isTargetEmpty
        if isValid:
            diff = i_to - i_from
            if self.__turn == BLACK:
                # print("검은 폰 움직임")
                if diff == 2:
                    is_ok = True
                    for di in range(1, diff + 1):
                        if self.__board[i_from + di][j_from] != EMPTY:
                            is_ok = False
                            break
                    if is_ok:
                        self.set_piece_pos(src_num, i_to, j_to)
                        return True
            # 흰 폰 움직임
            else:
                if diff == -2:
                    is_ok = True
                    for di in range(1, abs(diff) + 1):
                        if self.__board[i_from - di][j_from] != EMPTY:
                            is_ok = False
                            break
                    if is_ok:
                        self.set_piece_pos(src_num, i_to, j_to)
                        return True
        return False


    # 폰 정상 움직임 함수
    def pawn_move(self, i_from, j_from, i_to, j_to):
        src_piece = self.get_cell(i_from, j_from)
        src_piece_team = src_piece[0]
        target_piece = self.get_cell(i_to, j_to)
        target_piece_team = target_piece[0]
        src_num = self.get_piece_num(src_piece_team, i_from, j_from)
        target_num = self.get_piece_num(target_piece_team, i_to, j_to)
        print("소스넘버",src_num, "타겟넘버", target_num)
        isJPosSame = j_from == j_to
        isIPosNotSame = i_from != i_to
        isTargetEmpty = self.__board[i_to][j_to] ==  EMPTY 
        isValid = isJPosSame and isIPosNotSame and isTargetEmpty
        if isValid:
            # 흑일 때는 차이가 양수 1이나 2여야 함
            diff = i_to - i_from
            # print(diff)
            if src_piece_team == BLACK:
                # print("검은 폰 움직임")
                if diff == 1:
                    if self.__board[i_from + diff][j_from] == EMPTY:
                        self.set_piece_pos(src_num, i_to, j_to)
                        return True
            # 흰 폰 움직임
            else:
                if diff == -1:
                    if self.__board[i_from + diff][j_from] == EMPTY:
                        self.set_piece_pos(target_num, i_to, j_to)
                        return True
        return False

    # 폰 움직임 함수
    # pawn_move('b2', 'b4')
    def pawn_attack(self, i_from, j_from, i_to, j_to):
        src_piece = self.get_cell(i_from, j_from)
        src_piece_team = src_piece[0]
        target_piece = self.get_cell(i_to, j_to)
        target_piece_team = target_piece[0]
        src_num = self.get_piece_num(src_piece_team, i_from, j_from)
        target_num = self.get_piece_num(target_piece_team, i_to, j_to)
        print("소스넘버",src_num, "타겟넘버", target_num)
        diff_i = i_to - i_from
        diff_j = j_to - j_from

        # 움직임이 대각선인지 체크
        if abs(diff_i) != 1 or abs(diff_j) != 1:
            return False
        # 공격할 대상이 없는지 체크
        if target_piece == EMPTY:
            return False
        # 다른 편인지 체크
        if  src_piece_team == target_piece_team:
            return False
    
        if src_piece_team == BLACK:
            if diff_i == 1:
                # print("검은 폰 움직임")
                # print("before: ", self.get_piece_num(src_piece_team, i_from,j_from))
                self.set_piece_alive(target_num, False)
                self.set_piece_pos(src_num, i_to, j_to)
                return True
        else:
            if diff_i == -1:
                # print("흰 폰 움직임")
                # print("before: ", self.get_piece_num(src_piece_team, i_from,j_from))
                self.set_piece_alive(target_num, False)
                self.set_piece_pos(src_num, i_to, j_to)
                return True

        return False

    def rook_move(self, i_from, j_from, i_to, j_to):
        src_piece = self.get_cell(i_from, j_from)
        src_piece_team = src_piece[0]
        target_piece = self.get_cell(i_to, j_to)
        target_piece_team = target_piece[0]
        isValidTarget = src_piece[0] != target_piece[0]
        isHorizontal = i_from == i_to and j_from != j_to
        isVertical = i_from != i_to and j_from == j_to
        isHoriVert = isHorizontal or isVertical
        isValid = isValidTarget and isHoriVert
        if isValid:
            # 룩이 수평 이동하는 경우
            if isHorizontal:
                # 목적지 도착 직전 위치 계산
                j_to_before = j_from + (abs(j_to - j_from) - 1) * sign(j_to - j_from)
                # print("j_to_before",j_to_before)
                # 마지막 목적지 바로 전까지 경로가 다 비어있는지 검사한다
                # 경로가 하나라도 비어있지 않다면 바로 종료하여 움직일 수 없도록 한다
                if self.is_horizontal_clear(i_from, j_from, i_to, j_to):
                    # print("이동")
                    self.set_piece_pos(self.get_piece_num(src_piece_team, i_from,j_from), i_to, j_to)
                    return True


            # 룩이 수직이동하는 경우
            elif isVertical:
                # 목적지 도착 직전 위치 계산
                i_to_before = i_from + (abs(i_to - i_from) - 1) * sign(i_to - i_from)
                # 마지막 목적지 바로 전까지 경로가 다 비어있는지 검사한다
                if self.is_vertical_clear(i_from, j_from, i_to, j_to):
                    self.set_piece_pos(self.get_piece_num(src_piece_team, i_from,j_from), i_to, j_to)
                    return True
        return False
    
    def rook_attack(self, i_from, j_from, i_to, j_to):
        src_piece = self.get_cell(i_from, j_from)
        src_piece_team = src_piece[0]
        target_piece = self.get_cell(i_to, j_to)
        target_piece_team = target_piece[0]
        src_num = self.get_piece_num(src_piece_team, i_from, j_from)
        target_num = self.get_piece_num(target_piece_team, i_to, j_to)
        print("소스넘버",src_num, "타겟넘버", target_num)
        isValidTarget = src_piece[0] != target_piece[0]
        isHorizontal = i_from == i_to and j_from != j_to
        isVertical = i_from != i_to and j_from == j_to
        isHoriVert = isHorizontal or isVertical
        isValid = isValidTarget and isHoriVert
        if isValid:
            # 룩이 수평 이동하는 경우
            if isHorizontal:
                # 목적지 도착 직전 위치 계산
                j_to_before = j_from + (abs(j_to - j_from) - 1) * sign(j_to - j_from)
                # 다른 경로는 다 비어있고 
                # 마지막 목적지에만 적의 말이 놓여있는 경우
                # 말을 잡고 목적지로 움직인다
                if j_from == j_to_before:
                    # print("옆의놈먹자")
                    self.set_piece_alive(self.get_piece_num(target_piece_team, i_to,j_to), False)
                    self.set_piece_pos(self.get_piece_num(src_piece_team, i_from,j_from), i_to, j_to)
                    return True
                elif self.is_horizontal_clear(i_from, j_from, i_to, j_to_before):
                    self.set_piece_alive(self.get_piece_num(target_piece_team, i_to,j_to), False)
                    self.set_piece_pos(self.get_piece_num(src_piece_team, i_from,j_from), i_to, j_to)
                    return True

            # 룩이 수직이동하는 경우
            elif isVertical:
                # 목적지 도착 직전 위치 계산
                i_to_before = i_from + (abs(i_to - i_from) - 1) * sign(i_to - i_from)
                # # 마지막 목적지에만 적의 말이 놓여있는 경우
                # # 말을 잡고 목적지로 움직인다
                if i_from == i_to_before:
                    print("타겟 살았나?", self.get_piece_alive(target_num))
                    self.set_piece_alive(target_num, False)
                    print("타겟 살았나?", self.get_piece_alive(target_num))
                    print("소스 위치", self.get_piece_pos(src_num))
                    self.set_piece_pos(src_num, i_to, j_to)
                    print("소스 위치", self.get_piece_pos(src_num))
                    return True
                elif self.is_vertical_clear(i_from, j_from, i_to_before, j_to):
                    print("타겟 살았나?", self.get_piece_alive(target_num))
                    self.set_piece_alive(target_num, False)
                    print("타겟 살았나?", self.get_piece_alive(target_num))
                    print("소스 위치", self.get_piece_pos(src_num))
                    self.set_piece_pos(src_num, i_to, j_to)
                    print("소스 위치", self.get_piece_pos(src_num))
                    return True
        return False

    def bishop_move(self, i_from, j_from, i_to, j_to):
        src_piece = self.get_cell(i_from, j_from)
        src_piece_team = src_piece[0]
        target_piece = self.get_cell(i_to, j_to)
        target_piece_team = target_piece[0]
        isValidTarget = src_piece_team != target_piece_team
        diff_i = i_to - i_from 
        diff_j = j_to - j_from
        isDiagonal = abs(diff_i) == abs(diff_j)
        isValid = isValidTarget and isDiagonal
        if isValid:
            # print("비숍정상적 움직임")
            if self.is_diagonal_clear(i_from, j_from, i_to, j_to):
                # print("대각선 클리어")
                self.set_piece_pos(self.get_piece_num(src_piece_team, i_from,j_from), i_to, j_to)
                return True
        return False

    def bishop_attack(self, i_from, j_from, i_to, j_to):
        src_piece = self.get_cell(i_from, j_from)
        src_piece_team = src_piece[0]
        target_piece = self.get_cell(i_to, j_to)
        target_piece_team = target_piece[0]
        isValidTarget = src_piece_team != target_piece_team
        diff_i = i_to - i_from 
        diff_j = j_to - j_from
        sign_i = sign(diff_i)
        sign_j = sign(diff_j)
        isDiagonal = abs(diff_i) == abs(diff_j)
        isValid = isValidTarget and isDiagonal
        if isValid:
            # 목적지 도착 직전 위치 계산
            i_to_before = i_from + (abs(diff_i) - 1) * sign_i
            j_to_before = j_from + (abs(diff_j) - 1) * sign_j
            # 다른 경로는 다 비어있고 
            # 마지막 목적지에만 적의 말이 놓여있는 경우
            # 말을 잡고 목적지로 움직인다
            if i_from == i_to_before and j_from == j_to_before:
                # print("옆의놈먹자")
                self.set_piece_alive(self.get_piece_num(target_piece_team, i_to,j_to), False)
                self.set_piece_pos(self.get_piece_num(src_piece_team, i_from,j_from), i_to, j_to)
                return True
            elif self.is_diagonal_clear(i_from, j_from, i_to_before, j_to_before):
                self.set_piece_alive(self.get_piece_num(target_piece_team, i_to,j_to), False)
                self.set_piece_pos(self.get_piece_num(src_piece_team, i_from,j_from), i_to, j_to)
                return True

        return False
ch = Chess()
ch.print_board()