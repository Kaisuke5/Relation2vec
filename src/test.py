import pandas as pd
import numpy as np

def make_corpus(output="corpus.txt",input="../data/v7.pathfil.dthresh=500.pthresh=10"):


	dates=[]
	Sources=[]
	Receivers=[]
	verbs=[]
	v={}
	fw=open(output,"w")
	for line in open(input,"r"):
		data=line.split()
		date=data[2]
		Ca=data[3]
		Cb=data[4]
		verb=data[5].split("],")[1].split(",")[1].replace("\"","")

		dates.append(date)
		Sources.append(Ca)
		Receivers.append(Cb)
		verbs.append(verb)
		if not verb in v: v[verb]=1
		else: v[verb]+=1

		s=date+" "+Ca+" "+Cb+" "+verb+"\n"
		fw.write(s)

	fw.close()



def f2(ca="USA",cb="IRQ"):
	filename=ca+"_"+cb+".txt"
	fw=open(filename,"w")
	time=""
	#
	count=0
	a_lst=[]
	b_lst=[]
	for line in open("corpus.txt","r"):
		data=line.split()
		if len(set([ca,cb]) &set([data[1],data[2]])) == 2:


			if len(data[3])<3: continue

			if time=="" or time!=data[0][0:4]:
				print time,count
				count=0
				time=data[0][0:4]


			if count%1==0:s="(%s,%s,%s) %s " %(data[1],data[2],data[0][0:4],data[3])
			else: s=data[3]+" "
			if len(s)<3: continue
			fw.write(s)
			#print data[0],data[3]
			count+=1

	fw.close()
#make_corpus()


def print_count(dic):
	count=0
	for k,v in sorted(dic.items(),key=lambda x:x[1],reverse=True):
		print k,v
		count+=1
		if count==20: break



def f3(ca="USA",cb="IRQ"):
	time=""
	#
	count=0
	d1={}
	d2={}
	for line in open("corpus.txt","r"):
		data=line.split()

		if time !="" and time > data[0][0:4]: break


		if time=="" or time!=data[0][0:4]:
			print "---%s----"%time
			print "%s to %s" % (ca,cb)
			print_count(d1)
			print
			print "%s to %s" % (cb,ca)
			print_count(d2)
			print
			count=0
			time=data[0][0:4]
			d1={}
			d2={}


		if ca==data[1] and cb==data[2]:
			if data[3] in d1: d1[data[3]]+=1
			else: d1[data[3]]=1
		elif ca==data[2] and cb==data[1]:
			if data[3] in d2: d2[data[3]]+=1
			else: d2[data[3]]=1



def f4(ca="USA",cb="IRQ"):
	filename=ca+"_"+cb+"R.txt"
	fw=open(filename,"w")
	s1=""
	s2=""
	for line in open("corpus.txt","r"):
		data=line.split()

		if len(data[3])<3: continue

		if ca==data[1] and cb==data[2]:
			s="("+str(ca)+","+str(cb)+","+str(data[0][0:4])+") "+data[3]+" "
			s1+=s
		elif ca==data[2] and cb==data[1]:
			s="("+str(cb)+","+str(ca)+","+str(data[0][0:4])+") "+data[3]+" "
			s2+=s


	fw.write(s1)
	fw.write(s2)
	fw.close()







#f2(ca="USA",cb="IRQ")
#f4(ca="USA",cb="IRQ")
f3()


"""
from gensim.models import word2vec
data = word2vec.Text8Corpus('data.txt')
model = word2vec.Word2Vec(data, size=200)

out=model.most_similar(positive=[u'])
for x in out:
	print x[0],x[1]

"""