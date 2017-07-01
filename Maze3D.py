import QLearning

class Maze3D:
    """
    ４方向と上下に移動できる迷路の問題
    """
    def __init__(self,map,start,goal):
        self.map = map
        self.start = start
        self.goal = goal
        self.ql = QLearning.QLearning([len(map),len(map[0]),len(map[0][0])], 6, 0.05, 0.8, 0.1, 100, 1000, self.inif, self.act, self.checkg)
        self.ql.alabel({0:'L',1:'R',2:'U',3:'D',4:'上',5:'下'})

    def inif(self):
        """地図上でのスタート地点を表す状態値を返す"""
        return self.start.copy()

    def act(self, s, a):
        """状態sでアクションaを行った場合の次の状態と報酬を返す"""
        # 状態は(z,y,x）になっている
        r = -1
        if a == 0:
            # Left
            ##print('Left')
            if s[2] > 0 and self.map[s[0]][s[1]][s[2]-1]==0:
                s[2] -= 1
            else:
                r = -10 #衝突
        elif a==1:
            # Right
            ##print('Right')
            if s[2] < len(self.map[0][0])-1 and self.map[s[0]][s[1]][s[2]+1]==0:
                s[2] += 1
            else:
                r = -10
        elif a==2:
            # Up
            ##print('Down')
            if s[1] > 0 and self.map[s[0]][s[1]-1][s[2]]==0:
                s[1] -= 1
            else:
                r = -10
        elif a==3:
            # Down
            ##print('Up')
            if s[1] < len(self.map[0])-1 and self.map[s[0]][s[1]+1][s[2]]==0:
                s[1] += 1
            else:
                r = -10
        elif a==4:
            # 下
            if s[0] > 0 and self.map[s[0]-1][s[1]][s[2]]==0:
                s[0] -= 1
            else:
                r = -10
        else:
            # 上
            if s[0] < len(self.map)-1 and self.map[s[0]+1][s[1]][s[2]]==0:
                s[0] += 1
            else:
                r = -10
        if self.checkg(s):
            r = 100

        return r


    def checkg(self,state):
        """stateが終端状態がどうかを判定する"""
        if state == self.goal:
            return True
        else:
            return False

if __name__ == '__main__':
    map = [
        [[0,0,0,1,0,0],
        [0,1,0,1,1,1],
        [0,1,0,1,0,0],
        [1,1,0,1,1,0]],

        [[0,1,1,1,1,1],
         [0,1,0,0,0,1],
         [1,0,1,1,0,1],
         [0,1,1,1,1,1]]
    ]
    start = [0,0,0]
    goal = [0,3,5]
    m = Maze3D(map,start,goal)
    m.ql.learn()
    m.ql.plot_learning_curve()
    ss, acs = m.ql.replay()
    print(ss)
    print(acs)