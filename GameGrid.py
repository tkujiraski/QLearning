from tkinter import *
import numpy as np

class GameGrid:
    def __init__(self, m):
        self.color ={0:'red', 1:'pink', 2: 'black'} # 4台以上だとエラー
        self.agents  = m.multi_q.agents
        self.num_of_agents = len(self.agents)
        self.target_loc = m.target_loc
        self.len_of_steps = len(self.target_loc)
        self.area = m.area
        self.root = Tk()
        self.canvas = Canvas(self.root, width = 30*self.area.maxx, height = 30*self.area.maxy)
        self.cell = np.zeros((self.area.maxy, self.area.maxx), np.uint16)
        self.next_button = Button(self.root, text = 'Next', command = self._next)
        for y in range(self.area.maxy):
            for x in range(self.area.maxx):
                self.cell[y, x] = self.canvas.create_rectangle(x * 30, y * 30, x * 30 + 29, y * 30 + 29, fill='green',
                                                 stipple='gray25')
        self.canvas.grid(row=0, column=0, sticky='ew')
        self.next_button.grid(row=1, column=0, sticky='ew')
        self.step = -1
        self._next()
        self.root.mainloop()
        return

    def _next(self):
        # 表示をリセット
        for y in range(self.area.maxy):
            for x in range(self.area.maxx):
                self.canvas.itemconfigure(self.cell[y, x], fill='green')
        # 次の配置を表示し、最後まで再生したら終了
        self.step += 1
        if self.step == self.len_of_steps:
            self.root.quit()
            self.root.destroy()
            return
        for idx, agent in enumerate(self.agents):
            self.canvas.itemconfigure(self.cell[agent.states[self.step][0], agent.states[self.step][1]], fill=self.color[idx])
        self.canvas.itemconfigure(self.cell[self.target_loc[self.step][0],self.target_loc[self.step][1]], fill='blue')
        return




