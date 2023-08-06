# creat a grid of torque speed points 
# constant voltage 
#vary throttle setting between 50 and 100 
# creaete five lines in the middle 
# interpolate those lines to find the efficency and power at that point 
import evpy as ev
import numpy as np 
import matplotlib.pyplot as plt

#KDE 2304XF - 2350 motor
V0 = 8.4
kv = 2350.0
Rm = 0.091
IO = 0.7
kt = 60/(kv*2*np.pi) #[rpm/V]
d = np.linspace(0.5, 1, 100)

#V = np.linspace(0.5*V0, V0, 100)
N_max = kv*V0
N_range = np.linspace(0,N_max, num=100)
w_range = N_range*(np.pi/30.0)
#create torque values
T_all = np.zeros((len(d),100))
n_all = np.zeros((len(d), 100))
I_all = np.zeros((len(d),100))

#get values 
for i in range(0, len(d)):
    T,P_out,I_mot,P_mot,n_mot = ev.motor_pred(w_range, V0, d[i], kt, Rm, IO)
    T_all[i] = T*1e3
    n_all[i] = n_mot
    I_all[i] = I_mot
    

for i in range(0,len(d)):
    plt.scatter(N_range, T_all[i])
    plt.ylim(0,T_all[99][0])
    plt.show
    

    

N1= N_range[0]
N = 10000
tu = 90

#find closest x 
for i in range(0, len(N_range)):
    if abs(N_range[i]- N) < abs(N1-N):
        N1 = N_range[i]

#find poition of x 
for i in range(0, len(w_range)):
    if N_range[i] == N1:
        xnum = i

#find closest y at x 
t1 = T_all[0][xnum]
for i in range(0, len(d)):
    if abs(T_all[i][xnum] - tu) < abs((t1-tu)):
        t1 = T_all[i][xnum]
        
#find position of this y value 
for i in range(0, len(d)):
    if T_all[i][xnum] == t1:
        ynum = i
        
#efficency at point one 
n1 = n_all[ynum][xnum]
I1 = I_all[ynum][xnum]
        
#Delete that Line and find the next point 
T_all = np.delete(T_all, ynum, 0)
#find closest y2 at x 
t2 = T_all[0][xnum]
for i in range(0, len(d)-1):
    if abs(T_all[i][xnum] - tu) < abs((t2-tu)):
        t2 = T_all[i][xnum]
        
#find position of this y value 
for i in range(0, len(d)-1):
    if T_all[i][xnum] == t2:
        ynum2 = i

#efficency at point 2
n2 = n_all[ynum2][xnum]
I2 = I_all[ynum2][xnum]
#interpolate to find npnt

npnt = n1+(tu-t1)*((n2-n1)/(t2-t1))
Ipnt = I1+(tu-t1)*((I2-I1)/(t2-t1))
print(npnt)
print(Ipnt)





