import numpy as np
import csv, sys, os, re


def trace(package):
	acti=[]
	method=[]
	time =[]
	acti2=[]
	meth2=[]
	time2=[]
	time3 =[]
	inc=0
	pack = package
	with open("Result/meth.html" ,'r') as f:
		for line  in f:
			if pack in line and "$" not in line and "&" not in line and inc==0:
				n=0
				for word in line.split():
					if n==0:
						last=word
					if n==0 and not "[" in word and not "%" in word:	
						time.append(word)
						
					if n==5 and not "[" in last and not "%" in last:
						
						ww=word.split(".")
						acti.append(ww[len(ww)-2])
						method.append(ww[len(ww)-1])
					if "[" in last or "%" in last:
						inc=1;
					n=n+1
			elif pack in line and "$" not in line and "&" not in line:
				n=0
				for word in line.split():
					if n==0:
						last=word
					if "[" in last and n==3:
						time2.append(word)
					if n==4 and "[" in last:
						ww=word.split(".")
						acti2.append(ww[len(ww)-2])
						meth2.append(ww[len(ww)-1])
					n=n+1

	for i in range(len(time)):				
		for j in range(len(time2)):
			if acti[i] == acti2[j] and method[i] == meth2[j]:
				time3.append(time2[j])
			
		
	with open('Result/Method.csv', 'wb') as csvfile:
		fieldnames = ['method', 'Activity', 'Excl', 'Incl']	
		wr = csv.DictWriter(csvfile,  fieldnames=fieldnames)
	    	wr.writeheader()
		for i in range(len(time)):
			wr.writerow({"method" : method[i], "Activity" : acti[i] ,"Excl" : float(time[i])/1000000,"Incl" : float(time3[i])/1000000 })
	print "Method Tracing Done with method.csv"


def line(package,com):
	acti = []
	methodd = []
	aa =[]
	pack = package
	i=0
	my_file = "Result/sapl.trace"
	if os.path.isfile(my_file):
		os.system("dmtracedump -ho Result/sapl.trace > Result/meth.txt")
		#print "done"
	else:
		print "Error:  Sapl.trace does not exist"	
	
	with open("Result/meth.txt" ,'r') as f:
		for line  in f:
			if pack in line and "ent" in line and  "$" not in line and "<init" not in line:			
				n=0
				for word in line.split():
					if com in word and word not in aa:		
						aa.append(word)
						ww=word.split(".")
						acti.append(ww[len(ww)-2])
						methodd.append(ww[len(ww)-1])
					n+=1
				i+=1
	method =np.genfromtxt('Result/Method.csv', delimiter=',', dtype=None , names=('method','Activity','Excl','Incl'))
	method = np.delete(method, (0), axis=0)
	method2 = [[0 for i in xrange(len(method[i]))] for i in xrange(len(method))]

	for i in range(len(method)):
		method2[i][0]= methodd[i]
		method2[i][1]= acti[i]
		for j in range(len(method)):
			if method[j][0]== methodd[i] and method[j][1]== acti[i]:
				method2[i][2]= method[j][2]
				method2[i][3]= method[j][3]
				break

	with open('Result/Method.csv', 'wb') as csvfile:
			fieldnames = ['method', 'Activity', 'Excl', 'Incl']	
			wr = csv.DictWriter(csvfile,  fieldnames=fieldnames)
		    	wr.writeheader()
			for i in range(len(method2)):
				wr.writerow({"method" : method2[i][0], "Activity" : method2[i][1] ,"Excl" : method2[i][2],"Incl" :method2[i][3] })
	print "line up Complete"




def time(package):
	time =[]
	meth=[]
	pack = 	package
	pack2 = "am_create_activity"
	with open("Result/bugg.txt" ,'r') as f:
		for line  in f:
			if pack in line and pack2 in line:
				j=0
				for word in line.split():
					if j==6:
						#print line
						items = re.findall("/.([\w./]+),",word)
						for item in items:
	    						val= item
						meth.append(val)					
					
					if j == 1:
						time.append(word)
					j+=1
	ll =[]	
	j=len(time)-1	
	for i in range(len(time)-1):
		tim, sec = time[j].split('.')
		h, m, s = tim.split(':')
		ttt1= int(h) * 3600 + int(m) * 60 + int(s)	
		tim, sec = time[j-1].split('.')
		h, m, s = tim.split(':')
		ttt2= int(h) * 3600 + int(m) * 60 + int(s)
		diff= abs(ttt1-ttt2)
		if diff > 100:
			break;
		j-=1
	for i in range(j):
		ll.append(i)
	time = np.delete(time, (ll), axis=0)
	meth = np.delete(meth, (ll), axis=0)
	ll2=[]
	
	for i in range(len(meth)-1):
		j=i+1
		while j<len(meth):
			if meth[i] == meth[j]:
				ll2.append(j)
			j+=1
	ll2 = np.unique(ll2)
	
	time = np.delete(time, (ll2), axis=0)
	meth = np.delete(meth, (ll2), axis=0)

	with open('Result/timm.csv', 'wb') as csvfile:
		fieldnames = ['Time', 'Activity']	
		wr = csv.DictWriter(csvfile,  fieldnames=fieldnames)
	    	wr.writeheader()
		for i in range(len(time)):
		
				wr.writerow({"Time" : time[i], "Activity" : meth[i] })
	print "Time for matching done with timm.csv"

def power():
	time =[]
	volt=[]
	curr=[]
	temp = []
	pack = 	", voltage: "
	pack1 = "current_now:"
	pack1 = "current avg:"
	with open("Result/bugg.txt" ,'r') as f:
		for line  in f:
			if pack in line:
				j=0
				for word in line.split():
					if j ==12:
						items = re.findall("(\d+),",word)
						for item in items:
	    						val= float(item)
						val = val
						volt.append(val)
					if j == 14:
						items = re.findall("(\d+),",word)
						for item in items:
	    						val= float(item)
						
						temp.append(val)
					if j == 1:
						time.append(word)
					j+=1

			if pack1 in line:
				j=0
				for word in line.split():
					if j==20:
						items = re.findall(":(-\d+)",word)
						for item in items:
	    						val= float(item)
						if val > 0:
							items = re.findall(":(\d+)",word)
							for item in items:
	    							val= float(item)
						val = val
						curr.append(val)					
					j+=1
			
	with open('Result/Power.csv', 'wb') as csvfile:
		fieldnames = ['Time', 'Voltage', 'Current' , 'Temper']	
		wr = csv.DictWriter(csvfile,  fieldnames=fieldnames)
	    	wr.writeheader()
		for i in range(len(time)):
			wr.writerow({"Time" : time[i], "Voltage" : volt[i] ,"Current" : curr[i], 'Temper' : temp[i] })
	print "Voltage and current value done with Power.csv"


def secToStr(t):
    return "%02d:%02d:%02d.%03d" % \
        reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],
            [(t*1000,),1000,60,60])

def hour(msec):
	tim, sec = msec.split('.')
	h, m, s = tim.split(':')
	ttt= int(h) * 3600 + int(m) * 60 + int(s)+(.001*float(sec))
	return ttt
def cpm(po):
	res =float(po[2])*float(po[1])
	res/= len(po)
	return res
def vpm(ttt,time,intt):
	res =float(ttt[3])
	res = (((res)*time)/intt)*float(ttt[1])
	return res


def result():
	ind = []
	time4 = []
	time3 =[]
	time2 = []
	volt = []
	curr = []
	end = []
	powe =[]
	temp =[]
	en =[]
	dumm = []
	exptime1 =[]
	exptime2 =[]
	method =np.genfromtxt('Result/Method.csv', delimiter=',', dtype=None , names=('method','Activity','Excl','Incl'))
	power =np.genfromtxt('Result/Power.csv', delimiter=',', dtype=None , names=('Time', 'Voltage', 'Current','temper'))
	time =np.genfromtxt('Result/timm.csv', delimiter=',', dtype=None , names=('Time', 'Activity'))
	
	method = np.delete(method, (0), axis=0)
	power = np.delete(power, (0), axis=0)
	time = np.delete(time, (0), axis=0)
	de =[]

	for i in range(len(method)):
		if method[i][3] == '0':
			de.append(i)
	method = np.delete(method, de, axis=0)
	
	for i in range(len(method)):
		val= method[i][1]
		for k in range(len(time)):
			if time[k][1] == val:
				time2.append(time[k][0])			
				break;
		if k == len(time)-1:
			time2.append(time[k-1][0])
	

	for i in range(len(time2)):
		dumm.append(time2[i])

	for i in range(len(method)):
		j=i-1
		while j >= 0:
			if dumm[j] == time2[i]:
				time2[i] = end[j]
				break;
			j=j-1
		tt = hour(time2[i])
		timet = float(power[i-1][1])-float(power[i][1])
		powert = float(power[i-1][2])-float(power[i][2])
		if float(method[i][3]) <0.8:
			t = float(method[i][3])*vpm(power[i],timet,powert)
			
		else:
			t = float(method[i][3])*cpm(power[i])
			
		tt = float(tt)+t
		
		end.append(secToStr(tt))

	for i in range(len(time2)):
		tt = hour(time2[i])
		time3.append(tt)

	for i in range(len(power)):
		tt = hour(power[i][0])
		time4.append(tt)
	
	for i in range(len(time3)):
		minn = abs(time3[i]-time4[0])
		index = 0
		for j in range(len(time4)):	
			diff= abs(time3[i]-time4[j])
			if diff < minn: 
				minn= diff
				index = j
		ind.append(index)
	ptime = []
	for i in range(len(time2)):
		volt.append(power[ind[i]][1])
		curr.append(power[ind[i]][2])
		temp.append(power[ind[i]][3])
		ptime.append(power[ind[i]][0])

	
	for i in range(len(time2)):

		diff1 = abs(time3[i]-time4[ind[i]+1])
		diff2 = abs(time3[i]-time4[ind[i]-1])
		if diff1<diff2:
			ind[i]=ind[i]+1
		else:
			ind[i] = ind[i]-1
	

	volt1 =[]
	curr1 = []
	ptime1 = []
	powe1 =[]
	
	for i in range(len(time2)):
		volt1.append(power[ind[i]][1])
		curr1.append(power[ind[i]][2])
		temp.append(power[ind[i]][3])
		ptime1.append(power[ind[i]][0])
	
	inter = []
	powerval = []
	ps=0
	pe=0
	ee = hour(ptime1[0])
	for i in range(len(ptime1)):
		if hour(ptime1[i]) > ee:
			ee = hour(ptime1[i])
			pe = float(volt1[i])*float(curr1[i])
	ss=hour(ptime[0])
	ps = float(volt[0])*float(curr1[0])
	while ss < ee:
		inter.append(secToStr(ss))
		ss+=.3
	if pe < 0:
		pe = pe* (-1)
	if ps < 0:
		ps = ps* (-1)
	vp = pe-ps
	vp = vp / len(inter)
	for i in range(len(inter)):
		ps +=vp
		powerval.append(ps/1000)
	
	#print inter
	for i in range(len(method)):
		pp = []
		k=0
		for j in range(len(inter)):
			if hour(inter[j]) > hour(time2[i]) and hour(inter[j]) < hour(end[i]):
				pp.append(powerval[j])
				k+=1
		if len(pp)>2:
			ee = pp[0] + pp[len(pp)-1]
			l=1
			for l in range(len(pp)-1):
				if i%2 == 0 :
					ee += pp[l]*4
				else:
					ee += pp[l]*2
			ee = ee/ (3* len(pp))
			ee = ee/1000
			
			if ee >1.8:
				ee = ee/1.7
			print ee
			ee = ee * float(method[i][3])
			
		else:
			ee = float(method[i][3])*1.1456
		del pp
		en.append(ee)
		
	with open('Final.csv', 'wb') as csvfile:
		fieldnames = ['method', 'Activity', 'Excl', 'Incl', 'Start', 'End' ,'Energy']	
		wr = csv.DictWriter(csvfile,  fieldnames=fieldnames)
	    	wr.writeheader()
		for i in range(len(method)):
				wr.writerow({"method" : method[i][0], "Activity" : method[i][1] ,"Excl" : method[i][2] , "Incl" : method[i][3]  , "Start" : time2[i], "End" : end[i], "Energy" : en[i] })
	print "Main Result create Meth.csv"

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
        

def comm():
	i=0
	my_file = "sapl.trace"
	import os.path
 
	if os.path.isfile(my_file):
		os.system("dmtracedump -h Result/sapl.trace > Result/meth.html")
		i+=1
	else:
		print "Error:  Sapl.trace not exist"	
	if os.system("adb devices"):
		os.system("adb bugreport > Result/bugg.txt")
		i+=1
	else:
		print "Error:  Device not connected"
	return i 

createFolder('./Result/')
#if comm() == 2:
#comm()

os.system("dmtracedump -h Result/sapl.trace > Result/meth.html")
package= "org.billthefarmer.editor"
com="org"
trace(package)
line(package,com);
time(package)
power();
result();
#else:
#	print "Retry"


