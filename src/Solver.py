import PMI
import Mid
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn import svm



def extract_dataset(matrix,danger_id_lst,rate=5,test_rate=0.3):

	num=len(danger_id_lst)*rate
	danger_x=matrix[danger_id_lst]
	safe=np.delete(matrix,danger_id_lst,0)
	r=np.random.randint(len(safe)-1,size=num)

	safe_x=safe[r]


	safe_size=int(len(safe_x)*(1-test_rate))
	danger_size=int(len(danger_x)*(1-test_rate))

	# print danger_x
	# print danger_size,safe_size


	train_x=[]
	train_y=[]
	test_x=[]
	test_y=[]

	train_x.extend(danger_x[:danger_size])
	train_y.extend(np.ones(danger_size))
	train_x.extend(safe_x[:safe_size])
	train_y.extend(np.zeros(safe_size))

	test_x.extend(danger_x[danger_size:])
	test_y.extend(np.ones(len(danger_x)-danger_size))
	test_x.extend(safe_x[safe_size:])
	test_y.extend(np.zeros(len(safe_x)-safe_size))


	return [train_x,train_y,test_x,test_y]







if __name__ == "__main__":

	pmi=PMI.Corpus()
	pmi.all_load_corpus()
	md=Mid.mid_data()
	md.dump()


	train_x=[]
	train_y=[]

	danger_set=filter(lambda x:x[0] in pmi.tuple,md.dataset)
	danger_id=map(lambda x:pmi.tuple[x[0]],danger_set)
	danger_id.sort()

	pmi.factorize(d=700)
	m=np.dot(pmi.w,pmi.c.T)


	data1=extract_dataset(pmi.bow_matrix,danger_id,rate=5,test_rate=0.3)
	data2=extract_dataset(m,danger_id,rate=5,test_rate=0.3)
	print len(danger_id)*0.3,len(danger_id)-len(danger_id)*0.3



	s=svm.SVC()
	lr1=LogisticRegression()
	lr2=LogisticRegression()

	lr1.fit(data1[0],data1[1])
	lr2.fit(data2[0],data2[1])


	print "1:",len(filter(lambda x:x==1,data1[3]))

	lrout1=lr1.predict(data1[2])
	lrout2=lr2.predict(data2[2])
	print lrout1,len(filter(lambda x:x>0.3,lrout1[:30]))
	print lrout2,len(filter(lambda x:x>0.5,lrout2[:30]))

