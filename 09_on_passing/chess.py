from pickle import TRUE
from platform import java_ver
import math
from chess_const import *
from team import *
from display import *

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return x

       

  
class Chess:
    teams = {}
    def __init__(self):
        self.__board = []
        self.__turn = WHITE
        self.__teams = {}
        self.__teams[BLACK] = Team(BLACK)
        self.__teams[WHITE] = Team(WHITE)
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
        return self.__teams[colorStr]
   
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


   
    def pos_2_ij(self, pos):
        i = pos[0]
        j = pos[1]
        return i,j
    

    def is_valid_pos(self, pos):
        i, j = self.pos_2_ij(pos)
        if (i >= 0 and i <= 7) and (j >= 0 and j <= 7):
            return True




        
    # 픽셀 위치를 -> i, j롤 환산하는 함수
    def pixel_2_pos(self, sx, sy, px, py, stride):
        pad = 0.1
        i = (py - sy) / stride 
        j = (px - sx) / stride
        # i <= 4.801 --> 4 ;; 4.1 ~ 4.9
        # j <= 2.3 --> 2 ;; 2.1 ~ 2.9
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


    
    def get_piece_num_from_board(self, color, pos):
        if color == BLACK:
            pieces = self.get_team(BLACK).get_all_pieces()
        else:
            pieces = self.get_team(WHITE).get_all_pieces()
        for idx, piece in enumerate(pieces):
            if piece.get_alive():
                pos_i, pos_j = piece.get_pos()
                if pos_i == pos[0] and pos_j == pos[1]:
                    return idx
        return -1
    
    
    def get_cell_from_board(self, pos):
        return self.__board[pos[0]][pos[1]]

    def set_cell_into_board(self, colorStr, typeStr, pos, num):
        self.__board[pos[0]][pos[1]] =  colorStr + typeStr + "{:02d}".format(num) 
    
    def fill_board(self):
        pieces = self.get_team(BLACK).get_all_pieces()
        for piece in pieces:
            if piece.get_alive():
                self.set_cell_into_board(piece.get_team(), piece.get_type(), piece.get_pos(), piece.get_num())
        pieces = self.get_team(WHITE).get_all_pieces()
        for piece in pieces:
            if piece.get_alive():
                self.set_cell_into_board(piece.get_team(), piece.get_type(), piece.get_pos(), piece.get_num())

    def update_board(self):
        self.clear_board()
        self.fill_board()
        
    def get_current_turn(self):
        return self.__turn
    
    def set_turn(self, turn):
        self.__turn = turn
        
    def get_next_turn(self):
        if self.get_current_turn() == WHITE:
            return BLACK
        else:
            return WHITE

    def is_horizontal_clear(self, pos_from, pos_to):
        i_from, j_from = self.pos_2_ij(pos_from)
        i_to, j_to = self.pos_2_ij(pos_to)
        diff_j = j_to - j_from 
        for di in range(1, abs(diff_j) + 1):
            if self.get_cell_from_board((i_from, j_from + sign(diff_j) * di)) != EMPTY:
                return False
        return True
    
    def is_vertical_clear(self, pos_from, pos_to):
        i_from, j_from = self.pos_2_ij(pos_from)
        i_to, j_to = self.pos_2_ij(pos_to)
        diff_i = i_to - i_from 
        for di in range(1, abs(diff_i) + 1):
            if self.get_cell_from_board((i_from + sign(diff_i) * di, j_from)) != EMPTY:
                return False  
        return True       

    # 대각선 방향 경로가 비워져있는지
    def is_diagonal_clear(self, pos_from, pos_to):
        i_from, j_from = self.pos_2_ij(pos_from)
        i_to, j_to = self.pos_2_ij(pos_to)
        diff_i = i_to - i_from 
        diff_j = j_to - j_from 
        if abs(diff_i) != abs(diff_j):
            return False
        sign_i = sign(diff_i)
        sign_j = sign(diff_j) 
        for di in range(1, abs(diff_i) + 1):
            ic = i_from + sign_i * di
            jc = j_from + sign_j * di
            if self.get_cell_from_board((i_from + sign_i * di, j_from + sign_j * di)) != EMPTY:
                return False  
        return True     


    def is_pos_same(self, pos1, pos2):
        if pos1[0] == pos2[0] and pos1[1] == pos2[1]:
            return False


    def show_all_possible_move(self, pos_from):
        print("sadfasdfasdf")
        if not self.is_valid_pos(pos_from):
            return False
        src_cell = self.get_cell_from_board(pos_from)
        src_cell_team = src_cell[0]
        src_piece_num = self.get_piece_num_from_board(src_cell_team, pos_from)
        
       
        test_pos = []
        possible_pos = []
        for i in range(CHESS_NUM_CELLS):
            for j in range(CHESS_NUM_CELLS):
                if i != pos_from[0] or j != pos_from[1]:
                    test_pos.append([i,j])
        
        # print(test_pos)
        for pos_to in test_pos:
            
            target_cell = self.get_cell_from_board(pos_to)
            # print(pos_to, target_cell)
            target_cell_team = target_cell[0]
            target_piece_num = self.get_piece_num_from_board(target_cell_team, pos_to)
            target_piece_num_list = [target_piece_num]
            is_not_my_turn = src_cell_team != self.get_current_turn()
            is_not_valid_teams = src_cell_team == target_cell_team
            if is_not_my_turn or is_not_valid_teams:
                # print(pos_to, "is_not_valid_teams")
                continue
            
            isMoved = False
            isKilled = False
            
            if self.move(src_piece_num, pos_to):
                
                isMoved = True
                self.get_team(src_cell_team).get_piece(src_piece_num).set_pos(pos_to)
                self.update_board()
                # print("이동 가능:", pos_from, pos_to, target_piece_num)
                
            elif self.attack(src_piece_num, target_piece_num_list, pos_to):
                print("공격 가능:", target_cell_team, pos_from, pos_to, target_piece_num_list)
                self.get_team(src_cell_team).get_piece(src_piece_num).set_pos(pos_to)
                print(self.get_next_turn())
                print(target_piece_num_list[0])
                self.get_team(self.get_next_turn()).get_piece(target_piece_num_list[0]).set_alive(False)
                self.update_board()
                
                isKilled = True
            else:
                # print(pos_to, "no move")
                continue

            if isMoved or isKilled:
                if self.is_not_legal_move():
                    if self.get_team(src_cell_team).get_checked():
                        print("현재 체크 상태임")
                    # print("수를 놓을 수 없음")
                    if isKilled:
                        self.get_team(target_cell_team).get_piece(target_piece_num).set_alive(True)
                        isKilled = False
                    isMoved = False
                    self.get_team(src_cell_team).get_piece(src_piece_num).set_pos(pos_from)
                    self.update_board()
                    continue
            
            if isMoved or isKilled:
                self.get_team(src_cell_team).get_piece(src_piece_num).set_pos(pos_from)
                if isKilled:
                    self.get_team(self.get_next_turn()).get_piece(target_piece_num_list[0]).set_alive(True)
                self.update_board()
                possible_pos.append(pos_to)
                
                
        # print(possible_pos)
                    
        return possible_pos
    


    def put(self, pos_from, pos_to):
        print("원위치",pos_from, pos_to)
        is_two_pos_same = self.is_pos_same(pos_from, pos_to)
        is_not_valid_pos_from = not self.is_valid_pos(pos_from)
        is_not_valid_pos_to = not self.is_valid_pos(pos_to)
        
        if is_two_pos_same or is_not_valid_pos_from or is_not_valid_pos_to:
            return False
        
        src_cell = self.get_cell_from_board(pos_from)
        src_cell_team = src_cell[0]
        src_piece_num = self.get_piece_num_from_board(src_cell_team, pos_from)
        
        target_cell = self.get_cell_from_board(pos_to)
        target_cell_team = target_cell[0]
        target_piece_num = self.get_piece_num_from_board(target_cell_team, pos_to)
        target_piece_num_list = [target_piece_num]
        is_not_my_turn = src_cell_team != self.get_current_turn()
        is_not_valid_teams = src_cell_team == target_cell_team
        if is_not_my_turn or is_not_valid_teams:
            return False
        
        isMoved = False
        isKilled = False
        if self.move(src_piece_num, pos_to):
            isMoved = True
            self.get_team(src_cell_team).get_piece(src_piece_num).set_pos(pos_to)
            self.update_board()
        elif self.attack(src_piece_num, target_piece_num_list, pos_to):
            print("타켓넘버",target_piece_num_list[0])
            isKilled = True
            self.get_team(src_cell_team).get_piece(src_piece_num).set_pos(pos_to)
            self.get_team(self.get_next_turn()).get_piece(target_piece_num_list[0]).set_alive(False)
            
            self.update_board()
        else:
            return False
        
        # 허용되지 않은 수(illegal move)를 판단하는 부분:
        # 자신의 수로 인에 자신이 체크메이트에 걸리는지 검사
        # 킹은, 자신이나 신하에 의해 자살할 수 없음
        # 현재 체크되어있다면 체크되지 않도록 위치를 이동해야 함
        
        # 주의점: 체크메이트나 스테일메이트를 검사하려면
        # 자기말이나 킹을 옮겨서 체크를 피할 수 있는 자리가 있는지
        # 모두 확인을 해야 함
        # 그러려면 헬퍼를 만들어야 한다
        # 체크 상태일때, 체크를 피할 자신의 어떤 말의 위치가 있지 않다?
        # 그렇다면 체크메이트
        # 체크 상태가 아닐때, 자신의 어떤 말이라도 움직이면 체크가 된다?
        # 그렇다면 스테일메이트
        
        if isMoved or isKilled:
            if self.is_not_legal_move():
                if self.get_team(src_cell_team).get_checked():
                    print("현재 체크 상태임")
                print("수를 놓을 수 없음")
                if isKilled:
                    self.get_team(target_cell_team).get_piece(target_piece_num).set_alive(True)
                self.get_team(src_cell_team).get_piece(src_piece_num).set_pos(pos_from)
                self.update_board()
                return False
        
        # 프로모션 가능?
        if self.get_team(src_cell_team).get_piece(src_piece_num).get_type() == PAWN:
            if (self.get_team(src_cell_team).get_piece(src_piece_num).get_team() == WHITE and \
            self.get_team(src_cell_team).get_piece(src_piece_num).get_pos()[0] == 0) or \
            (self.get_team(src_cell_team).get_piece(src_piece_num).get_team() == BLACK and \
            self.get_team(src_cell_team).get_piece(src_piece_num).get_pos()[0] == 7):
                # print("퀸으로 프로모션")
                self.get_team(src_cell_team).get_piece(src_piece_num).set_type(QUEEN)
                self.update_board()
                
        
        if self.get_team(src_cell_team).get_checked():
            print("체크에서 벗어났나?")
        # 안전한 수를 놓아 자신의 킹이 체크에서 벗어났음
        self.get_team(src_cell_team).set_checked(False)
        # 반대로 자신의 수로 인에 상대방이 체크메이트에 걸리는지 검사
        if self.is_check():
            # print("상대편이 체크 상태에 놓였습니다")
            self.get_team(self.get_next_turn()).set_checked(True)
        
        
        
        return True
 
 
 ####################단순 기물 이동 부분#############################
    def move(self, src_piece_num, pos_to):
        is_target_filled = self.get_cell_from_board(pos_to) !=  EMPTY 
        if is_target_filled:
            return False
        src_team = self.get_current_turn()
        src_piece = self.get_team(src_team).get_piece(src_piece_num)
        print("단순기물이동", src_piece.get_pos(), pos_to)
        if self.piece_move(src_piece, pos_to):
            return True
        return False
 

    def piece_move(self,src_piece, pos_to):
        src_piece_team = src_piece.get_team()
        src_piece_type = src_piece.get_type()
        src_piece_moved = src_piece.get_moved()
        src_pos = src_piece.get_pos()
        if src_piece_type == PAWN:
             
            if src_piece_team == BLACK and src_pos[0] == 1 or src_piece_team == WHITE and src_pos[0] == 6:
                if self.pawn_twostep_move(src_piece, pos_to):
                    return True         
            if self.pawn_move(src_piece, pos_to):
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
                if self.get_cell_from_board([i_from + di, j_from]) != EMPTY:
                    is_ok = False
                    break
            if is_ok:
                return True
        elif src_team == WHITE and diff_i == -2:
            is_ok = True
            for di in range(1, abs(diff_i) + 1):
                if self.get_cell_from_board([i_from - di, j_from]) != EMPTY:
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
            if self.get_cell_from_board([i_from + diff_i, j_from]) == EMPTY:
                return True
        return False
    
    def rook_move(self, src_piece, pos_to):
        pos_from = src_piece.get_pos()
        i_from, j_from = self.pos_2_ij(pos_from)
        i_to, j_to = self.pos_2_ij(pos_to)
        isHorizontal = i_from == i_to and j_from != j_to
        isVertical = i_from != i_to and j_from == j_to
        if not (isHorizontal or isVertical):
            return False
        # 룩이 수평 이동하는 경우
        if isHorizontal:
            if self.is_horizontal_clear(pos_from, pos_to):
                return True
        # 룩이 수직이동하는 경우
        elif isVertical:
            # print("ver")
            if self.is_vertical_clear(pos_from, pos_to):
                return True
        return False
    
    def bishop_move(self, src_piece, pos_to):
        pos_from = src_piece.get_pos()
        i_from, j_from = self.pos_2_ij(pos_from)
        i_to, j_to = self.pos_2_ij(pos_to)
        diff_i = i_to - i_from 
        diff_j = j_to - j_from
        is_not_diag_move = abs(diff_i) != abs(diff_j)
        if is_not_diag_move:
            return False
        if self.is_diagonal_clear(pos_from, pos_to):
            return True
        return False
    
    def knight_move(self, src_piece, pos_to):
        pos_from = src_piece.get_pos()
        i_from, j_from = self.pos_2_ij(pos_from)
        i_to, j_to = self.pos_2_ij(pos_to)
        diff_i = i_to - i_from 
        diff_j = j_to - j_from
        move_cond1 =  abs(diff_i) >= 1 and abs(diff_i) << 2 
        move_cond2 =  abs(diff_j) >= 1 and abs(diff_j) << 2
        move_cond3 = (abs(diff_i) + abs(diff_j)) == 3
        if not (move_cond1 and move_cond2 and move_cond3):
            return False
        return True  
    
    def queen_move(self, src_piece, pos_to):
        # print(src_piece.get_type(), src_piece.get_pos(), pos_to)
        if self.rook_move(src_piece, pos_to):
            return True
        elif self.bishop_move(src_piece, pos_to):
            return True
        return False
    
    def king_move(self, src_piece, pos_to):
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
    def attack(self, src_piece_num, target_piece_num_list, pos_to):
        print("어택")
        src_team = self.get_current_turn()
        src_piece = self.get_team(src_team).get_piece(src_piece_num)
        pos_from = src_piece.get_pos()
        target_team = self.get_next_turn()
        target_piece = self.get_team(target_team).get_piece(target_piece_num_list[0])
        if target_piece == -1:
            target_cell = self.get_cell_from_board([pos_from[0], pos_to[1]])
            target_cell_team = target_cell[0]
            if target_cell ==  EMPTY:
                return False
            target_piece_num_list[0] = self.get_piece_num_from_board(target_cell_team, [pos_from[0], pos_to[1]])
            print("어택타켓넘버",target_piece_num_list[0])
            target_piece = self.get_team(target_cell_team).get_piece(target_piece_num_list[0])
            cond1 = src_team != target_cell_team
            cond2 = src_piece.get_type() == PAWN and target_piece.get_type() == PAWN
            if not cond1 or not cond2:
                return False
                
        is_target_empty = target_piece.get_type() ==  EMPTY 
        if is_target_empty:
            print("엠프티")
            return False
        
        if self.piece_attack(src_piece, target_piece, pos_to):
            return True
        return False
        
    
    def piece_attack(self, src_piece, target_piece, pos_to):
        pos_from = src_piece.get_pos()
        src_piece_type = src_piece.get_type()
        if src_piece_type == PAWN:
            if self.pawn_attack(src_piece, target_piece):
                # print("폰 공격 성공")
                return True
            elif self.pawn_on_passing_attack(src_piece, target_piece, pos_to):
                # print("폰 공격 성공")
                return True
        elif src_piece_type == ROOK:
            if self.rook_attack(src_piece, target_piece):
                # print("룩 공격 성공")
                return True
        elif src_piece_type == BISHOP:
            if self.bishop_attack(src_piece, target_piece):
                # print("비숍 공격 성공")
                return True
        elif src_piece_type == KNIGHT:
            if self.knight_attack(src_piece, target_piece):
                # print("나이트 공격 성공")
                return True
        elif src_piece_type == QUEEN:
            if self.queen_attack(src_piece, target_piece):
                # print("퀸 공격 성공")
                return True
        elif src_piece_type == KING:
            if self.king_attack(src_piece, target_piece):
                # print("킹 공격 성공")
                return True
        return False


    def pawn_attack(self, src_piece, target_piece):
        src_team = src_piece.get_team()
        pos_from = src_piece.get_pos()
        pos_to = target_piece.get_pos()
        print("위치",pos_from, "대상",pos_to)
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
 
    def pawn_on_passing_attack(self, src_piece, target_piece, pos_to_empty):
        
        src_team = src_piece.get_team()
        pos_from = src_piece.get_pos()
        pos_to = target_piece.get_pos()
        
        i_from, j_from = self.pos_2_ij(pos_from)
        i_to, j_to = self.pos_2_ij(pos_to)
        print("on_passing",pos_from, pos_to)
        diff_i = i_to - i_from
        diff_j = j_to - j_from
        diff_i2 = pos_to_empty[0] - i_from
        
        if abs(diff_i) != 0 or abs(diff_j) != 1:
            return False
        
        if src_team == BLACK and diff_i2 == 1:
            return True
        elif src_team == WHITE and diff_i2 == -1:
            return True
              
       
        return False
          
    def rook_attack(self, src_piece, target_piece):
        pos_from = src_piece.get_pos()
        pos_to = target_piece.get_pos()
        # print("룩 공격1", pos_from, pos_to)
        i_from, j_from = self.pos_2_ij(pos_from)
        i_to, j_to = self.pos_2_ij(pos_to)
        diff_i = i_to - i_from
        diff_j = j_to - j_from
        sign_i  = sign(diff_i)
        sign_j  = sign(diff_j)
        isHorizontal = i_from == i_to and j_from != j_to
        isVertical = i_from != i_to and j_from == j_to
        if not (isHorizontal or isVertical):
            return False
        # print("룩 공격", pos_from, pos_to)
        # 룩이 수평 이동하는 경우
        if isHorizontal:
            # print("수평공격")
            # 목적지 도착 직전 위치 계산
            j_to_before = j_from + (abs(diff_j) - 1) * sign_j
            # 다른 경로는 다 비어있고 
            # 마지막 목적지에만 적의 말이 놓여있는 경우
            # 말을 잡고 목적지로 움직인다
            if j_from == j_to_before:
                return True
            elif self.is_horizontal_clear(pos_from, [i_to, j_to_before]):
                return True

        # 룩이 수직이동하는 경우
        elif isVertical:
            # print("수직공격")
            # 목적지 도착 직전 위치 계산
            i_to_before = i_from + (abs(diff_i) - 1) * sign_i
            # print("i_to_before",i_to_before)
            # # 마지막 목적지에만 적의 말이 놓여있는 경우
            # # 말을 잡고 목적지로 움직인다
            if i_from == i_to_before:
                return True
            elif self.is_vertical_clear(pos_from, [i_to_before, j_to]):
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
        is_not_diag_move = abs(diff_i) != abs(diff_j)
        # print(src_piece.get_type(), pos_from, pos_to)
        if is_not_diag_move:
            # print(src_piece.get_type(), pos_from, pos_to)
            return False
        i_to_before = i_from + (abs(diff_i) - 1) * sign_i
        j_to_before = j_from + (abs(diff_j) - 1) * sign_j
        # 다른 경로는 다 비어있고 
        # 마지막 목적지에만 적의 말이 놓여있는 경우
        # 말을 잡고 목적지로 움직인다
        if self.is_pos_same(pos_from, [i_to_before, j_to_before]):
            # print("1", pos_from, [i_to_before, j_to_before])
            return True
        elif self.is_diagonal_clear(pos_from, [i_to_before, j_to_before]):
            # print("2", pos_from, [i_to_before, j_to_before])
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
        if not (move_cond1 and move_cond2 and move_cond3):
            return False
        return True  
     
    def queen_attack(self, src_piece, target_piece):
        pos_from = src_piece.get_pos()
        pos_to = target_piece.get_pos()
        # print("퀸 어태크",pos_from, pos_to)
        if self.rook_attack(src_piece, target_piece):
            # print("퀸 룩형식의 공격 성공")
            return True
        elif self.bishop_attack(src_piece, target_piece):
            # print("퀸 비숍형식의 공격 성공")
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
    
    

    # 적의 살아있는 기물이 자신의 킹을 잡을 수 있는지 판단한다
    # (즉, 체크메이트가 되는 형국인지)     
    def is_not_legal_move(self):
        print("sadfasdfasdf")
        # print("king num:", NUM_KING_PIECE)
        my_king_piece = self.get_team(self.get_current_turn()).get_piece(NUM_KING_PIECE)
        # print(self.get_next_turn())
        enemy_pieces = self.get_team(self.get_next_turn()).get_all_pieces()
        # 잠시 공수를 교대한다
        isVulnerable = False
        self.set_turn(self.get_next_turn())
        # print("마이프레셔스킹", my_king_piece.get_type(), my_king_piece.get_pos())
        for enemy_piece in enemy_pieces:
            if enemy_piece.get_alive():
                # print(enemy_piece.get_type(), enemy_piece.get_pos())
                isVulnerable = self.piece_attack(enemy_piece, my_king_piece, my_king_piece.get_pos())
                # print(isVulnerable)
                if isVulnerable == True:
                    break
        # 공수를 원래대로 복귀시킨다
        self.set_turn(self.get_next_turn())
        if isVulnerable:
            return True
        return False
        
 
    # 자신의 수로 인해 상대방이 체크당하는지 검사   
    def is_check(self):
        my_pieces = self.get_team(self.get_current_turn()).get_all_pieces()
        enemy_king_piece = self.get_team(self.get_next_turn()).get_piece(NUM_KING_PIECE)
        isVulnerable = False
        # print("체크 검사중", enemy_king_piece.get_type(), enemy_king_piece.get_pos())
        for my_piece in my_pieces:
            if my_piece.get_alive():
                # print(my_piece.get_type(), my_piece.get_pos())
                isVulnerable = self.piece_attack(my_piece, enemy_king_piece, enemy_king_piece.get_pos())
                # print(isVulnerable)
                if isVulnerable == True:
                    break
        if isVulnerable:
            return True
        return False