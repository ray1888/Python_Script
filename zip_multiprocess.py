import os
import re
import datetime
import multiprocessing
import Queue

def gettarlist(oldfl, newfl):
    for i in oldfl:
	if re.search('py', i): 
            pass
	elif i == "job.log":
	    pass
	elif re.search('tar.gz', i): 
	    pass
	elif i == "": 
	    pass
	elif re.search('bak', i):
            pass
	else:
	    file_split = i.split(".")
	    file_date = file_split[2]
	    if file_date < now_date:
	        newfl.append(i)
    return newfl

def zipp(q, workpath):
    while 1:
        if q.empty():
            break
        else:
            i = q.get()
	    q.task_done()
            backname = i+".tar.gz"
            print "i= %s"%(i)
            print "backname = %s"%(backname)
            if os.path.exists(workpath+"/"+backname):
	        print "%s already exist"%(backname)
		continue
            else:
	        print "%s is ready to zipped"%(i)    
	        action = os.system("tar -czvf "+backname+" "+i)
	        if action == 0:
	            print i+"has already zipped" 


if __name__ == "__main__":
    workdir = "/root/"
    filelist = os.listdir(workdir)
    filelist1 = []
    now_date = datetime.datetime.now().strftime('%Y-%m-%d')
    filelist1 = gettarlist(filelist, filelist1) 
    print filelist1
    q = multiprocessing.JoinableQueue()
    process_list = []
    for i in filelist1:
	q.put(i)
    for i in range(3):
            process = multiprocessing.Process(target=zipp,args=(q, workdir)) 
            process.start()
    q.join()
    print "the zip program is finished"
