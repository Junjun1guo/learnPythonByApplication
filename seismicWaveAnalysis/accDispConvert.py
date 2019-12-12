#-*-coding: UTF-8-*-
import numpy as np
import os

##############---acceleration (g) to veloctiy (cm/s)---##############
def AccToVelocity (dt,acc):
		#�����ٶ�(g)ת��Ϊ�ٶ�(cm/s)
		#���룺dt--��¼���(s)
		#     acc--���ٶ�ʱ��(g/s2)
		#���:vel--�ٶ�ʱ��(cm/s)
		vel=[0]
		num=len(acc)
		for i in range(num-1):
			velocity=(acc[i]+acc[i+1])*dt/float(2)*981+vel[-1]
			vel.append(velocity)
		return vel
#############---velocity (cm/s) to displacement (cm)---#############
def VelToDisplacement (dt,vel):
		#�ٶ�(cm/s)ת��Ϊλ��(cm)
		#���룺dt--��¼���(s)
		#     vel--�ٶ�ʱ��(cm/s)
		#���:disp--λ��ʱ��(cm)
		disp=[0]
		num=len(vel)
		for i in range(num-1):
			displacement=(vel[i]+vel[i+1])*dt/float(2)+disp[-1]
			disp.append(displacement)
		return disp
#############---displacement (cm) to velocity (cm/s)---#############
def DispToVelocity (dt,displacement):
		#��λ��(cm)ת��Ϊ�ٶ�(cm/s)
		#displacement-��Ҫת��Ϊ�ٶȵ�����(cm)
		#dt-ʱ����(s)
		n=len(displacement)
		vel=[0]
		disp=displacement
		for i in range(n-1):
			vell=2*(disp[i+1]-disp[i])/float(dt)-vel[-1]
			vel.append(vell)
		return vel
#############---velocity (cm/s) to acceleration (g/s2)---#############		
def VelToAccele (dt,vel):
	#���ٶ�(cm/s)ת��Ϊ���ٶ�(g)
	#vel-��Ҫת��Ϊ���ٶȵ�����(cm/s)
	#dt-ʱ����(s)
	n=len(vel)
	acc=[0]
	for i in range(n-1):
		accel=2*(vel[i+1]-vel[i])/(981*float(dt))-acc[-1]
		acc.append(accel)
	return acc





if __name__=='__main__':
	pass