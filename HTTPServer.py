import sys
import os
import datetime
import time
from socket import * #for socket programming
import threading     #for implementing Multi threading
from _thread import *
import logging       #for creating log file
from config import * #importing config file

#create and configure logg
LOG_FORMAT = '%(asctime)s : %(filename)s : %(message)s' #creating format for log
logging.basicConfig( filename = ROOT + '/serverfile.log', 
			level = logging.INFO,
			format = LOG_FORMAT)
logger = logging.getLogger()

#function to return current date
def cdate():
	l = time.ctime().split(' ')
	l[0] = l[0] + ','
	string = (' ').join(l)
	string = 'Date: ' + string
	return string


# function to fetch last modified date of the resource
def mdate(element):
	l = time.ctime(os.path.getmtime(element)).split(' ')
	for i in l:
		if len(i) == 0:
			l.remove(i)
	l[0] = l[0] + ','
	string = (' ').join(l)
	string = 'Last-Modified: ' + string
	return string

#Implementing Status Codes
def status(status, connectionsocket):
	
	if status == "400":	#bad request
		f = open(ROOT+ "/statuscodes/400.html","r")
		
	if status == "401":	#authentication error
		f = open(ROOT+ "/statuscodes/401.html","r")
		
	if status == "403":	#forbidden
		f = open(ROOT+ "/statuscodes/403.html","r")
		
	if status == "404":	#File not found
		f = open(ROOT+ "/statuscodes/404.html","r")
		
	if status == "415":	#Unsupported media type
		f = open(ROOT+ "/statuscodes/415.html","r")
		
	if status == "500":	#internal server error
		f = open(ROOT+ "/statuscodes/500.html","r")
		
	if status == "503":	#server unavailable
		f = open(ROOT+ "/statuscodes/503.html","r")
		
	if status == "505":	#HTTP Version Not Supported
		f = open(ROOT+ "/statuscodes/505.html","r")
	content = f.read()
	connectionsocket.send(content.encode())

#HTTP methods
def methods(connectionsocket, addr, thread_list, COOKIE_ID):
	recv = connectionsocket.recv(1024).decode('utf-8')
	request = recv.split()
	req = "Request:"
	address = "Client address:"
	prt = "Port_no :"
	logging.info('{}  {}  {}  {}  {} {} \n'.format(address, addr[0], prt, addr[1], req, request))#writing in log files

	#GET method
	if (request[0] == "GET"):
		response = [] #creating response list
		element = ROOT + request[1]
		if os.path.isfile(element):
			if (os.access(element, os.W_OK) and os.access(element, os.R_OK)): #checking the accessibility of the file
				response.append("HTTP/1.1 200 OK")
				response.append(cdate())
				response.append("Server: HTTP/1.1")
				response.append(mdate(element))
				size = os.path.getsize(element)
				s1 = str(size)
				strz = "Content-Length: " + s1
				response.append(strz)
				file_ext = os.path.splitext(element)
				if file_ext[1] in file_extension.keys():  #getting the content type from extension of file
					str1 = file_extension[file_ext[1]]
					str2 = "Content-Type: " + str1
					response.append(str2)
				str3 = COOKIE1 + str(COOKIE_ID) + ' '  
				str3 = str3 + COOKIE2
				response.append(str3)
				response.append("Connection closed\n\n")
				f = open(element, "r")		#sending the contents of the requested file
				content = f.read()
				encoded = '\r\n'.join(response).encode()
				connectionsocket.send(encoded)
				connectionsocket.send(content.encode())
				thread_list.remove(connectionsocket)
				connectionsocket.close()

			else:
				status("403", connectionsocket)	 #forbidden
				thread_list.remove(connectionsocket)
				connectionsocket.close()
		else:	
			status("404", connectionsocket)		#File not found
			thread_list.remove(connectionsocket)
			connectionsocket.close()

	#HEAD method
	if (request[0] == "HEAD"):
		response = []
		element = ROOT + request[1]
		if os.path.isfile(element):
			if (os.access(element, os.W_OK) and os.access(element, os.R_OK)):	#checking the accessibility of the file
				response.append("HTTP/1.1 200 OK")
				response.append(cdate())
				response.append("Server: HTTP/1.1")
				response.append(mdate(element))
				size = os.path.getsize(element)
				strz = "Content-Length: " + str(size)
				response.append(strz)
				file_ext = os.path.splitext(element)
				if file_ext[1] in file_extension.keys():      #getting the content type from extension of file
					str1 = file_extension[file_ext[1]]
					str2 = "Content-Type: " + str1
					response.append(str2)
				str3 = COOKIE1 + str(COOKIE_ID) + ' '
				str3 = str3 + COOKIE2
				response.append(str3)
				response.append("Connection: closed\n\n")
				encoded = '\r\n'.join(response).encode()
				connectionsocket.send(encoded)
				thread_list.remove(connectionsocket)
				connectionsocket.close()
			else:
				status("403", connectionsocket)	 #forbidden
				thread_list.remove(connectionsocket)
				connectionsocket.close()
			
		else:
			status("404", connectionsocket) 		#File not found
			thread_list.remove(connectionsocket)
			connectionsocket.close()

	#PUT method
	if (request[0] == "PUT"):
		file = ROOT + request[1]
		str1 = "Host: "
		connectionsocket.send(str1.encode())
		host = connectionsocket.recv(1024).decode()
		str1 = "Content-type: "
		connectionsocket.send(str1.encode())
		file_type = connectionsocket.recv(1024).decode()
		str1 = "Content: "
		connectionsocket.send(str1.encode())
		content = connectionsocket.recv(1024).decode()
		f = open(file, "a")
		f.write(content)
		f.close()
		thread_list.remove(connectionsocket)
		connectionsocket.close()
		
	#DELETE method		
	if (request[0] == "DELETE"):
		element = ROOT + request[1]
		str1 = "Enter username : "  				#taking username and passwrd for authentication.
		connectionsocket.send(str1.encode())
		un = connectionsocket.recv(1024).decode()
		un = un.split()
		str1 = "Enter password : "
		connectionsocket.send(str1.encode())
		pwd = connectionsocket.recv(1024).decode()
		pwd = pwd.split()
		if un[0] == USERNAME and pwd[0] == PASSWORD:
			authenticity = 1
		if(authenticity == 1):
			if os.path.isfile(element):
				os.remove(element)
				str3 = "File Deletion successful!\n"
				connectionsocket.send(str3.encode())
			else :
				status("404", connectionsocket)		 #forbidden
				thread_list.remove(connectionsocket)
				connectionsocket.close()
		else:
			status("401", connectionsocket)			 #authentication error
		thread_list.remove(connectionsocket)
		connectionsocket.close()
		
	#POST method
	if (request[0] == "POST"):
		response = []
		sentence = connectionsocket.recv(1024).decode()
		line = sentence.split("\r\n\r\n")
		f = open("forpost.txt", 'a')
		inp = line[1].split("&")	#seperating multiple values
		f.write("\n")
		f.write(inp[0]+"\n")		#writing the keys and values in file
		f.write(inp[1]+"\n")
		f.close()
		print("\n")
		print(inp[0])
		print(inp[1])
		response.append("HTTP/1.1 200 OK")
		date = mdate("forpost.txt")
		response.append(date)
		response.append("Server:HTTP/1.1 (Ubuntu)")
		response.append("Content-Language : en-US, en")
		size = os.path.getsize("forpost.txt")
		sz = str(size)
		response.append("Content length:"+ sz)
		response.append("Content-Type: text/html")
		l = len(response)
		for i in range(0,l):
			print(response[i])
		thread_list.remove(connectionsocket)
		connectionsocket.close()
		
#function for handling multiple requests		
def connect():
	COOKIE_ID = 0
	while True:
		connectionsocket, addr = serversocket.accept()
		thread_list.append(connectionsocket)
		if(len(thread_list) <= MAX_REQUESTS):		#checking if the current request is under the maximum number of requests allowed.
			print("Client address is :", addr)
			COOKIE_ID += 1
			try :
				start_new_thread(methods, (connectionsocket, addr, thread_list, COOKIE_ID)) 	#starting new thread for each client
			except:
				print("No thread creation")
		else:
			#print("No thread possible now")
			thread_list.remove(connectionsocket)
			status("503", connectionsocket)			#503 Server Unavailable
			connectionsocket.close()

#main function
if __name__ == '__main__':
	try:
		serverport = int(sys.argv[1])	#taking port number as command line input
	except:
		print("Usage : python3 s1.py <port_number>")
		sys.exit()
	serversocket = socket(AF_INET, SOCK_STREAM)
	try:
		serversocket.bind(('', serverport))
	except:
		print('HTTPServer invalid arguements')
		print('Usage: python3 webserver.py <port_number>')
	serversocket.listen(1)
	print('Server Welcomes you...')
	connect()
	serversocket.close()
	sys.exit()
