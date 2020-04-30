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

#MAIN PROGRAM
n = 200  #Jumlah orang
p_infected = 5  #presentasi jumlah orang yang terinfeksi 
r_spread = 2  #radius transmisi virus
prob_spread = 4  #kemungkinan transmisi
prob = 80  #probabilitas individu bergerak
t_recovery = 10   #hari untuk sembuh


spread=0
arr_orang=[]

#membuat individu dan bergerak secara random walk positions. menginfeksi populasi
for i in range(n):
    p = Orang(i,np.random.random()*20, np.random.random()*20,np.random.random() * 20, np.random.random() * 20,t_recovery, False)

    if np.random.random()<p_infected/100:
        p.infect(0)
        spread=spread+1
    if np.random.random()>prob/100:
        p.permanent=True

    arr_orang.append(p)


#membuat grafik plot
fig = plt.figure(figsize=(18,9))
ax = fig.add_subplot(1,2,1)
cx = fig.add_subplot(1,2,2)

#gambar penyebaran 
ax.axis([0,20,0,20])
#gambar kurva
cx.axis([0,50,0,200])
scatt=ax.scatter([p.x_pos for p in arr_orang],[p.y_pos for p in arr_orang],c='blue',s=8)

#membuat box
kotak = plt.Rectangle((0,0),100,100,fill=False)
ax.add_patch(kotak)

#memberikan warna plot
gambar1,=cx.plot(spread,color="red",label="Terinfeksi")
gambar2,=cx.plot(spread,color="green",label="Sembuh")
cx.legend(handles=[gambar2,gambar1])

#label pada plot kurva
cx.set_xlabel("Hari")
cx.set_ylabel("Populasi")

#membuat array
st=[spread]
rt=[0]
t=[0]

#update posisi
def update(frame,rt,st,t):
    infek = 0
    reco = 0
    colour = []
    sizes = [8 for iter1 in arr_orang]
    for iter1 in arr_orang :
        #Cek jumlah orang yang terinfeksi
        iter1.checkSpread(frame)
        #animasi gerak orang
        iter1.updatePos(0,0)
        if iter1.removed:
            reco=reco+1 
            #menghitung yang sembuh
        if iter1.infected:
            infek=infek+1 
            #menghitung yang terifeksi
            #cek jika virus menyebar
            for iter2 in arr_orang:
                if iter2.index==iter1.index or iter2.infected or iter2.removed:
                    pass
                else:
                    d=iter1.getDistance(iter2.x_pos,iter2.y_pos)
                    if d<r_spread:
                        if np.random.random() < prob_spread / 100:
                            iter2.infect(frame)
                            sizes[iter2.index]=80
        colour.append(iter1.setColor())

    print("Day -",frame)
    print("Infected = ",infek)
    print("Recovery = ",reco)
    print()

    #update data 
    st.append(infek)
    rt.append(reco)
    t.append(frame)

    #memplot ke matplotlib
    offsets=np.array([[iter1.x_pos for iter1 in arr_orang],[iter1.y_pos for iter1 in arr_orang]])
    scatt.set_offsets(np.ndarray.transpose(offsets))
    scatt.set_color(colour)
    scatt.set_sizes(sizes)
    gambar1.set_data(t,st)
    gambar2.set_data(t,rt)
    return scatt,gambar1,gambar2

#Animasi
animation = FuncAnimation(fig, update, interval=50,fargs=(rt,st,t),blit=True)

plt.show()

i = 1
while st[i] != 0:  
    i += 1

print("Everyone cured in day -",t[i])