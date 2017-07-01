import QTable
import MovingAgent
import random
import numpy as np
import matplotlib.pyplot as plt

class Hunter(MovingAgent):
    def __init__(self, nstate, naction, area):
        super().__init__(area,255)
        self.nstate = nstate
        self.naction = naction
        self.q = QTable.QTable(nstate, naction)
        self.adic = {}
        self.state = self.position + [self.watch()]

    def act(self, s, a):
        super().act(s,a)#引数でたらめ
        q.update()#引数でたらめ。

    def _reset(self):
        self.area.


    def act(self, s, a):

