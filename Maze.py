import QLearning

class Maze:
    """
    ４方向に移動できる迷路の問題
    """
    def __init__(self,map,start,goal):
        self.map = map
        self.start = start
        self.goal = goal
        self.ql = QLearning.QLearning([len(map),len(map[0])], 4, 0.05, 0.8, 0.1, 100, 1000, self.inif, self.act, self.checkg)

    def inif(self):
        """地図上でのスタート地点を表す状態値を返す"""
        return self.start.copy()

    def act(self, s, a):
        """状態sでアクションaを行った場合の次の状態と報酬を返す"""
        # 状態は(y,x）になっている
        r = -1
        if a == 0:
            # Left
            ##print('Left')
            if s[1] > 0 and self.map[s[0]][s[1]-1]==0:
                s[1] -= 1
            else:
                r = -10 #衝突
        elif a==1:
            # Right
            ##print('Right')
            if s[1] < len(self.map[0])-1 and self.map[s[0]][s[1]+1]==0:
                s[1] += 1
            else:
                r = -10
        elif a==2:
            # Down
            ##print('Down')
            if s[0] > 0 and self.map[s[0]-1][s[1]]==0:
                s[0] -= 1
            else:
                r = -10
        else:
            # Up
            ##print('Up')
            if s[0] < len(self.map)-1 and self.map[s[0]+1][s[1]]==0:
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
        [0,0,0,1,0,0],
        [0,1,0,1,0,1],
        [0,1,0,0,0,0],
        [1,1,0,1,1,0]
    ]
    start = [0,0]
    goal = [3,5]
    m = Maze(map,start,goal)
    m.ql.learn()
    m.ql.plot_learning_curve()
    ss, acs = m.ql.replay()
    print(ss)
    print(acs)

