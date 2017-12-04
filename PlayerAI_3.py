from random import randint
from BaseAI_3 import BaseAI
import Minmax_3
 
class PlayerAI(BaseAI):
    def getMove(self, grid):
        return Minmax_3.minimax(grid)

