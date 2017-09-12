from Agent import Agent
from Area import Area
import numpy as np
import random

class MovingAgent(Agent):
    def __init__(self, area, id, eps, nstate, naction, touch):
        super().__init__(eps, nstate, naction)
        self.area = area
        self.id = id
        self.touch = touch
        # 0:left 1:down 2:right 3:up
        self.mv = {0: [0, -1], 1: [1, 0], 2: [0, 1], 3: [-1, 0], 4: [0, 0]}
        self.initState()

    # Agentの共通メソッド
    def initState(self):
        super().initState()
        self.position = self.area.random_position()
        self.area.setId(self.position,self.id)
        self.updateState()

    def updateState(self):
        # 周囲にターゲットがいないか調べる
        dy, dx = self.area.search_target(self.position)
        # 自分の位置と、ターゲットとの位置関係の４次元で状態を定義
        self.state = self.position + [dy, dx]

    def act(self):
        # 状態sでの行動aを選択(ε-Greedy)
        # 行動の結果positionが変わる
        r = -1
        rnd = np.random.rand()
        if rnd < self.eps:
            # ランダムな行動選択
            self.action = random.randint(0, self.naction - 1)
        else:
            self.action = self.q.getMaxAction(tuple(self.state))
        objid = self._move(self.action)

        # ターゲットと隣接した場合報酬。これはタスク依存しすぎ
        dy, dx = self.area.search_target(self.position)
        if (abs(dx) == 1 and dy == 0) or (abs(dy) == 1 and dx == 0):
            r = self.touch
        self.r = r
        self.earned_reward += r

    # 公開メソッド
    def reset_position(self):
        self.position = self.area.random_position()

    # 内部メソッド
    def _move(self, dir):
        # 移動先の状態を返す(0:空白　1:壁 それ以外:オブジェクトID) ->必要か考える
        # self.positionを書き換える。
        # self.stateは変わらない
        ret = 0
        prev_position = self.position.copy()
        self.position[0] += self.mv[dir][0]
        self.position[1] += self.mv[dir][1]
        # 一歩進んで壁にぶつかったら戻る
        if self.position[0] < 0 or self.position[0] >= self.area.maxy or self.position[1] < 0 or self.position[1] >= self.area.maxx:
            self.position = prev_position
            ret = 1
        id = self.area.getId(self.position)
        # 他のエージェントやターゲットがいた場合移動しないで、すでにいるオブジェクトのIDを返す
        if id != 0 and id != self.id:
            ret = id
            self.position = prev_position
        # Areaを更新する
        self.area.setId(prev_position,0)
        self.area.setId(self.position, self.id)

        return ret

if __name__ == '__main__':
    a = Area(7,7,3)
    ma = MovingAgent(a, 1, 0.3, [7,7,3*2+1,3*2+1], 4)
    print(ma.state)
    ma.act()
    ma.updateState()
    print(ma.state)

