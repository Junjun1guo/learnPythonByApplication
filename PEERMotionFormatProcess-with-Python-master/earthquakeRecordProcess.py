#-*-coding: UTF-8-*-
##########################################################################
#  Author: Junjun Guo
#  E-mail: guojj@tongji.edu.cn/guojj_ce@163.com
#    Date: 11/01/2019
#  Environemet: Successfully excucted in python 2.7
# -------------------------------------
##########################################################################
import os
import numpy as np
import shutil
##########################################################################
def peerMotionProcess (fileName):
	"""
	Processing each file and return the processed resutls(percolumn data list, 
	timestep and pointers number)
	"""

	accList=[]
	fopen=open(fileName)
	saveList1=[]
	saveList2=[]
	lines=fopen.readlines()
	for line_counter,line in enumerate(lines):
		curLine=line.strip().split(" ")
		removeSpace=[x for x in curLine if x!=""]
		print curLine
		if line_counter<=3:
			[saveList1.append(x) for x in removeSpace]
		else:
			[saveList2.append(x) for x in removeSpace]	
	fopen.close()

	indexNumber=saveList1.index("NPTS=")
	indexDt=saveList1.index("DT=")
	pointNumber=saveList1[indexNumber+1].split(",")[0]
	deltaT=saveList1[indexDt+1].split(",")[0]
	saveList=[ float(x) for x in saveList2]
	return pointNumber,deltaT,saveList
##########################################################################
if __name__=='__main__':

	# Processing downloaded PEER ground motions to different tests with one 
	# column data
	# Preparing: 1. save downloaded motions to file-downLoadPeerMotion
	#           2. save the names of the files (.AT2) to FileName.txt
	#   Output: 1. Acceleration (g),velcocity(cm/s) and dispplacemnt(cm) of 
	#              each records in EW, NS
	#              and UD directions
	#           2. The point number of each record (MotonLength.txt)
	#           3. The time step for each record (deltaT.txt)
############################################################################
	direction=["E","N","V"]
	postFixList=[".AT2",".VT2",".DT2"]
	timeFileDict={".AT2":"Acceleration",".VT2":"Velocity",".DT2":"Displacement"}
	#Generating all saving file paths
	midirList=[(topFile,secFile) for topFile in timeFileDict.values() for secFile in direction]
	#Clearing existing files
	[shutil.rmtree(x) for x in timeFileDict.values()]
	for toplevel,seclevel in midirList:
			os.makedirs(toplevel+"/"+seclevel)
	
	fileListE=[]
	fileListN=[]
	fileListV=[]
	# text file read and process
	fileNameOpen=open("FileName.txt")
	for line in fileNameOpen.readlines():
		curLine=line.strip().split("\t")
		fileListE.append(curLine[0].split(".AT2")[0])
		fileListN.append(curLine[1].split(".AT2")[0])
		fileListV.append(curLine[2].split(".AT2")[0])
	fileNameOpen.close()	

	finalLengthList=[]
	finaltimeList=[]
	finalFileNameList=[]

	for i1 in range(len(fileListE)):

		fileNameENV=[{fileListE[i1]:direction[0]},{fileListN[i1]:direction[1]},{fileListV[i1]:direction[2]}]

		caseList=[(xx,yy) for xx in fileNameENV for yy in postFixList]

		lengthList=[]
		timeList=[]

		for eachCase in caseList:
			fileDirection=eachCase[0].values()[0]
			filePrefix=eachCase[0].keys()[0].strip()

			loadFilePath=os.path.join("downLoadPeerMotion/",filePrefix+eachCase[1])

			if filePrefix=="NoFile":
				accPointNum=1e8
				accDeltaT=1e8
				accTimeHistory=[0.0]
			else:
				accResult=peerMotionProcess (loadFilePath)
				accPointNum=int(accResult[0])
				accDeltaT=float(accResult[1])
				accTimeHistory=accResult[2]

			lengthList.append(accPointNum)
			timeList.append(accDeltaT)

			cwd=os.getcwd()
			savePathName=os.path.join(cwd,timeFileDict[eachCase[1]]+"/"+fileDirection+"/",filePrefix+".txt")
			np.savetxt(savePathName,accTimeHistory,fmt="%f")
		
		
		finalLengthList.append(min(lengthList))
		finaltimeList.append(min(timeList))

	np.savetxt("MotonLength.txt",finalLengthList,fmt="%d")
	np.savetxt("deltaT.txt",finaltimeList,fmt="%f")
		
