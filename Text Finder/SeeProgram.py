import os,re,sys
from argparse import ArgumentParser as AP

version = 1.95

G = '\u001b[100;106m' #Green Background
Y = '\033[93m' #Yellow
R = '\033[91m' #Red
W = '\033[0m'  #Colour Reset Code, Here White
P = '\u001b[95m' #Pink
C = '\u001b[36m' #Cyan

#---------------------------------------------
##To Print Beautifully, Is Called By All Funcs
def Print(func,args):
	word = args[0]
	word = word.replace("_"," ")
	dir = args[1]
	
	print("\n" + "—"*65)
	print("The Word Searched For:",word)
	print("-"*40)
	found, not_working,accessed = func(word,dir)
	
	if found == 0:
		print(f"\nNo Files Containing {R}{word}{W} Found")
	else:
		print(f"\nTotal File(s) Found Containing {R}{word}{W}: {G} {found} {W}")
	
	if len(not_working) > 0:
		print("\n" + "*"*65 + "\n")
		print("Accessed Files:",accessed,"\n")
		l = len(not_working)
		print(l,"File(s) Not Accessible:\n")
		if l > 100: l = 100
		for i in range(l):
			print(f"{i+1}) {not_working[i]} Can Not Be Processed.")
		
	print("\n" + "—"*65)
	

#---------------------------------------------
#Word Search With Sensitive Case 
#Including Line Number

def func_m(word,dir):
	found = 0
	not_working = []
	accessed = 0
	
	for files in os.walk(dir):
		cwd = (files[0])
		
		#Prints Files Containing Word
		#And Increment Number Of Founds
		#While Collecting Non-Accessible Files
		for each in files[2]:
			accessed += 1
			try:
				f= open(f"{cwd}/{each}", 'r')
				data = f.read()
				f.close()
			except:
				not_working.append(each)
				continue
			#Collecting Non-Accessible Files
				
			#Searching For Word Inside File
			m = re.search(word, data)
			if m:
				found +=1
				line= data[:m.start()].count("\n") + 1
				#If Count=0, No Lines Before m And m.group() Will Be In Line 1
				print(f"{R}{m.group()}{W} Found In {C}{cwd}/{each}{W} In Line {P}{line}{W}")
				#os.getcwd() = files[0]
	
	#When All Files Are Accessed Or 
	#No Files Are Available,
	#Return The No. Of Found And
	#Non Accessible File Names
	return found, not_working, accessed
	
	
#---------------------------------------------
#Word Search With Sensitive Case 
#Without Line Number

def func_s(word,dir):
	not_working = []
	found = 0
	accessed = 0
	
	for files in os.walk(dir):
		cwd = (files[0])
		
		#Prints Files Containing Word
		#And Increment Number Of Founds
		#While Collecting Non-Accessible Files
		for each in files[2]:
			accessed += 1
			try:
				f= open(cwd+"/"+each, 'r')
				data = f.read()
				f.close()
			except:
				not_working.append(each)
				continue
			#Collecting Non-Accessible Files
				
			#Searching For Word Inside File
			m = re.search(word, data)
			if m:
				found += 1
				print(f"{R}{m.group()}{W} Found In {C}{cwd}/{each}{W}")
				#os.getcwd() = files[0]
	
	#When All Files Are Accessed Or 
	#No Files Are Available,
	#Return The No. Of Found And
	#Non Accessible File Names
	return found, not_working, accessed

#---------------------------------------------
#Recursively Searching Through Files 
#For Case Sensitive Word

def func_r(word,dir,found= 0,not_working= [],accessed= 0):
	
	#To Get All Dirs Available
	dirs = [i for i in os.listdir(dir) if os.path.isdir(dir+"/"+i)]
	#To Get All Files Available
	files = [i for i in os.listdir(dir) if os.path.isfile(dir+"/"+i)]
	
	#Accessing The Deepest Folder First
	#Calls Itself And Prints Files Containing
	#Word And Increment Number Of Founds
	#While Collecting Non-Accessible Files
	if len(dirs) > 0:
		for i in dirs:
			path = (dir+"/"+i)
			found,not_working,accessed = func_r(word,path,found,not_working,accessed)
	
	#Printing The Accessible Files 
	#Containing Word
	#From The Bottom To The Top
	#Using Recursion
	for each in files:
		accessed += 1
		try:
			f= open(dir+"/"+each, 'r')
			data = f.read()
			f.close()
		except:
			#Collecting Non-Accessible Files
			not_working.append(each)
			continue
		
		#Searching For The Word Inside File
		m = re.search(word, data)
		if m:
			#When Word Is Found,
			#Increase Count
			found += 1
			#And Print
			lin=data[:m.start()].count('\n')+1
			print(f"{R}{m.group()}{W} Found In {C}{dir}/{each}{W} In Line {P}{lin}{W}")
			#os.getcwd() = files[0]
	
	#When All Files Are Accessed Or 
	#No Files Are Available,
	#Return The No. Of Found And
	#Non Accessible File Names
	return found, not_working, accessed
	
	
#---------------------------------------------
#Word Search With Insensitive Case & Line No.

def func_mi(word,dir):
	found = 0
	not_working = []
	accessed = 0
	
	for files in os.walk(dir):
		cwd = (files[0])
		
		#Prints Files Containing Word
		#And Increment Number Of Founds
		#While Collecting Non-Accessible Files
		for each in files[2]:
			accessed += 1
			try:
				f= open(f"{cwd}/{each}", 'r')
				data = f.read()
				f.close()
			except:
				not_working.append(each)
				continue
			#Collecting Non-Accessible Files
				
			#Searching For Word Inside File
			m = re.search(word, data, re.I)
			if m:
				found +=1
				line= data[:m.start()].count("\n") + 1
				#If Count=0, No Lines Before m And m.group() Will Be In Line 1
				print(f"{R}{m.group()}{W} Found In {C}{cwd}/{each}{W} In Line {P}{line}{W}")
				#os.getcwd() = files[0]
	
	#When All Files Are Accessed Or 
	#No Files Are Available,
	#Return The No. Of Found And
	#Non Accessible File Names
	return found, not_working, accessed
	
	
#---------------------------------------------
#Search With Insensitive Case Without Line No.

def func_si(word,dir):
	not_working = []
	found = 0
	accessed = 0
	
	for files in os.walk(dir):
		cwd = (files[0])
		
		#Prints Files Containing Word
		#And Increment Number Of Founds
		#While Collecting Non-Accessible Files
		for each in files[2]:
			accessed += 1
			try:
				f= open(cwd+"/"+each, 'r')
				data = f.read()
				f.close()
			except:
				not_working.append(each)
				continue
			#Collecting Non-Accessible Files
				
			#Searching For Word Inside File
			m = re.search(word, data, re.I)
			if m:
				found += 1
				print(f"{R}{m.group()}{W} Found In {C}{cwd}/{each}{W}")
				#os.getcwd() = files[0]
	
	#When All Files Are Accessed Or 
	#No Files Are Available,
	#Return The No. Of Found And
	#Non Accessible File Names
	return found, not_working, accessed

#---------------------------------------------
#Seaching Word Through Files Recursively
#For Finding Case Insensitive Word

def func_ri(word,dir,found= 0,not_working= [],accessed= 0):
	
	#To Get All Dirs Available
	dirs = [i for i in os.listdir(dir) if os.path.isdir(dir+"/"+i)]
	#To Get All Files Available
	files = [i for i in os.listdir(dir) if os.path.isfile(dir+"/"+i)]
	
	#Accessing The Deepest Folder First
	#Calls Itself And Prints Files Containing
	#Word And Increment Number Of Founds
	#While Collecting Non-Accessible Files
	if len(dirs) > 0:
		for i in dirs:
			path = (dir+"/"+i)
			found,not_working,accessed = func_ri(word,path,found,not_working,accessed)
	
	#Printing The Accessible Files 
	#Containing Word
	#From The Bottom To The Top
	#Using Recursion
	for each in files:
		accessed += 1
		try:
			f= open(dir+"/"+each, 'r')
			data = f.read()
			f.close()
		except:
			#Collecting Non-Accessible Files
			not_working.append(each)
			continue
		
		#Searching For The Word Inside File
		m = re.search(word, data, re.I)
		if m:
			#When Word Is Found,
			#Increase Count
			found += 1
			#And Print
			lin=data[:m.start()].count('\n')+1
			print(f"{R}{m.group()}{W} Found In {C}{dir}/{each}{W} In Line {P}{lin}{W}")
			#os.getcwd() = files[0]
	
	#When All Files Are Accessed Or 
	#No Files Are Available,
	#Return The No. Of Found And
	#Non Accessible File Names
	return found, not_working, accessed
	
	
#---------------------------------------------
##Main Function To Run The Whole Program

def main(input_str = None):
	a = AP(description= "Finds First Occurence Of The Searched [str] Word In Text Files Provided By [DIR] (RegEx Available) (Current Directory When No Dir Given) ('_' Inplace Of ' ' Can Be Given)")
	
	
	a.add_argument("-v", dest= "version", default= None, action= 'store_true', help= 'Print Current Version Number Of This Program')
	a.add_argument("-m", nargs= 2, metavar= ('[str]', '[DIR]'), help = 'To Get Files With Line Number Containing str')
	a.add_argument("-s", nargs= 2, metavar= ('[str]', '[DIR]'), help = 'To Get Only The Files Containing str')
	a.add_argument("-r", nargs= 2, metavar= ('[str]', '[DIR]'), help = 'To Search Like -m Option In Recursive Order')
	a.add_argument("-mi", nargs= 2, metavar= ('[str]', '[DIR]'), help = '-m Option With Case Insensitive')
	a.add_argument("-si", nargs= 2, metavar= ('[str]', '[DIR]'), help = '-s Option With Case Insensitive')
	a.add_argument("-ri", nargs= 2, metavar= ('[str]', '[DIR]'), help = '-r Option With Case Insensitive')
	
	#a.print_help()
	if input_str: #== 'if input_str != None:'
		args = a.parse_args(input_str.split(" ",2))
	else:
		#When Dir Not Given In CLI
		dir_yes1 = re.search('/storage/', str(sys.argv),re.I)
		dir_yes2 = re.search('[C-F]:', str(sys.argv),re.I)
		if dir_yes1 == None or dir_yes2 == None:
			sys.argv.append(os.getcwd())
		args = a.parse_args()
	#args: -mode word dir
	 
	if args.version:
		print("—"*65)
		print("\nCurrent Version: %.3f\n"%version)
		print("—"*65)
	
	if args.m: 	Print(func_m,args.m)
	
	elif args.s: 	Print(func_s,args.s)
		
	elif args.r: 	Print(func_r,args.r)
		
	elif args.mi:	Print(func_mi,args.mi)
	
	elif args.si:	Print(func_si,args.si)
		
	elif args.ri:	Print(func_ri,args.ri)
	
	
#---------------------------------------------
#Running The Program
from time import time
if __name__ == "__main__":
	
	if len(sys.argv) > 1:
		#CLI args Available
		main()
		exit()
	
	while True:
		#CLI args Not Available
		
		a = input("$ python SeeProgram.py ")
		if a == '': break
		
		if a == '-v':
			main(a)
			continue
			
		if a.count("-") > 1:
			print("\nOnly One Mode Supported At A Time For This Version. \nAll [Modes] Have A Single '-'. Check help using '-h'.\n\n")
			continue
		
		#When Mode Not Given In Input
		mode_yes= re.search('-[hmsr]',a,re.I)
		if  mode_yes == None:
			a = "-mi" + ' ' + a
		
		#When Dir Not Given In Input
		dir_yes= re.search('/',a,re.I)
		if  dir_yes == None:
			a = a + ' ' +os.getcwd()
		
		#By Default, Search Within Root Dir
		#If Not Given In Input
		## -mode word dir
		
		print()
		t1 = time()
		main(a)
		t2 = time()
		print(f"\n[Program Finished In {t2-t1} seconds]\n")