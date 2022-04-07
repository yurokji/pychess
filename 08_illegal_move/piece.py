from chess_const import *

# 기본적인 말
class Piece:
    def __init__(self, teamColor, type, pos, num):
        self.__type = type
        self.__team = teamColor
        self.__pos = pos
        self.__num = num
        self.__alive = False
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