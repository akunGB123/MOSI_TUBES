import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Orang:
    def __init__(org,i, x_pos, y_pos, x_obj, y_obj, t_spread, permanent):
        #objek x dan y ditempatkan ke tempatnya
        org.x_obj=x_obj
        org.y_obj=y_obj
        #Penamaan orang
        org.index=i
        org.numbr="Person "+str(i)
        #status dari orang yaitu:
        org.infected = False #terinfeksi
        org.suspected = True #yang belum/tidak terinfeksi
        org.removed = False #sembuh
        #posisi dari orang
        org.x_pos = x_pos
        org.y_pos=y_pos
        #cek status karantina
        org.permanent = permanent

        #perpindahan orang 
        if org.permanent:
            org.deltax = 0
            org.deltay = 0
        else:
            org.deltax = org.x_obj - org.x_pos
            org.deltay = org.y_obj - org.y_pos
        #waktu orang terinfeksi
        org.i_spread=-1
        #waktu orang sembuh
        org.t_spread = t_spread

    def __str__(org):
        return org.numbr+" in position "+str(org.x_pos)+", "+str(org.y_pos)

    def infect(org,i):
        #orang saat terinfeksi
        org.infected=True
        org.suspected=False
        org.removed = False
        org.i_spread=i

    def remove(org):
        #orang saat sembuh
        org.removed=True
        org.suspected=False
        org.infected=False

    def setObjective(org,x_obj,y_obj):
        #tempatkan orang di posisi masing masing
        org.x_obj=x_obj
        org.y_obj=y_obj
        if org.permanent:
            org.deltax = 0
            org.deltay=0
        else:
            org.deltax = org.x_obj - org.x_pos
            org.deltay = org.y_obj - org.y_pos

    def checkSpread(org,i):
        #orang sembuh sesuai waktu yang ditentukan
        if org.i_spread>-1:
            if i-org.i_spread>org.t_spread:
                org.remove()

    def setColor(org):
        #mewarnai dot
        if org.infected:
            return 'red'
        if org.suspected:
            return 'blue'
        if org.removed:
            return 'green'

    def updatePos(org, n_x_pos, n_y_pos):
        #animasi fungsi
        if(n_x_pos==0 and n_y_pos==0):
            org.x_pos=org.x_pos+org.deltax
            org.y_pos=org.y_pos+org.deltay
        else:
            org.x_pos=n_x_pos
            org.y_pos=n_y_pos
        #PBC
        if abs(org.x_pos-org.x_obj) < 3 and abs(org.y_pos-org.y_obj) <3:
            org.setObjective(np.random.random()*20, np.random.random()*20)
        if org.x_pos>20:
            org.x_pos=20
        if org.y_pos>20:
            org.y_pos=20
        if org.x_pos<0:
            org.x_pos=0
        if org.y_pos<0:
            org.y_pos=0

    def getDistance(org,x,y):
        #menghitung jarak antar individu.
        return math.sqrt((org.x_pos-x)**2+(org.y_pos-y)**2)


