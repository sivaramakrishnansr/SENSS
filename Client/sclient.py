import httplib
from time import sleep
from threading import Thread

SERVER_IP = "10.1.2.2"
SERVER_PORT = "5000"

retry_count = 0

def send_request_to_server(conn):
	global retry_count
	conn.request("GET", "/")
	retry_count = 0
	resp = conn.getresponse()
	print resp.status, resp.reason
	data = resp.read()

def session_initiation():
	conn = httplib.HTTPSConnection(SERVER_IP+":"+SERVER_PORT)
	while True:
		send_request_to_server(conn)
		sleep(1)
	conn.close()

def retry_connecting_to_server():
	global retry_count
	sleep(2)
	retry_count += 1
	try:
		print retry_count
		session_initiation()
	except StandardError:
		pass

def connecting_to_server():
	print "Start thread"
	try:
		session_initiation()
	except StandardError:
		while True:
			retry_connecting_to_server()
			if retry_count > 3:
				print "Initiate redirect via proxy"
				break
	print "Exit thread"


t1 = Thread(target = connecting_to_server, args = [])

t1.start()
t1.join()
