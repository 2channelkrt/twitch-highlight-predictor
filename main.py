import numpy as np
from Loader import *
from HLoader import *
import os
import random
import argparse
import sys
def work(args):
	path=os.getcwd()
	data_path=path+args.Dpath
	
	if(args.file==None):
		filelist=os.listdir(data_path)
	else:
		filelist=args.file
		if(args.verbose):
			print("datafile: total {} files given".format(len(filelist)))	
	
	L=[]
	
	

	for i, filename in enumerate(filelist):
		L.append(Log(path=data_path, filename=filename))
		#if(args.verbose):
			#print("loading file {}/{} {}...".format(i, len(filelist), filename), end='')
			#sys.stdout.flush()
		#L[-1].load_data(trim=True)
		#if(args.verbose):
			#print("done.")
		#if(args.offload==True):
		#	L[-1].data=[]
	
	Hpath=path+args.Hpath
	HL=HLoader(Hpath, args.Hfile)
	HL.load_data(data_reload=True)

	if(args.method=='burst'):
		for i, f in enumerate(L):
			if(args.verbose):
				sys.stdout.flush()
				print("predicting file {}/{} {}...".format(i, len(L), f.filename),end='\r')
			sys.stdout.flush()
			f.predict(args)
		print(" "*100, end='\r')

		preds=[]
		for i in L:
			f=[]
			f.append(i.filename[:-4])
			f.append(i.predictions)
			preds.append(f)

		TP, FP, FN = evaluate(preds, HL.data, args.tol)
		result="{}, dur={}, thsld={}, words={}, TP: {}, FP: {}, TN: NaN, FN: {}".format(args.method, args.duration, args.threshold, args.words, TP, FP, FN)

	elif(args.method=='rise'):
		for i, f in enumerate(L):
			if(args.verbose):
				sys.stdout.flush()
				print("predicting file {}/{} {}...".format(i, len(L), f.filename),end='\r')
			sys.stdout.flush()
			f.predict(args)
		print(" "*100, end='\r')

		preds=[]
		for i in L:
			f=[]
			f.append(i.filename[:-4])
			f.append(i.predictions)
			preds.append(f)

		TP, FP, FN = evaluate(preds, HL.data, args.tol)
		result="{}, {}, step={}, TP: {}, FP: {}, TN: NaN, FN: {}".format(args.method, args.method2, args.step, TP, FP, FN)

	elif(args.method=='trendy'):
		for i, f in enumerate(L):
			if(args.verbose):
				sys.stdout.flush()
				print("predicting file {}/{} {}...".format(i, len(L), f.filename),end='\r')
			sys.stdout.flush()
			f.predict(args)
		print(" "*100, end='\r')

		preds=[]
		for i in L:
			f=[]
			f.append(i.filename[:-4])
			f.append(i.predictions)
			preds.append(f)

		TP, FP, FN = evaluate(preds, HL.data, args.tol)
		result="{}, dur={}, tsld={}, tol={}, TP: {}, FP: {}, TN: NaN, FN: {}".format(args.method, args.duration, args.threshold, args.tolerance, TP, FP, FN)

	print(result)
	ff=open('./result.txt', 'a')
	ff.write(result+'\n')
	ff.close()
	

	

if __name__ == "__main__":

	parser=argparse.ArgumentParser(description='returns list of \
		possible hightlights from the stream based on the chat log')

	parser.add_argument('-file', nargs='+', type=str, help="chat log file name to be analyzed.\
						If not given, all files are considered inputs.", default=None)
	
	parser.add_argument('-method', type=str, help='method of extracting highlight. \
						Supported methods are "burst", and "rise". defualt is burst', default='burst')

	parser.add_argument('-threshold', metavar='T', type=int, default=20, help="Only active if 'method' is 'burst'.\
						Minimum occurance limit of 'words' in 'duration'.. defualt is 20")
	parser.add_argument('-duration', metavar='D', type=int, default=3, help="Only active if 'method' is 'burst'.\
						Maxmimum time span for given 'words' to occur above 'threshold'. default is 3")
	parser.add_argument('-words', metavar='W', nargs='*', type=str, default='ㅋㅋㅋ', help="Only active if  'burst' is given.\
						substring which will be counted in the chat log. defualt is 'ㅋㅋㅋ'")

	parser.add_argument('-step', metavar='S', type=int, default=5, help="Only active if method is 'rise'.\
						Minimum rising step without falling of chat frequency per second. default is 5")

	parser.add_argument('-Dpath', metavar='D', type=str, help="relative path \
						from current directory to data folder where chat log is stored.\
						defualt is '\\data'", default=r'\data')
	
	parser.add_argument('-Hpath', metavar='HP', type=str, help="relative path \
						from current directory to highlights folder where highlights are logged.\
						default is '.'", default="\\")
	parser.add_argument('-Hfile', metavar='HF', type=str, help="filename for logged highlights.\
						default is 'hightlights.txt'", default='highlights.txt')
	parser.add_argument('-tol', metavar='T', type=int, help="prediction tolerance value. default is 60(seconds)", default=60)
	parser.add_argument('-verbose', metavar='V', type=str, help="if True, print working status. Good for debugging.\
						if False, only prints results. default is False", default='False')
	parser.add_argument('-offload', metavar='O', type=bool, help="save RAM by offloading original data from RAM after logging predictions.\
						If False, loaded data are kept in RAM. If True, data is removed from RAM after making single prediction.\
						It dramatically saves RAM, but every new predictions require another data load, which takes lot more time.\
						If 'out of memory' error occurs, set to True. default is False. If you wish to set it 'False', do not mention.", default=False)
	parser.add_argument('-method2', metavar='m2', type=str, help="method used by step method. supported are 'mov_av' and 'naive'. default is 'mov_av'", default='mov_av')

	args=parser.parse_args()
	
	if(args.verbose.lower() in ('yes', 'true', '1', 't')):
		args.verbose=True
	elif(args.verbose.lower() in ('no', 'false', '0', 'f')):
		args.verbose=False
	else:
		print("verbose input error. given {}".format(args.verbose))
		exit()

	if((args.method=='burst' or args.method=='rise' or args.method=='trendy') is False):
		print("feed for argument 'method' is unknown. Supported"+
				"methods are 'burst' and 'rise'. Given value:{}".format(args.method))
		quit()
	
	work(args)
	#print("done..terminating")
	'''
	c_path=os.getcwd()
	data_path=c_path+'\\data'
	file_list=os.listdir(data_path)
	print(file_list)
	'''