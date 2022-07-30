import csv
import numpy as np
from models import parameters
f = open('predicta2.0.csv','w',encoding='utf-8',newline='' "")
csv_writer = csv.writer(f)
with open('agro.csv') as csv_file:
    row = csv.reader(csv_file, delimiter=',')

    next(row)  # 读取首行
    x = []
    y=[]


    for r in row:
        agrox=float(r[11])
        agroy = float(r[12])
        Ax = (agrox  - 0.031574933) * 0.98941694+0.0305688385621904
        Ay = (agroy - 0.027907728) * 0.98990419+0.0274278939135515
        zhenagrox = float(r[14])
        zhenagroy = float(r[15])
        errx=Ax-zhenagrox
        erry=Ay-zhenagroy
        x.append(errx)
        y.append(erry)
        csv_writer.writerow([errx, erry])
print('errx平均值',np.mean(x))
print('errx标准差',np.std(x,ddof=1))
print('max',max(x),'','min',min(x))
print(np.var(x))
print('erry平均值',np.mean(y))
print('erry标准差',np.std(y,ddof=1))
print('max',max(y),'','min',min(y))
print(np.var(y))

