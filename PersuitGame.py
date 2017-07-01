import Area

class PersuitGame:
    """AreaにHunterとTargetを登録し、各HunterとTargetを動かして、HunterのQ Tableを更新する"""
    def __init__(self, area):
        self.area = area
        self.hunters = []

    def __register_hunter(self, hunter):
        self.hunters.append(hunter)

    def __register_target(self, target):
        self.target = target

if __name__ == '__main__':
    a = Area(7,7)
    pg = PersuitGame(a)
