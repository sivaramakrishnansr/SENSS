import subprocess
import select

poller = select.epoll()
subprocs = {} #map stdout pipe's file descriptor to the Popen object
i = 0
content_arr = []


with open("all_reader_calls.txt", "r") as file_handler:
    #global content_arr, i
    content_arr = file_handler.read()
    for i in range(0, len(content_arr)):
        if content_arr[i].strip() != "":
            if content_arr[i].strip()[0] == "-":
                break
            cmd = content_arr[i].strip()
	    #cmd = "python reader.py"
            subproc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocs[subproc.stdout.fileno()] = subproc
            poller.register(subproc.stdout, select.EPOLLHUP)

    #loop that polls until completion
    while True:
	#print dir(poller)
        for fd, flags in poller.poll(timeout=1): #never more than a second without a UI update
            done_proc = subprocs[fd]
            poller.unregister(fd)
            print "complete: " + str(fd)
        
