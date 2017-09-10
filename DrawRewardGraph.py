import csv
import matplotlib.pyplot as plt

class DrawRewardGraph:
    def __init__(self,filename,step):
        with open(filename,'r') as f:
            reader = csv.reader(f)
            next(reader)
            next(reader)
            data = next(reader)

        drawdata = []
        for i in range(len(data)//step):
            sum = 0
            for j in range(step):
                sum += int(data[i*step+j])
            drawdata.append(sum/step)
        # 余りのデータはとりあえず無視(100の倍数分だけ表示)

        fig = plt.figure()

        ax = fig.add_subplot(1, 1, 1)
        ax.plot(range(len(drawdata)), drawdata, c='blue')
        plt.show()

if __name__ == '__main__':
    #drg = DrawRewardGraph('log/JALPursuit.py20170910_201613.csv',100)
    drg = DrawRewardGraph('log/JALPursuit.py20170910_201613.csv', 100)