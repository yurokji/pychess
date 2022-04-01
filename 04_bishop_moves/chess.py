from pickle import TRUE
from platform import java_ver
from numpy import True_
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
        self.SURFACE = pygame.display.set_mode((CHES_BOARD_SIZE,CHES_BOARD_SIZE))
        self.img_horse = pygame.image.load((CHESS_HORSE_IMAGE_NAME))
        self.white_horse_list = []
        self.black_horse_list = []
        self.prep_horse_picture()
        self.SURFACE.fill((100,100,100))

    def prep_horse_picture(self):
        for i in range(2):
            for j in range(6):
                self.img_horse = pygame.transform.scale(self.img_horse, (CHESS_HORSE_PIXELS * 6,CHESS_HORSE_PIXELS * 2))
                cropped_region = (j * CHESS_HORSE_PIXELS, i * CHESS_HORSE_PIXELS, CHESS_HORSE_PIXELS, CHESS_HORSE_PIXELS)
                cropped = pygame.Surface((CHESS_HORSE_PIXELS, CHESS_HORSE_PIXELS), pygame.SRCALPHA)
                cropped.blit(self.img_horse, (0,0), cropped_region)
                if i == 0:
                    self.white_horse_list.append(cropped)
                else:
                    self.black_horse_list.append(cropped)


# 기본적인 말
class Horse:
    def __init__(self, color, type, pos, num, alive=True):
        self.type = type
        self.color = color
        self.pos = pos
        self.prevPos = pos
        self.num = num
        self.alive = alive
        
    def setAlive(self, alive):
        self.alive = alive

# 검은색/ 흰색 팀 만들기
class Team:
    def __init__(self, color):
        self.color = color
        self.horses = []
        self.makeTeam()
    
    # 초기 말의 위치를 정함
    def makeTeam(self):
         # 검은색 팀일 경우
        if self.color == BLACK:
            for x in range(CHESS_BOARD_CELL_WIDTH):
                self.horses.append(Horse(self.color, PAWN, [1, x], int(x)))
            self.horses.append(Horse(self.color, ROOK, [0, 0], 8))
            self.horses.append(Horse(self.color, KNIGHT, [0, 1],9))
            self.horses.append(Horse(self.color, BISHOP, [0, 2],10))
            self.horses.append(Horse(self.color, KING, [0, 3],11))
            self.horses.append(Horse(self.color, QUEEN, [0, 4],12))
            self.horses.append(Horse(self.color, BISHOP, [0, 5],13))
            self.horses.append(Horse(self.color, KNIGHT, [0, 6],14))
            self.horses.append(Horse(self.color, ROOK, [0, 7],15))
        # 흰색 팀일 경우
        else:
            for x in range(CHESS_BOARD_CELL_WIDTH):
                self.horses.append(Horse(self.color, PAWN, [6, x], 20+int(x)))
            self.horses.append(Horse(self.color, ROOK, [7, 0],28))
            self.horses.append(Horse(self.color, KNIGHT, [7, 1],29))
            self.horses.append(Horse(self.color, BISHOP, [7, 2],30))
            self.horses.append(Horse(self.color, KING, [7, 3],31))
            self.horses.append(Horse(self.color, QUEEN, [7, 4],32))
            self.horses.append(Horse(self.color, BISHOP, [7, 5],33))
            self.horses.append(Horse(self.color, KNIGHT, [7, 6],34))
            self.horses.append(Horse(self.color, ROOK, [7, 7],35))
     
        


  
class Chess:
    teams = {}
    def __init__(self):
        self.num_moves = 0  
        self.board = []
        self.turn = WHITE
        self.teams["black"] = Team(BLACK)
        self.teams["white"] = Team(WHITE)
        self.clear_board()
        self.fill_board()
        self.display = Display()
        self.running = True

   
    def clear_board(self):
        self.board = []
        for N in range(CHESS_BOARD_CELL_WIDTH):
            row = []
            for M in range(CHESS_BOARD_CELL_WIDTH):
                row.append(EMPTY)
            self.board.append(row)
    
    def print_board(self):
        for N in range(CHESS_BOARD_CELL_WIDTH):
            for M in range(CHESS_BOARD_CELL_WIDTH):
                print(self.board[N][M][:2], end=" ")
            print()
        print()


    def erase_board(self):
        for N in range(CHESS_BOARD_CELL_WIDTH):
            for M in range(CHESS_BOARD_CELL_WIDTH):
                self.board[N][M] = EMPTY

    
    def is_valid_pos_str(self, pos_str):
        if len(pos_str) != 2:
            return False
        else:
            if ord(pos_str[0]) >= ord('a') and ord(pos_str[0]) <= ord('h'):
                if int(pos_str[1]) >= 1 and int(pos_str[1]) <= 8:
                    return True

    def isValidPos(self, i, j):
        if (i >= 0 and i <= 7) and (j >= 0 and j <= 7):
            return True
        return False


    def isValidCell(self, i,j):
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
    def posPixel2Num(self, sx, sy, px, py, stride):
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


    #) 예 -> posNum2Str(i=1, j=1) --> 'b7'
    def posNum2Str(self, i, j):
        str_pos =""
        if self.isValidPos(i) and self.isValidPos(j):
            str_pos = chr(ord('a') + j) + str(CHESS_BOARD_CELL_WIDTH - i)
            # print(i,j, "-->", str_pos)
            return True, str_pos
        return False, str_pos
    
    
    def get_horse_team(self, i, j):
        return self.board[i][j][0]
    
    def get_horse_type(self, i,j):
        return self.board[i][j][1]

    
    def get_horse_num(self, color, i,j):
        if color == BLACK:
            for black_horse in self.teams["black"].horses:
                if black_horse.pos[0] == i and black_horse.pos[1] == j:
                    return black_horse.num
        else:   
            for white_horse in self.teams["white"].horses:
                print(white_horse.pos, i, j)
                if white_horse.pos[0] == i and white_horse.pos[1] == j:
                    return white_horse.num
        return -1
    
    def get_horse_pos(self, horse_num):
        if horse_num < 20:
            for black_horse in self.teams["black"].horses:
                if black_horse.num == horse_num:
                    return black_horse.pos[0], black_horse.pos[1]
        else:
            for white_horse in self.teams["white"].horses:
                if white_horse.num == horse_num:
                    return white_horse.pos[0], white_horse.pos[1]
        return -1, -1
    
    def set_horse_pos(self, horse_num, i_to, j_to):
        if horse_num < 20:
            for i in range(len(self.teams["black"].horses)):
                if self.teams["black"].horses[i].num == horse_num:
                    self.teams["black"].horses[i].pos = [i_to, j_to]
                    break
        else:  
            for i in range(len(self.teams["white"].horses)):
                if self.teams["white"].horses[i].num == horse_num:
                    self.teams["white"].horses[i].pos = [i_to, j_to]
                    break
   
   
    def set_horse_alive(self, horse_num, alive):
        if horse_num < 20:
            for i in range(len(self.teams["black"].horses)):
                if self.teams["black"].horses[i].num == horse_num:
                    self.teams["black"].horses[i].setAlive(alive)
                    break
        else:  
            for i in range(len(self.teams["white"].horses)):
                if self.teams["white"].horses[i].num == horse_num:
                    self.teams["white"].horses[i].setAlive(alive)
                    break
   
    
    def get_cell(self, i, j):
        return self.board[i][j]
    
    def set_cell(self, colorStr, typeStr, i, j, num):
        self.board[i][j] =  colorStr + typeStr + "{:02d}".format(num) 

    
    # def set_cell(self, pos_str, horse_type_str):
    #     isValid, i, j  = self.posStr2Num(pos_str)
    #     if isValid:
    #         self.board[i][j] = horse_type_str
    #         return True
    #     return False

    def fill_board(self):
        for black_horse in self.teams["black"].horses:
            if black_horse.alive:
                self.set_cell(black_horse.color, black_horse.type, black_horse.pos[0], black_horse.pos[1], black_horse.num)
            else:
                print(black_horse, "black not alive")
        for white_horse in self.teams["white"].horses:
            if white_horse.alive:
                self.set_cell(white_horse.color, white_horse.type, white_horse.pos[0], white_horse.pos[1], white_horse.num)
            else:
                print(white_horse, "white not alive")


    def update_board(self):
        self.clear_board()
        print("cleared")
        self.print_board()
        self.fill_board()
        self.print_board()
        
    def nextTurn(self, moved):
        if moved:
            if self.turn == WHITE:
                self.turn = BLACK
            else:
                self.turn = WHITE

    def checkHorseType(self, i, j, HORSETYPE):
        return HORSETYPE == self.get_horse_type(i,j)


    def move(self, i_from, j_from, i_to, j_to):
        if i_from == i_to and j_from == j_to:
            return False
        srcTeam = self.get_cell(i_from, j_from)[0]
        teamStr = ""
        if srcTeam == BLACK:
            teamStr = "검은색"
        else:
            teamStr = "흰색"
            
        isSrcTurn = (self.turn == srcTeam)
        isValid_from = self.isValidPos(i_from, j_from)
        isValid_to = self.isValidPos(i_to, j_to)
        if not isSrcTurn or not isValid_from or not isValid_to:
            return False
        isMoved = False
        if self.checkHorseType(i_from, j_from, PAWN):
            if self.pawn_move(i_from, j_from, i_to, j_to):
                print(teamStr+"폰 이동")
                isMoved = True
            elif self.pawn_attack(i_from, j_from, i_to, j_to):
                print(teamStr+"폰 공격")
                isMoved = True
        elif self.checkHorseType(i_from, j_from, ROOK):
            if self.rook_move(i_from, j_from, i_to, j_to):
                print(teamStr+"룩 이동")
                isMoved = True
            elif self.rook_attack(i_from, j_from, i_to, j_to):
                print(teamStr+"룩 공격")
                isMoved = True

       
        # 말이 성공적으로 움직였다면
        if isMoved: 
             # 보드 업데이트
            self.update_board()
               # 상대편 차례
            self.nextTurn(isMoved)
                
    # 폰 움직임 함수
    def pawn_move(self, i_from, j_from, i_to, j_to):
        src_horse = self.get_cell(i_from, j_from)
        src_horse_team = src_horse[0]
        target_horse = self.get_cell(i_to, j_to)
        target_horse_team = target_horse[0]
        isJPosSame = j_from == j_to
        isIPosNotSame = i_from != i_to
        isTargetEmpty = self.board[i_to][j_to] ==  EMPTY 
        isValid = isJPosSame and isIPosNotSame and isTargetEmpty
        if isValid:
            # 흑일 때는 차이가 양수 1이나 2여야 함
            diff = i_to - i_from
            if self.turn == BLACK:
                # print("Asdfsadf")
                # print("검은 폰 움직임")
                if diff >= 1 and diff <= 2:
                    is_ok = True
                    for di in range(1, diff + 1):
                        if self.board[i_from + di][j_from] != EMPTY:
                            is_ok = False
                            break
                    if is_ok:
                        self.set_horse_pos(self.get_horse_num(src_horse_team, i_from,j_from), i_to, j_to)
                        return True
            # 흰 폰 움직임
            else:
                if diff >= -2 and diff <= -1:
                    is_ok = True
                    for di in range(1, abs(diff) + 1):
                        if self.board[i_from - di][j_from] != EMPTY:
                            is_ok = False
                            break
                    if is_ok:
                        self.set_horse_pos(self.get_horse_num(src_horse_team, i_from,j_from), i_to, j_to)
                        return True
        return False

    # 폰 움직임 함수
    # pawn_move('b2', 'b4')
    def pawn_attack(self, i_from, j_from, i_to, j_to):
        src_horse = self.get_cell(i_from, j_from)
        src_horse_team = src_horse[0]
        target_horse = self.get_cell(i_to, j_to)
        target_horse_team = target_horse[0]
        is_killed = False
        diff_i = i_to - i_from
        diff_j = j_to - j_from

        # 움직임이 대각선인지 체크
        if abs(diff_i) != 1 or abs(diff_j) != 1:
            return False
        
        # 공격할 대상이 없는지 체크
        if target_horse == EMPTY:
            return False
        
        # 다른 편인지 체크
        if  src_horse[0] == target_horse[0]:
            return False
    
        if team_color == BLACK:
           
            if diff_i == 1:
                print("검은 폰 움직임")
                print("before: ", self.get_horse_num(src_horse_team, i_from,j_from))
                self.set_horse_alive(self.get_horse_num(target_horse_team, i_to,j_to), False)
                self.set_horse_pos(self.get_horse_num(src_horse_team, i_from,j_from), i_to, j_to)
                return True
        else:
           
            if diff_i == -1:
                print("흰 폰 움직임")
                print("before: ", self.get_horse_num(src_horse_team, i_from,j_from))
                self.set_horse_alive(self.get_horse_num(target_horse_team, i_to,j_to), False)
                self.set_horse_pos(self.get_horse_num(src_horse_team, i_from,j_from), i_to, j_to)
                return True

        return False
        
        
        

    def isHoriClear(self, i_from, j_from, i_to, j_to):
        diff = j_to - j_from 
        for di in range(1, abs(diff) + 1):
            if self.board[i_from][j_from + sign(diff) * di] != EMPTY:
                return False
        return True
    
    def isVertClear(self, i_from, j_from, i_to, j_to):
        diff = i_to - i_from 
        for di in range(1, abs(diff) + 1):
            if self.board[i_from + sign(diff) * di][j_from] != EMPTY:
                return False  
        return True          
                

    def rook_move(self, i_from, j_from, i_to, j_to):
        src_horse = self.get_cell(i_from, j_from)
        src_horse_team = src_horse[0]
        target_horse = self.get_cell(i_to, j_to)
        target_horse_team = target_horse[0]
        isTargetMine = src_horse[0] != target_horse[0]
        isHorizontal = i_from == i_to and j_from != j_to
        isVertical = i_from != i_to and j_from == j_to
        isHoriVert = isHorizontal or isVertical
        isValid = isTargetMine and isHoriVert
        if isValid:
            # 룩이 수평 이동하는 경우
            if isHorizontal:
                # 목적지 도착 직전 위치 계산
                j_to_before = j_from + (abs(j_to - j_from) - 1) * sign(j_to - j_from)
                print("j_to_before",j_to_before)
                # 마지막 목적지 바로 전까지 경로가 다 비어있는지 검사한다
                # 경로가 하나라도 비어있지 않다면 바로 종료하여 움직일 수 없도록 한다
                if self.isHoriClear(i_from, j_from, i_to, j_to):
                    print("이동")
                    self.set_horse_pos(self.get_horse_num(src_horse_team, i_from,j_from), i_to, j_to)
                    return True


            # 룩이 수직이동하는 경우
            elif isVertical:
                # 목적지 도착 직전 위치 계산
                i_to_before = i_from + (abs(i_to - i_from) - 1) * sign(i_to - i_from)
                # 마지막 목적지 바로 전까지 경로가 다 비어있는지 검사한다
                if self.isVertClear(i_from, j_from, i_to, j_to):
                    self.set_horse_pos(self.get_horse_num(src_horse_team, i_from,j_from), i_to, j_to)
                    return True
        return False
    
    def rook_attack(self, i_from, j_from, i_to, j_to):
        src_horse = self.get_cell(i_from, j_from)
        src_horse_team = src_horse[0]
        target_horse = self.get_cell(i_to, j_to)
        target_horse_team = target_horse[0]
        isTargetMine = src_horse[0] != target_horse[0]
        isHorizontal = i_from == i_to and j_from != j_to
        isVertical = i_from != i_to and j_from == j_to
        isHoriVert = isHorizontal or isVertical
        isValid = isTargetMine and isHoriVert
        if isValid:
            # 룩이 수평 이동하는 경우
            if isHorizontal:
                # 목적지 도착 직전 위치 계산
                j_to_before = j_from + (abs(j_to - j_from) - 1) * sign(j_to - j_from)
                # 다른 경로는 다 비어있고 
                # 마지막 목적지에만 적의 말이 놓여있는 경우
                # 말을 잡고 목적지로 움직인다
                if j_from == j_to_before:
                    print("옆의놈먹자")
                    self.set_horse_alive(self.get_horse_num(target_horse_team, i_to,j_to), False)
                    self.set_horse_pos(self.get_horse_num(src_horse_team, i_from,j_from), i_to, j_to)
                    return True
                elif self.isHoriClear(i_from, j_from, i_to, j_to_before):
                    self.set_horse_alive(self.get_horse_num(target_horse_team, i_to,j_to), False)
                    self.set_horse_pos(self.get_horse_num(src_horse_team, i_from,j_from), i_to, j_to)
                    return True

            # 룩이 수직이동하는 경우
            elif isVertical:
                # 목적지 도착 직전 위치 계산
                i_to_before = i_from + (abs(i_to - i_from) - 1) * sign(i_to - i_from)
                # # 마지막 목적지에만 적의 말이 놓여있는 경우
                # # 말을 잡고 목적지로 움직인다
                if i_from == i_to_before:
                    if target_horse[:2] != EMPTY:
                        self.set_horse_alive(self.get_horse_num(target_horse_team, i_to,j_to), False)
                    self.set_horse_pos(self.get_horse_num(src_horse_team, i_from,j_from), i_to, j_to)
                    return True
                elif self.isVertClear(i_from, j_from, i_to_before, j_to):
                    self.set_horse_alive(self.get_horse_num(target_horse_team, i_to,j_to), False)
                    self.set_horse_pos(self.get_horse_num(src_horse_team, i_from,j_from), i_to, j_to)
                    return True



        return False



ch = Chess()
ch.print_board()