#a=() b=verb
import numpy as np
import math
import function as F


class Corpus:

	def __init__(self):
		self.tuple={}
		self.verb={}
		self.pair={}
		self.count_tuple=[]
		self.count_verb=[]
		self.t_v_dic={}

		self.stopword="disappear revert customer destination chairman shower shun envision Poland guarantor sensitive blocklist be with ready hopeful take make begin set bring have rap down pad challenge work produce end start not home different direct subject bone grateful market".split()









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

	def load_line2(self,line,ignore_contry=[]):
		t,verb=F.make_tuple_from_line(line)

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
		CORPUS_FILE="Corpus_fixed.txt"

		count=0
		#for line in open("corpus.txt","r"):
		for line in open(CORPUS_FILE,"r"):

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
		#self.w=np.dot(U[:,0:d],np.sqrt(s))
		# self.c=np.dot(V.T[:,0:d],np.sqrt(s))
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
		ans=[]

		#vc/(|v|*|c|)
		cos_vec=np.sum(self.c*v,axis=1)/(np.linalg.norm(self.c,axis=1)*np.linalg.norm(v))
		l=np.argsort(cos_vec)
		l=l[::-1]
		vl=self.verb.items()
		print "PMI Matrix"

		lst=[]
		for i in l[0:N]:
			obj=filter(lambda x:x[1]==i,vl)[0][0]
			print obj#,np.sum(self.c[i]*v)/(np.linalg.norm(self.c[i])*np.linalg.norm(v))
			lst.append(obj)
		ans.append(lst)


		if bow:
			lst=[]
			v=self.bow_matrix.T[id]
			print "\noption bow rank\n"
			#cos_vec= np.sum(self.c2*v,axis=1)/(np.linalg.norm(self.c2,axis=1)*np.linalg.norm(v))
			cos_vec= np.sum(self.bow_matrix.T*v,axis=1)/(np.linalg.norm(self.bow_matrix.T,axis=1)*np.linalg.norm(v))

			l=np.argsort(cos_vec)
			l=l[::-1]

			for i in l[0:N]:

				obj=filter(lambda x:x[1]==i,vl)[0][0]
				print obj#,np.sum(self.c2[i]*v)/(np.linalg.norm(self.c2[i])*np.linalg.norm(v))
				lst.append(obj)

			ans.append(lst)
			print

		if non_factorize:
			lst=[]
			v=self.pmi_matrix.T[id]
			print "\nnon_factorize_pmi rank\n"
			cos_vec= np.sum(self.pmi_matrix.T*v,axis=1)/(np.linalg.norm(self.pmi_matrix.T,axis=1)*np.linalg.norm(v))

			l=np.argsort(cos_vec)
			l=l[::-1]

			for i in l[0:N]:

				obj=filter(lambda x:x[1]==i,vl)[0][0]
				print obj#,np.sum(self.c2[i]*v)/(np.linalg.norm(self.c2[i])*np.linalg.norm(v))
				lst.append(obj)

			ans.append(lst)

		return ans


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






	def similar(self,t1,v2,t2,N=10):
		id_t1=self.tuple[t1]
		id_t2=self.tuple[t2]
		v2=self.verb[v2]

		v=self.c[v2]+1.2*(self.w[id_t1]-self.w[id_t2])
		cos_vec=np.sum(self.c*v,axis=1)/(np.linalg.norm(self.c,axis=1)*np.linalg.norm(v))
		l=np.argsort(cos_vec)
		l=l[::-1]
		vl=self.verb.items()
		print "PMI Matrix"

		lst=[]
		for i in l[0:N]:
			obj=filter(lambda x:x[1]==i,vl)[0][0]
			print obj#,np.sum(self.c[i]*v)/(np.linalg.norm(self.c[i])*np.linalg.norm(v))
			lst.append(obj)




	def freq_verb(self,t,N=10):
		id=self.tuple[t]
		vec=self.pmi_matrix[id]
		l=np.argsort(vec)

		l=l[::-1]
		vl=self.verb.items()
		print "PMI Matrix"

		lst=[]
		for i in l[0:N]:
			obj=filter(lambda x:x[1]==i,vl)[0][0]
			print obj








if __name__=="__main__":
	c=Corpus()
	c.all_load_corpus()

	# for key,value in sorted(c.verb.items(),key=lambda x:x[1],reverse=True):
	# 	print key,value
















