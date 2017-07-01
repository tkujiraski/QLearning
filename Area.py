import numpy as np

class Area:
    def __init__(self, maxy, maxx, view):
        # エージェントの能力ではなく、場所に視界があるという設定
        self.maxy = maxy
        self.maxx = maxx
        self.view = view
        self.state = self.__init_state()

    def __init_state(self):
        return np.zeros([self.maxy+2*self.view, self.maxx+2*self.view]).astype('uint8')

    def reset_state(self):
        self.state = self.__init_state()

    def getId(self,position):
        # state座標に変換
        by = position[0] + self.view
        bx = position[1] + self.view
        return self.state[by, bx]

    def setId(self,position, id):
        # 強制的にその場所にidのオブジェクトを置く。Area側では妥当性チェックはしない
        # state座標に変換
        by = position[0] + self.view
        bx = position[1] + self.view
        self.state[by, bx] = id

    def search_target(self, position):
        # state座標に変換
        by = position[0] + self.view
        bx = position[1] + self.view
        # positionの周辺にターゲットがあるか確認
        for y in range(by-self.view, by+self.view+1):
            for x in range(bx-self.view, bx+self.view+1):
                if self.state[y,x] == 128:
                    return y-by, x-bx
        return 0, 0 # 範囲内になしの場合何を返すのが良い？

    def random_position(self):
        # 他のオブジェクトがない場所をランダムに返す
        while True:
            y = np.random.randint(self.maxy)
            x = np.random.randint(self.maxx)
            if self.state[y+self.view, x+self.view] == 0:
                break
        return [y, x]

    def find_object(self,id):
        ret = []
        for y in range(self.view, self.view+self.maxy):
            for x in range(self.view, self.view+self.maxx):
                if self.state[y,x] == id:
                    ret.append([y,x])
        return ret

if __name__ == "__main__":
    a = Area(7,7,3)
    a.state[2+3,1+3] = 128
    dy, dx = a.search_target([3,3])
    print(dy,dx)