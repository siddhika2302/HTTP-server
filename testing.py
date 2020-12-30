import webbrowser, os, sys
from socket import *
root = os.getcwd()
s = socket(AF_INET, SOCK_DGRAM)
port = sys.argv[1]

IP = '127.0.0.1'
s.close()
url = "localhost:"+port
def starttab(url = (url)):
    webbrowser.open_new_tab(url)


starttab(url + "/form.html")
starttab(url + "/hello.txt")
starttab(url + "/hello.c")
starttab(url + "/hello.py")
starttab(url + "/hello.java")
starttab(url + "/hello.cpp")
starttab(url + "/Style.css")
starttab(url + "/action.html")
