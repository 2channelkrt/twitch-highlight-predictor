import numpy as np
import matplotlib.pyplot as plt
import copy
def time_to_int(text): #supported input is np.array, list. Output format is same as input
	if(type(text) is str):
		if(check_time_input(text)==True):
			x=text[1:-1].split(":")
		else:
			x=text.split(":")
		return int(x[0])*3600+int(x[1])*60+int(x[2]) 

	if(type(text) is list):
		out=[]
		for i, t in enumerate(text):
			if(check_time_input(t)==False):
				print("list line {} time format error".format(i))
				return None

			x=t[1:-1].split(":")
			out.append(int(x[0])*3600+int(x[1])*60+int(x[2]))
		return out

	if(type(text).__module__ is 'numpy'):
		out=[]
		text=text.tolist()
		if(type(text) is str): ## numpy changes single element np array to str
			return time_to_int(text)

		for i, t in enumerate(text):
			if(check_time_input(t)==False):
				print("numpy line {} time format error".format(i))
				print(t)
				return None

		out=[t[1:-1].split(":") for t in text]
		out=np.asarray(out, dtype=int)
		m=np.asarray([3600, 60, 1], dtype=int)
		out = np.sum(np.multiply(out, m), axis=1)
		return out
def time_to_text(time):
	h=time//3600
	time%=3600
	m=time//60
	s=time%60
	return str(h).zfill(2)+':'+str(m).zfill(2)+':'+str(s).zfill(2)

def seconds_to_HMS(time): #supported input is np.array, list. Output is always List
	if(type(time) is int):
		return time_to_text(time)

	if(type(time).__module__ is 'numpy'):
		time=time.tolist()

	if(type(time) is list):
		out=[]
		for t in time:
			out.append(time_to_text(t))
		return out

def check_time_input(text):
	#print(text)
	if(text[0]!='[' or text[-1]!=']'):
		return False
	return True
def my_plot(x, y, x_label='HMS'):
		plt.rcParams['figure.figsize']=(200,10)
		plt.rcParams['lines.linewidth']=1
		#plt.rcParams['lines.markersize']=3
		xtick=np.arange(x[0], x[-1], step=int((x[-1]-x[0])/400))
		if(x_label is 'HMS'):
			plt.xticks(xtick, seconds_to_HMS(xtick), rotation=90)
		else:
			plt.xticks(xtick, rotation=90)

		plt.plot(x,y)
		return

def prune_highlight(preds, tolerance):
	new_preds=[]
	prev_time=-61
	for time in preds:
		cur_time=time_to_int(time)
		if(cur_time-prev_time<tolerance):
			new_preds.pop()
			new_preds.append(time)
			prev_time=cur_time
		else:
			new_preds.append(time)
			prev_time=cur_time

	return new_preds

def evaluate(preds, highlights, tolerance):
    ##check if datas are in right format
	#print("predictions")
	#print(preds)
	#print("highlights")
	#print(highlights)

	TP, FP, FN = 0, 0, 0
	cur_highlights=copy.deepcopy(highlights)
	last_look=0
	pop_index=0
	for f in preds:
		last_look=-tolerance-1
		#print("looking at {}".format(f[0]))
		for guess in f[1]:
			pred_hit=False
			current_look=time_to_int(guess)
			if(abs(current_look-last_look)>tolerance):
				for index, h in enumerate(cur_highlights):
					if(h[0]==f[0] and abs(time_to_int(guess)-time_to_int(h[1]))<tolerance):
						pred_hit=True
						pop_index=index
						break
				if(pred_hit==True):
					TP+=1
					cur_highlights.pop(pop_index)
				else:
					FP+=1
			last_look=current_look
	last_file=''
	last_look=0
	for h in cur_highlights:
		if(h[0]!=last_file):
			last_look=-tolerance-1
		current_look=time_to_int(h[1])
		if(abs(current_look-last_look)>tolerance):
			FN+=1
		last_look=current_look

		last_file=h[0]
	
	#print("TP: {}, FP: {}, TN: NaN, FN: {}".format(TP, FP, FN))
	return (TP, FP, FN)

