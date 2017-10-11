import socket, os, sys, time, thread



running_ports = []
buff = 1024
banner ="MultiNC - CODED BY KRYPT0N (https://github.com/Krypt0n36/)"
shost = "127.0.0.1" #the address to bind channel on.

def log(string):
	if VERBOSE == True:
		print string
	else:
		pass

def execute(command):
	os.system(command)

def handle(portnumber, conn, addr):
	s1 = socket.socket()
	try:
		s1.bind((shost, portnumber))
		s1.listen(1)
	except socket.error:
		handle(portnumber + 1, conn, addr)
	print("[%s] Client connected, channel opened [%s:%s]."%(addr[0], lhost, str(portnumber)))
	command = 'xterm -e "ncat %s %s -v"'%(lhost, str(portnumber))
	if AUTO == True:
		thread.start_new_thread(execute, (command,))
	else:
		pass
	while 1:
		conn1, addr1 = s1.accept()
		log("[%s] User joined."%addr[0])
		try:
			thread.start_new_thread(repeater0,(conn1, conn))
			thread.start_new_thread(repeater1,(conn1, conn))
		except:
			pass

def repeater0(conn1, conn):
	try:
		data = conn1.recv(buff)
		conn.send(data)
		repeater0(conn1, conn)
	except socket.error as e:
		print "[!] Error: %s ."%str(e)
	except Exception as e:
		pass

def repeater1(conn1, conn):
	try:
		conn1.send(conn.recv(buff))
		repeater1(conn1, conn)
	except socket.error as e:
		print "[!] Error: %s ."%str(e)
	except:
		pass

def serv(host, port):
	s = socket.socket()
	try:
		s.bind((host, port))
		s.listen(1)
		print("Serving on %s:%s"%(host, str(port)))
	except Exception as e:
		print("[!] Error while binding socket, %s ."%str(e))
		sys.exit()
	while 1:
		conn, addr = s.accept()
		for portnumber in range(50, 100):
			if portnumber in running_ports:
				pass
			else:
				running_ports.append(portnumber)
				thread.start_new_thread(handle, (portnumber, conn, addr))
				break

print banner

try:
	lhost = sys.argv[1]
	lport = sys.argv[2]
except:
	print "Usage:"
	print "%s [Address to bind] [Port]"%sys.argv[0]
	print "Options:"
	print "-a	--auto		Automaticaly interract (xterm required)"
	print "-v	--verbose	Be Verbose"
	sys.exit()


AUTO = False
VERBOSE = False

if "-a" in sys.argv:
	print "AutoInterract mode : ON"
	AUTO = True
else:
	pass

if "-v" in sys.argv:
	VERBOSE = True
	print "Verbose mode 	   : ON"
else:
	pass

try:
	serv(sys.argv[1], int(sys.argv[2]))
except KeyboardInterrupt:
	print "\n[!] Ctrl+C detected, closing.."
	sys.exit()
