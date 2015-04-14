
import re
import os
import sys
import time
import urllib2
import threading
from netaddr import *

class colors:
     BLUE='\033[94m'
     GREEN='\033[92m'
     YELLOW='\033[93m'
     RED='\033[91m'
     ENDC='\033[0m'

def getWebServer(ip, ports, msg):
	for port in ports:
		try:
			req = urllib2.Request("http://"+ip+":"+str(port))
			req.add_header('User-Agent', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')
			res = urllib2.urlopen(req)
			server = res.info().get('Server')
			if server:
				print "[+] IP:"+ip,"Port:"+str(port),"Running:",server
				os.system('CutyCapt --url=http://%s:%s --out=%s%s_%s.png'%(ip,str(port),thumbs_dir,ip,str(port)))
			else:
				print "Unable to find Web Server on "+ip
		except: pass

#########################################################################
if __name__ == "__main__":



	# Define ports
	ports = [80,8000,8080,10000]
	# Help
	if len(sys.argv) != 2:
		print colors.RED+"Usage:   "+colors.ENDC,colors.BLUE+"python",sys.argv[0],"<network>"+colors.ENDC
		print colors.BLUE+"          You can specify IP address value and the CIDR prefix like this:"+colors.ENDC
		print colors.RED+"Example: "+colors.ENDC,colors.BLUE+"python",sys.argv[0],"192.168.0.0/24"+colors.ENDC
		print colors.RED+"Example: "+colors.ENDC,colors.BLUE+"python",sys.argv[0],"192.168.0.0/21"+colors.ENDC
		sys.exit(1)

	# Get current working directory
	current_dir = os.getcwd()
	# If directory thumbs doesn't exist, create thumbs dir.
	if not os.path.exists(current_dir+'/thumbs'):
		try:
			os.mkdir('thumbs')
		except: pass

	thumbs_dir = current_dir+'/thumbs/'

	try:
		network = sys.argv[1]
	except(ValueError):
		print colors.RED+"[-] Incorrect Network values\n"+colors.ENDC
		sys.exit(1)

	total_ip = IPNetwork(network)
	print colors.RED+"\n[+] Scanning:"+colors.ENDC,len(total_ip)-2,"ips\n"
	print "save capture image to "+thumbs_dir

	for ip in IPNetwork(network).iter_hosts():
		ip = str(ip).strip()
		time.sleep(1)
		threading.Thread( target=getWebServer, args=(ip, ports, 0) ).start()