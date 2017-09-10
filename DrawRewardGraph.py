import csv
import matplotlib.pyplot as plt

class DrawRewardGraph:
    def __init__(self,filenames,step):
        c = ['blue','red','green','glay']
        num = len(filenames)
        data = []
        drawdata = []
        for filename in filenames:
            with open(filename,'r') as f:
                reader = csv.reader(f)
                next(reader)
                next(reader)
                data = next(reader)

            draw = []
            for i in range(len(data)//step):
                sum = 0
                for j in range(step):
                    sum += int(data[i*step+j])
                draw.append(sum/step)
            # 余りのデータはとりあえず無視(100の倍数分だけ表示)
            drawdata.append(draw)

        fig = plt.figure()

        ax = fig.add_subplot(1, 1, 1)
        for i in range(len(filenames)):
            ax.plot(range(len(drawdata[i])), drawdata[i], c=c[i])
        plt.show()

if __name__ == '__main__':
    drg = DrawRewardGraph(['log/JALPursuit.py20170910_201613.csv','log/MultiPursuit.py20170910_221639.csv','log/JALPursuit.py20170910_224612.csv'],100)
