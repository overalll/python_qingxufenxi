import re
import jieba
from haversine import haversine
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']   #解决中文显示问题
plt.rcParams['axes.unicode_minus'] = False
from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import GeoType


def func1_1():
    '''
    数据清洗
    '''
    n = 0
    f1 = open('weibo.txt', encoding="utf-8")
    for data in f1.readlines():
        #去除url
        data = re.sub('''http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+''', '', data)
        data = re.sub('[我在]', '', data)  #去掉url前缀词
        data = re.sub(':', '', data)
        pattern = re.compile(r'<[^>]+>', re.S)  #去除html
        data = pattern.sub('', data)
        data = re.sub(r'\[\S+\]', '', data)  #去除表情
        data = re.sub(r'\s+', ' ', data)  #去除多余空格
        f2 = open('clean.txt', 'r', encoding="utf-8")
        data_i = f2.readlines()
        f22 = open('clean.txt', 'a', encoding="utf-8")
        if data not in data_i:  #避免重复数据被写入新文档
            f22.write(data+'\n')
            n += 1
        print(n)
    return


def func1_2(emotions):
    '''
    将情绪词放入jieba自定义词典
    '''
    #jieba自定义词典的创建
    for i in emotions:
        jieba.load_userdict(i)
    return


def func2(emotions, matrix_1, matrix_2, emotionslist):
    for i in range(len(emotions)):
        ff = open(emotions[i], 'r', encoding="utf-8")
        emotionslist.append([data.strip() for data in ff.readlines()])  #包含了所有情绪词的列表
        op = '气死'
    def funcinner():
        j = 0
        f4 = open('clean.txt', 'r', encoding="utf-8")
        data = f4.readlines()
        #分词并统计分出来的词属于哪一个类别的情绪词
        for i_1 in range(len(data)):
            m = data[i_1].split()
            mm = m[2]
            split_word = jieba.lcut(mm)
            n1, n2, n3, n4, n5 = 0, 0, 0, 0, 0
            for k0 in split_word:  #统计每句话中有多少不同类别的情绪词个数
                if k0 in emotionslist[0]:
                    matrix_1[i_1][0] += 1
                    n1 += 1
                elif k0 in emotionslist[1]:
                    matrix_1[i_1][1] += 1
                    n2 += 1
                elif k0 in emotionslist[2]:
                    matrix_1[i_1][2] += 1
                    n3 += 1
                elif k0 in emotionslist[3]:
                    matrix_1[i_1][3] += 1
                    n4 += 1
                elif k0 in emotionslist[4]:
                    matrix_1[i_1][4] += 1
                    n5 += 1
            #判断这一句话属于哪一种情绪
            if n1 > n2 and n1 and n3 and n1 > n4 and n1 > n5:
                matrix_2[i_1].append('anger')
            elif n2 > n1 and n2 > n3 and n2 > n4 and n2 > n5:
                matrix_2[i_1].append('disgust')
            elif n3 > n1 and n3 > n2 and n3 > n4 and n3 > n5:
                matrix_2[i_1].append('fear')
            elif n4 > n1 and n4 > n2 and n4 > n3 and n4 > n5:
                matrix_2[i_1].append('joy')
            elif n5 > n1 and n5 > n2 and n5 > n3 and n5 > n4:
                matrix_2[i_1].append('sadness')
            elif n1 == 0 and n2 == 0 and n3 == 0 and n4 == 0 and n5 == 0:
                matrix_2[i_1].append('none')  #无情绪
            else:
                matrix_2[i_1].append('mix')   #混合情绪
            n = n1 + n2 + n3 + n4 + n5
            for ll in range(5):
                if n == 0:
                    matrix_1[i_1][ll] = 0
                else:
                    matrix_1[i_1][ll] = matrix_1[i_1][ll] / n  #情绪比例
            j += 1
        return
    return funcinner


def func3(time, what, emotion, matrix_2):
    '''
    某情绪随时间变化的模式
    :param time: 选择时间，小时？周？月？
    :param what: 选择某种情绪，anger? disgust? fear? joy? sadness?
    :param matrix_2: 记录某条微博数据属于哪种情绪的list
    '''
    shijian = ['hour', 'week', 'month']
    hour = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
            '16', '17', '18', '19', '20', '21', '22', '23']
    hour_list = [0]*24
    week = ['Mon', 'Tus', 'Wed', 'Ths', 'Fri', 'Sat', 'Sun']
    week_list = [0]*7
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_list = [0]*12
    if time == 0:
        f52 = open('clean.txt', 'r', encoding="utf-8")
        data = f52.readlines()
        n = len(data)
        for i_1 in range(n):  #取出小时时间对比
            m = data[i_1].split()
            mm = m[-3][0] + m[-3][1]
            if mm in hour:
                j_1 = hour.index(mm)
                if emotion[what] == ''.join(matrix_2[i_1]):
                    hour_list[j_1] += 1
        print(emotion[what]+shijian[time])
        print(hour_list)
        x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
             16, 17, 18, 19, 20, 21, 22, 23]
        plt.plot(x, hour_list, color="red", marker="+")
        plt.scatter(x, hour_list)
        for a, b in zip(x, hour_list):
            plt.text(a, b, b, ha='center', va='bottom')
        plt.title(emotion[what] + shijian[time])
        plt.grid()
        plt.show()
    elif time == 1:   #取出周时间对比
        f52 = open('clean.txt', 'r', encoding="utf-8")
        data = f52.readlines()
        n = len(data)
        for i_2 in range(n):
            m = data[i_2].split()
            if len(m) > 6:
                if m[-6] in week:
                    j_2 = week.index(m[-6])
                    if emotion[what] == ''.join(matrix_2[i_2]):
                        week_list[j_2] += 1
        print(emotion[what]+shijian[time])
        print(week_list)
        x = [1, 2, 3, 4, 5, 6, 7]
        plt.plot(x, week_list, color="orange", marker="+")
        plt.scatter(x, week_list)
        for a, b in zip(x, week_list):
            plt.text(a, b, b, ha='center', va='bottom')
        plt.title(emotion[what]+shijian[time])
        plt.grid()
        plt.show()
    elif time == 2:    #取出月时间对比
        f53 = open('clean.txt', 'r', encoding="utf-8")
        data = f53.readlines()
        n = len(data)
        for i_3 in range(n):
            m = data[i_3].split()
            if m[-5] in month:
                j_3 = month.index(m[-5])
                if emotion[what] == ''.join(matrix_2[i_3]):
                    month_list[j_3] += 1
        print(emotion[what]+shijian[time])
        print(month_list)
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        plt.plot(x, month_list, color="blue", marker="+")
        plt.scatter(x, month_list)
        for a, b in zip(x, month_list):
            plt.text(a, b, b, ha='center', va='bottom')
        plt.title(emotion[what] + shijian[time])
        plt.grid()
        plt.show()
    return


def func4(emotion, matrix_2, ar, loj, low):
    count = [0]*len(emotion)
    f5 = open('clean.txt', 'r', encoding="utf-8")
    data = f5.readlines()
    n = len(data)
    central = (39.9075, 116.38806)   #北京城市中心点对应的经纬度
    for i_1 in range(n):
        m = data[i_1].split()
        ms = ''.join(m)
        mm = re.findall(r'\d+\.?\d*', ms)
        lo = (float(mm[0]), float(mm[1]))   #发微博地点的经纬度
        loj[i_1] += float(mm[1])
        low[i_1] += float(mm[0])
        dis = haversine(central, lo)   #求两地距离
        if dis <= ar:
            for i_2 in range(len(emotion)):
                if emotion[i_2] == ''.join(matrix_2[i_1]):
                    count[i_2] += 1
    print(count)
    plt.title('情绪分布')
    plt.pie(count, labels=['anger', 'disgust', 'fear', 'joy', 'sadness'])
    plt.pie(count, autopct='%1.1f%%')
    plt.show()
    emoji = {'anger': 3, 'disgust': 8, 'fear': 12, 'joy': 17, 'sadness': 24}
    g = Geo()
    g.add_schema(maptype='china')
    data_pair = []
    for i in range(len(matrix_2)):
        if matrix_2[i] in emotion:
            g.add_coordinate(matrix_2[i], loj[i], low[i])
            p = ''.join(matrix_2[i])
            data_pair.append((matrix_2[i], emoji[p]))
    colors = [{'max': 5, 'label': 'anger', 'color': '#00B2EE'},
              {'min': 6, 'max': 10, 'label': 'disgust', 'color': '3700A4'},
              {'min': 11, 'max': 15, 'label': 'fear', 'color': '71C671'},
              {'min': 16, 'max': 20, 'label': 'joy', 'color': '#CD4F39'},
              {'min': 21, 'label': 'sadness', 'color': '#FF0000'}]
    g.add('', data_pair, type_=GeoType.EFFECT_SCATTER, symbol_size=5)
    # 设置样式
    g.set_series_opts(label_opts=opts.LabelOpts(is_show=True))
    g.set_global_opts(visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=colors), title_opts=opts.TitleOpts(title="微博情绪分布"))
    return g


def main():
    func1_1()
    emotions = ['anger.txt', 'disgust.txt', 'fear.txt', 'joy.txt', 'sadness.txt']
    emotion = ['anger', 'disgust', 'fear', 'joy', 'sadness']
    func1_2(emotions)
    matrix_1 = [[0] * 5 for ii in range(5000000)]
    matrix_2 = [[] for ii in range(5000000)]
    emotionslist = []
    loj = [0]*400000
    low = [0]*400000
    result = func2(emotions, matrix_1, matrix_2, emotionslist)
    result()
    func3(1, 4, emotion, matrix_2)
    g = func4(emotion, matrix_2, 20, loj, low)
    g.render('outcome.html')
    return


main()

