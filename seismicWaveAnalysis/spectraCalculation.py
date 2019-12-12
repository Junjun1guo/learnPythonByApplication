"""
python 2.7
"""
import numpy as np
#####################################################
def calResponseSpe (acc,dt,m,T,beta):
    """
    acc - acceleration
    dt - time interval
    m - mass take 1
    T = period(s)
    beta - damping ratio
    return :accSpect(g) velSpect(cm/s) dispSpect(cm)
    """
    accel = acc * 9.81
    t = dt
    k = ((2 * np.pi / float(T)) ** 2) * m
    w0 = 2 * np.pi / float(T)
    c = 2 * m * w0 * beta
    # newMark-beta parameters set
    r = 1.0 / 2.0
    b = 1.0 / 4.0
    accList = []
    velList = [0]
    dispList = [0]
    acc0 = (accel[0] - c * velList[0] - k * dispList[0]) / float(m)
    accList.append(acc0)
    a1 = m / float(b * t ** 2) + r * c / float(b * t)
    a2 = m / float(b * t) + (r / float(b) - 1) * c
    a3 = (1.0 / float(2 * b) - 1) * m + t * c * (r / float(2 * b) - 1.0)
    k1 = k + a1

    for i1 in range(len(accel) - 1):
        ptemp = -accel[i1 + 1] + a1 * dispList[-1] + a2 * velList[-1] + a3 * accList[-1]
        disptemp = ptemp / float(k1)
        dispList.append(disptemp)
        velTemp = r * (dispList[-1] - dispList[-2]) / float(b * t) + \
                  (1 - r / float(b)) * velList[-1] + t * accList[-1] * (1 - r / float(2 * b))
        velList.append(velTemp)
        accTemp = (dispList[-1] - dispList[-2]) / float(b * (t ** 2)) - \
                  velList[-2] / float(b * t) - accList[-1] * (1 / float(2 * b) - 1)
        accList.append(accTemp)
    maxDisp = max(np.abs(dispList)) * 100
    maxVel = max(np.abs(velList)) * 100
    absAcc = [value1 + value2 for value1, value2 in zip(accList, accel)]
    maxAcc = max(np.abs(absAcc)) / 9.81
    return T, maxAcc, maxVel, maxDisp


#################################################
if __name__=='__main__':
    acc=np.loadtxt("RSN6_IMPVALL.I_I-ELC180.txt")
    inputAcc=acc[:,1]
    dt=acc[1,0]-acc[0,0]
    calResponseSpe(inputAcc,dt,1,2,0.04)