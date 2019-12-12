#-*-coding: UTF-8-*-
import numpy as np
import os

##############---acceleration (g) to veloctiy (cm/s)---##############
def AccToVelocity (dt,acc):
		#将加速度(g)转换为速度(cm/s)
		#输入：dt--记录间隔(s)
		#     acc--加速度时程(g/s2)
		#输出:vel--速度时程(cm/s)
		vel=[0]
		num=len(acc)
		for i in range(num-1):
			velocity=(acc[i]+acc[i+1])*dt/float(2)*981+vel[-1]
			vel.append(velocity)
		return vel
#############---velocity (cm/s) to displacement (cm)---#############
def VelToDisplacement (dt,vel):
		#速度(cm/s)转换为位移(cm)
		#输入：dt--记录间隔(s)
		#     vel--速度时程(cm/s)
		#输出:disp--位移时程(cm)
		disp=[0]
		num=len(vel)
		for i in range(num-1):
			displacement=(vel[i]+vel[i+1])*dt/float(2)+disp[-1]
			disp.append(displacement)
		return disp
#############---displacement (cm) to velocity (cm/s)---#############
def DispToVelocity (dt,displacement):
		#将位移(cm)转换为速度(cm/s)
		#displacement-需要转换为速度的序列(cm)
		#dt-时间间隔(s)
		n=len(displacement)
		vel=[0]
		disp=displacement
		for i in range(n-1):
			vell=2*(disp[i+1]-disp[i])/float(dt)-vel[-1]
			vel.append(vell)
		return vel
#############---velocity (cm/s) to acceleration (g/s2)---#############		
def VelToAccele (dt,vel):
	#将速度(cm/s)转换为加速度(g)
	#vel-需要转换为加速度的序列(cm/s)
	#dt-时间间隔(s)
	n=len(vel)
	acc=[0]
	for i in range(n-1):
		accel=2*(vel[i+1]-vel[i])/(981*float(dt))-acc[-1]
		acc.append(accel)
	return acc





if __name__=='__main__':
	pass