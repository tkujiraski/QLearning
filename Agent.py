import numpy as np
import QTable

class Agent:
    # JavaであればInterface。特に実装はしない。Agentが持つべきメソッドを規定
    # HunterもTargetも含むクラス
    def __init__(self, eps, nstate, naction):
        self.eps = eps
        self.nstate = nstate
        self.naction = naction
        self.action = -1
        self.state = []
        self.old_s = []
        self.r = 0
        self.earned_reward = 0
        self.q = QTable.QTable(nstate,naction)

    def initState(self):
        # 状態を初期化する
        self.earned_reward = 0

    def act(self):
        # 行動を実行して取った行動を返す
        return

    def updateState(self):
        # 状態を更新する
        return

    def updateQ(self,alpha,gamma):
        qvec = self.q.getQvector(tuple(self.old_s))
        qvec[self.action] += alpha * (self.r + gamma*self.q.getMaxQ(tuple(self.state))-qvec[self.action])

    def get_state(self):
        # 現在の状態を返す
        return self.state

if __name__ == '__main__':
    a = Agent(0.3, [7,7], 4)

