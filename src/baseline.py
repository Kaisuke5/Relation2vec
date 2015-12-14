import numpy as np
from sklearn.linear_model import LogisticRegression




def print_count(dic):
	count=0
	for k,v in sorted(dic.items(),key=lambda x:x[1],reverse=True):
		print k,v
		count+=1
		if count==10: break



#x_dic={1992:[0,1,2,3,4]}
x_dic={}
y_dic={}


##load all vocab

time=""
#
count=0
d={}
ca="USA"
cb="IRQ"


for line in open("corpus.txt","r"):
	data=line.split()
	if len(set([ca,cb]) &set([data[1],data[2]])) == 2:
		if data[3] in d: d[data[3]]+=1
		else: d[data[3]]=1

		#print data[0],data[3]



lst=d.copy()
for key,val in lst.items():
	lst[key]=0

#print lst


##load x data
time=0
#
count=0

for line in open("corpus.txt","r"):
	data=line.split()
	if len(set([ca,cb]) &set([data[1],data[2]])) == 2:

		if time==0 or time!=int(data[0][0:4]):
			if time > int(data[0][0:4]):
				print "break!"
				break
			#print "---%s----"%time
			x_dic[time]=lst.copy()

			time=int(data[0][0:4])
			lst=d.copy()
			for key,val in lst.items():
				lst[key]=0

		lst[data[3]]+=1



##load y data

f1=open("")
f2=open("")









#make data set

x=[]
y=[]


for x_key,x_val in sorted(x_dic.items()):
	for y_key,y_val in sorted(y_dic.items()):

		if x_key == y_key:
			x.append(x_val)
			y.append(y_val)

		if x_key < y_key: break

x=[[1,1,1],[1,2,1],[1,3,1]]
y=[0,1,1]

model=LogisticRegression()
model.fit(x,y)
print model.predict([[1,4,1]])



