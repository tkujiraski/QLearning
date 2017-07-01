from MultiQLearning import MultiQLearning
from MovingAgent import *
from Area import *
import numpy as np
from GameGrid import *

class MultiPursuit:
    def __init__(self, num_of_agents, eps, ysize, xsize, view, erate):
        self.eps = eps
        # 0:left 1:down 2:right 3:up
        self.mv = {0: [0, -1], 1: [1, 0], 2: [0, 1], 3: [-1, 0]}
        self.multi_q = MultiQLearning(0.1, 0.8, 10000, 500, self.env_init, self.env_update, self.extra_reward, self.check_goal)
        # この問題特有
        self.ysize = ysize
        self.xsize = xsize
        self.view = view
        self.erate = erate
        self.num_of_agents = num_of_agents
        self.area = Area(ysize,xsize,view)
        for i in range(num_of_agents):
            self.multi_q.regAgent(MovingAgent(self.area,i+1,self.eps,[ysize, xsize, view*2+1,view*2+1],len(self.mv)))
        # 記録用
        self.target_loc = []
        self.multi_q.alabel({0:'左',1:'下',2:'右',3:'上',4:'-'})

    def env_init(self):
        # 環境の初期化。Areaの初期化とターゲットの配置
        self.area.reset_state()
        self.target = self.area.random_position()
        self.area.setId(self.target,128)
        self.target_loc = []

    def env_update(self, agents):
        # ターゲットの位置を記録
        self.target_loc.append(self.target.copy())
        # ターゲットの移動
        ta = np.random.randint(4)
        err = np.random.rand()
        if err > self.erate:
            self._move(ta)


    def extra_reward(self):
        # 複数のエージェントがターゲットを取り囲んだ場合追加報酬
        if self._is_target_caputured():
            r = 10
        else:
            r = 0
        return r

    def check_goal(self):
        # 複数のエージェントがターゲットを取り囲んだ場合終了
        if self._is_target_caputured():
            return True
        else:
            return False

    def _move(self, dir):
        # ターゲットを移動させる
        # self.targetを書き換える。
        prev_position = self.target.copy()
        self.target[0] += self.mv[dir][0]
        self.target[1] += self.mv[dir][1]
        # 一歩進んで壁にぶつかったら戻る
        if self.target[0] < 0 or self.target[0] >= self.area.maxy or self.target[1] < 0 or self.target[1] >= self.area.maxx:
            self.target = prev_position
        id = self.area.getId(self.target)
        # 他のエージェントやターゲットがいた場合移動しない
        if id != 0 and id != 128:
            self.target = prev_position
        # Areaを更新する
        self.area.setId(prev_position, 0)
        self.area.setId(self.target, 128)

    def _is_target_caputured(self):
        sum = self.area.getId([self.target[0]-1,self.target[1]])+self.area.getId([self.target[0]+1,self.target[1]])+self.area.getId([self.target[0],self.target[1]-1])+self.area.getId([self.target[0],self.target[1]+1])
        id_sum = (self.num_of_agents+1)*self.num_of_agents//2
        if sum == id_sum:
            return True
        else:
            return False

def print_list(s,s2,tloc,a1,a2):
    for idx, val in enumerate(s):
        print(val, s2[idx], tloc[idx], a1[idx], a2[idx])

if __name__ == '__main__':
    m = MultiPursuit(2, 0.05, 10, 10, 5, 0.3)
    m.multi_q.learn()
    m.multi_q.plot_learning_curve()

    for i in range(5):
        m.multi_q.replay()
        print_list(m.multi_q.agents[0].states, m.multi_q.agents[1].states, m.target_loc, m.multi_q.agents[0].actions, m.multi_q.agents[1].actions)
        print('')

        g = GameGrid(m)



