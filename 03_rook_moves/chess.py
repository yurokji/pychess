from pickle import TRUE
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

class Input:
	def __init__(self):
		self.mouse_pressed = False
		self.mouse_clicked = False
		self.mx = 0
		self.my = 0
		
		self.src_pos = ""
		self.src_horse_type = ""
		self.src_rect = (CHESS_BOARD_PADDING, CHESS_BOARD_PADDING, CHESS_BOARD_CELL_PIXELS, CHESS_BOARD_CELL_PIXELS)
		self.is_src_set = False
		
		self.target_pos = ""
		self.target_horse_type = ""
		self.target_rect = (CHESS_BOARD_PADDING, CHESS_BOARD_PADDING, CHESS_BOARD_CELL_PIXELS, CHESS_BOARD_CELL_PIXELS)
		self.is_target_set = False
		

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


class Chess:
	def __init__(self):
		self.board = []
		self.turn = WHITE
		self.inventory = {}
		self.inventory[WHITE] = []
		self.inventory[BLACK] = []
		self.create_board()
		self.make_init_board()
		self.display = Display()
		self.input = Input()
		self.running = True

	def create_board(self):
		for N in range(CHESS_BOARD_TOTAL_CELLS):
			row = []
			for M in range(CHESS_BOARD_TOTAL_CELLS):
				row.append(EMPTY)
			self.board.append(row)
	
	def print_board(self):
		for N in range(CHESS_BOARD_TOTAL_CELLS):
			for M in range(CHESS_BOARD_TOTAL_CELLS):
				print(self.board[N][M], end=" ")
			print()
		print()


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

	def is_valid_pos_num(self, pos_num):
		if pos_num >= 0 and pos_num <= 7:
			return True
		return False


	# 변환 'a8' --> (i=0, j=0)
	# 변환 'b7' --> (i=1, j=1)
	def posStr2Num(self, pos_str):
		if self.is_valid_pos_str(pos_str):
			i = CHESS_BOARD_TOTAL_CELLS - int(pos_str[1])
			j = ord(pos_str[0]) - ord('a')
			return True, i, j
		else:
			return False, -1, -1

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
		print(i , j, i_upper, i_lower, j_left, j_right)
		if i >= i_upper + pad and i <= i_lower - pad:
			if j >= j_left + pad and j <= j_right - pad:
				return True, i_upper, j_left

		return False, i_upper, j_left


	#) 예 -> posNum2Str(i=1, j=1) --> 'b7'
	def posNum2Str(self, i, j):
		str_pos =""
		if self.is_valid_pos_num(i) and self.is_valid_pos_num(j):
			str_pos = chr(ord('a') + j) + str(CHESS_BOARD_TOTAL_CELLS - i)
			# print(i,j, "-->", str_pos)
			return True, str_pos
		return False, str_pos
	

	# set_cell('a8', BLACK + ROOK)
	def set_cell(self, pos_str, horse_type_str):
		isValid, i, j  = self.posStr2Num(pos_str)
		if isValid:
			self.board[i][j] = horse_type_str
			return True
		return False

	def make_init_board(self):
		self.set_cell('a8', BLACK + ROOK)
		self.set_cell('b8', BLACK + KNIGHT)
		self.set_cell('c8', BLACK + BISHOP)
		self.set_cell('d8', BLACK + KING)
		self.set_cell('e8', BLACK + QUEEN)
		self.set_cell('f8', BLACK + BISHOP)
		self.set_cell('g8', BLACK + KNIGHT)
		self.set_cell('h8', BLACK + ROOK)
		for x in range(CHESS_BOARD_TOTAL_CELLS):
			pos_str = chr(ord('a') + x)
			self.set_cell(pos_str + '7', BLACK + PAWN)

		for x in range(CHESS_BOARD_TOTAL_CELLS):
			pos_str = chr(ord('a') + x)
			self.set_cell(pos_str + '2', WHITE + PAWN)

		self.set_cell('a1', WHITE + ROOK)
		self.set_cell('b1', WHITE + KNIGHT)
		self.set_cell('c1', WHITE + BISHOP)
		self.set_cell('d1', WHITE + KING)
		self.set_cell('e1', WHITE + QUEEN)
		self.set_cell('f1', WHITE + BISHOP)
		self.set_cell('g1', WHITE + KNIGHT)
		self.set_cell('h1', WHITE + ROOK)

	def nextTurn(self, moved):
		if moved:
			if self.turn == WHITE:
				self.turn = BLACK
			else:
				self.turn = WHITE

	def checkHorseType(self, i, j, HORSETYPE):
		horse = self.board[i][j]
		return horse == self.turn+HORSETYPE

	def getCurrHorse(self):
		return self.input.src_horse_type

	def move(self, from_pos_str, to_pos_str):
		from_pos_str = from_pos_str.lower()
		to_pos_str = to_pos_str.lower()
		if from_pos_str == to_pos_str:
			return False
		isSrcTurn = self.turn == self.input.src_horse_type[0]
		isValid_from, i_from, j_from  = self.posStr2Num(from_pos_str)
		isValid_to, i_to, j_to  = self.posStr2Num(to_pos_str)
		if not isSrcTurn or not isValid_from or not isValid_to:
			return False

		isMoved = False
		if self.checkHorseType(i_from, j_from, PAWN):
			if self.pawn_move(i_from, j_from, i_to, j_to):
				isMoved = True
			elif self.pawn_attack(i_from, j_from, i_to, j_to):
				isMoved = True
		elif self.checkHorseType(i_from, j_from, ROOK):
			if self.rook_move(i_from, j_from, i_to, j_to):
				isMoved = True

		# 말이 성공적으로 놓여졌다면 상대편 차례
		self.nextTurn(isMoved)
				
	# 폰 움직임 함수
	# pawn_move('b2', 'b4')
	def pawn_move(self, i_from, j_from, i_to, j_to):
		isJPosSame = j_from == j_to
		isIPosNotSame = i_from != i_to
		isTargetEmpty = self.board[i_to][j_to] ==  EMPTY 
		isValid = isJPosSame and isIPosNotSame and isTargetEmpty
		# print("SRC:", i_from, j_from, "TGT:", i_to, j_to)
		# print("SRC TYPE:", self.turn, self.input.src_horse_type)
		if isValid:
			tempStr = self.board[i_to][j_to]
			# 흑일 때는 차이가 양수 1이나 2여야 함
			diff = i_to - i_from
			if self.turn == BLACK:
				# print("검은 폰 움직임")
				if diff >= 1 and diff <= 2:
					is_ok = True
					for di in range(1, diff + 1):
						if self.board[i_from + di][j_from] != EMPTY:
							is_ok = False
							break
					if is_ok:
						self.board[i_from][j_from] = EMPTY
						self.board[i_to][j_to] = self.getCurrHorse()
						return True
			
			else:
				# print("흰 폰 움직임")
				if diff >= -2 and diff <= -1:
					is_ok = True
					for di in range(1, abs(diff) + 1):
						if self.board[i_from - di][j_from] != EMPTY:
							is_ok = False
							break
					if is_ok:
						self.board[i_from][j_from] = EMPTY
						self.board[i_to][j_to] = self.getCurrHorse()			
						return True

		return False

	# 폰 움직임 함수
	# pawn_move('b2', 'b4')
	def pawn_attack(self, i_from, j_from, i_to, j_to):
		is_killed = False
		tempStr = self.board[i_to][j_to]

		diff_i = i_to - i_from
		diff_j = j_to - j_from

		# 움직임이 대각선인지 체크
		if abs(diff_i) != 1 or abs(diff_j) != 1:
			return False
			
		if self.board[i_to][j_to] == EMPTY:
			return False

		if  self.board[i_to][j_to][0] == self.input.src_horse_type[0]:
			return False
	
		if self.turn == BLACK:
			# print("검은 폰 움직임")
			if diff_i == 1:
				self.board[i_from][j_from] = EMPTY
				self.board[i_to][j_to] = self.getCurrHorse()
				is_killed = True
		else:
			# print("흰 폰 움직임")
			if diff_i == -1:
				self.board[i_from][j_from] = EMPTY
				self.board[i_to][j_to] = self.getCurrHorse()	
				is_killed = True		

		if is_killed:
			self.inventory[self.turn].append(tempStr)
			print("inventory", self.inventory[self.turn])
			return True
		else:
			return False


	def rook_move(self, i_from, j_from, i_to, j_to):
		# print("SRC:", i_from, j_from, "TGT:", i_to, j_to)
		# print("SRC TYPE:", self.turn, self.input.src_horse_type, self.input.target_horse_type)
		isTargetMine = self.input.src_horse_type[0] != self.input.target_horse_type[0]
		isHorizontal = i_from == i_to and j_from != j_to
		isVertical = i_from != i_to and j_from == j_to
		isHoriVert = isHorizontal or isVertical
		isValid = isTargetMine and isHoriVert
		print(isTargetMine, isHoriVert)
		if isValid:
			isTargetEmpty = self.board[i_to][j_to] ==  EMPTY
			tempStr = self.board[i_to][j_to]

			is_ok = True
			is_killed = False
			if isHorizontal:
				diff = j_to - j_from 
				for di in range(1, abs(diff) + 1):
					if di < diff:
						if self.board[i_from][j_from + sign(diff) * di] != EMPTY:
							is_ok = False
							break


			elif isVertical:
				diff = i_to - i_from 
				for di in range(1, abs(diff + 1)):
					if di < diff:
						if self.board[i_from + sign(diff) * di][j_from] != EMPTY:
							is_ok = False
							break
					else:
						if self.board[i_from + sign(diff) * di][j_from]!= EMPTY:
							is_killed = True
				
			if is_ok:
				self.board[i_from][j_from] = EMPTY
				self.board[i_to][j_to] = self.getCurrHorse()
				if is_killed:
					self.inventory[self.turn].append(tempStr)
					print("inventory", self.inventory[self.turn])
				return True
		return False

