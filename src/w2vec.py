from gensim.models import word2vec
import numpy as np
import matplotlib.pyplot as pl



def pp(out):
	for x in out:
		if x[0][0]!="(": print x[0],x[1]


def cal(out):
	neg=["kill","fire","invade","bomb","violate","defeat","die","missile"]
	pos=["apologize","help","donate","encourage","approve","rescue"]

	pos_avr=0
	neg_avr=0
	p_count=0
	n_count=0


	pos_lst=filter(lambda x:x[0] in pos,out)
	neg_lst=filter(lambda x:x[0] in neg,out)

	print pos_lst
	print
	print neg_lst


	for p,n in zip(pos_lst,neg_lst):
		if p[1]>0:pos_avr+=p[1]
		if n[1]>0:neg_avr+=n[1]

	#pos_avr/=len(pos)
	#neg_avr/=len(neg)

	return pos_avr,neg_avr





filename="USA_IRQ.txt"
data=word2vec.Text8Corpus(filename)
model=word2vec.Word2Vec(data,window=5)



lst=np.arange(1996,2007,1)
for year in lst:

	print "----%d---"%year
	tupple="(USA,IRQ,%d)" % year
	out=model.most_similar(positive=[tupple],topn=15)
	pp(out)
	print


"""
pos_rate=[]
neg_rate=[]
for year in lst:
	tupple="(USA,IRQ,%d)" % year
	out=model.most_similar(positive=[tupple],topn=10000)

	print "-----%d---" % year

	words=[]
	for i in out[:5]:
		#print i[0],i[1],":"
		words.append(i)
		words.append(model.most_similar(positive=[i[0]],topn=3))
	pp(words)
	p,n=cal(out)
	print p,n
	pos_rate.append(p)
	neg_rate.append(n)

pl.plot(lst,pos_rate,"ob")
pl.plot(lst,neg_rate,"xr")
pl.savefig("demo.jpg")

"""""

