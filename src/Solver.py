import PMI
import Mid
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn import metrics


def extract_dataset(matrix,danger_id_lst,train_rate=0.7,train_safe=2,test_safe=20):

	danger_train_num=int(len(danger_id_lst)*train_rate)
	danger_test_num=len(danger_id_lst)-danger_train_num
	danger_x=matrix[danger_id_lst]

	safe=np.delete(matrix,danger_id_lst,0)

	# print "d_r:%d d_e:%d"%(danger_train_num,danger_test_num)
	# print "d_r:%d d_e:%d"%(danger_train_num*train_safe,danger_test_num*test_safe)


	r=np.random.randint(len(safe)-1,size=(danger_train_num*train_safe+danger_test_num*test_safe))


	safe_x=safe[r]



	train_x=[]
	train_y=[]
	test_x=[]
	test_y=[]

	train_x.extend(danger_x[:danger_train_num])
	train_y.extend(np.ones(danger_train_num))
	train_x.extend(safe_x[:danger_train_num*train_safe])
	train_y.extend(np.zeros(danger_train_num*train_safe))

	test_x.extend(danger_x[danger_train_num:])
	test_y.extend(np.ones(len(danger_x)-danger_train_num))
	test_x.extend(safe_x[danger_train_num*train_safe:])
	test_y.extend(np.zeros(len(safe_x)-danger_train_num*train_safe))


	return [train_x,train_y,test_x,test_y]







if __name__ == "__main__":






	## make pmi and mid dataset
	pmi=PMI.Corpus()
	pmi.all_load_corpus()
	md=Mid.mid_data()
	md.dump()


	train_x=[]
	train_y=[]

	danger_set=filter(lambda x:x[0] in pmi.tuple,md.dataset)
	print len(danger_set)
	danger_id=map(lambda x:pmi.tuple[x[0]],danger_set)
	danger_id.sort()

	pmi.factorize(d=300)
	m=np.dot(pmi.w,pmi.c.T)


	a1=0
	a2=0
	#for i in range(5):
	data1=extract_dataset(pmi.bow_matrix,danger_id,train_rate=0.5,train_safe=3)
	data2=extract_dataset(m,danger_id,train_rate=0.5,train_safe=3)




	s=svm.SVC()
	lr1=LogisticRegression()
	lr2=LogisticRegression()
	#lr1=svm.SVC()


	lr1.fit(data1[0],data1[1])
	lr2.fit(data2[0],data2[1])

	T=len(filter(lambda x:x==1,data1[3]))
	F=len(filter(lambda x:x==0,data1[3]))
	print "1:",T,"0:",F

	lrout1=lr1.predict(data1[2])
	lrout2=lr2.predict(data2[2])
	l=len(filter(lambda x:x==1,data1[3]))


	FP1=len(filter(lambda x:x==0,lrout1[:l]))
	TP1=len(filter(lambda x:x==1,lrout1[:l]))
	TN1=len(filter(lambda x:x>0,lrout1[l:]))
	FN1=len(filter(lambda x:x==0,lrout1[l:]))

	FP2=len(filter(lambda x:x==0,lrout2[:l]))
	TP2=len(filter(lambda x:x==1,lrout2[:l]))
	TN2=len(filter(lambda x:x>0,lrout2[l:]))
	FN2=len(filter(lambda x:x==0,lrout2[l:]))


	print "-----bow------"
	print "TP",TP1
	print "FN",FN1
	print "accuracy",float(TP1+FN1)/(T+F)

	print "-----our method----"
	print "TP",TP2
	print "FN",FN2
	print "accuracy",float(TP2+FN2)/(T+F)


	fpr1, tpr1, thresholds1 = metrics.roc_curve(data1[3], lrout1, pos_label=1)
	fpr2, tpr2, thresholds2 = metrics.roc_curve(data2[3], lrout2, pos_label=1)
	print "auc1:",metrics.auc(fpr1,tpr1)
	print "auc2:",metrics.auc(fpr2,tpr2)

	a1+=metrics.auc(fpr1,tpr1)
	a2+=metrics.auc(fpr2,tpr2)