import pandas as pd


DATA_EVENT_PATH="../data/MID_data.csv"
DATA_ID_PATH="../data/contry_code.csv"






class mid_data:

	def __init__(self):
		data_id=pd.read_csv(DATA_ID_PATH)
		self.event=pd.read_csv(DATA_EVENT_PATH)
		self.contry_id={}

		for i,row in data_id.iterrows():
			self.contry_id[row["CCode"]]=row["StateAbb"]



	def dump(self):
		self.dataset=[]
		for i,row in self.event.iterrows():
			ca=self.contry_id[row["CCodeA"]]
			cb=self.contry_id[row["CCodeB"]]
			ha=row["HostlevA"]
			hb=row["HostlevB"]

			sy=int(row["StYear"])
			ey=int(row["EndYear"])

			for i in range(ey-sy):
				ta="(%s,%s,%d)" % (ca,cb,sy+i)
				self.dataset.append([ta,ha,ca,cb])



	def serach(self,ca=None,cb=None,hostlev=None):

		lst=self.dataset

		if ca!=None:
			lst=filter(lambda x:x[2]==ca,lst)

		if cb!=None:
			lst=filter(lambda x:x[2]==cb,lst)

		if hostlev!=None:
			lst=filter(lambda x:x[1]==float(hostlev),lst)



		return lst



if __name__=="__main__":
	print "kai"