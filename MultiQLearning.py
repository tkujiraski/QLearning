import matplotlib.pyplot as plt
import csv

class MultiQLearning():
    # タスクに依存しない処理を記述する
    def __init__(self, alpha, gamma, maxEpisode, maxSteps, env_init, env_update, extra_reward, check_goal):
        self.agents = []
        self.env_init = env_init
        self.env_update = env_update
        self.alpha = alpha
        self.gamma = gamma
        self.maxEpisode = maxEpisode
        self.maxSteps = maxSteps
        self.extra_reward = extra_reward
        self.check_goal = check_goal
        self.stepsForGoal = []
        self.earnedReward = []
        self.adic = []

    def alabel(self,adic):
        self.adic = adic

    def regAgent(self, agent):
        self.agents.append(agent)

    def learn(self):
        for ep in range(self.maxEpisode):
            print('#episode %d' % ep)
            # 状態sを初期化
            self.env_init()
            for agent in self.agents:
                agent.initState()
                agent.earnedReward = 0

            # 各ステップでの行動選択・行動・Qテーブル更新
            for step in range(self.maxSteps):
                # 環境側の更新
                self.env_update(self.agents) # 渡した情報を環境側で使うかどうかは設定次第

                # 各エージェントごとの行動 self.old_s/state/positionが変わる
                for agent in self.agents:
                    # 行動し、r,s'を観測
                    agent.old_s = agent.state.copy()
                    agent.act() # 単独隣接でも報酬を得られることにする

                # 各エージェントの状態の更新
                for agent in self.agents:
                    agent.updateState()

                # 追加報酬の決定
                r = self.extra_reward()
                for agent in self.agents:
                    agent.r += r
                    agent.earned_reward += r

                # 各エージェントのQTable更新
                for agent in self.agents:
                    agent.updateQ(self.alpha, self.gamma)

                # sが終端状態ならばエピソードを終了
                if self.check_goal():
                    print('終了状態へ到達 %d step' % step)
                    self.stepsForGoal.append(step)
                    reward = 0
                    for agent in self.agents:
                        reward += agent.earned_reward
                    self.earnedReward.append(reward)
                    break
                if step == self.maxSteps - 1:
                    self.stepsForGoal.append(step)
                    reward = 0
                    for agent in self.agents:
                        reward += agent.earned_reward
                    self.earnedReward.append(reward)
                    break

    def save_learning_curve(self,filename):
        with open(filename, 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            header = []
            for agent in self.agents:
                header += agent.nstate
                header += [agent.naction, agent.eps]
            writer.writerow(header+[self.gamma, self.alpha, self.maxEpisode, self.maxSteps])
            writer.writerow(self.stepsForGoal)
            writer.writerow(self.earnedReward)

    def plot_learning_curve(self):
        fig = plt.figure()

        ax = fig.add_subplot(1, 1, 1)
        ax.plot(range(self.maxEpisode), self.stepsForGoal, c='red')
        ax.plot(range(self.maxEpisode), self.earnedReward, c='blue')
        plt.show()

    def replay(self):
        """最大のQ値選択のみでGoalまでのアクション系列を返す"""

        # 状態sを初期化
        self.env_init()
        for agent in self.agents:
            agent.initState()
            agent.earnedReward = 0
            agent.eps = 0.0 # 最大Q値のみを選択
            agent.states = []
            agent.actions = []

        # 各ステップでの行動選択・行動・Qテーブル更新
        for step in range(self.maxSteps):
            # 環境側の更新
            self.env_update(self.agents)  # 渡した情報を環境側で使うかどうかは設定次第

            # 各エージェントごとの行動 self.old_s/state/positionが変わる
            for agent in self.agents:
                # 行動し、r,s'を観測
                agent.old_s = agent.state.copy()
                agent.states.append(agent.old_s)
                agent.act()  # 単独隣接でも報酬を得られることにする
                if self.adic:
                    agent.actions.append(self.adic[agent.action])
                else:
                    agent.actions.append(agent.action)

            # 各エージェントの状態の更新
            for agent in self.agents:
                agent.updateState()
                #agent.states.append(agent.state.copy())

            # sが終端状態ならばエピソードを終了
            if self.check_goal():
                for agent in self.agents:
                    agent.states.append(agent.state.copy())
                    agent.actions.append("-")
                self.env_update(self.agents) # 最後の位置を記録するためだけ
                break



