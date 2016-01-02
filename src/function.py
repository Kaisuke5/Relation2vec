
WRONG_LST="GMY CHA UKG NTH FRN SPN KUW CRO YUF PHI THJ DRC POR CMO SUD GUI ANG NIG".split()
RIGHT_LST="DEU TCD GBR NLD FRA ESP KWT HRV MKD PHL TJK COG PRT CMR SDN GIN AGO NGA".split()


def rule(ca,cb,year,v,n):
	n_lst=[]
	v_lst=["have"]
	v_n=v+"_"+n
	
	t="("+ca+","+cb+","+year+")"
	t=year+" "+ca+" "+cb
	if v=="":return None

	if n=="":return t,v
	
	if v in v_lst: return t,v_n

	if n=="missile": return t,"missile"

	if n=="troops": return t,v_n




def to_write_abb(contry):
	if contry in RIGHT_LST:
		return WRONG_LST[RIGHT_LST.index(contry)]

	return contry


def make_tuple_from_line(line):
	lst=line.split()
	#print lst[2],lst[3:5],lst[5]
	elements=lst[5].split("],")
	t="("+lst[3]+","+lst[4]+","+lst[2][:4]+")"


	ca=to_write_abb(lst[3])
	cb=to_write_abb(lst[4])
	year=lst[2][:4]
	n=""
	v=""

	
	for e in elements:
		if len(e)==0: continue
		e=e.replace("[","").replace('"','')
		e_childs=e.split(",")
		#print e_childs,"\n"
		if e_childs[2]=="verb": v=e_childs[1]
		if e_childs[2]=="noun": n=e_childs[1]

	ans=rule(ca,cb,year,v,n)
	return ans





if __name__=="__main__":
	# d={}

	# f=open("Corpus_fixed.txt","w")

	# for line in open("../data/v7.pathfil.dthresh=500.pthresh=10","r"):
	# 	ans=make_tuple_from_line(line)
	# 	if ans == None: continue
		
	# 	line=ans[0]+" "+ans[1]+"\n"
	# 	f.write(line)

	# 	v=ans[1]
	# 	if v in d: d[v]+=1
	# 	else: d[v]=1

	# for key,value in sorted(d.items(),key=lambda x:x[1],reverse=True):
	# 	print key,value

	f=open("Corpus_fixed.txt","w")
	for line in open("../data/v7.pathfil.dthresh=500.pthresh=10","r"):
		data=make_tuple_from_line(line)
		if data==None: continue
		a=data[0]+" "+data[1]+"\n"
		f.write(a)