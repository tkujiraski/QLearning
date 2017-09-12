import csv
import matplotlib.pyplot as plt

class DrawRewardGraph:
    def __init__(self,filenames,step,max):
        c = ['blue','red','green','black','grey','pink','purple','orange']
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
            for i in range(max//step):
                sum = 0
                for j in range(step):
                    sum += float(data[i*step+j])
                draw.append(sum/step)
            # 余りのデータはとりあえず無視(100の倍数分だけ表示)
            drawdata.append(draw)

        fig = plt.figure()

        ax = fig.add_subplot(1, 1, 1)
        for i in range(len(filenames)):
            ax.plot(range(len(drawdata[i])), drawdata[i], c=c[i])
        plt.show()

if __name__ == '__main__':
    #drg = DrawRewardGraph(['log/JALPursuit.py20170910_201613.csv','log/MultiPursuit.py20170910_221639.csv','log/JALPursuit.py20170910_224612.csv'],100,100000) #JAL_Multi_7_7_100000
    #drg = DrawRewardGraph(['log/MultiPursuit.py20170911_081104.csv','log/MultiPursuit.py20170911_225000.csv','log/JALPursuit.py20170911_231641.csv','log/JALPursuit.py20170911_232134.csv'],100,7500) #JAL_Multi_3vs05_7_7_7500
    #drg = DrawRewardGraph(['log/MultiPursuit.py20170910_221639.csv','log/JALPursuit.py20170910_201613.csv','log/MultiPursuit.py20170911_081104.csv', 'log/MultiPursuit.py20170911_225000.csv','log/JALPursuit.py20170911_231641.csv', 'log/JALPursuit.py20170911_232134.csv'], 100, 20000)  # JAL_Multi_0vs05vs3_7_7_20000
    #drg = DrawRewardGraph(['log/JALPursuit.py20170912_073825.csv', 'log/MultiPursuit.py20170912_075202.csv'], 100, 20000)  #JAL_Multi_05_8_8_20000
    #drg = DrawRewardGraph(['log/MultiPursuit.py20170910_221639.csv','log/JALPursuit.py20170910_201613.csv',
    #                       'log/MultiPursuit.py20170912_101236.csv','log/JALPursuit.py20170912_085956.csv',
    #                       'log/MultiPursuit.py20170911_225000.csv', 'log/JALPursuit.py20170911_232134.csv',
    #                       'log/MultiPursuit.py20170911_081104.csv', 'log/JALPursuit.py20170911_231641.csv'], 100,
    #                      100000)  #JAL_Multi_-1vs-05vs05vs3_7_7_20000
    drg = DrawRewardGraph(['log/MultiPursuit.py20170912_121242.csv','log/JALPursuit.py20170912_121625.csv'],100,200000)