
t=0
set=[]
y=0
x=0
def circule( a, b, x, r):
    if abs(x - a) < r:
        y = b + (r ** 2 - (x - a) ** 2) ** 0.5
    else:
        y = b
    return y

while t<4:
    t+=0.01
    x-=0.005
    set.append([x, 0])
t = round(t, 2)
while t<6 and t>=4:
    t=t+0.01
    y+=0.005
    set.append([x,y])

t = round(t, 2)
while t<6.5 and t>=6:
    x=x+0.003
    t=t+0.01

    set.append([x,y])


t = round(t, 2)
while t<7.5 and t>=6.5:
    x=x+0.0025
    t=t+0.01
    y=circule(-1.85,0.75,x,0.25)
    set.append([x,y])


t = round(t, 2)
while t>=7.5 and round(t, 2)<9.5:
    x=x-0.00125
    t+=0.01
    y=-circule(-1.85,0.75,x,0.25)+1.5
    set.append([x, y])
t = round(t, 2)
while t < 10 and t >= 9.5:
    x = x - 0.003
    t = t + 0.01

    set.append([x, y])
while t>=10 and round(t, 2)<11:
    x+=0.004
    y-=0.005
    t+=0.01
    set.append([x, y])
t = round(t, 2)


while t>=11 and round(t, 2)<12:
    x+=0.0036
    t+=0.01

    set.append([x, y])

t = round(t, 2)

while t>=12 and round(t, 2)<13:
    t = round(t, 2)
    x+=0.0021
    y = -circule(-1.25, 0.21, x, 0.21)+0.42
    t+=0.01
    set.append([x, y])


t = round(t, 2)

while t>= 13  and round(t, 2) < 15:
    x-=0.0021
    y = circule(-1.25, 0.21, x, 0.21)
    t += 0.01

    set.append([x, y])
t = round(t, 2)

while t>= 15  and round(t, 2) < 16:
    x += 0.0021
    y = -circule(-1.25, 0.21, x, 0.21) + 0.42
    t += 0.01
    set.append([x, y])
t = round(t, 2)

while t>= 16  and round(t, 2) < 17:


    x +=0.0025
    t += 0.01
    set.append([x, y])
t = round(t, 2)
while t>= 17  and round(t, 2) < 18:


    y +=0.01
    t += 0.01
    set.append([x, y])
t = round(t, 2)
while t>= 18  and round(t, 2) < 19:
    y -=0.005
    t += 0.01
    set.append([x, y])
t = round(t, 2)

while t>= 19  and round(t, 2) < 19.5:
    x+=0.003
    set.append([x, y])

    t+=0.01
t = round(t, 2)

while t>= 19.5  and round(t, 2) < 20.5:
    x += 0.0025
    y = circule(-0.85, 0.25, x, 0.25)
    t += 0.01
    set.append([x, y])
t = round(t, 2)

while t>=20.5 and round(t, 2)<21.5:
    t = round(t, 2)
    x-=0.0025
    y = -circule(-0.85, 0.25, x, 0.25)+0.5

    t+=0.01
    set.append([x, y])

while t>= 21.5  and round(t, 2) < 22:
    x-=0.003
    set.append([x, y])

    t+=0.01
t = round(t, 2)
while t>= 22  and round(t, 2) < 24:
    x+=0.00375
    set.append([x, y])

    t+=0.01
t = round(t, 2)
#圆圈
while t>=24 and round(t, 2)<25:
    t = round(t, 2)
    x+=0.0021
    y = -circule(-0.25, 0.21, x, 0.21)+0.42
    t+=0.01
    set.append([x, y])
t = round(t, 2)
while t>= 25  and round(t, 2) < 27:
    x -= 0.0021
    y = circule(-0.25, 0.21, x, 0.21)
    t += 0.01
    set.append([x, y])
t = round(t, 2)
while t>=27 and round(t, 2)<28:
    t = round(t, 2)
    x+=0.0021
    y = -circule(-0.25, 0.21, x, 0.21)+0.42
    t+=0.01
    set.append([x, y])
t = round(t, 2)
while t>= 28  and round(t, 2) < 28.5:
    x+=0.005
    set.append([x, y])

    t+=0.01
t = round(t, 2)
while t>= 28.5  and round(t, 2) < 30.1:
    y+=0.00625
    set.append([x, y])

    t+=0.01
while t>= 30.1  and round(t, 2) < 31.1:
    y-=0.005
    x+=0.0025
    set.append([x, y])

    t+=0.01
t = round(t, 2)
while t>= 31.1  and round(t, 2) < 32.1:
    y+=0.005
    x+=0.0025
    set.append([x, y])

    t+=0.01
t = round(t, 2)
while t>= 32.1  and round(t, 2) < 33.7:
    y-=0.00625
    set.append([x, y])
    t = round(t, 2)
    t+=0.01

t = round(t, 2)

while t>= 33.7  and round(t, 2) < 34.5:
    x+=0.003125
    set.append([x, y])

    t+=0.01
    t = round(t, 2)

t = round(t, 2)
while t>=34.5 and round(t, 2)<35.5:
    t = round(t, 2)
    x+=0.0020
    y = -circule(0.75, 0.21, x, 0.21)+0.42
    t+=0.01
    set.append([x, y])
t = round(t, 2)

while t>= 35.5  and round(t, 2) < 36.5:

    y +=0.0032
    t += 0.01
    set.append([x, y])
t = round(t, 2)

while t>= 36.5  and round(t, 2) < 38.5:
    x -= 0.0018
    y = circule( 0.76,0.46367, x, 0.19)
    t += 0.01
    set.append([x, y])
t = round(t, 2)

while t>= 38.5  and round(t, 2) < 40.5:
    x += 0.0018
    y = circule( 0.76,0.46367, x, 0.19)
    t += 0.01
    set.append([x, y])
t = round(t, 2)

while t>= 40.5  and round(t, 2) < 41:

    y -=0.0031
    t += 0.01
    set.append([x, y])
t = round(t, 2)

while t>= 41  and round(t, 2) < 41.5:

    x -=0.004
    t += 0.01
    set.append([x, y])
t = round(t, 2)

while t>= 41.5  and round(t, 2) < 42.5:
    x -= 0.0015
    y = circule( 0.74,0.15, x, 0.15)
    t += 0.01
    set.append([x, y])
t = round(t, 2)
while t>= 42.5  and round(t, 2) < 43.5:
    x += 0.0015
    y = -circule( 0.74,0.15, x, 0.15)+0.3
    t += 0.01
    set.append([x, y])
t = round(t, 2)


#s
while t>= 43.5  and round(t, 2) < 44.5:

    x +=0.005
    t += 0.01
    set.append([x, y])
t = round(t, 2)

while t>= 44.5  and round(t, 2) < 45.5:
    x += 0.0015
    y = -circule( 1.25,0.15, x, 0.15)+0.3
    t += 0.01
    set.append([x, y])
t = round(t, 2)
while t>= 45.5  and round(t, 2) < 46.5:
    x -= 0.0015
    y = circule( 1.25,0.15, x, 0.15)
    t += 0.01
    set.append([x, y])
t = round(t, 2)
while t>= 46.5  and round(t, 2) < 47:

    x -=0.002
    t += 0.01
    set.append([x, y])
t = round(t, 2)

while t>= 47  and round(t, 2) < 48:
    x -= 0.0015
    y = -circule( 1.15,0.45, x, 0.15)+0.9
    t += 0.01
    set.append([x, y])

t = round(t, 2)
while t >= 48 and round(t, 2) < 49:
    x += 0.0015
    y = circule(1.15, 0.45, x, 0.15)
    t += 0.01
    set.append([x, y])
t = round(t, 2)
#t
while t >= 49 and round(t, 2) < 51:
    x += 0.0045

    t += 0.01
    set.append([x, y])
t = round(t, 2)
while t >= 51 and round(t, 2) < 51.5:
    x -= 0.005

    t += 0.01
    set.append([x, y])
t = round(t, 2)
while t >= 51.5 and round(t, 2) < 52:
    y+= 0.003

    t += 0.01
    set.append([x, y])
t = round(t, 2)
while t >= 52 and round(t, 2) < 53.5:
    y-= 0.004

    t += 0.01
    set.append([x, y])
t = round(t, 2)

while t >= 53.5 and round(t, 2) < 54.5:
    x += 0.0015
    y = -circule(1.95, 0.15, x, 0.15)+0.3
    t += 0.01
    set.append([x, y])
t = round(t, 2)

#e
while t >= 54.5 and round(t, 2) < 55:
    x += 0.006

    t += 0.01
    set.append([x, y])
t = round(t, 2)

while t >= 55 and round(t, 2) < 56:
    x -=0.0025
    y = -circule(2.25, 0.25, x, 0.25)+0.5
    t += 0.01
    set.append([x, y])
t = round(t, 2)


while t >= 56 and round(t, 2) < 60:
    x +=0.00125
    y = circule(2.25, 0.25, x, 0.25)
    t += 0.01
    set.append([x, y])
t = round(t, 2)
while t >= 60 and round(t, 2) < 62:
    x -= 0.0025

    t += 0.01
    set.append([x, y])

t = round(t, 2)

while t >= 62 and round(t, 2) < 64:
    x +=0.0014
    y = -circule(2.25, 0.25, x, 0.25)+0.5
    t += 0.01
    set.append([x, y])
t = round(t, 2)
#r
while t >= 64 and round(t, 2) < 65:
    x +=0.0032

    t += 0.01
    set.append([x, y])
t = round(t, 2)
while t >= 65 and round(t, 2) < 66:
    y+=0.003

    t += 0.01
    set.append([x, y])
t = round(t, 2)


while t >= 66 and round(t, 2) < 68:
    x +=0.0025
    y =circule(2.85, 0.3, x, 0.25)

    t += 0.01
    set.append([x, y])
print(set)





