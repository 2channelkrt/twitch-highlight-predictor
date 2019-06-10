import numpy as np
from util import *

class Log:
	def __init__(self, path, filename):
		self.path=path
		self.filename=filename
		self.abspath=path+"\\"+filename

		self.data=[]
		self.predictions=[]
	def print_info(self):
		print("Link: ", "https://twitch.tv/videos/"+self.filename[:-4])
		if(self.data_loaded()):
			print("Total Runtime: ", self.data[-1,0])
	def trim(self, line):#add trimming rule.
		user=line[1]
		text=line[2]
		ul=len(user)
		if(user.find('bot',ul-3,ul) != -1):#if bot
			return True
		if(user.find('Bot',ul-3, ul) != -1):
			return True
		if(text.find('!',0,1) != -1):
			return True
		#add trimming rule; ex: bot commands, bot responds, subscriptions, donation
		return False
	def load_data(self, trim=True, data_reload=False):
		if(data_reload is True):
			self.data=[]
		elif(self.data_loaded()):
			print("data seems to be already loaded.\nTo reload, set parameter 'data_reload' to True")
			return

		f=open(self.abspath, "r", encoding='UTF8')
		for line in f:
			#print(line[:-1])
			s=line.split(" ",2)
			d=[]
			d.append(s[0])
			d.append(s[1][1:-1])
			d.append(s[2][:-1])
			if(trim is False or self.trim(d)==False):
				self.data.append(d)

		self.data=np.asarray(self.data)
		f.close()
		return

	def chat_frequency(self, plot=True):
		if(self.data_loaded()==False):
			print("Data not loaded")
			return
		times=self.data[:,0]
		l=time_to_int(times)

		if(type(l) is list):
			l=np.asarray(l)
		timestamp, count=np.unique(l, return_counts=True)
		plt.close()
		if(plot is True):
			my_plot(timestamp, count)
		return timestamp, count

	def chat_mov_average(self, window, plot=True):
		timestamp, count=self.chat_frequency(plot=False)
		

		index=0
		mx=[i for i in range(timestamp[-1])]
		my=[]

		for i in mx:
			if (timestamp[index]==i):
				my.append(count[index])
				index+=1
			else:
				my.append(0)

		my2=[]

		for i in mx:
			start	= int(0 if i-window/2 <= 0 else i-window/2)
			end 	= int(timestamp[-1] if i+window/2>= timestamp[-1] else i+window/2)

			my2.append(int(sum(my[start:end])/(end-start)))
		my=None

		plt.close()
		if(plot is True):
			my_plot(mx, my2)
		return mx, my2 #timestamp, frequency
	def data_loaded(self):
		return False if len(self.data)==0 else True

##########################################################################
##########################################################################
#following functions are recommended to be called in self.predict fnction#
##########################################################################
##########################################################################

	#prediction methods.
	#input parameter: data
	#return : list of candidates
	def trendy(self, duration, threshold):
		if(self.data_loaded()==False):
			print("data not loaded")
			return
		
		out=[]

		total={}
		current={}
		cur_t=self.data[0][0]
		for line in self.data:
			if(line[0]!=cur_t):#new time
				prev_t=cur_t
				#prune duplicates
				remove={}

				for i, focus in enumerate(current):
					for j, target in enumerate(current):
						if (i>=j):
							continue
						if (target.find(focus)!=-1):
							#if focus is part of target
							#add to remove list
							remove[focus]=target
							continue
				
				for key, val in remove.items():
					current[val]+=current[key]
					del current[key]
				#evaluate
				for key, val in current.items(): #merge to total
					if key in total:
						total[key][-1]+=val
					else:
						total[key]=[0]*(duration-1) + [val]
				
				remove=[]
				current={}

				for key, val in total.items():
					#check for elements not occuring right now
					tot=sum(val)
					if tot==0:
						remove.append(key)
					elif tot>=threshold:
						out.append(time_to_int(line[0]))#found!
				for item in remove:#delete words not occuring right now
					del total[item]

				
				#update
				cur_t=line[0]
				diff=time_to_int(cur_t)-time_to_int(prev_t)
				for word in total:#shift new slot
					for a in range(diff):
						total[word].pop(0)
						total[word].append(0)
			
			words=line[2].split(' ')
			for word in words:
				if word in current:
					current[word]+=1
				else:
					current[word]=1
		return out
			

			

	def word_bursts(self, words, threshold=20,duration=3):#words are in lists
	#word in words is shown in min of 'threshold' in 'duration'
		predictions=[]
		field=np.zeros((len(words), duration))
		last_time=0
		for line in self.data:
			cur_time=time_to_int(line[0])
			if(cur_time != last_time):
				if(sum([i >= threshold for i in np.sum(field, axis=1)]) > 0):
					predictions.append(cur_time)
				field[:,cur_time%duration]=0
			for i, target in enumerate(words):
				if(line[2].find(target) != -1):
					#print(line, target)
					#todo: implement the case when chat is empty for more than duration
					field[i, cur_time%duration]+=1
			last_time=cur_time
			#if(sum(field).any()>0):
				#print(field)
			#if(cur_time>1000):
			#	break
		return predictions

	def rise_without_down(self, func='mov_av', step=5):
		#'chat frequency per second' is continuously increasing for number of steps
		if(func=='naive'):
			time, freq=self.chat_frequency(plot=False)
		elif(func=='mov_av'):
			time, freq=self.chat_mov_average(window=100, plot=False)
		predictions=[]
		combo=0
		prev=0
		cur_time=0

		for t, f in zip(time, freq):
			if(t != cur_time):##if current t has freq of 0
				cur_time+=2
				prev=0
				combo=0
				continue
			if(f>prev):##compare frequency with previous time
				combo+=1
			elif(f<prev):
				combo=0
			if(combo>=step):
				combo=0
				predictions.append(t)
			cur_time+=1
			prev=f
		return predictions






	def predict(self,args):
		if(self.data_loaded()==False):
			self.load_data()
			#print("Data not loaded")
		if(args.method=='burst'):
			predictions=self.word_bursts(words=args.words, threshold=args.threshold, duration=args.duration)
		elif(args.method=='rise'):
			predictions=self.rise_without_down(step=args.step, func=args.method2)
		elif(args.method=='trendy'):
			predictions=self.trendy(duration=args.duration, threshold=args.threshold)
		else:
			print("args.method is not recognized. given: {}".format(args.method))
		predictions=seconds_to_HMS(predictions)
		self.predictions=prune_highlight(predictions, args.tol)
		self.data=[]
		return self.predictions

##########################################################################
##########################################################################