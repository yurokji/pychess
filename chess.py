from chess_const import *
import math
import pygame
from pygame.locals import *

class Input:
    def __init__(self):
        self.mouse_pressed = False
        self.mouse_clicked = False
        self.mx = 0
        self.my = 0
        self.src_pos = ""
        self.src_horse_type = ""
        self.src_rect = (CHESS_BOARD_PADDING, CHESS_BOARD_PADDING, CHESS_BOARD_CELL_PIXELS, CHESS_BOARD_CELL_PIXELS)
        self.target_pos = ""
        self.is_src_set = False
        self.is_target_set = False
        self.target_rect = (CHESS_BOARD_PADDING, CHESS_BOARD_PADDING, CHESS_BOARD_CELL_PIXELS, CHESS_BOARD_CELL_PIXELS)

class Display:
    def __init__(self):
        self.SURFACE = pygame.display.set_mode((CHESS_BOARD_IMAGE_PIXELS,CHESS_BOARD_IMAGE_PIXELS))
        self.img_horse = pygame.image.load(CHESS_BOARD_IMAGE_NAME)
        self.white_horse_list = []
        self.black_horse_list = []
        self.prep_horse_picture()
        self.SURFACE.fill((100,100,100))
        # self.SURFACE.blit(self.black_horse_list[3], (3 * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, 1 * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING))
    def prep_horse_picture(self):
        for i in range(2):        
            for j in range(6):
                self.img_horse = pygame.transform.scale(self.img_horse, (CHESS_HORSE_PIXELS * 6, CHESS_HORSE_PIXELS * 2))
                cropped_region = (j * CHESS_HORSE_PIXELS, i * CHESS_HORSE_PIXELS, CHESS_HORSE_PIXELS, CHESS_HORSE_PIXELS)
                cropped = pygame.Surface((CHESS_HORSE_PIXELS, CHESS_HORSE_PIXELS), pygame.SRCALPHA)
                cropped.blit(self.img_horse, (0,0), cropped_region)
                if i == 0:
                    self.white_horse_list.append(cropped)
                else:
                    self.black_horse_list.append(cropped)

class Horse:
    def __init__(self, side):
        self.side = side
        self.pos = ""
        self.prev = ""
        self.type = 0

    def setPos(self, val):
        self.pos = val


class Horse:
    def __init__(self, side, pos):
        self.side = side
        self.pos = ""
        self.prev = self.pos
        self.type = 0

    def setPos(self, val):
        self.pos = val


class Pawn(Horse):
    def __init__(self, side, pos):
        super().__init__(side, pos)

class King(Horse):
    def __init__(self, side, pos):
        super().__init__(side, pos)

class Queen(Horse):
    def __init__(self, side, pos):
        super().__init__(side, pos)

class Bishop(Horse):
    def __init__(self, side, pos):
        super().__init__(side, pos)

class Knight(Horse):
    def __init__(self, side, pos):
        super().__init__(side, pos)

class Rook(Horse):
    def __init__(self, side, pos):
        super().__init__(side, pos)


class Chess:
    def __init__(self):
        self.board = []
        self.create_board()
        self.make_init_board()
        self.display = Display()
        self.input = Input()
        self.running = True
        # self.display.SURFACE.blit(self.display.black_horse_list[3], (3 * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING, 1 * CHESS_BOARD_CELL_PIXELS + CHESS_BOARD_PADDING))
        print(self.board)

    def create_board(self):
        for N in range(CHESS_BOARD_TOTAL_CELLS):
            row = []
            for M in range(CHESS_BOARD_TOTAL_CELLS):
                row.append(EMPTY)
            self.board.append(row)

    # 보드판 지우기
    def erase_board(self):
        for N in range(CHESS_BOARD_TOTAL_CELLS):
            for M in range(CHESS_BOARD_TOTAL_CELLS):
                self.board[N][M] = EMPTY


    def is_valid_pos_str(self, pos_str):
        if len(pos_str) != 2:
            print("not two digits of string")
            return False
        else:
            if ord(pos_str[0]) >= ord('a') and ord(pos_str[0]) <= ord('h'):
                if int(pos_str[1]) >= 1 and int(pos_str[1]) <= 8:
                    return True
        return False

    def is_valid_pos_num(self, num):
        if num >= 0 and num <= 7:
            return True 
        return False



    def posPixel2Num(self, sx, sy, px, py, stride):
        pad = 0.1
        i = (py - sy) / stride
        j = (px - sx) / stride
        # i <= 4.801 -> 4
        # j <= 2.456  -> 2

        i_upper = math.floor(i) # 4
        i_lower = math.ceil(i) # 5
        j_left = math.floor(j) # 2
        j_right = math.ceil(j) # 3

        if i >= i_upper + pad and i <= i_lower - pad:
            if j >= j_left + pad and j <= j_right - pad:
                return True, i_upper, j_left

        return False, i_upper, j_left

    # 예) posNum2Str(i=1, j=1) -> 'b7' 
    def posNum2Str(self, i, j):
        str_pos =""
        if self.is_valid_pos_num(j):
            str_pos = chr(ord('a') + j)
            if self.is_valid_pos_num(i):
                str_pos += str(CHESS_BOARD_TOTAL_CELLS - i)        
            return True, str_pos
        return False, str_pos



    # 알파벳숫자로 된 문자열을
    # 수직수평 숫자로 바꿔주는 (리스트를 위해)
    # 변환 함수 
    # 예) posStr2Num('b7') -> (1,1)
    def posStr2Num(self, pos_str):
        if self.is_valid_pos_str(pos_str):
            i = CHESS_BOARD_TOTAL_CELLS - int(pos_str[1]) 
            j = ord(pos_str[0]) - ord('a')
            return True, i, j
        else:
            return False, -1, -1
    
    def set_cell(self, pos_str, horse_type_str):
        isValid, i, j = self.posStr2Num(pos_str)
        if isValid:
            self.board[i][j] = horse_type_str
        else:
            print("set_cell failed", isValid, i, j)
            return False   




     # 보드 초기상태 만들기
    def make_init_board(self):
        self.set_cell('a8', BLACK + ROOK)
        self.set_cell('b8', BLACK + KNIGHT)
        self.set_cell('c8', BLACK + BISHOP)
        self.set_cell('d8', BLACK + KING)
        self.set_cell('e8', BLACK + QUEEN)
        self.set_cell('f8', BLACK + BISHOP)
        self.set_cell('g8', BLACK + KNIGHT)
        self.set_cell('h8', BLACK + ROOK)
        for x in range(8):
            pos_str = chr(x + ord('a'))
            self.set_cell(pos_str + '7', BLACK + PAWN)

        for x in range(8):
            pos_str = chr(x + ord('a'))
            self.set_cell(pos_str + '2', WHITE + PAWN)


        self.set_cell('a1', WHITE + ROOK)
        self.set_cell('b1', WHITE + KNIGHT)
        self.set_cell('c1', WHITE + BISHOP)
        self.set_cell('d1', WHITE + KING)
        self.set_cell('e1', WHITE + QUEEN)
        self.set_cell('f1', WHITE + BISHOP)
        self.set_cell('g1', WHITE + KNIGHT)
        self.set_cell('h1', WHITE + ROOK)



    def print_board(self):
        for N in range(CHESS_BOARD_TOTAL_CELLS):
            for M in range(CHESS_BOARD_TOTAL_CELLS):
                print(self.board[N][M], end= "  ")
            print()


    def checkHorseType(self, i, j, str, HORSETYPE):
        return self.board[i][j][-2:] == str[0] + HORSETYPE


    # 각각의 말의 종류에 따라 출발지와 목적지를 넣었을때
    # (그 사이에 셀은 빈 것으로 일단 가정하고)
    # 그 움직임이 올바른지 체크한다
    # 일단 폰부터
    def move_pawn(self, from_str, to_str):
        from_str = from_str.lower()
        to_str = to_str.lower()
        if from_str[-2:] == to_str:
            return False
        isValidPos_from, i_from, j_from = self.posStr2Num(from_str[-2:])
        isSrcPawn = self.checkHorseType(i_from, j_from, from_str, PAWN)
        isValidPos_to, i_to, j_to = self.posStr2Num(to_str)
        isValidPos = isValidPos_from and isValidPos_to
        isJPosame = j_from == j_to
        isIPosNotSame = i_from != i_to
        isTargetEmpty = self.board[i_to][j_to] == EMPTY
        isValid = isValidPos and isJPosame and isIPosNotSame and isSrcPawn and isTargetEmpty
        print("SRC:", i_from, j_from, "TARGET:", i_to, j_to)
        print(self.board[i_from - 1][j_from])
        if isValid:
            tempStr = self.board[i_to][j_to]
            # 흑일 때는 차이가 양수 1 혹은 2여야 함
            diff = i_to - i_from
            print(diff)
            if from_str[0] == BLACK:
                print("black pawn move")
                # 폰이 움직일 수 있는 방향과 수에 해당한다면
                if diff >= 1 and diff <= 2:
                    is_ok = True
                    for di in range(1, diff + 1):
                        print(self.board[i_from + di][j_from])
                        if self.board[i_from + di][j_from] != EMPTY:
                            is_ok = False
                            break
                    if is_ok:
                        self.board[i_from][j_from] = EMPTY
                        self.board[i_to][j_to] = from_str[0] + PAWN
                        return True

            # 백일 때는 차이가 음수 -1 혹은 -2여야 함
            else:
                print("white pawn move")
                if diff >= -2 and diff <= -1:
                    is_ok = True
                    for di in range(1, abs(diff) + 1):
                        print(self.board[i_from - di][j_from])
                        if self.board[i_from - di][j_from] != EMPTY:
                            is_ok = False
                            break 
                    if is_ok:
                        self.board[i_from][j_from] = EMPTY
                        self.board[i_to][j_to] = from_str[0] + PAWN
                        return True
        else:
            return False
        return False




