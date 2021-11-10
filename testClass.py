class Horse:
    def __init__(self, side):
        self.side = side
        self.pos = ""
        self.prev = ""
        self.type = 0

    def setPos(self, val):
        self.pos = val



class Pawn(Horse):
    def __init__(self, side):
        super().__init__(side)

class King(Horse):
    def __init__(self, side):
        super().__init__(side)

class Queen(Horse):
    def __init__(self, side):
        super().__init__(side)

class Bishop(Horse):
    def __init__(self, side):
        super().__init__(side)

class Knight(Horse):
    def __init__(self, side):
        super().__init__(side)

class Rook(Horse):
    def __init__(self, side):
        super().__init__(side)


