import csv
import numpy as np
from models import parameters
import math

last_enc = [0 for _ in range(4)]

encoder1=0
encoder2=0
encoder3=0
encoder4=0
err1=[]
err2=[]
t=0.01
f = open('yaw.csv','w',encoding='utf-8',newline='' "")
csv_writer = csv.writer(f)

with open('new.csv') as csv_file:
    row = csv.reader(csv_file, delimiter=',')

    next(row)  # 读取首行
    encoder = []  # 建立一个数组来存encoder
    w = [0, 0, 0, 0]
    last_enc = [0 for _ in range(4)]
    for r in row:
        encoder.append(float(r[4]))
        encoder.append(float(r[5]))
        encoder.append(float(r[6]))
        encoder.append(float(r[7]))
        yaw1=(float(r[10]))
        yaw1 = (yaw1 + 0.300480158903466) * 0.98641682
        yaw_true=float(r[3])
        for i in range(4):
            if (encoder[i] - last_enc[i] > 3.14):
                w[i] = encoder[i] - 2 * 3.1415926 - last_enc[i]
            elif (encoder[i] - last_enc[i] < -3.14):
                w[i] = encoder[i] + 2 * 3.1415926 - last_enc[i]
            else:

                w[i] = encoder[i] - last_enc[i]
        w[0] = 0.98284149 * (w[0] - 0.004916151)
        w[1] = 0.98708168 * (w[1] + 0.00114977)
        w[2] = 0.98601081 * (w[2] - 0.000181461)
        w[3] = 0.98734884 * (w[3] - 0.004097596)

        last_enc = encoder
        encoder = []

        yaw2= (-w[0] + w[1] - w[2] + w[3]) / (parameters.CAR_A + parameters.CAR_B) * parameters.WHEEL_RADIUS / 4*100


        err1.append(yaw1-yaw_true)
        err2.append(yaw2-yaw_true)


        csv_writer.writerow([yaw_true,yaw1,yaw2,err1])
print('err1平均值',np.mean(err1))
print('err1标准差',np.std(err1,ddof=1))
print(np.var(err1))
print('err2平均值',np.mean(err2))
print('err2标准差',np.std(err2,ddof=1))
print(np.var(err2))
