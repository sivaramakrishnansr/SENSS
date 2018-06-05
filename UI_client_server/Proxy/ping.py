import os
import subprocess
import time
check=0
ok_count=0
while True:
	try:
		ping_response=subprocess.check_output(['ping', '57.0.0.1','-c 1'], timeout=1)
		ping_response=ping_response.split("\n")[1].split(" ")[-2].split("=")[-1]
		rtt=float(ping_response)
	except:
		rtt=1
	if rtt>0.8:		
		check=check+1
		print "Not OK",check
	if rtt<=0.8:
		print "OK",check
		ok_count=ok_count+5
		if ok_count==5:
			ok_count=0
			check=0
	if check>=5:
		os.system("php filter_proxy.php")
		check=0
			
	time.sleep(1)
