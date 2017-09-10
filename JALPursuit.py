import QLearning
import numpy as np
from numpy.random import randint
from GameGrid import GameGrid
from datetime import datetime
import csv

class JALPursuit:
    """
    状態を共有した２つのエージェントがランダムに動く獲物を追跡する問題

    状態：現在の位置(y[0-6],x[0-6])、獲物の方向(上下左右、斜め各方向、視野外で９)
    アクション：上下左右への移動と停止の５つ
    """
    def __init__(self, ysize, xsize, erate, view, eps, gamma, alpha, maxEpisodes, maxSteps):
        """
        Persuitの初期化
        :param erate: 獲物が移動に失敗する率
        """
        self.erate = erate
        self.view = view
        self.dif = [[0,-1],[0,1],[-1,0],[1,0],[0,0]]
        self.ysize = ysize
        self.xsize = xsize
        self.ql = QLearning.QLearning([self.ysize,self.xsize,self.view*2+1,self.view*2+1,self.ysize, self.xsize, self.view*2+1, self.view*2+1], 25, eps, gamma, alpha, maxEpisodes, maxSteps, self.inif, self.act, self.checkg)
        self.ql.alabel({0:'左左',1:'左右',2:'左上',3:'左下',4:'左-',5:'右左',6:'右右',7:'右上',8:'右下',9:'右-',10:'上左',11:'上右',12:'上上',13:'上下',14:'上-',15:'下左',16:'下右',17:'下上',18:'下下',19:'下-',20:'-左',21:'-右',22:'-上',23:'-下',24:'--',})

    def inif(self):
        """地図上でのスタート地点を表す状態値を返す"""
        # ハンターの位置を決定
        hunter1 = [randint(self.ysize), randint(self.xsize)]
        while True:
            hunter2 = [randint(self.ysize),randint(self.xsize)]
            if hunter1 != hunter2:
                break
        # 獲物の位置を決定
        while True:
            self.target = [randint(self.ysize),randint(self.xsize)]
            if self.target != hunter1 and self.target != hunter2:
                break
        self.target_loc  = [self.target.copy()]
        # 獲物の見えている方向を決定
        dy1, dx1 = self.direction(hunter1, self.target, self.view)
        dy2, dx2 = self.direction(hunter2, self.target, self.view)
        return hunter1 + [dy1, dx1] + hunter2 + [dy2, dx2]

    def act(self, s, a):
        """状態sでアクションaを行った場合の次の状態にsを書き換え、報酬を返す"""
        hunter1 = [s[0],s[1]]
        hunter2 = [s[4],s[5]]
        # ハンターの行動
        a1 = a // 5
        a2 = a % 5
        # 獲物の行動
        ta = randint(5)
        ng = [hunter1, hunter2] # ハンターの位置には移動できない。実際にはハンターの位置に移動できる場合、すでに捕まっている
        err = np.random.rand()
        if err > self.erate:
            self.target, _ = self.move(self.target, ta, ng)
        self.target_loc.append(self.target.copy())

        # ハンター1の行動
        ng = [self.target, hunter2] # 獲物の移動が優先。実際にはこの条件で移動できない場合は、結果的に捕捉することになる
        hunter1, cond1 = self.move(hunter1, a1, ng)
        dy, dx = self.direction(hunter1, self.target, self.view)
        # 状態更新
        s[0] = hunter1[0]
        s[1] = hunter1[1]
        s[2] = dy
        s[3] = dx

        # ハンター2の行動
        ng = [self.target, hunter1] # 獲物の移動が優先。実際にはこの条件で移動できない場合は、結果的に捕捉することになる
        hunter2, cond2 = self.move(hunter2, a2, ng)
        dy, dx = self.direction(hunter2, self.target, self.view)
        # 状態更新
        s[4] = hunter2[0]
        s[5] = hunter2[1]
        s[6] = dy
        s[7] = dx

        # どちらかが隣接すれば3, 捕獲すれば1,それ以外は-1
        r = self.reward(hunter1,hunter2,self.target)

        return r

    def reward(self, h1, h2, t):
        # MultiPursuitと合わせる 通常-1, 両方隣接 10
        n1 = [t[0]-1,t[1]]
        n2 = [t[0]+1,t[1]]
        n3 = [t[0],t[1]-1]
        n4 = [t[0],t[1]+1]
        n = [n1,n2,n3,n4]
        sum = 0
        if h1 in n:
            sum += 1
        if h2 in n:
            sum += 1
        if sum == 2:
            return 10
        else:
            return -1

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
        if abs(dy) > self.view or abs(dx) > self.view:
            return 0,0
        else:
            return dy, dx


    def checkg(self,state):
        """stateが終端状態がどうかを判定する"""
        hunter1 = [state[0],state[1]]
        hunter2 = [state[4],state[5]]
        if self.reward(hunter1,hunter2,self.target) == 10:
            return True
        else:
            return False

def print_list(s,tloc,a):
    a += ['']
    for idx, val in enumerate(s):
        print(val, tloc[idx], a[idx])

def save_movement(n, ysize, xsize, s,tloc,a,filename):
    a += ['']
    with open(filename,'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        row = [n, ysize, xsize]
        writer.writerow(row)
        for idx, val in enumerate(s):
            row = [val[0],val[1],val[4],val[5],tloc[idx][0],tloc[idx][1]]
            writer.writerow(row)

if __name__ == '__main__':
    ysize = 7
    xsize = 7
    erate = 0.3
    view = 5
    eps = 0.05
    gamma = 0.8
    alpha = 0.1
    maxEpisodes = 100000
    maxSteps = 500
    m = JALPursuit(ysize,xsize,erate, view, eps, gamma, alpha, maxEpisodes, maxSteps)
    m.ql.learn()
    m.ql.save_learning_curve('log/'+__file__.split('/')[-1]+datetime.now().strftime("%Y%m%d_%H%M%S")+'.csv')
    m.ql.plot_learning_curve()

    for i in range(5):
        ss, acs = m.ql.replay()
        print_list(ss, m.target_loc, acs)
        save_movement(2, xsize, ysize, ss, m.target_loc, acs, 'log/move_'+__file__.split('/')[-1]+datetime.now().strftime("%Y%m%d_%H%M%S")+'_'+str(i)+'.csv')
        print('')