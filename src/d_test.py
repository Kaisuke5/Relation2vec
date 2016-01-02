import PMI
import pandas as pd
p=PMI.Corpus()
p.all_load_corpus()


d_num=[100,300,500,1000]
v_lst=["say","accuse","fight","sensitive","oppose","apologize","aid","shoot","follow"]


for verb in v_lst:

	data={}
	for d in d_num:
		print "----d=%d-----" % d
		p.factorize(d)

		lst=p.c_similar(verb,N=8)[0]
		data[str(d)]=pd.Series(lst)




	print "-----bow-----"

	lst=p.c_similar(verb,N=8,bow=True)[1]
	data[str("bow")]=pd.Series(lst)
	print "-------------"

	df=pd.DataFrame(data)

	print "\nsaving %s.csv"%verb
	#df.to_csv("verb_csvs/"+verb+"_sqrt"+".csv")
	df.to_csv("verb_csvs/"+verb+".csv")

