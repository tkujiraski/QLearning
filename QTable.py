import numpy as np

class QTable:
    """
    状態とアクションの組に対するQ値を保持するクラス

    """
    def __init__(self, nstate, naction):
        """ QTableの初期化
            nstate: 状態変数ごとの状態数の配列
            naction: アクションの数
        """
        self.nstate = nstate
        self.naction = naction
        self.qvalue  = np.zeros(nstate+[naction])

    def getQ(self, state, action):
        """
        状態state, 行動actionのQ値を返す
        :param state:
        :param action:
        :return:
        """
        return self.getQvector(state)[action]

    def getMaxQ(self, state):
        """
        状態stateで最大のQ値を返す
        :param state:
        :return: 最大のQ値
        """
        return self.getQvector(state).max()

    def getMaxAction(self, state):
        """
        状態stateで最大のQ値となる行動aを返す
        :param state:
        :return: 最大のQ値となる行動a
        """
        return self.getQvector(state).argmax()

    def getQvector(self,state):
        # 直接[0,1,1]のようなリストを引数として配列にアクセスする方法が分からないので関数化
        #  -> タプルを引数とすればOK
        # 下記はforを使っているので良くない
        """dim = len(state)
        el = self.qvalue
        for i in range(dim):
            el = el[state[i]]
        return el"""
        return self.qvalue[state]


    def update(self, r, old_state, new_state, action, gamma, alpha):
        ##print('updating')
        ##print(self.qvalue)
        ##print(old_state)
        ##print(new_state)
        ##print(old_state+[action])
        # 下の記述は「リストで指定したndarrayの特定の要素を書き換える」ことをしたいが、実際にはそうなっていない
        # どうすればよい？どのサンプルも特定の次元数の配列に特化している
        # N次元配列ではなくて、状態は1次元に展開するしかないか？
        #self.qvalue[old_state+[action]] += alpha * (r + gamma*self.getMaxQ(new_state)-self.getQ(old_state,action))

        # 下記はgetQvectorを使って特定の状態のQ値のベクターを取得し、該当するactionのQ値を書き換えている
        # Q値まで取ってきてしまうと、書き換えられない?
        qvec = self.getQvector(old_state)
        qvec[action] += alpha * (r + gamma*self.getMaxQ(new_state)-qvec[action])

        ##print('updated')
        ##print(self.qvalue)



