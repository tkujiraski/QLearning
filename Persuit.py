import QLearning
import random
import numpy as np
from numpy.random import randint
from GameGrid import GameGrid

class Persuit:
    """
    １つのエージェントがランダムに動く獲物を追跡する問題

    状態：現在の位置(y[0-6],x[0-6])、獲物の方向(上下左右、斜め各方向、視野外で９)
    アクション：上下左右への移動と停止の５つ
    """
    def __init__(self, ysize, xsize, erate, view):
        """
        Persuitの初期化
        :param erate: 獲物が移動に失敗する率
        """
        self.erate = erate
        self.view = view
        self.dif = [[0,-1],[0,1],[-1,0],[1,0],[0,0]]
        self.ysize = ysize
        self.xsize = xsize
        self.ql = QLearning.QLearning([self.ysize,self.xsize,9], 5, 0.05, 0.8, 0.1, 10000, 50000, self.inif, self.act, self.checkg)
        self.ql.alabel({0:'左',1:'右',2:'上',3:'下',4:'-'})

    def inif(self):
        """地図上でのスタート地点を表す状態値を返す"""
        hunter = [3, 3]
        # 獲物の位置を決定
        while True:
            self.target = [randint(7),randint(7)]
            if self.target != hunter:
                break
        self.target_loc  = [self.target.copy()]
        # 獲物の見えている方向を決定
        dir = self.direction(hunter, self.target, self.view)
        return hunter + [dir] # 真ん中からスタート

    def act(self, s, a):
        """状態sでアクションaを行った場合の次の状態にsを書き換え、報酬を返す"""
        hunter = [s[0],s[1]]
        # 獲物の行動
        ta = randint(5)
        ng = [hunter] # ハンターの位置には移動できない。実際にはハンターの位置に移動できる場合、すでに捕まっている
        err = np.random.rand()
        if err > self.erate:
            self.target, _ = self.move(self.target, ta, ng)
        self.target_loc.append(self.target.copy())

        # ハンターの行動
        r = -1
        ng = [self.target] # 獲物の移動が優先。実際にはこの条件で移動できない場合は、結果的に捕捉することになる
        hunter, cond = self.move(hunter, a, ng)
        dir = self.direction(hunter, self.target, self.view)
        # 状態更新
        s[0] = hunter[0]
        s[1] = hunter[1]
        s[2] = dir
        if cond == 1:
            r = -10
        if self.checkg(s):
            r = 100

        return r

    def move(self, loc, a, ng):
        """
        位置locから行動aを取った場合の更新された位置と移動ステータスを返す。
        範囲外への移動や、位置ngへの移動を試みると元の位置にとどまる

        移動ステータス
            0: 正常移動
            1: 壁に衝突
            2: 競合で移動できず
        """
        cond = 0
        new_y = loc[0] + self.dif[a][0]
        new_x = loc[1] + self.dif[a][1]
        if new_y < 0:
            cond = 1 #壁に衝突
            new_y = 0
        elif new_y >= self.ysize:
            cond = 1  # 壁に衝突
            new_y = self.ysize - 1
        if new_x < 0:
            cond = 1  # 壁に衝突
            new_x = 0
        elif new_x >= self.xsize:
            cond = 1  # 壁に衝突
            new_x = self.xsize - 1
        new_loc = [new_y, new_x]
        if new_loc in ng:
            cond = 2 # 競合のため移動できず
            return loc.copy(), cond
        else:
            return new_loc, cond

    def direction(self, loc1, loc2, view):
        dy = loc1[0] - loc2[0]
        dx = loc1[1] - loc2[1]
        if 1 <= dx and dx <= view:
            if dy == 0:
                return 4
            elif 1 <= dy and dy <= view:
                return 3
            elif -view <= dy and dy <= -1:
                return 5
            else:
                return 8
        if dx == 0:
            if 1 <= dy and dy <= view:
                return 2
            elif -view <= dy and dy <= -1:
                return 6
            else:
                return 8
        if -view <= dx and dx <= -1:
            if dy == 0:
                return 0
            elif 1 <= dy and dy <= view:
                return 1
            elif -view <= dy and dy <= -1:
                return 7
            else:
                return 8
        return 8

    def checkg(self,state):
        """stateが終端状態がどうかを判定する"""
        #上下左右に獲物がいれば終了
        dy = abs(state[0] - self.target[0])
        dx = abs(state[1] - self.target[1])
        if (dx+dy) == 1 and dx*dy == 0:
            return True
        else:
            return False

def print_list(s,tloc,a):
    a += ['']
    for idx, val in enumerate(s):
        print(val, tloc[idx], a[idx])

if __name__ == '__main__':
    m = Persuit(7,7,0.3, 3)
    m.ql.learn()
    m.ql.plot_learning_curve()

    for i in range(5):
        ss, acs = m.ql.replay()
        print_list(ss, m.target_loc, acs)
        print('')

