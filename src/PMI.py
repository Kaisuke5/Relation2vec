#a=() b=verb
import numpy as np
import math
class Corpus:

	def __init__(self):
		self.tuple={}
		self.verb={}
		self.pair={}
		self.count_tuple=[]
		self.count_verb=[]
		self.t_v_dic={}

		self.stopword="be with ready hopeful take make begin set bring have rap down pad challenge buy work produce turn join end start not home different direct subject remind bone grateful market".split()









	def load_line(self,line,ignore_contry=[]):
		data=line.split()
		year=data[0][0:4]
		ca=data[1]
		cb=data[2]
		verb=data[3]

		if ca in ignore_contry or cb in ignore_contry or data[3] in self.stopword: return
		t="("+ca+","+cb+","+year+")"
		t_v=t+"="+verb

		if t in self.tuple:
			id=self.tuple[t]
			self.count_tuple[id]+=1

		else:
			id=len(self.tuple)
			self.tuple[t]=id
			self.count_tuple.append(1)

		if verb in self.verb:
			id=self.verb[verb]
			self.count_verb[id]+=1

		else:
			id=len(self.verb)
			self.verb[verb]=id
			self.count_verb.append(1)

		if t_v in self.t_v_dic: self.t_v_dic[t_v]+=1
		else: self.t_v_dic[t_v]=1






	def PMI(self,alpha=0.05):

		self.pmi_matrix=np.zeros((len(self.tuple),len(self.verb)))
		self.bow_matrix=np.zeros((len(self.tuple),len(self.verb)))

		for key,value in self.t_v_dic.items():
			tuple,verb=key.split("=")
			tuple_id=self.tuple[tuple]
			verb_id=self.verb[verb]
			self.pmi_matrix[tuple_id][verb_id]=value
			self.bow_matrix[tuple_id][verb_id]=value


		t=np.array([self.count_tuple],np.float).T
		v=np.array([self.count_verb],np.float)


		self.pmi_matrix[self.pmi_matrix==0]=alpha
		self.pmi_matrix*=(len(self.verb)*len(self.tuple)/len(self.t_v_dic))
		#print self.pmi_matrix[18]
		self.pmi_matrix/=t
		self.pmi_matrix/=v
		#print self.pmi_matrix[18]
		self.pmi_matrix=np.log(self.pmi_matrix)
		#self.pmi_matrix[self.pmi_matrix<0]=0

		print "size:%d %d" % (len(self.pmi_matrix),len(self.pmi_matrix[0]))








	def load_corpus(self):

		ca="USA"
		cb="IRQ"
		for line in open("corpus.txt","r"):
		#if count==10: break
			data=line.split()
			if len(data[3])>2 and len(set([ca,cb]) &set([data[1],data[2]])) == 2:

				self.load_line(line)
		print "tuple:%d verb:%d pair:%d" %(len(self.tuple),len(self.verb),len(self.t_v_dic))
		print "caluculating PMI...."
		self.PMI()

	def all_load_corpus(self):

		#c="USA IRQ AFG ISR PSE IRN SYR".split()
		count=0
		for line in open("corpus.txt","r"):
			#if count==10: break
			data=line.split()

			#if len(data[3])>2 and (data[1] in c or data[2] in c):
			self.load_line(line)
			count+=1
			#if count%10000==0:print count
		print "begin pmi"

		self.PMI()





	def factorize(self,d=42):
		U,s,V=np.linalg.svd(self.pmi_matrix,full_matrices=False)
		#s=s[::-1]
		s=np.diag(s[:d])
		self.w=np.dot(U[:,0:d],s)
		self.c=np.dot(V.T[:,0:d],s)


		# U2,s2,V2=np.linalg.svd(self.bow_matrix,full_matrices=False)
		# s2=np.diag(s2[:d])
		# self.w2=np.dot(U2[:,0:d],s2)
		# self.c2=np.dot(V2.T[:,0:d],s2)



	#similar option = 1 print bow


	# similar verb
	def c_similar(self,verb,bow=False,non_factorize=False,N=10):
		id=self.verb[verb]
		v=self.c[id]


		#vc/(|v|*|c|)
		cos_vec=np.sum(self.c*v,axis=1)/(np.linalg.norm(self.c,axis=1)*np.linalg.norm(v))
		l=np.argsort(cos_vec)
		l=l[::-1]
		vl=self.verb.items()
		print "PMI Matrix"
		for i in l[0:N]:
			obj=filter(lambda x:x[1]==i,vl)[0][0]
			print obj#,np.sum(self.c[i]*v)/(np.linalg.norm(self.c[i])*np.linalg.norm(v))




		if bow:
			v=self.bow_matrix.T[id]
			print "\noption bow rank\n"
			#cos_vec= np.sum(self.c2*v,axis=1)/(np.linalg.norm(self.c2,axis=1)*np.linalg.norm(v))
			cos_vec= np.sum(self.bow_matrix.T*v,axis=1)/(np.linalg.norm(self.bow_matrix.T,axis=1)*np.linalg.norm(v))

			l=np.argsort(cos_vec)
			l=l[::-1]
			for i in l[0:N]:
				obj=filter(lambda x:x[1]==i,vl)[0][0]
				print obj#,np.sum(self.c2[i]*v)/(np.linalg.norm(self.c2[i])*np.linalg.norm(v))


		if non_factorize:
			v=self.pmi_matrix.T[id]
			print "\nnon_factorize_pmi rank\n"
			cos_vec= np.sum(self.pmi_matrix.T*v,axis=1)/(np.linalg.norm(self.pmi_matrix.T,axis=1)*np.linalg.norm(v))

			l=np.argsort(cos_vec)
			l=l[::-1]
			for i in l[0:N]:
				obj=filter(lambda x:x[1]==i,vl)[0][0]
				print obj#,np.sum(self.c2[i]*v)/(np.linalg.norm(self.c2[i])*np.linalg.norm(v))





	def w_similar(self,tuple,option=0,N=10):

		tl=self.tuple.items()
		id=self.tuple[tuple]


		#PMI matrix
		print "PMI Matrix"
		t=self.w[id]
		cos_vec=np.sum(self.w*t,axis=1)/(np.linalg.norm(self.w,axis=1)*np.linalg.norm(t))
		l=np.argsort(cos_vec)[::-1]

		count=0
		for i in l:
			if count==N: break
			count+=1

			obj=filter(lambda x:x[1]==i,tl)[0][0]
			#if self.count_tuple[self.tuple[obj]]< 500:break
			print obj,self.count_tuple[self.tuple[obj]]




		if option==0: return

		#BOW matrix
		print "\noption bow rank\n"
		t=self.w2[id]
		cos_vec=np.sum(self.w2*t,axis=1)/(np.linalg.norm(self.w2,axis=1)*np.linalg.norm(t))
		l=np.argsort(cos_vec)[::-1]

		for i in l[0:N]:
			obj=filter(lambda x:x[1]==i,tl)[0][0]
			print obj





	def similar(self,tp,verb,tn,N=10):

		id_tp=self.tuple[tp]
		id_v=self.verb[verb]
		id_tn=self.tuple[tn]



		p=self.c<0
		squared_c=np.sqrt(np.fabs(self.c))
		squared_c[p]=squared_c[p]*-1
		ans=self.w[id_tp]-self.w[id_tn]+squared_c[id_v]
		cos_vec=np.sum(self.c*ans,axis=1)/(np.linalg.norm(self.c,axis=1)*np.linalg.norm(ans))
		l=np.argsort(cos_vec)[::-1]

		vl=self.verb.items()
		for i in l[0:N]:
			obj = filter(lambda x:x[1]==i,vl)[0][0]
			print obj

		ans=self.w[id_tp]-self.w[id_tn]+(self.c[id_v])
		cos_vec=np.sum(self.c*ans,axis=1)/(np.linalg.norm(self.c,axis=1)*np.linalg.norm(ans))
		l=np.argsort(cos_vec)[::-1]

		print "----------------"

		vl=self.verb.items()
		for i in l[0:N]:
			obj = filter(lambda x:x[1]==i,vl)[0][0]
			print obj






if __name__=="__main__":
	c=Corpus()
	c.all_load_corpus()

	for key,value in sorted(c.verb.items(),key=lambda x:x[1],reverse=True):
		print key,value
















