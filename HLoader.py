class HLoader:
	def __init__(self, path, filename):
		self.path=path
		self.filename=filename
		self.abspath=path+"/"+filename

		self.data=[]

	def load_data(self, data_reload=False):
		if(data_reload is True):
			self.data=[]
		f=open(self.abspath, "r", encoding='UTF8')
		for line in f:
			try:
				int(line[0])
				l=line.split(" ")
				d=[]
				d.append(l[0])
				d.append(l[1][:-1])
				self.data.append(d)
			except:
				continue
		self.data.sort()
	def data_loaded(self):
		return False if len(self.data)==0 else True


