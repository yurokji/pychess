from chess_const import *
import pygame
from pygame.locals import *

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
    