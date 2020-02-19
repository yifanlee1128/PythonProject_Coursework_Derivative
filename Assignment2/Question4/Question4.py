import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import interp1d

swaprate=[1.67, 1.47, 1.39, 1.35, 1.38, 1.45, 1.63]
timeline = [1, 2, 3, 5, 7, 10, 30]

swaprate = [p / 100. for p in swaprate]
timeline = [p * 12 for p in timeline]
function = interp1d(timeline, swaprate, kind='quadratic')

timeline_month = [t for t in range(12, 361)]
initial_R = function(timeline_month)


def get_newRn(alpha,Z):
    cumsumlist=alpha*Z.cumsum()
    newRn=[(1-z)/de for z,de in zip(Z,cumsumlist)]
    return np.array(newRn)


def get_newZn(alpha,Rn):
    new_Zn=[]
    for i in range(len(Rn)):
        if i==0:
            new_Zn.append(1/(1+alpha*Rn[i]))
        else:
            new_Zn.append((1-Rn[i]*alpha*sum(new_Zn))/(1+alpha*Rn[i]))
    return np.array(new_Zn)


def get_distance(newRn,Rn):
    return np.abs(newRn-Rn).sum()

distance=1
newRn=initial_R
while distance>1e-15:
    oldRn=newRn
    newZn = get_newZn(1 / 12, oldRn)
    newRn = get_newRn(1 / 12, newZn)
    distance=get_distance(newRn,oldRn)

plt.plot(timeline_month, newRn, '-')
plt.title("Question 4 smooth result")
plt.savefig("smooth_result.pdf")
plt.show()
