from chess import Move

class MockGame:  
    
    def mainline_moves(self):
        move1 = Move.from_uci("b2b3")
        move2 = Move.from_uci("a7a6")
        return [move1, move2]