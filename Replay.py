from tkinter import *
import numpy as np
import csv

# 2エージェント専用
class Replay:
    def __init__(self, filename):
        size = 50
        self.color ={0:'red', 1:'pink', 2:'blue'}
        self.root = Tk()
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            self.n = int(header[0])
            self.ysize = int(header[1])
            self.xsize = int(header[2])
            self.data = []
            for row in reader:
                self.data.append(row)
        self.steps = len(self.data)
        self.canvas = Canvas(self.root, width = size * self.xsize, height = size * self.ysize)
        self.cell = np.zeros((self.ysize, self.xsize), np.uint16)
        self.next_button = Button(self.root, text = 'Next', command = self._next)
        for y in range(self.ysize):
            for x in range(self.xsize):
                self.cell[y, x] = self.canvas.create_rectangle(x * size, y * size, x * size + size - 1, y * size + size - 1, fill='green',
                                                 stipple='gray25')
        self.canvas.grid(row=0, column=0, sticky='ew')
        self.next_button.grid(row=1, column=0, sticky='ew')
        self.step = -1
        self._next()
        self.root.mainloop()
        return

    def _next(self):
        # 表示をリセット
        for y in range(self.ysize):
            for x in range(self.xsize):
                self.canvas.itemconfigure(self.cell[y, x], fill='green')
        # 次の配置を表示し、最後まで再生したら終了
        self.step += 1
        if self.step == self.steps:
            self.root.quit()
            self.root.destroy()
            return
        for i in range(self.n+1):
            self.canvas.itemconfigure(self.cell[int(self.data[self.step][i*2]), int(self.data[self.step][i*2+1])], fill = self.color[i])

        return

if __name__ == '__main__':
    fname = 'log/move_JALPursuit.py20170910_234359'
    for i in range(5):
        filename = fname + '_'+str(i)+'.csv'
        r = Replay(filename)