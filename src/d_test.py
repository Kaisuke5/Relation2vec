import PMI
import pandas as pd
p=PMI.Corpus()
p.all_load_corpus()


d_num=[10,50,100,300,500,1000]
v_lst=["attack","accuse","help","threat","talk","benefit","defend","kill"]


for verb in v_lst:

	data={}
	for d in d_num:
		print "----d=%d-----" % d
		p.factorize(d)

		lst=p.c_similar("help",N=8)[0]
		data[str(d)]=pd.Series(lst)




	print "-----bow-----"
	p.factorize(d=1000)
	lst=p.c_similar("help",N=8,bow=True)[1]
	data[str("bow")]=pd.Series(lst)
	print "-------------"

	df=pd.DataFrame(data)

	print "\nsaving %s.csv"%verb
	df.to_csv("verb_csvs/"+verb+".csv")

